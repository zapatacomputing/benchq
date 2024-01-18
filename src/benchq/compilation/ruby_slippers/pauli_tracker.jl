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
        the first index.
    n_nodes: Qubit
        The number of qubits in the circuit.
    layering: Vector{Vector{Qubit}}
        A vector containing order in which the qubits must be measured.
        The first index is the layer, and the vector contained in that
        index is the qubits in that layer. The qubits in each layer are
        measured in parallel.
    layering_optimization: String
        The optimization used to calculate the layering. Can be "ST-Volume",
        "Time", "Space", and "Variable".
    layer_width: Int
        The width parameter used for the space optimization. Corresponds to
        the maximum number of qubits which can be measured in each time
        step. Note that if one picks the number of qubits to be too small,
        we will resort to the smallest width which can fit the circuit.
"""
mutable struct PauliTracker
    cond_paulis::Vector{Vector{Vector{Qubit}}}
    measurements::Vector{Vector{Union{UInt8,Float64}}}
    n_nodes::Qubit
    layering::Vector{Vector{Qubit}}
    layering_optimization::String
    layer_width::Int

    PauliTracker(n_qubits, layering_optimization, layer_width) = new(
        [[[], []] for _ in range(1, n_qubits)],
        [[H_code, 0.0] for _ in range(1, n_qubits)],
        n_qubits,
        [],
        layering_optimization,
        layer_width,
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
        "layer_width" => pauli_tracker.layer_width,
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
            y             |    n     |       y      | Add self to predecessors
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
function get_predecessors(
    pauli_tracker::PauliTracker,
    target,
    predecessors,
    is_base::Bool=false,
    is_output::Bool=false,
)
    non_clifford_measurement =
        pauli_tracker.measurements[target][1] in non_clifford_gate_codes || is_output
    is_x_target = pauli_tracker.cond_paulis[target][1] != []

    if non_clifford_measurement
        if is_base
            if is_x_target
                for control in pauli_tracker.cond_paulis[target][1]
                    union!(
                        predecessors,
                        get_predecessors(pauli_tracker, control, predecessors),
                    )
                end
            end
        else
            push!(predecessors, target)
            if !is_x_target
                for control in pauli_tracker.cond_paulis[target][2]
                    union!(
                        predecessors,
                        get_predecessors(pauli_tracker, control, predecessors),
                    )
                end
            end
        end
    else
        if !is_base
            push!(predecessors, target)
            if pauli_tracker.measurements[target][1] == H_code
                for control in pauli_tracker.cond_paulis[target][1]
                    union!(
                        predecessors,
                        get_predecessors(pauli_tracker, control, predecessors),
                    )
                end
            elseif pauli_tracker.measurements[target][1] == I_code
                for control in pauli_tracker.cond_paulis[target][2]
                    union!(
                        predecessors,
                        get_predecessors(pauli_tracker, control, predecessors),
                    )
                end
            end
        end
    end

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
)
    new_dag = [[] for _ in range(1, pauli_tracker.n_nodes)]

    for node in nodes_to_include
        if pauli_tracker.measurements[node][1] in non_clifford_gate_codes ||
           node in output_nodes
            new_dag[node] = collect(
                get_predecessors(pauli_tracker, node, Set([]), true, node in output_nodes),
            )
        end
    end

    println("dag: ", new_dag)
    println("nodes to include: ", nodes_to_include)

    return new_dag
end

"""
A simple function for creating a measurement DAG. This DAG is not nearly as
efficient as the one created by get_measurement_dag, but it is much easier
to understand and thus is good for debugging stitching. It also preserves
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
function get_simple_measurement_dag(pauli_tracker::PauliTracker, nodes_to_include)
    new_dag = [[] for _ in range(1, pauli_tracker.n_nodes)]
    for node in nodes_to_include
        new_dag[node] =
            vcat(pauli_tracker.cond_paulis[node][1], pauli_tracker.cond_paulis[node][2])
    end

    return new_dag
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
function calculate_layering!(pauli_tracker::PauliTracker, asg, ignored_nodes)
    nodes_to_include = [node for node = 1:pauli_tracker.n_nodes if !(node in ignored_nodes)]

    if pauli_tracker.layering_optimization == "ST-Volume"
        output_nodes = asg.stitching_properties.graph_output_nodes
        measurement_dag = get_simple_measurement_dag(pauli_tracker, nodes_to_include)
        pauli_tracker.layering =
            gansner_layering(measurement_dag, pauli_tracker.n_nodes, nodes_to_include)
    elseif pauli_tracker.layering_optimization == "Time"
        output_nodes = asg.stitching_properties.graph_output_nodes
        measurement_dag =
            get_sparse_measurement_dag(pauli_tracker, output_nodes, nodes_to_include)
        pauli_tracker.layering =
            variable_width(measurement_dag, asg, typemax(Int), nodes_to_include)
    elseif pauli_tracker.layering_optimization == "Space"
        measurement_dag = get_simple_measurement_dag(pauli_tracker, nodes_to_include)
        pauli_tracker.layering = variable_width(
            measurement_dag,
            asg,
            maximum(length, asg.edge_data) + 1,
            nodes_to_include,
        )
    elseif pauli_tracker.layering_optimization == "Variable"
        @warn "Variable layering optimization is unstable. May produce incorrect results."
        measurement_dag = get_simple_measurement_dag(pauli_tracker, nodes_to_include)
        min_num_logical_qubits = maximum(length, asg.edge_data)
        if pauli_tracker.layer_width < min_num_logical_qubits
            if pauli_tracker.layer_width != -1
                println(
                    "Warning: Required number of logical qubits is too small " *
                    "for the circuit given. Using $(min_num_logical_qubits) " *
                    "logical qubits instead.",
                )
            end
            pauli_tracker.layer_width = min_num_logical_qubits
        end
        pauli_tracker.layering = variable_width(
            measurement_dag,
            asg,
            pauli_tracker.layer_width,
            nodes_to_include,
        )
    else
        error("Invalid layering optimization")
    end

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

function topological_sort(measurement_dag, n_nodes, nodes_to_include)
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

function variable_width(measurement_dag, asg, max_width::Int, nodes_to_include)
    layering = [[] for _ in range(1, asg.n_nodes)]
    inv_layering = zeros(UInt, asg.n_nodes)
    nodes_in_layer = fill(Set([]), asg.n_nodes)

    max_layer = 1
    for node in topological_sort(measurement_dag, asg.n_nodes, nodes_to_include)
        # Find the maximum layer of the neighbors
        min_layer = 1
        for neighbor in measurement_dag[node]
            min_layer = max(min_layer, inv_layering[neighbor] + 1)
        end

        # Find the first layer with enough remaining width for the node
        for layer = min_layer:asg.n_nodes
            bigger_layer = Set([node]) ∪ nodes_in_layer[layer]
            size = length(get_neighborhood(bigger_layer, asg))
            if size <= max_width
                # Update the rank of the node
                push!(layering[layer], node)
                inv_layering[node] = layer
                max_layer = max(max_layer, layer)
                # Update remaining width for the chosen layer
                nodes_in_layer[layer] = bigger_layer
                break
            end
        end
    end

    return resize!(layering, max_layer)
end

function get_neighborhood(centers, asg)
    neighborhood = Set([])
    for center in centers
        for neighbor in asg.edge_data[center]
            push!(neighborhood, neighbor)
        end
    end

    return union(neighborhood, centers)
end

function get_n_logical_qubits(pauli_tracker::PauliTracker, asg)
    active_nodes = pauli_tracker.layering[1]
    n_logical_qubits = length(active_nodes)

    for layer in pauli_tracker.layering
        setdiff!(active_nodes, layer)
        union!(active_nodes, get_neighborhood(layer, asg))
        n_logical_qubits = maximum(n_logical_qubits, length(active_nodes))
    end

    return n_logical_qubits
end


function get_n_measurement_steps(pauli_tracker::PauliTracker)
    return length(pauli_tracker.layering)
end
