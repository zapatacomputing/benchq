function two_row_scheduler(asg, pauli_tracker, num_logical_qubits)
    curr_physical_nodes = get_neighborhood(layering[1], asg)
    measured_nodes = Set{Qubit}([])
    new_nodes_to_add = curr_physical_nodes

    patches_to_node = [-1 for _ in 1:num_logical_qubits]
    node_to_patch = [-1 for _ in 1:asg.n_nodes]
    bars = [(-1, -1) for _ in 1:asg.n_nodes]

    measurement_steps_per_layer = [0 for _ in 1:length(pauli_tracker.layering)]
    num_t_states_per_layer = [0 for _ in 1:length(pauli_tracker.layering)]
    num_rotations_per_layer = [0 for _ in 1:length(pauli_tracker.layering)]

    for layer_num in VerboseIterator(1:length(layering), verbose, "Scheduling Clifford operations...")
        # assign nodes to patches by simply finding the first open patch and placing the node there
        for node in new_nodes_to_add
            for patch in patches
                if patch == -1
                    patches_to_node[patch] = node
                    node_to_patch[node] = patch
                    break
                end
            end
        end

        # get the bar for each node we are measuring in this layer
        for node in pauli_tracker.layering[layer_num]
            bar = [nodes_to_patch[node], nodes_to_patch[node]]
            for neighbor in asg.edge_data[node]
                if node_to_patch[neighbor] > bar[1]
                    bar[1] = node_to_patch[neighbor]
                end
                if node_to_patch[neighbor] < bar[2]
                    bar[2] = node_to_patch[neighbor]
                end
            end
            bars[node] = bar
            if pauli_tracker.measurements[node][1] in [T_code, T_dagger_code]
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
            for i in 1:length(bars)
                if bars[i][1] > bar[2]
                    bar[2] = bars[i][2]
                    bars = bars[1:i-1] + bars[i+1:end]
                end
            end
            measurement_steps_per_layer[layer_num] += 1
        end

        if layer_num < length(pauli_tracker.layering)
            union!(measured_nodes, pauli_tracker.layering[layer_num])
            added_nodes = pauli_tracker.layering[layer_num+1]

            setdiff!(curr_physical_nodes, pauli_tracker.layering[layer_num])
            new_nodes_to_add = setdiff(get_neighborhood(added_nodes, asg), measured_nodes)
            union!(curr_physical_nodes, new_nodes_to_add)
        end
    end

    return measurement_steps_per_layer, num_t_states_per_layer, num_rotations_per_layer
end