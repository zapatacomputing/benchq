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

function time_optimal_two_row_scheduler(asg, pauli_tracker, num_logical_qubits, verbose=false)
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
        # assign nodes to patches by simply finding the first open patch and placing the node there
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

        # get the bar for each node we are measuring in this layer
        nodes_to_satisfy_this_layer = setdiff(get_neighborhood(pauli_tracker.layering[layer_num], asg), satisfied_nodes)
        union!(satisfied_nodes, nodes_to_satisfy_this_layer)
        bars = []
        for node in nodes_to_satisfy_this_layer
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
    curr_physical_nodes = get_neighborhood(pauli_tracker.layering[1], asg)
    measured_nodes = Set{Qubit}([])
    new_nodes_to_add = curr_physical_nodes
    satisfied_nodes = Set{Qubit}([])

    patches_to_node = [-1 for _ in 1:num_logical_qubits]
    node_to_patch = [-1 for _ in 1:asg.n_nodes]

    num_tocks_for_graph_creation = [0 for _ in 1:length(pauli_tracker.layering)]
    num_t_states_per_layer = [0 for _ in 1:length(pauli_tracker.layering)]
    num_rotations_per_layer = [0 for _ in 1:length(pauli_tracker.layering)]

    for layer_num in VerboseIterator(1:length(pauli_tracker.layering), verbose, "Scheduling Clifford operations...")
        # assign nodes to patches by simply finding the first open patch and placing the node there
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

        # Enact each of the edges of the graph individually
        bars = []
        nodes_to_satisfy_this_layer = setdiff(get_neighborhood(pauli_tracker.layering[layer_num], asg), satisfied_nodes)
        for node_1 in nodes_to_satisfy_this_layer
            for node_2 in nodes_to_satisfy_this_layer
                if node_to_patch[node_1] < node_to_patch[node_2]
                    push!(bars, [node_to_patch[node_1], node_to_patch[node_2]])
                end
            end
        end
        sort!(bars, by=x -> x[2])

        # layer the bars to parallelize them
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

    verbose && println("num_tocks_for_graph_creation: ", sum(num_tocks_for_graph_creation))

    return num_tocks_for_graph_creation, num_t_states_per_layer, num_rotations_per_layer
end
