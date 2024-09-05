using Graphs

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
        
        # Account for the number of t measurements and number of rotations in the layer
        for node in pauli_tracker.layering[layer_num]
            if pauli_tracker.measurements[node][1] in [T_code, T_Dagger_code]
                num_t_states_per_layer[layer_num] += 1
            end
            if pauli_tracker.measurements[node][1] == RZ_code
                num_rotations_per_layer[layer_num] += 1
            end
        end

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
        union!(satisfied_nodes, nodes_to_satisfy_this_layer)
        bars = []
        subnodes_this_layer = setdiff(nodes_to_satisfy_this_layer, nodes_satisfied_by_initialization)
        for node in subnodes_this_layer
            bar = [node_to_patch[node], node_to_patch[node]]
            for neighbor in asg.edge_data[node]
                if node_to_patch[neighbor] < bar[1] && node in curr_physical_nodes
                    bar[1] = node_to_patch[neighbor]
                end
                if node_to_patch[neighbor] > bar[2] && node in curr_physical_nodes
                    bar[2] = node_to_patch[neighbor]
                end
            end
            push!(bars, bar)
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
    # In this strategy we simply apply the cz gates that are required in order to create the graph state
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

        sort!(bars, by=x -> x[2])

        # layer the bars to parallelize them
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
                # each cz requires 2 tocks
                num_tocks_for_graph_creation[layer_num] += 2
            end
        end

        for node in pauli_tracker.layering[layer_num]
            if pauli_tracker.measurements[node][1] in [T_code, T_Dagger_code]
                num_t_states_per_layer[layer_num] += 1
            end
            if pauli_tracker.measurements[node][1] == RZ_code
                num_rotations_per_layer[layer_num] += 1
            end
        end

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

    num_tocks_for_graph_creation = [0 for _ in 1:length(pauli_tracker.layering)]
    num_t_states_per_layer = [0 for _ in 1:length(pauli_tracker.layering)]
    num_rotations_per_layer = [0 for _ in 1:length(pauli_tracker.layering)]


    # Phase 2: For each layer of nodes in the remaining graph, group the multi-qubit stabilizer measurements 
    # into co-measurable sets to determine the number of tocks required to prepare the graph state of that layer.
    for layer_num in VerboseIterator(1:length(pauli_tracker.layering), verbose, "Scheduling Clifford operations...")

        # Account for the number of t measurements and number of rotations in the layer
        for node in pauli_tracker.layering[layer_num]
            if pauli_tracker.measurements[node][1] in [T_code, T_Dagger_code]
                num_t_states_per_layer[layer_num] += 1
            end
            if pauli_tracker.measurements[node][1] == RZ_code
                num_rotations_per_layer[layer_num] += 1
            end
        end

        # Get the subnodes that require stablizer measurements this layer
        nodes_to_satisfy_this_layer = setdiff(get_neighborhood(pauli_tracker.layering[layer_num], asg), satisfied_nodes)
        union!(satisfied_nodes, nodes_to_satisfy_this_layer)
        subnodes_this_layer = setdiff(nodes_to_satisfy_this_layer, nodes_satisfied_by_initialization)

        
        # Compute number of tocks for graph state creation using greedy graph coloring on extension graph
        num_tocks_for_graph_creation[layer_num] += compute_active_volume_tocks_to_prepare_subgraph(asg.edge_data, subnodes_this_layer)
        
        if layer_num < length(pauli_tracker.layering)
            union!(measured_nodes, pauli_tracker.layering[layer_num])
            for measured_node in pauli_tracker.layering[layer_num]
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

"""
Groups nodes into 2-independent sets using a greedy algorithm. The algorithm orders 
the neighborhoods according to non-decreasing size and iteratively adds neighborhoods 
that are disjoint from the current neighborhood set.

Note 1: This function consistently requires more tocks than the graph coloring approach, 
but is kept here for future development.

Note 2: This function doesn't keep track of the groups as would be needed by a compiler, 
but only accounts for the number of tocks that would result from a lattice surgery compilation.

Args:
    asg::AlgorithmSpecificGraph       Graph state compilation object
    subnodes_this_layer::List         List of the graph subnodes to be measured in a layer

Returns:
    num_tocks::Int                               Number of tocks to prepare the graph state
"""
function active_volume_greedy_group_neighborhoods(asg, subnodes_this_layer)
    # Construct set of neighborhoods
    neighborhoods = []
    for node in subnodes_this_layer
        neighborhood = asg.edge_data[node]
        push!(neighborhoods, neighborhood)
    end
    num_tocks = 0
    remaining_neighborhoods = neighborhoods
    sort!(neighborhoods, by=x -> length(x))

    # Loop to iteratively construct groups of disjoint neighborhoods.
    # Each loop removes a set of neighborhoods from the list of remaining 
    # neighborhoods to indicate that those neighborhoods have been added
    # to the group of that loop.
    
    # While not all neighborhoods have been grouped
    while length(remaining_neighborhoods) > 0
        # We only keep track of the nodes in the group as this is sufficient to 
        # Separate the first neighborhood from the remaining and add to the group
        # determine co-measurability with other neighborhoods.
        group_nodes = remaining_neighborhoods[1]
        remaining_neighborhoods = remaining_neighborhoods[2:end]

        # If there are no neighborhoods left, count the tock needed to 
        # prepare this group and break the loop
        if length(remaining_neighborhoods) == 0
            num_tocks += 1
            break
        else
    
            # Scan through the remaining neighborhoods to find disjoint neighborhoods
            # to add to the current group.
            for (i, neighborhood) in enumerate(remaining_neighborhoods)
                if isdisjoint(neighborhood, group_nodes)
                    group_nodes = union(group_nodes, neighborhood)
                    deleteat!(remaining_neighborhoods, i)
                end
            end
    
            # Increment the number of tocks by one to account for the stabilizer 
            # measurements of the nodes in the current group.
            num_tocks += 1
        end

    end

    return num_tocks
end

"""
Constructs a subgraph from the edge data of the AlgorithmSpecificGraph that contains
only the nodes in the input set. The subgraph is constructed by adding edges between
nodes that are neighbors in the original graph.

Args:
    edge_data::List{List{Int}}          Edge data describing a graph
    nodes::Set{Int}                     Set of nodes to include in the subgraph
"""
function construct_subgraph_from_edge_data(edge_data::Vector{Set{UInt32}}, nodes::Set{UInt32})
    # Create a SimpleGraph with the same number of nodes as the input set
    n = length(nodes)
    g = SimpleGraph(n)
    
    # Create a mapping from original node indices to new subgraph indices
    node_map = Dict{UInt32, Int64}(node => i for (i, node) in enumerate(nodes))
    for original_node in nodes
        i = node_map[original_node]  # Get the index in the subgraph
        for neighbor in edge_data[Int(original_node)]
            if haskey(node_map, neighbor)
                j = node_map[neighbor]  # Get the index of the neighbor in the subgraph
                if i != j
                    Graphs.add_edge!(g, i, j)  # Add edge between the two nodes in the subgraph
                end
            else
                # Add a new entry to the node map for the neighbor
                node_map[neighbor] = length(node_map) + 1
                Graphs.add_vertex!(g)
                Graphs.add_edge!(g, i, node_map[neighbor])
            end
        end
    end
    return g
end


# Function that generates the extension graph for a given set of edges and
# subnodes such that the output graph has edges added to the original graph 
# between any two nodes that are distance 2 apart in the original edge data.
# This is helpful for grouping nodes that are 2-independent in the original graph.
function generate_extension_graph(edge_data::Vector{Set{UInt32}}, nodes::Set{UInt32})
    # Initialize an empty graph with Int64 type for vertices
    extension_graph = SimpleGraph{Int64}(length(nodes))

    # Create a mapping from node indices to vertex indices
    node_to_vertex_map = Dict{UInt32, Int}()
    for (i, node) in enumerate(nodes)
        node_to_vertex_map[node] = i
    end
    
    # Iterate over nodes and add edges
    for node in nodes
        node_index = node_to_vertex_map[node]
        for neighbor in edge_data[node]
            # Add edge between the current node and neighbor
            # if that neighbor is in nodes
            if haskey(node_to_vertex_map, neighbor) && neighbor != node
                Graphs.add_edge!(extension_graph, node_index, node_to_vertex_map[neighbor])
            end
            
            # Iterate over the neighbors of the neighbor node
            for nn_neighbor in edge_data[neighbor]
                # Skip to avoid creating self loops in the graph
                if nn_neighbor == node
                    continue
                end

                if haskey(node_to_vertex_map, node) && haskey(node_to_vertex_map, nn_neighbor)
                    nn_neighbor_index = node_to_vertex_map[nn_neighbor]
                    Graphs.add_edge!(extension_graph, node_index, nn_neighbor_index)
                end
            end
        end
    end
    return extension_graph, node_to_vertex_map
end

# Function that generates the extension graph and solves graph coloring using 
# a specified algorithm from the Graphs.jl package. 
# Note: this function doesn't keep track of the groups as would be
# needed by a compiler, but only accounts for the number of tocks that would 
# result from a lattice surgery compilation.
function compute_active_volume_tocks_to_prepare_subgraph(edge_data, subnodes, coloring_algorithm=Graphs.degree_greedy_color)
    # Check if the graph is empty
    if length(subnodes) == 0
        return 0
    end
    
    # Generate extension graph
    extension_graph, _ = generate_extension_graph(edge_data, subnodes)
    # Solve graph coloring using the specified algorithm
    coloring = coloring_algorithm(extension_graph)
    # Return the number of colors used
    return coloring.num_colors
end