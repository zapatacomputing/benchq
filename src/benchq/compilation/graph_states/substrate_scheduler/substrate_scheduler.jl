# This file contains the functions to schedule the measurements of a graph state on a quantum computer.
# This file is not well tested as Athena did not have time to write tests for it. It is also not well documented
# so you might want to reach out to her if you have questions on how it works.

function two_row_scheduler(asg, pauli_tracker, num_logical_qubits, optimization, verbose=false)
    if optimization == "Time"
        return time_optimal_two_row_scheduler(asg, pauli_tracker, num_logical_qubits, verbose)
    elseif optimization == "Space"
        return space_optimal_two_row_scheduler(asg, pauli_tracker, num_logical_qubits, verbose)
    elseif optimization == "Variable"
        return space_optimal_two_row_scheduler(asg, pauli_tracker, num_logical_qubits, verbose)
    else
        throw(ArgumentError("Invalid optimization type."))
    end
end

function get_max_independent_set(asg)
    # Initialize an empty set to store the maximal independent set
    independent_set = Set{Int}()

    # Create an array to keep track of the state of each vertex (included or not)
    included = falses(asg.n_nodes)

    # Iterate over each vertex in the graph
    for v in 1:asg.n_nodes
        # Check if the vertex is not included and its neighbors are not included
        if !included[v] && all(!included[neighbor] for neighbor in asg.edge_data[v])
            # Add the vertex to the independent set
            push!(independent_set, v)
            # Mark the vertex as included
            included[v] = true
        end
    end

    return independent_set
end

function time_optimal_two_row_scheduler(asg, pauli_tracker, num_logical_qubits, verbose=false)
    # Here we use the procedure of https://arxiv.org/abs/2306.03758 to schedule measurements
    # We choose to skip phase 3 of the optimization. Because it is costly in terms of compilation
    # time and does not provide a significant improvement in the number of tocks required.

    # Phase 1: We can choose to ignore the nodes in a maximal independent set of the graph
    # as they can be initialized in a way that satisfies the stabilizers of the graph state
    nodes_satisfied_by_initialization = get_max_independent_set(asg)

    curr_physical_nodes = get_neighborhood(pauli_tracker.layering[1], asg, 2)
    measured_nodes = Set{Qubit}([])
    new_nodes_to_add = curr_physical_nodes
    satisfied_nodes = Set{Qubit}([])

    patches_to_node = [-1 for _ in 1:num_logical_qubits]
    node_to_patch = [-1 for _ in 1:asg.n_nodes]

    num_tocks_for_graph_creation = [0 for _ in 1:length(pauli_tracker.layering)]
    num_t_states_per_layer = [0 for _ in 1:length(pauli_tracker.layering)]
    num_rotations_per_layer = [0 for _ in 1:length(pauli_tracker.layering)]

    for layer_num in VerboseIterator(1:length(pauli_tracker.layering), verbose, "Scheduling Clifford operations...")
        # assign nodes to patches randomly by simply finding the first open patch and placing the node there
        for new_node in new_nodes_to_add
            node_placement_found = false
            for (patch, node_in_patch) in enumerate(patches_to_node)
                if node_in_patch == -1
                    patches_to_node[patch] = new_node
                    node_to_patch[new_node] = patch
                    node_placement_found = true
                    break
                end
            end
            if !node_placement_found
                println("Error: No patch found for node ", new_node)
            end
        end

        # Phase 2: Schedule the multi-qubit measurements for each of the remaining stabilizers of the graph state
        # which correspond to nodes in the graph.

        # get the bar for each node we are measuring in this layer
        nodes_to_satisfy_this_layer = setdiff(get_neighborhood(pauli_tracker.layering[layer_num], asg), satisfied_nodes)
        union!(satisfied_nodes, nodes_to_satisfy_this_layer)
        bars = []
        for node in setdiff(nodes_to_satisfy_this_layer, nodes_satisfied_by_initialization)
            bar = [node_to_patch[node], node_to_patch[node]]
            for neighbor in asg.edge_data[node]
                if node_to_patch[neighbor] < bar[1] & node in curr_physical_nodes
                    bar[1] = node_to_patch[neighbor]
                end
                if node_to_patch[neighbor] > bar[2] & node in curr_physical_nodes
                    bar[2] = node_to_patch[neighbor]
                end
            end
            push!(bars, bar)
            if pauli_tracker.measurements[node][1] in [T_code, T_Dagger_code]
                num_t_states_per_layer[layer_num] += 1
            end
            if pauli_tracker.measurements[node][1] == RZ_code
                num_rotations_per_layer[layer_num] += 1
            end
        end
        sort!(bars, by=x -> x[2])

        # layer the bars
        while length(bars) > 0
            bar = bars[1]
            bars = bars[2:end]
            i = 1
            bars_length = length(bars)
            while i <= bars_length
                if bars[i][1] > bar[2]
                    bar[2] = bars[i][2]
                    deleteat!(bars, i)
                    bars_length -= 1
                end
                i += 1
            end
            num_tocks_for_graph_creation[layer_num] += 1
        end

        if layer_num < length(pauli_tracker.layering)
            union!(measured_nodes, pauli_tracker.layering[layer_num])
            for measured_node in pauli_tracker.layering[layer_num]
                patches_to_node[node_to_patch[measured_node]] = -1
            end
            added_nodes = pauli_tracker.layering[layer_num+1]

            setdiff!(curr_physical_nodes, pauli_tracker.layering[layer_num])
            new_nodes_to_add = setdiff(setdiff(get_neighborhood(added_nodes, asg, 2), measured_nodes), curr_physical_nodes)
            union!(curr_physical_nodes, new_nodes_to_add)
        end
    end

    verbose && println("num_tocks_for_graph_creation: ", sum(num_tocks_for_graph_creation))

    return num_tocks_for_graph_creation, num_t_states_per_layer, num_rotations_per_layer
end

function space_optimal_two_row_scheduler(asg, pauli_tracker, num_logical_qubits, verbose=false)
    # In this strategy we simply apply the cz gates that are requires in order to create the graph state
    curr_physical_nodes = get_neighborhood(pauli_tracker.layering[1], asg)
    measured_nodes = Set{Qubit}([])
    new_nodes_to_add = curr_physical_nodes
    satisfied_edges = copy(asg.edge_data)

    patches_to_node = [-1 for _ in 1:num_logical_qubits]
    node_to_patch = [-1 for _ in 1:asg.n_nodes]

    num_tocks_for_graph_creation = [0 for _ in 1:length(pauli_tracker.layering)]
    num_t_states_per_layer = [0 for _ in 1:length(pauli_tracker.layering)]
    num_rotations_per_layer = [0 for _ in 1:length(pauli_tracker.layering)]

    for layer_num in VerboseIterator(1:length(pauli_tracker.layering), verbose, "Scheduling Clifford operations...")
        # assign nodes to patches by simply finding the first open patch and placing the node there
        # println("Assigning Nodes to Patches...")
        begin
            for new_node in new_nodes_to_add
                node_placement_found = false
                for (patch, node_in_patch) in enumerate(patches_to_node)
                    if node_in_patch == -1
                        patches_to_node[patch] = new_node
                        node_to_patch[new_node] = patch
                        node_placement_found = true
                        break
                    end
                end
                if !node_placement_found
                    println("Error: No patch found for node ", new_node)
                end
            end
        end

        # Enact each of the edges of the graph individually
        # println("layer_num: ", layer_num)
        # println("Getting Bars...")
        begin
            bars = []
            for node in pauli_tracker.layering[layer_num]
                for neighbor in asg.edge_data[node]
                    if neighbor in satisfied_edges[node] && node in satisfied_edges[neighbor]
                        toggle_edge!(satisfied_edges, node, neighbor)
                        push!(bars, [node_to_patch[node], node_to_patch[neighbor]])
                    end
                end
            end
        end
        # println("nodes_to_satisfy_this_layer: ", Set([Int(x) for x in pauli_tracker.layering[layer_num]]))
        # println("patches_to_node: ", patches_to_node)

        sort!(bars, by=x -> x[2])

        # layer the bars to parallelize them
        # println("bars: ", bars)
        # println("Layering Bars...")
        begin
            while length(bars) > 0
                bar = bars[1]
                bars = bars[2:end]
                i = 1
                bars_length = length(bars)
                while i <= bars_length
                    if bars[i][1] > bar[2]
                        bar[2] = bars[i][2]
                        deleteat!(bars, i)
                        bars_length -= 1
                    end
                    i += 1
                end
                num_tocks_for_graph_creation[layer_num] += 1
            end
            # each cz requires 2 tocks
            num_tocks_for_graph_creation[layer_num] *= 2
        end

        for node in pauli_tracker.layering[layer_num]
            if pauli_tracker.measurements[node][1] in [T_code, T_Dagger_code]
                num_t_states_per_layer[layer_num] += 1
            end
            if pauli_tracker.measurements[node][1] == RZ_code
                num_rotations_per_layer[layer_num] += 1
            end
        end

        # println("preparing for next layer")
        begin
            if layer_num < length(pauli_tracker.layering)
                union!(measured_nodes, pauli_tracker.layering[layer_num])
                for measured_node in pauli_tracker.layering[layer_num]
                    patches_to_node[node_to_patch[measured_node]] = -1
                end
                added_nodes = pauli_tracker.layering[layer_num+1]

                setdiff!(curr_physical_nodes, pauli_tracker.layering[layer_num])
                new_nodes_to_add = setdiff(setdiff(get_neighborhood(added_nodes, asg), measured_nodes), curr_physical_nodes)
                union!(curr_physical_nodes, new_nodes_to_add)
            end
        end
    end

    verbose && println("num_tocks_for_graph_creation: ", sum(num_tocks_for_graph_creation))

    return num_tocks_for_graph_creation, num_t_states_per_layer, num_rotations_per_layer
end
