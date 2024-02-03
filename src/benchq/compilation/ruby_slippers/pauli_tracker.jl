################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
Holds data for tracking conditional Pauli operators through a circuit.

    cond_paulis: Vector{Vector{Vector{Qubit}}}
        A vector containing the information on the conditional paulis
        for each qubit. The first index is the qubit which the pauli is
        conditioned on, the second index is the type of pauli (1 for X,
        2 for Z), and the third index is the qubit which the pauli
        acts on. For example, cond_paulis[3][1] = [6, 7] means that we must
        apply an X gate to qubits 6 and 7 if qubit 3 is measured to be 1.
    measurements: Vector{Vector{Union{UInt8,Float64}}}
        A vector containing the information on the measurements
        performed on each qubit. The first index is the qubit, and the
        vector contained in that index is the operation applied before
        measurement, the second index is the phase of the RZ gate. If
        the second index is 0.0, then no RZ gate is applied and the first
        index should not be RZ. We asume that an H gate is applied to
        each qubit before measurement right after the gate specified by
        the first index. For example, measurements[3] = [H_code, 0.0]
        means that we must apply an H gate to qubit 3 before measurement and
        measurements[3] = [RZ_code, 0.5] means that we must apply an RZ(0.5)
    n_nodes: Qubit
        The number of qubits in the circuit.
    layering: Vector{Vector{Qubit}}
        A vector containing order in which the qubits must be measured.
        The first index is the layer, and the vector contained in that
        index is the qubits in that layer. The qubits in each layer are
        measured in parallel.
    layering_optimization: String
        The optimization used to calculate the layering. Can be "Gansner",
        "Time", "Space", and "Variable".
    max_num_qubits: Int
        The width parameter used for the "Variable" optimization. Corresponds
        to the maximum number of qubits which can exist at each time step.
        Note that if one picks max_num_qubits to be too small, we will
        resort to the smallest width which can fit the circuit.
"""
mutable struct PauliTracker
    cond_paulis::Vector{Vector{Vector{Qubit}}}
    measurements::Vector{Vector{Union{UInt8,Float64}}}
    n_nodes::Qubit
    layering::Vector{Vector{Qubit}}
    layering_optimization::String
    max_num_qubits::Int

    PauliTracker(n_qubits, layering_optimization, max_num_qubits) = new(
        [[[], []] for _ in range(1, n_qubits)],
        [[H_code, 0.0] for _ in range(1, n_qubits)],
        n_qubits,
        [],
        layering_optimization,
        max_num_qubits,
    )
end

"""Convert pauli tracker to a python object"""
function python_pauli_tracker(pauli_tracker)
    python_cond_paulis = []
    for node in pauli_tracker.cond_paulis
        push!(python_cond_paulis, pylist([pylist(node[1] .- 1), pylist(node[2] .- 1)]))
    end

    python_pauli_tracker = Dict(
        "cond_paulis" => pylist(python_cond_paulis),
        "measurements" => pylist(pauli_tracker.measurements),
        "n_nodes" => pauli_tracker.n_nodes,
        "layering" => python_adjlist!(pauli_tracker.layering),
        "layering_optimization" => pauli_tracker.layering_optimization,
        "max_num_qubits" => pauli_tracker.max_num_qubits,
    )

    return python_pauli_tracker
end

function add_new_qubit_to_pauli_tracker!(pauli_tracker::PauliTracker)
    push!(pauli_tracker.cond_paulis, [[], []])
    push!(pauli_tracker.measurements, [H_code, 0.0])
    pauli_tracker.n_nodes += 1
end

"""
Add a conditional Pauli operator to the PauliTracker object.
"""

function add_z_to_pauli_tracker!(
    cond_paulis::Vector{Vector{Vector{Qubit}}},
    control_qubit::Qubit,
    target_qubit::Qubit,
)
    push!(cond_paulis[target_qubit][2], control_qubit)
end

function add_x_to_pauli_tracker!(
    cond_paulis::Vector{Vector{Vector{Qubit}}},
    control_qubit::Qubit,
    target_qubit::Qubit,
)
    push!(cond_paulis[target_qubit][1], control_qubit)
end

"""
Indicate that a node is being measured.
"""

function add_measurement!(measurements, op_code::UInt8, qubit::Qubit)
    measurements[qubit][1] = op_code
end

function add_measurement!(measurements, op_code::UInt8, qubit::Qubit, phase::Float64)
    measurements[qubit][1] = op_code
    measurements[qubit][2] = phase
end

"""
Functions for tracking the paulis through gates.
"""

function track_conditional_paulis_through_h(
    cond_paulis::Vector{Vector{Vector{Qubit}}},
    qubit,
)
    x_cond_paulis = cond_paulis[qubit][1]
    cond_paulis[qubit][1] = cond_paulis[qubit][2]
    cond_paulis[qubit][2] = x_cond_paulis
end

function track_conditional_paulis_through_s(
    cond_paulis::Vector{Vector{Vector{Qubit}}},
    qubit,
)
    for x_control in cond_paulis[qubit][1]
        toggle_pauli_z(cond_paulis, x_control, qubit)
    end


end

function track_conditional_paulis_through_cz(
    cond_paulis::Vector{Vector{Vector{Qubit}}},
    qubit_1,
    qubit_2,
)
    for x_control in cond_paulis[qubit_1][1]
        toggle_pauli_z(cond_paulis, x_control, qubit_2)
    end
    for x_control in cond_paulis[qubit_2][1]
        toggle_pauli_z(cond_paulis, x_control, qubit_1)
    end
end

"""
If a controlled Z exists on the target qubit, then we get rid of it.
If a controlled Z doesn't exist on the target qubit, then we add one.
"""
function toggle_pauli_z(cond_paulis, toggled_qubit, target_qubit)
    if toggled_qubit in cond_paulis[target_qubit][2]
        setdiff!(cond_paulis[target_qubit][2], [toggled_qubit])
    else
        push!(cond_paulis[target_qubit][2], toggled_qubit)
    end
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
function get_predecessors_iterative(pauli_tracker::PauliTracker, initial_target, initial_predecessors)::Set{Qubit}
    # Initialize a stack with the initial target
    stack = [initial_target]
    predecessors = copy(initial_predecessors)
    curr_recursion_level = 0
    max_recursion_level = 10

    while !isempty(stack) && curr_recursion_level <= max_recursion_level
        target = pop!(stack)
        non_clifford_measurement = pauli_tracker.measurements[target][1] in non_clifford_gate_codes
        is_x_target = pauli_tracker.cond_paulis[target][1] != []

        if non_clifford_measurement
            push!(predecessors, target)
            append!(stack, pauli_tracker.cond_paulis[target][2])
        else
            if pauli_tracker.measurements[target][1] == H_code || pauli_tracker.measurements[target][1] == I_code
                push!(predecessors, target)
                append!(stack, pauli_tracker.cond_paulis[target][2])
            end
        end

        curr_recursion_level += 1
    end

    # Handle the case when the recursion limit is reached
    if curr_recursion_level > max_recursion_level
        for target in stack
            union!(predecessors, pauli_tracker.cond_paulis[target][2])
        end
    end

    return predecessors
end



function fill_dag_for_this_node!(
    new_target::Qubit,
    pauli_tracker::PauliTracker,
    output_nodes_set::Set{Qubit},
    second_level_dag,
)
    stack = [new_target]
    predecessors = Set{Qubit}([])

    while !isempty(stack)
        target = pop!(stack)
        push!(predecessors, target)

        if isempty(second_level_dag[target])
            if pauli_tracker.measurements[target][1] in non_clifford_gate_codes || target in output_nodes_set
                append!(stack, pauli_tracker.cond_paulis[target][2])
            else
                # We always insert a hadamard gate before the measurement
                # so we must follow the x edges up the tree for H_code
                # and z edges up the tree for I_code.
                if pauli_tracker.measurements[target][1] == H_code
                    append!(stack, pauli_tracker.cond_paulis[target][1])
                elseif pauli_tracker.measurements[target][1] == I_code
                    append!(stack, pauli_tracker.cond_paulis[target][2])
                end
            end
            println("stack: ", stack)
        else
            union!(predecessors, second_level_dag[predecessor])
        end
    end

    return predecessors
end

# function dag_filler_factory(pauli_tracker::PauliTracker, output_nodes_set::Set{Qubit}, second_level_dag)
#     return @memoize function fill_dag_for_this_node(new_target::Qubit)
#         stack = [new_target]
#         predecessors = Set{Qubit}([])

#         while !isempty(stack)
#             target = pop!(stack)
#             push!(predecessors, target)

#             if pauli_tracker.measurements[target][1] in non_clifford_gate_codes || target in output_nodes_set
#                 append!(stack, pauli_tracker.cond_paulis[target][2])
#             else
#                 # We always insert a hadamard gate before the measurement
#                 # so we must follow the x edges up the tree for H_code
#                 # and z edges up the tree for I_code.
#                 if pauli_tracker.measurements[target][1] == H_code
#                     append!(stack, pauli_tracker.cond_paulis[target][1])
#                 elseif pauli_tracker.measurements[target][1] == I_code
#                     append!(stack, pauli_tracker.cond_paulis[target][2])
#                 end
#             end
#         end

#         return predecessors
#     end
# end

function fill_dag_for_this_node!(
    new_target::Qubit,
    pauli_tracker::PauliTracker,
    output_nodes_set::Set{Qubit},
    second_level_dag,
)
    stack = [new_target]
    predecessors = Set{Qubit}([])

    while !isempty(stack)
        target = pop!(stack)
        push!(predecessors, target)

        if isempty(second_level_dag[target])
            if pauli_tracker.measurements[target][1] in non_clifford_gate_codes || target in output_nodes_set
                append!(stack, pauli_tracker.cond_paulis[target][2])
            else
                # We always insert a hadamard gate before the measurement
                # so we must follow the x edges up the tree for H_code
                # and z edges up the tree for I_code.
                if pauli_tracker.measurements[target][1] == H_code
                    append!(stack, pauli_tracker.cond_paulis[target][1])
                elseif pauli_tracker.measurements[target][1] == I_code
                    append!(stack, pauli_tracker.cond_paulis[target][2])
                end
            end
            # println("stack: ", stack)
        else
            union!(predecessors, second_level_dag[new_target])
        end
    end

    second_level_dag[new_target] = predecessors

    return predecessors
end


"""
Create the DAG representing the order in which measurements need to be made.
The only measurements which have to be made in order are the non-clifford ones.
So for each non-clifford measurement, we find the nodes which depend on it
and add them to the DAG. We then repeat this process for each node in the DAG
until we have found all of the nodes which need to be measured. This results
in a DAG with the minimal number of edges.

Attributes:
    pauli_tracker (PauliTracker): The PauliTracker object containing the
        information on the conditional Pauli operators and measurements
        performed on each qubit.
    output_nodes (Vector{Qubit}): The nodes which are outputs of the graph.
    nodes_to_include (Vector{Qubit}): The nodes which should be included
        in the DAG.

Returns:
    new_dag (Vector{Vector{Qubit}}): A vector containing the order in
        which the qubits must be measured. The first index is the layer,
        and the vector contained in that index is the qubits in that
        layer. The qubits in each layer are measured in parallel.
"""
function get_sparse_measurement_dag(
    pauli_tracker::PauliTracker,
    output_nodes,
    nodes_to_include,
    verbose,
)::Vector{Vector{Qubit}}
    new_dag = [Set([]) for _ in range(1, pauli_tracker.n_nodes)]
    second_level_dag = [Set([]) for _ in range(1, pauli_tracker.n_nodes)]
    output_nodes_set = Set(output_nodes)

    for node in VerboseIterator(nodes_to_include, verbose, "Creating sparse single-qubit measurement DAG...")
        non_clifford_measurement = pauli_tracker.measurements[node][1] in non_clifford_gate_codes
        if non_clifford_measurement || node in output_nodes_set
            for predecessor in pauli_tracker.cond_paulis[node][1]
                union!(new_dag[node], fill_dag_for_this_node!(predecessor, pauli_tracker, output_nodes_set, second_level_dag))
            end
        end
    end

    newer_dag = [[] for _ in range(1, pauli_tracker.n_nodes)]
    for (i, adj) in enumerate(new_dag)
        newer_dag[i] = collect(adj)
    end

    return newer_dag
end

"""
A simple function for creating a measurement DAG. This DAG is not nearly as
efficient as the one created by get_sparse_measurement_dag, but it is much
easier to understand and thus is good for debugging stitching. It also preserves
the order in which qubits are created in the circuit, so it can be useful
for Space optimal layerings.

Attributes:
    pauli_tracker (PauliTracker): The PauliTracker object containing the
        information on the conditional Pauli operators and measurements
        performed on each qubit.
    nodes_to_include (Vector{Qubit}): The nodes which should be included
        in the DAG.

Returns:
    new_dag (Vector{Vector{Qubit}}): A dependency graph of which qubits
        need to be measured before which other qubits. The first index
        is the qubit which needs to be measured, and the vector contained
        in that index is the qubits which need to be measured before it.
"""
function get_simple_measurement_dag(pauli_tracker::PauliTracker, nodes_to_include, verbose)::Vector{Vector{Qubit}}
    new_dag = [[] for _ in range(1, pauli_tracker.n_nodes)]
    for node in nodes_to_include
        new_dag[node] =
            vcat(pauli_tracker.cond_paulis[node][1], pauli_tracker.cond_paulis[node][2])
    end
    return new_dag
end


function reverseDAG(dag::Vector{Vector{Qubit}}, verbose::Bool=false)::Vector{Vector{Qubit}}
    n = length(dag)  # Number of nodes in the DAG
    reversedDAG = [Vector{Int}() for _ in 1:n]  # Initialize reversed DAG

    for (node, adjNodes) in enumerate(dag)
        for adjNode in adjNodes
            push!(reversedDAG[adjNode], node)
        end
    end

    return reversedDAG
end

"""
Given a pauli tracker and an ASG, calculate the order in which qubits
have to be measured. This is done by creating a DAG of the qubits which
depend on each other. We then find a layering of this DAG based on the
layering_optimization parameter. The layering is then stored in the
pauli_tracker object.

Attributes:
    pauli_tracker (PauliTracker): The PauliTracker object containing the
        information on the conditional Pauli operators and measurements
        performed on each qubit.
    asg (ASG): The ASG object containing the information on the circuit.
    ignored_nodes (Vector{Qubit}): The nodes which should be ignored when
        calculating the layering. This is used when calculating the
        layering for a subgraph.
"""
function calculate_layering!(pauli_tracker::PauliTracker, asg, ignored_nodes::Set{Qubit}, verbose::Bool=false)
    verbose && println("Scheduling single qubit measurements...")
    nodes_to_include = Vector{Qubit}([node for node = 1:pauli_tracker.n_nodes if !(node in ignored_nodes)])

    if pauli_tracker.layering_optimization == "Time"
        verbose && println("Calculating time optimized layering...")
        output_nodes = asg.stitching_properties.graph_output_nodes
        sparse_dag = get_sparse_measurement_dag(pauli_tracker, output_nodes, nodes_to_include, verbose)
        pauli_tracker.layering =
            unadjustable_coffman_grahm(sparse_dag, asg, nodes_to_include, verbose)
    elseif pauli_tracker.layering_optimization == "Space"
        verbose && println("Calculating space optimized layering...")
        output_nodes = asg.stitching_properties.graph_output_nodes

        measurement_dag = get_simple_measurement_dag(pauli_tracker, nodes_to_include, verbose)
        reverse_dag = reverseDAG(measurement_dag, verbose)
        sparse_dag = get_sparse_measurement_dag(pauli_tracker, output_nodes, nodes_to_include, verbose)

        pauli_tracker.layering =
            variable_width(measurement_dag, reverse_dag, sparse_dag, asg, 1, nodes_to_include, verbose)
    elseif pauli_tracker.layering_optimization == "Variable"
        verbose && println("Calculating layering with $(pauli_tracker.max_num_qubits) qubits...")
        output_nodes = asg.stitching_properties.graph_output_nodes

        measurement_dag = get_simple_measurement_dag(pauli_tracker, nodes_to_include, verbose)
        sparse_dag = get_sparse_measurement_dag(pauli_tracker, output_nodes, nodes_to_include, verbose)
        reverse_dag = reverseDAG(sparse_dag)

        pauli_tracker.layering = variable_width(
            measurement_dag,
            reverse_dag,
            sparse_dag,
            asg,
            pauli_tracker.max_num_qubits,
            nodes_to_include,
            verbose,
        )
    elseif pauli_tracker.layering_optimization == "Gansner"
        verbose && println("Calculating Gansner layering...")
        output_nodes = asg.stitching_properties.graph_output_nodes
        measurement_dag =
            get_sparse_measurement_dag(pauli_tracker, output_nodes, nodes_to_include, verbose)
        pauli_tracker.layering =
            gansner_layering(measurement_dag, pauli_tracker.n_nodes, nodes_to_include)
    elseif pauli_tracker.layering_optimization == "Longest Path"
        verbose && println("Calculating longest path layering...")
        output_nodes = asg.stitching_properties.graph_output_nodes
        measurement_dag =
            get_sparse_measurement_dag(pauli_tracker, output_nodes, nodes_to_include, verbose)
        reverse_dag = reverseDAG(measurement_dag, verbose)
        pauli_tracker.layering =
            longest_path_layering(measurement_dag, reverse_dag, n_nodes, nodes_to_include, verbose)
    else
        error("Invalid layering optimization.")
    end

    verbose && println("Layering complete.")
end

function gansner_layering(measurement_dag, n_nodes, nodes_to_include)
    function dfs(node, visited, node_layers)
        visited[node] = true
        maxLayer = 0

        for neighbor in measurement_dag[node]
            if !visited[neighbor]
                maxLayer = max(maxLayer, dfs(neighbor, visited, node_layers))
            elseif node_layers[neighbor] != -1
                maxLayer = max(maxLayer, node_layers[neighbor])
            end
        end

        node_layers[node] = maxLayer + 1
        return node_layers[node]
    end

    visited = falses(n_nodes)
    node_layers = fill(-1, n_nodes)

    for node in nodes_to_include
        if !visited[node]
            dfs(node, visited, node_layers)
        end
    end

    layering = [[] for _ in range(1, maximum(node_layers))]
    for node in nodes_to_include
        layer = node_layers[node]
        push!(layering[layer], node)
    end

    return layering
end

"""
A depth first search which returns the nodes in the order that they are
visited. This is used to find a topological  ordering of a graph.
"""
function depth_first_sort(measurement_dag, n_nodes, nodes_to_include)
    visited = falses(n_nodes)
    ordering = []

    function dfs(node)
        visited[node] = true
        for neighbor in measurement_dag[node]
            if !visited[neighbor]
                dfs(neighbor)
            end
        end
        push!(ordering, node)
    end

    for node in nodes_to_include
        if !visited[node]
            dfs(node)
        end
    end

    return ordering
end

"""
Given a DAG, finds  layering in the dag which minimizes the width due to
the ASG adding nodes to the DAG. This is done by finding the first layer in
the graph that can accommodate each node as it is created. If it cannot find
a layer with sufficently small width, then it will increase the width of the
layering to fit the node at the last layer currently being laid.
"""
function unadjustable_coffman_grahm(measurement_dag, asg, nodes_to_include, verbose)
    layering = [[] for _ in range(1, asg.n_nodes)]
    inv_layering = zeros(UInt, asg.n_nodes)

    max_layer = 1
    for node in VerboseIterator(
        depth_first_sort(measurement_dag, asg.n_nodes, nodes_to_include),
        verbose,
        "Creating time optimal layering..."
    )
        # Find the maximum layer of the neighbors
        min_layer = 1
        for neighbor in measurement_dag[node]
            min_layer = max(min_layer, inv_layering[neighbor] + 1)
        end

        # Update the rank of the node
        push!(layering[min_layer], node)
        inv_layering[node] = min_layer
        max_layer = max(max_layer, min_layer)
    end

    println("max_layer: ", max_layer)
    return resize!(layering, max_layer)
end

"""
Create the layering based on the longest path in the DAG. This is done by
finding the longest path from a source to each node. The layer of each node
is then determined by the longest path from a source.

Attributes:
    measurement_dag (Vector{Vector{Qubit}}): A dependency graph of which qubits
        need to be measured before which other qubits. The first index
        is the qubit which needs to be measured, and the vector contained
        in that index is the qubits which need to be measured before it.
    n_nodes (Qubit): The number of qubits in the circuit.
    nodes_to_include (Vector{Qubit}): The nodes which should be included
        in the DAG.

Returns:
    longest_path (Vector{Vector{Qubit}}): The layer of each node in the DAG.
"""
function longest_path_layering(measurement_dag, reverse_dag, n_nodes, nodes_to_include::Vector{Qubit}, verbose::Bool=false)
    longest_path = zeros(Qubit, n_nodes)

    sorted_nodes = depth_first_sort(reverse_dag, n_nodes, nodes_to_include)
    nodes_to_include = Set(nodes_to_include)

    final_layer = 0
    for u in VerboseIterator(sorted_nodes, verbose, "Assigning path lengths...")
        for v in measurement_dag[u]
            if v in nodes_to_include
                longest_path[v] = max(longest_path[v], longest_path[u] + 1)
            end
        end
        final_layer = max(final_layer, longest_path[u])
    end

    verbose && println("Creating layering...")
    layers = [[] for _ in range(1, final_layer + 1)]
    for node in nodes_to_include
        # correct for reverse layering given by above
        corrected_layer = final_layer - longest_path[node] + 1
        append!(layers[corrected_layer], node)
    end

    return layers
end



"""
Kahn's algorithm for topological sorting. This is used to find the layering
of the DAG for the variable width optimization. We also choose to prioritize
nodes with the smallest neighborhoods first, as this tends to produce better
results as it allows for all the neighbors of a highly connected node to be
measured before the highly connected node.

Attributes:
    measurement_dag (Vector{Vector{Qubit}}): A dependency graph of which qubits
        need to be measured before which other qubits. The first index
        is the qubit which needs to be measured, and the vector contained
        in that index is the qubits which need to be measured before it.
        For example, measurement_dag[3] = [6, 7] means that we must measure
        qubits 6 and 7 before qubit 3.
    n_nodes (Qubit): The number of qubits in the circuit.
    nodes_to_include (Vector{Qubit}): The nodes which should be included
        in the measurement DAG.
    asg (AlgorithmSpecificGraph): The ASG object containing the information of the
        prepared state's conectivity.
"""
function kahns_algorithm(
    measurement_dag::Vector{Vector{Qubit}},
    reverse_dag::Vector{Vector{Qubit}},
    n_nodes::Qubit,
    nodes_to_include::Vector{Qubit},
    asg,
    verbose::Bool=false,
)::Vector{Qubit}
    in_degree = zeros(Int, n_nodes)
    for node in nodes_to_include
        in_degree[node] = length(measurement_dag[node])
    end

    queue = Vector{Qubit}([])
    for node in nodes_to_include
        if in_degree[node] == 0
            push!(queue, node)
        end
    end
    # start with nodes that require the smallest neighborhoods
    # sort!(queue, by=x -> length(asg.edge_data[x]))

    ordering = Vector{Qubit}([])

    if verbose
        println("Performing topological sort via Kahn's Algorithm...")
        total_length = length(in_degree)
        counter = dispcnt = 0
        start_time = time()
    end

    curr_physical_nodes = Set{Qubit}([])
    measured_nodes = Set{Qubit}([])

    while !isempty(queue)
        # add nodes with the smallest neighborhoods first. This will help
        # measure the nodes with the larger neighborhoods later, which
        # will cut down on the number of nodes that need to be added to
        # measure the large nodes.
        node = queue[1]
        min_pos = 1
        min_node_cost = 1000000000
        # Calculate which qubits would exist if we added this node
        for (pos, possible_node) in enumerate(queue)
            new_nodes_to_add = setdiff(get_neighborhood(possible_node, asg), measured_nodes)
            num_qubits_after_adding_node = length(union(curr_physical_nodes, new_nodes_to_add))
            if num_qubits_after_adding_node < min_node_cost
                node = possible_node
                min_pos = pos
                min_node_cost = num_qubits_after_adding_node
            end
            if num_qubits_after_adding_node < 5
                break
            end
        end
        deleteat!(queue, min_pos)

        # update the current physical nodes to reflect the addition of the new node
        new_nodes_to_add = setdiff(get_neighborhood([node], asg), measured_nodes)
        union!(curr_physical_nodes, new_nodes_to_add)
        push!(measured_nodes, node)
        setdiff!(curr_physical_nodes, measured_nodes)

        push!(ordering, node)
        for neighbor in reverse_dag[node]
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0
                push!(queue, neighbor)
            end
        end

        # Show progress in real time
        counter += 1
        dispcnt += 1

        if verbose && dispcnt >= 1000
            percent = round(Int, 100 * counter / total_length)
            elapsed_time = round(time() - start_time, digits=2)
            print("\r$(percent)% ($counter) completed in $(elapsed_time)s")
            dispcnt = 0  # Reset display counter
        end
    end

    if verbose
        elapsed = round(time() - start_time, digits=2)
        println("\r100% ($counter) completed in $erase_line$(elapsed)s")
    end

    return ordering
end

function get_new_num_node_after_adding_qubit(new_qubit, asg, curr_physical_nodes, measured_nodes)
    new_nodes_to_add = setdiff(get_neighborhood(new_qubit, asg), measured_nodes)
    return length(union(curr_physical_nodes, new_nodes_to_add))
end

"""
Given a DAG, finds  layering in the dag which minimizes the width due to
the ASG adding nodes to the DAG. This is done by finding the first layer in
the graph that can accommodate each node as it is created. If it cannot find
a layer with sufficently small width, then it will increase the width of the
layering to fit the node at the last layer currently being laid.
"""
function variable_width(measurement_dag, reverse_dag, sparse_dag, asg, max_width::Int, nodes_to_include::Vector{Qubit}, verbose::Bool=false)
    space_optimized = max_width == 1
    sorted_nodes = kahns_algorithm(measurement_dag, reverse_dag, asg.n_nodes, nodes_to_include, asg, verbose)

    # create a layering that is just the topological sort
    ordering_layering = []
    for node in sorted_nodes
        push!(ordering_layering, [node])
    end
    min_logical_qubits = get_num_logical_qubits(ordering_layering, asg)

    if space_optimized == 1
        max_width = min_logical_qubits
    elseif max_width < min_logical_qubits
        @warn "max_width $max_width is too small. Setting max width to $min_logical_qubits."
    end

    curr_physical_nodes = get_neighborhood(ordering_layering[1], asg)
    measured_nodes = Set{Qubit}([])

    verbose && println("Combining adjacent timesteps without increasing qubit number...")
    curr_layer = Vector{Qubit}([sorted_nodes[1]])
    layering = Vector{Vector{Qubit}}([])
    for new_node_to_add in VerboseIterator(
        sorted_nodes[2:end],
        verbose,
        "Combining adjacent timesteps without increasing qubit number...",
    )
        new_neighborhood_to_add = setdiff(get_neighborhood(new_node_to_add, asg), measured_nodes)
        union!(curr_physical_nodes, new_neighborhood_to_add)

        if length(curr_physical_nodes) <= max_width && isempty(intersect(sparse_dag[new_node_to_add], curr_physical_nodes))
            push!(curr_layer, new_node_to_add)
        else
            push!(layering, curr_layer)
            union!(measured_nodes, curr_layer)
            setdiff!(curr_physical_nodes, measured_nodes)
            curr_layer = [new_node_to_add]
        end
    end
    push!(layering, curr_layer)

    return layering
end

function get_neighborhood(centers, asg)
    neighborhood = Set{Qubit}([])
    for center in centers
        for neighbor in asg.edge_data[center]
            push!(neighborhood, neighbor)
        end
    end

    return union(neighborhood, centers)
end


"""
Get the number of logical qubits in the circuit. This is done by finding
the maximum number of physical qubits which are connected to each other
through the conditional Pauli operators at each layer of the pauli tracker.
"""
function get_num_logical_qubits(layering, asg, verbose=false)
    curr_physical_nodes = get_neighborhood(layering[1], asg)
    n_logical_qubits = length(curr_physical_nodes)
    measured_nodes = Set{Qubit}([])

    # iterate through every pair of consecutive layers
    for i in VerboseIterator(1:length(layering)-1, verbose, "Calculating number of logical qubits...")
        union!(measured_nodes, layering[i])
        added_nodes = layering[i+1]

        setdiff!(curr_physical_nodes, layering[i])
        new_nodes_to_add = setdiff(get_neighborhood(added_nodes, asg), measured_nodes)
        union!(curr_physical_nodes, new_nodes_to_add)

        n_logical_qubits = max(n_logical_qubits, length(curr_physical_nodes))
    end

    return n_logical_qubits
end

function get_n_measurement_steps(pauli_tracker::PauliTracker)
    return length(pauli_tracker.layering)
end
