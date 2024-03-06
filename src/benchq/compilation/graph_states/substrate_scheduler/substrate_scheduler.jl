# mutable struct TwoRowSchedule
#     schedule
#     num_tocks_for_graph_creation
#     num_t_states_per_layer
#     num_rotations_per_layer
# end


function two_row_scheduler(asg, pauli_tracker, num_logical_qubits, verbose)
    curr_physical_nodes = get_neighborhood(pauli_tracker.layering[1], asg)
    measured_nodes = Set{Qubit}([])
    new_nodes_to_add = curr_physical_nodes

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
        bars = []
        for node in pauli_tracker.layering[layer_num]
            bar = [node_to_patch[node], node_to_patch[node]]
            for neighbor in asg.edge_data[node]
                if node_to_patch[neighbor] < bar[1]
                    bar[1] = node_to_patch[neighbor]
                end
                if node_to_patch[neighbor] > bar[2]
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
        bars = sort(bars, by=x -> x[2])

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
            new_nodes_to_add = setdiff(setdiff(get_neighborhood(added_nodes, asg), measured_nodes), curr_physical_nodes)
            union!(curr_physical_nodes, new_nodes_to_add)
        end
    end

    return num_tocks_for_graph_creation, num_t_states_per_layer, num_rotations_per_layer
end