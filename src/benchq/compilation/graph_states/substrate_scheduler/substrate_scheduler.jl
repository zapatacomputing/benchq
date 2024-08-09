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


function active_volume_scheduler(asg, pauli_tracker, num_logical_qubits, optimization, verbose=false)
    if optimization == "Time"
        return time_optimal_active_volume_scheduler(asg, pauli_tracker, num_logical_qubits, verbose)
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

        # Co-measurability of two nodes for the two-row architecture is determined by the
        # the disjointness of the contiguous bus qubits between the nodes' left-most and right-most
        # qubits. We refer to these contiguous bus qubits as a "bar". 
        
        # Get the bar for each node we are measuring in this layer
        nodes_to_satisfy_this_layer = setdiff(get_neighborhood(pauli_tracker.layering[layer_num], asg), satisfied_nodes)
        # println("nodes_to_satisfy_this_layer: ", collect(nodes_to_satisfy_this_layer))   
        union!(satisfied_nodes, nodes_to_satisfy_this_layer)
        bars = []
        for node in setdiff(nodes_to_satisfy_this_layer, nodes_satisfied_by_initialization)
            # println("node: ", node)   
            # println("neigbors: ", asg.edge_data[node])   
            bar = [node_to_patch[node], node_to_patch[node]]
            # println("initial bar:", bar)
            # println("neighbors", asg.edge_data[node])
            for neighbor in asg.edge_data[node]
                # println("neighbor: ", neighbor)
                # println(node_to_patch[neighbor] < bar[1], node_to_patch[neighbor] > bar[2], node in curr_physical_nodes)
                if node_to_patch[neighbor] < bar[1] && node in curr_physical_nodes
                    bar[1] = node_to_patch[neighbor]
                end
                if node_to_patch[neighbor] > bar[2] && node in curr_physical_nodes
                    bar[2] = node_to_patch[neighbor]
                end
                # println("temp bar: ", bar)
            end
            # println("final bar: ", bar)
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


        verbose && println("Two row num_tocks_for_graph_creation $layer_num: ", num_tocks_for_graph_creation[layer_num])

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

function time_optimal_active_volume_scheduler(asg, pauli_tracker, num_logical_qubits, verbose=false)
    # Here we model the active volume scheduler as a two row scheduler with the following modifications:
    # 1. The order of patches can be reconfigured "for free"
    # 2. No bus is needed because stabilizer measurements can be made via lattice
    #    surgery operations on the boundaries of patches
    # 3. The condition of co-measurability is disjointness of Pauli strings
    #    which translates into 2-independence of graph nodes (i.e. more than two edges apart)
    # 4. We greedily construct 2-independent sets by sorting nodes according to degree
    #    and then filling the sets with compatible nodes as we go along

    # Phase 1: We can choose to ignore the nodes in a maximal independent set of the graph
    # as they can be initialized in a way that satisfies the stabilizers of the graph state
    nodes_satisfied_by_initialization = get_max_independent_set(asg)

    curr_physical_nodes = get_neighborhood(pauli_tracker.layering[1], asg, 2)
    measured_nodes = Set{Qubit}([])
    new_nodes_to_add = curr_physical_nodes
    satisfied_nodes = Set{Qubit}([])

    # patches_to_node = [-1 for _ in 1:num_logical_qubits]
    # node_to_patch = [-1 for _ in 1:asg.n_nodes]

    num_tocks_for_graph_creation = [0 for _ in 1:length(pauli_tracker.layering)]
    num_t_states_per_layer = [0 for _ in 1:length(pauli_tracker.layering)]
    num_rotations_per_layer = [0 for _ in 1:length(pauli_tracker.layering)]

    # print out the number of edges in the original graph
    println("asg is", asg)
    println("number of nodes in asg is", asg.n_nodes)
    println("length of edge data is", length(asg.edge_data))
    verbose && println("Number of edges in the original graph: ", sum(length(asg.edge_data[node])/2 for node in 1:asg.n_nodes))

    # Construct the neighborhood extension graph that adds edges between nodes 
    # that are at most distance 2 apart in the original graph
    neighbor_extension_graph = deepcopy(asg)
    for node in 1:asg.n_nodes
        for neighbor in asg.edge_data[node]
            for neighbor_node in asg.edge_data[neighbor]
                if !(neighbor_node in neighbor_extension_graph.edge_data[node])
                    add_edge!(neighbor_extension_graph.edge_data, node, neighbor_node)
                end
            end
        end
    end

    println("extended edge asg is", neighbor_extension_graph)
    print("number of nodes in extended edge asg is", neighbor_extension_graph.n_nodes)
    println("length of edge data is", length(neighbor_extension_graph.edge_data))

    # println("Are there any duplicates in the edge set of neighbor_extension_graph? ", length(neighbor_extension_graph.edge_data) != length(Set(neighbor_extension_graph.edge_data)))
    # println("list", length(neighbor_extension_graph.edge_data), "set",  length(Set(neighbor_extension_graph.edge_data)))

    # print out the number of edges in the neighbor extension graph
    verbose && println("Number of edges in the neighbor extension graph: ", sum(length(neighbor_extension_graph.edge_data[node])/2 for node in 1:asg.n_nodes))

    for layer_num in VerboseIterator(1:length(pauli_tracker.layering), verbose, "Scheduling Clifford operations...")

        # Get the neighborhood for each node we are measuring in this layer
        nodes_to_satisfy_this_layer = setdiff(get_neighborhood(pauli_tracker.layering[layer_num], asg), satisfied_nodes)
        # println("nodes_to_satisfy_this_layer: ", collect(nodes_to_satisfy_this_layer))   
        union!(satisfied_nodes, nodes_to_satisfy_this_layer)
        # for node in setdiff(nodes_to_satisfy_this_layer, nodes_satisfied_by_initialization)
        #     neighborhood = asg.edge_data[node]
        #     push!(neighborhoods, neighborhood)
        #     if pauli_tracker.measurements[node][1] in [T_code, T_Dagger_code]
        #         num_t_states_per_layer[layer_num] += 1
        #     end
        #     if pauli_tracker.measurements[node][1] == RZ_code
        #         num_rotations_per_layer[layer_num] += 1
        #     end
        # end

        # # sort neighborhoods into sets of non-decreasing size
        # sort!(neighborhoods, by=x -> length(x))

        # # group the neighborhoods into co-measurable sets
        # while length(neighborhoods) > 0
        #     neighborhood = neighborhoods[1]
        #     neighborhoods = neighborhoods[2:end]
        #     i = 1
        #     neighborhoods_length = length(neighborhoods)
        #     while i <= neighborhoods_length
        #         if isdisjoint(neighborhoods[i], neighborhood)
        #             # neighborhood[2] = neighborhoods[i][2]
        #             deleteat!(neighborhoods, i)
        #             neighborhoods_length -= 1
        #         end
        #         i += 1
        #     end
        #     # Increment the number of tocks as each co-measurable set is defined
        #     num_tocks_for_graph_creation[layer_num] += 1
        # end
        neighborhoods = []
        for node in setdiff(nodes_to_satisfy_this_layer, nodes_satisfied_by_initialization)
            neighborhood = asg.edge_data[node]
            push!(neighborhoods, neighborhood)
            if pauli_tracker.measurements[node][1] in [T_code, T_Dagger_code]
                num_t_states_per_layer[layer_num] += 1
            end
            if pauli_tracker.measurements[node][1] == RZ_code
                num_rotations_per_layer[layer_num] += 1
            end
        end

        # sort neighborhoods into sets of non-decreasing size
        sort!(neighborhoods, by=x -> length(x))

        # group the neighborhoods into co-measurable sets
        while length(neighborhoods) > 0
            neighborhood = neighborhoods[1]
            neighborhoods = neighborhoods[2:end]
            i = 1
            neighborhoods_length = length(neighborhoods)
            while i <= neighborhoods_length
                if isdisjoint(neighborhoods[i], neighborhood)
                    # neighborhood[2] = neighborhoods[i][2]
                    deleteat!(neighborhoods, i)
                    neighborhoods_length -= 1
                end
                i += 1
            end
            # Increment the number of tocks as each co-measurable set is defined
            num_tocks_for_graph_creation[layer_num] += 1
        end


        # Phase 2: Schedule the multi-qubit measurements for each of the remaining stabilizers of the graph state
        # which correspond to nodes in the graph. 
        
        verbose && println("Active volume num_tocks_for_graph_creation $layer_num: ", num_tocks_for_graph_creation[layer_num])
        
        if layer_num < length(pauli_tracker.layering)
            union!(measured_nodes, pauli_tracker.layering[layer_num])
            for measured_node in pauli_tracker.layering[layer_num]
                # patches_to_node[node_to_patch[measured_node]] = -1
                measured_node = -1
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


# function get_co_measurable_stabilizers(pauli_tracker, asg, layer_num, satisfied_nodes, nodes_satisfied_by_initialization, curr_physical_nodes, node_to_patch)
# # Function to construct sets of disjoint neighbors
# function partition_nodes_into_neighborhood_disjoint_sets(graph::Graph)
#     satisfied_nodes = Set{Int}()
#     sets_of_neighbors = []

#     for node in keys(graph.edge_data)
#         # Skip if the node is already satisfied
#         if node in satisfied_nodes
#             continue
#         end

#         # Get the neighbors of the current node
#         neighbors = get_neighborhood(graph, node)

#         # Add the current node to the set of satisfied nodes
#         push!(satisfied_nodes, node)

#         # Create a new set for the current node and its neighbors
#         current_set = Set{Int}()
#         push!(current_set, node)

#         for neighbor in neighbors
#             if neighbor ∉ satisfied_nodes
#                 push!(current_set, neighbor)
#                 push!(satisfied_nodes, neighbor)
#             end
#         end

#         # Add the current set to the list of sets of neighbors
#         push!(sets_of_neighbors, current_set)
#     end

#     return sets_of_neighbors
# end