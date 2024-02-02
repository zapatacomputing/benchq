################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
BUFFER_SIZE = 100
if BUFFER_SIZE % 2 != 0
    error("Buffer size must be even.")
end
"""
Initialize the graph state with a buffer of teleportations for each qubit.
This allows the graph state to be stitched with other graph states before it.

Attributes:
    max_graph_size (UInt32): maximum number of nodes in the graph
    n_qubits (UInt32): number of qubits in the graph
    layering_optimization (Bool): whether or not to use the layering optimization

Returns:
    asg (AlgorithmSpecificGraph): graph after initialization
    pauli_tracker (PauliTracker): pauli tracker for the graph
"""
function initialize_for_graph_input(max_graph_size, n_qubits, layering_optimization, max_num_qubits)
    asg = AlgorithmSpecificGraphAllZero(max_graph_size, 0)
    pauli_tracker = PauliTracker(0, layering_optimization, max_num_qubits)
    for _ = 1:n_qubits
        # create start to next buffer
        asg.n_nodes += 1
        push!(asg.stitching_properties.gate_output_nodes, Qubit(asg.n_nodes))
        add_new_qubit_to_pauli_tracker!(pauli_tracker)
        asg.sqs[asg.n_nodes] = I_code # start buffer in the |+> state
        asg.sqp[asg.n_nodes] = I_code
        # create a buffer of teleportations for each qubit
        teleportation!(
            asg,
            last(asg.stitching_properties.gate_output_nodes),
            pauli_tracker,
            default_hyperparams,
            BUFFER_SIZE,
        )
        # println("data nodes: $(asg.stitching_properties.gate_output_nodes)")
    end
    return asg, pauli_tracker
end

"""
Add the output nodes to the graph state by creating the beginning of
a buffer of teleportations for each qubit. This allows the graph state
to be stitched with other graph states after it. The excess nodes in the
buffer are removed from the graph state and marked to be removed by the
minimize_node_labels! function.

This function adds two teleporations to the buffer (corresponding to adding
4 qubits to the graph state). We needed 2 teleportations to ensure that the
buffer only has hadamard gates as local symplectics. We have to preserve
the first qubit in the buffer because it contains all the pauli tracking
information that would be passed to the buffer.

Both of these facts together prove that this stitching method is optimal
for the case of stitching two graph states together produced from ruby
slippers. More optimial stitching method might exist for other ASG
producing algorithms such as Jabalizer.

Attributes:
    asg (AlgorithmSpecificGraph): graph to be stitched
    pauli_tracker (PauliTracker): pauli tracker for the graph
    nodes_to_remove (Vector{UInt32}): nodes to be removed from the graph
"""
function add_output_nodes!(asg, pauli_tracker, nodes_to_remove::Set{Qubit})
    data_nodes = collect(asg.stitching_properties.gate_output_nodes)
    for data_node in asg.stitching_properties.gate_output_nodes
        teleportation!(asg, data_node, pauli_tracker, default_hyperparams, 4)
        push!(asg.stitching_properties.graph_output_nodes, asg.n_nodes - 3)

        remove_edge!(asg.edge_data, asg.n_nodes, asg.n_nodes - 1)
        remove_edge!(asg.edge_data, asg.n_nodes - 1, asg.n_nodes - 2)
        remove_edge!(asg.edge_data, asg.n_nodes - 2, asg.n_nodes - 3)

        pauli_tracker.cond_paulis[asg.n_nodes] = [[], []]
        pauli_tracker.cond_paulis[asg.n_nodes-1] = [[], []]
        pauli_tracker.cond_paulis[asg.n_nodes-2] = [[], []]

        push!(nodes_to_remove, asg.n_nodes)
        push!(nodes_to_remove, asg.n_nodes - 1)
        push!(nodes_to_remove, asg.n_nodes - 2)
    end

    new_graph_output_nodes = []
    for i in eachindex(data_nodes)
        push!(new_graph_output_nodes, asg.stitching_properties.graph_output_nodes[i])
        push!(new_graph_output_nodes, data_nodes[i])
    end
    asg.stitching_properties.graph_output_nodes = new_graph_output_nodes

    asg.stitching_properties.gate_output_nodes = []
    asg.stitching_properties.gives_graph_output = true
end

"""
Given a graph state which has been initialized with a buffer of teleportations
for each qubit, this function finds the part of the buffer that was not consumed
during graph creation. It hen removes the connections in the unconsumed buffer nodes
and marks them to be removed from the graph state. It also dismantles the dependencies
in the pauli tracker so that the unconsumed nodes are not considered in the layering.

Attributes:
    asg (AlgorithmSpecificGraph): graph to be pruned
    pauli_tracker (PauliTracker): pauli tracker for the graph
    n_qubits (UInt32): number of qubits in the graph
    nodes_to_remove (Vector{UInt32}): nodes to be removed from the graph
"""
function prune_buffer!(asg, pauli_tracker, n_qubits, nodes_to_remove::Set{Qubit})
    for i = 1:n_qubits
        buffer_start = (i - 1) * (BUFFER_SIZE + 1) + 3
        buffer_end = i * (BUFFER_SIZE + 1) # +1 to include the data qubit
        correct_sqs_start =
            asg.sqs[buffer_start] == H_code && asg.sqs[buffer_start+1] == H_code
        correct_sqp_start =
            asg.sqp[buffer_start] == I_code && asg.sqs[buffer_start+1] == I_code
        correct_adj_start =
            asg.edge_data[buffer_start+1] == Set([buffer_start + 1, buffer_start - 1]) &&
            asg.edge_data[buffer_start] == Set([buffer_start + 1])
        if correct_sqs_start && correct_sqp_start && correct_adj_start
            throw(
                DomainError(
                    "Entire buffer was consumed! Please either:\n" +
                    "1. Increase the BUFFER_SIZE variable (may lead to high resource counts)\n" +
                    "2. Decrease the ratio of two qubit gates to T gates in your circuit.",
                ),
            )
        end
        for j = buffer_start:2:buffer_end
            adj_consumed =
                asg.edge_data[j-1] != Set([j, j - 2]) ||
                asg.edge_data[j-2] != Set([j - 1, j - 3])
            sqs_consumed = asg.sqs[j-1] != H_code || asg.sqs[j] != H_code
            sqp_consumed = asg.sqp[j-1] != I_code || asg.sqp[j] != I_code
            if !adj_consumed || !sqs_consumed || !sqp_consumed
                if j == buffer_end
                    push!(asg.stitching_properties.graph_input_nodes, j - 1)
                    push!(asg.stitching_properties.graph_input_nodes, j - 2)
                    break
                end
                pauli_tracker.cond_paulis[j+1] = [[], []]
                pauli_tracker.cond_paulis[j] = [[], []]
                pauli_tracker.cond_paulis[j-1] = [[], []]
                pauli_tracker.cond_paulis[j-2] = [[], []]
                remove_edge!(asg.edge_data, j, j - 1)
                remove_edge!(asg.edge_data, j - 1, j - 2)
                push!(nodes_to_remove, j - 1)
                push!(nodes_to_remove, j - 2)
            else
                push!(asg.stitching_properties.graph_input_nodes, j - 1)
                push!(asg.stitching_properties.graph_input_nodes, j - 2)
                break
            end
        end
    end

    asg.stitching_properties.takes_graph_input = true
end

"""
Given some nodes which have been removed from the graph, this function
relabels the nodes in the graph to skip the removed nodes. Thus function
must run in O(n_nodes^2) time, so it's best to just to be used to test
that stitching works for small examples.

Attributes:
    asg (AlgorithmSpecificGraph): graph to be relabeled
    pauli_tracker (PauliTracker): pauli tracker for the graph
    nodes_to_remove (Vector{UInt32}): nodes to be removed from the graph

Returns:
    asg (AlgorithmSpecificGraph): graph after relabeling
    pauli_tracker (PauliTracker): pauli tracker after relabeling
"""
function minimize_node_labels!(asg::AlgorithmSpecificGraph, pauli_tracker, nodes_to_remove)
    if isempty(nodes_to_remove)
        return asg, pauli_tracker
    end

    nodes_to_remove = sort(collect(nodes_to_remove))
    nodes_to_keep = setdiff(1:asg.n_nodes, nodes_to_remove)


    # relabel nodes to skip isolated nodes
    for (new_node_index, old_node_index) in enumerate(nodes_to_keep)
        for neighborhood in asg.edge_data
            for neighbor in neighborhood
                if neighbor == old_node_index
                    delete!(neighborhood, old_node_index)
                    push!(neighborhood, new_node_index)
                end
            end
        end
        asg.stitching_properties.gate_output_nodes = [
            old_node_index == node ? new_node_index : node for
            node in asg.stitching_properties.gate_output_nodes
        ]
        asg.stitching_properties.graph_input_nodes = [
            old_node_index == node ? new_node_index : node for
            node in asg.stitching_properties.graph_input_nodes
        ]
        asg.stitching_properties.graph_output_nodes = [
            old_node_index == node ? new_node_index : node for
            node in asg.stitching_properties.graph_output_nodes
        ]
    end

    for i = 1:length(pauli_tracker.cond_paulis)
        for j = 1:length(pauli_tracker.cond_paulis[i])
            for k = 1:length(pauli_tracker.cond_paulis[i][j])
                if pauli_tracker.cond_paulis[i][j][k] in nodes_to_remove
                    println(i, " ", j, " ", k)
                    error(
                        "Node $(pauli_tracker.cond_paulis[i][j][k]) was designated " *
                        "for relabelling but was not removed.",
                    )
                else
                    pauli_tracker.cond_paulis[i][j][k] =
                        findfirst(nodes_to_keep .== pauli_tracker.cond_paulis[i][j][k])
                end
            end
        end
    end

    for i = 1:length(pauli_tracker.layering)
        sublist = pauli_tracker.layering[i]
        for j = 1:length(sublist)
            if sublist[j] in nodes_to_keep
                sublist[j] = findfirst(nodes_to_keep .== sublist[j])
            elseif sublist[j] in nodes_to_remove
                error(
                    "Node $(sublist[j]) was designated for relabelling but was " *
                    "included in layering.",
                )
            end
        end
        pauli_tracker.layering[i] = sublist
    end
    pauli_tracker.layering = [layer for layer in pauli_tracker.layering if !isempty(layer)]


    # delete isolated nodes from data structures
    for node in reverse(nodes_to_remove)
        deleteat!(asg.edge_data, node)
        deleteat!(asg.sqs, node)
        deleteat!(asg.sqp, node)
        deleteat!(pauli_tracker.cond_paulis, node)
        deleteat!(pauli_tracker.measurements, node)

        pauli_tracker.cond_paulis[:] .=
            [filter(x -> x != node, frame) for frame in pauli_tracker.cond_paulis[:]]
    end

    asg.n_nodes = length(nodes_to_keep)
    pauli_tracker.n_nodes = length(nodes_to_keep)

    return asg, pauli_tracker
end


"""
Given two graphs which are stitchable, stitchs the two graphs.
Assumes graphs have minimized node lables as well as that they
have the same number of qubits. This function is not optimized
for speed, so It is mainly used for testing purposes.

Attributes:
    asg_1 (AlgorithmSpecificGraph): first graph to be stitched
    pauli_tracker_1 (PauliTracker): pauli tracker for first graph
    asg_2 (AlgorithmSpecificGraph): second graph to be stitched
    pauli_tracker_2 (PauliTracker): pauli tracker for second graph

Returns:
    asg_1 (AlgorithmSpecificGraph): first graph after stitching
    pauli_tracker_1 (PauliTracker): pauli tracker for first graph after stitching
"""
function stitch_graphs(asg_1, pauli_tracker_1, asg_2, pauli_tracker_2)
    if !(
        asg_1.stitching_properties.gives_graph_output &&
        asg_2.stitching_properties.takes_graph_input
    )
        error(
            """Provided graphs don't have the correct types of inputs and outputs to be stitched.
            Graph 1 gives graph output: $(asg_1.stitching_properties.gives_graph_output)
            Graph 2 takes graph input: $(asg_2.stitching_properties.takes_graph_input)
            """,
        )
    end
    if (
        length(asg_1.stitching_properties.graph_output_nodes) !=
        length(asg_2.stitching_properties.graph_input_nodes)
    )
        error(
            """Provided graphs don't have the correct numbers of inputs and outputs to be stitched.
            Outputs: $(asg_1.stitching_properties.graph_output_nodes)
            Inputs: $(asg_2.stitching_properties.graph_input_nodes)
            """,
        )
    end

    shift = asg_1.n_nodes
    for neighborhood in asg_2.edge_data
        push!(asg_1.edge_data, Set(neighborhood .+ shift))
    end
    append!(asg_1.sqs, asg_2.sqs)
    append!(asg_1.sqp, asg_2.sqp)
    asg_1.n_nodes += asg_2.n_nodes

    for neighborhood in pauli_tracker_2.cond_paulis
        push!(
            pauli_tracker_1.cond_paulis,
            [neighborhood[1] .+ shift, neighborhood[2] .+ shift],
        )
    end
    for layer in pauli_tracker_2.layering
        push!(pauli_tracker_1.layering, layer .+ shift)
    end

    append!(pauli_tracker_1.measurements, pauli_tracker_2.measurements)
    pauli_tracker_1.n_nodes += pauli_tracker_2.n_nodes

    for index_of_inner_output_node =
        2:2:length(asg_1.stitching_properties.graph_output_nodes)
        inner_output_node =
            asg_1.stitching_properties.graph_output_nodes[index_of_inner_output_node]
        outter_output_node =
            asg_1.stitching_properties.graph_output_nodes[index_of_inner_output_node-1]
        outter_input_node =
            asg_2.stitching_properties.graph_input_nodes[index_of_inner_output_node] + shift
        inner_input_node =
            asg_2.stitching_properties.graph_input_nodes[index_of_inner_output_node-1] + shift

        # connect input node to output node
        push!(asg_1.edge_data[outter_output_node], outter_input_node)
        push!(asg_1.edge_data[outter_input_node], outter_output_node)

        pauli_tracker_1.cond_paulis[outter_input_node] =
            [[inner_output_node], [outter_output_node]]
        pauli_tracker_1.cond_paulis[inner_input_node] = [[outter_output_node], []]
    end


    asg_1.stitching_properties.gate_output_nodes =
        asg_2.stitching_properties.gate_output_nodes .+ shift
    asg_1.stitching_properties.graph_output_nodes =
        asg_2.stitching_properties.graph_output_nodes .+ shift

    return asg_1, pauli_tracker_1
end
