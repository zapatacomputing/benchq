################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
using Memoize

"""
Given that pauli_tracker.cond_paulis is full, compute the DAG which results from the
conditional Pauli operators. This is done by separating the conditional Pauli operators
into two separate graphs, one for the X gates which act on qubits which are measured in
the T basis (called the static_DAG), and one for all other measurements (called the
pushable_DAG). The pushable DAG is so called because dependencies in the pushable DAG
can be "pushed" to the dependencies of the next node in the DAG. By setting the final_depth
variable, one can specify how many nodes to push a dependency to. This is useful for
choosing how sparse the DAG will be. Setting the final_depth to larger values will result
in a more dense DAG. Sparser DAGs will be easier to layer and take up less space in memory,
however, denser DAGs will have a less defined "arrow of time" and will be harder to layer.

Attributes:
    pauli_tracker (PauliTracker): The PauliTracker object containing the
        information on the conditional Pauli operators and measurements
        performed on each qubit.
    nodes_to_include (Vector{Qubit}): The nodes which should be included
        in the DAG.
    final_depth (Int): How many nodes to push a dependency to.
    verbose (bool): Whether to print out the progress of the function.
Returns:
    dag (Vector{Vector{Qubit}}): The DAG which results from the conditional
        Pauli operators.
"""
function get_dag(pauli_tracker, nodes_to_include, final_depth=1, verbose::Bool=false)::Vector{Vector{Qubit}}
    pushable_dag::Vector{Vector{Qubit}} = [[] for _ in range(1, pauli_tracker.n_nodes)]
    static_dag::Vector{Vector{Qubit}} = [[] for _ in range(1, pauli_tracker.n_nodes)]

    for node in VerboseIterator(nodes_to_include, verbose, "Creating sparse single-qubit measurement DAGs...")
        if pauli_tracker.measurements[node][1] in non_clifford_gate_codes
            for predecessor in pauli_tracker.cond_paulis[node][1]
                push!(static_dag[node], predecessor)
            end
            for predecessor in pauli_tracker.cond_paulis[node][2]
                push!(pushable_dag[node], predecessor)
            end
        end
        if pauli_tracker.measurements[node][1] == H_code
            for predecessor in pauli_tracker.cond_paulis[node][1]
                push!(pushable_dag[node], predecessor)
            end
        end
        if pauli_tracker.measurements[node][1] == I_code
            for predecessor in pauli_tracker.cond_paulis[node][2]
                push!(pushable_dag[node], predecessor)
            end
        end
    end

    pushable_dag = get_reversed_dag(pushable_dag)
    static_dag = get_reversed_dag(static_dag)

    function dag_densifier(control::Qubit, depth::Int)
        if depth == 0
            return control
        end

        sucessors = Set{Qubit}(static_dag[control])
        for target in pushable_dag[control]
            union!(sucessors, dag_densifier(target, depth - 1))
        end

        return sucessors
    end

    densified_dag::Vector{Vector{Qubit}} = [[] for _ in range(1, pauli_tracker.n_nodes)]
    for node in VerboseIterator(nodes_to_include, verbose, "Densifying single-qubit measurement DAG...")
        densified_dag[node] = collect(dag_densifier(node, final_depth))
    end

    return get_reversed_dag(densified_dag, verbose)
end

"""
Given a "base node" which is measured in the T basis, find all the nodes which
depend on it. This is done by following the X edges up the tree. We go up the tree
using the following logic:

Measured in T basis: Is the node measured in a non-clifford basis or a graph output node?
is base: Is this node where this part of the dependency graph starts?
is x target: Is this node the target of an conditional Pauli X?

non-clifford measurement? | is base? | is x target? | What to do?
            y             |    y     |       y      | Follow x edges up the tree
            y             |    y     |       n      | do nothing, this node has no dependencies
            y             |    n     |       y      | Follow z edges up the tree, add self to predecessors
            y             |    n     |       n      | Follow z edges up the tree, add self to predecessors
            n             |    y     |       y      | do nothing, this node has no dependencies
            n             |    y     |       n      | do nothing, this node has no dependencies
            n             |    n     |       y      | Follow non-trivial edges up the tree, add self to predecessors
            n             |    n     |       n      | Follow non-trivial edges up the tree, add self to predecessors

Attributes:
    pauli_tracker (PauliTracker): The PauliTracker object containing the
        information on the conditional Pauli operators and measurements
        performed on each qubit.
    target (Qubit): The qubit which we are finding the predecessors of.
    predecessors (Set{Qubit}): The set of predecessors which we have found so far.
    is_base (bool): Whether the current node is the base node.
Returns:
    predecessors (Set{Qubit}): All the nodes which depend on the base node.
"""
function optimal_dag_filler_factory(pauli_tracker, output_nodes_set)
    @memoize function fill_dag_for_this_node(target::Qubit)
        predecessors = Set{Qubit}(target)
        if pauli_tracker.measurements[target][1] in non_clifford_gate_codes || target in output_nodes_set
            for predecessor in pauli_tracker.cond_paulis[target][2]
                union!(predecessors, fill_dag_for_this_node(predecessor))
            end
        else
            # We always insert a hadamard gate before the measurement
            # so we must follow the x edges up the tree for H_code
            # and z edges up the tree for I_code.
            if pauli_tracker.measurements[target][1] == H_code
                for predecessor in pauli_tracker.cond_paulis[target][1]
                    union!(predecessors, fill_dag_for_this_node(predecessor))
                end
            elseif pauli_tracker.measurements[target][1] == I_code
                for predecessor in pauli_tracker.cond_paulis[target][2]
                    union!(predecessors, fill_dag_for_this_node(predecessor))
                end
            end
        end

        return predecessors
    end
    return fill_dag_for_this_node
end

"""
Create the DAG representing the order in which measurements need to be made.
The only measurements which have to be made in order are the non-clifford ones.
So for each non-clifford measurement, we find the nodes which depend on it
and add them to the DAG. We then repeat this process for each node in the DAG
until we have found all of the nodes which need to be measured. This results
in a DAG with the minimal number of edges. Although this same DAG can be
created by calling get_dag with final_depth = inf, this function is much faster
because it doesn't have to recalculate the DAG for each node in the graph.

Attributes:
    pauli_tracker (PauliTracker): The PauliTracker object containing the
        information on the conditional Pauli operators and measurements
        performed on each qubit.
    output_nodes (Vector{Qubit}): The nodes which are outputs of the graph.
    nodes_to_include (Vector{Qubit}): The nodes which should be included
        in the DAG.

Returns:
    optimal_dag (Vector{Vector{Qubit}}): A vector containing the order in
        which the qubits must be measured. The first index is the layer,
        and the vector contained in that index is the qubits in that
        layer. The qubits in each layer are measured in parallel.
"""
function get_optimal_measurement_dag(
    pauli_tracker::PauliTracker,
    output_nodes,
    nodes_to_include,
    verbose,
)::Vector{Vector{Qubit}}
    optimal_dag = [[] for _ in range(1, pauli_tracker.n_nodes)]
    output_nodes_set = Set(output_nodes)
    fill_dag_for_this_node = optimal_dag_filler_factory(pauli_tracker, output_nodes_set)

    for node in VerboseIterator(nodes_to_include, verbose, "Creating optimal single-qubit measurement DAG...")
        non_clifford_measurement = pauli_tracker.measurements[node][1] in non_clifford_gate_codes
        if non_clifford_measurement || node in output_nodes_set
            predecessors = Set([])
            for predecessor in pauli_tracker.cond_paulis[node][1]
                union!(predecessors, fill_dag_for_this_node(predecessor))
            end
            optimal_dag[node] = collect(predecessors)
        end
    end

    return optimal_dag
end

function get_reversed_dag(dag::Vector{Vector{Qubit}}, verbose::Bool=false)::Vector{Vector{Qubit}}
    n = length(dag)  # Number of nodes in the DAG
    reversed_dag::Vector{Vector{Qubit}} = [[] for _ in 1:n]

    for (node, adjNodes) in enumerate(VerboseIterator(dag, verbose, "Reversing measurement DAG..."))
        for adjNode in adjNodes
            push!(reversed_dag[adjNode], node)
        end
    end

    return reversed_dag
end