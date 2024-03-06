################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
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
    output_nodes = asg.stitching_properties.graph_output_nodes

    if pauli_tracker.use_fully_optimized_dag
        optimal_dag = get_optimal_measurement_dag(pauli_tracker, output_nodes, nodes_to_include, verbose)
    else
        optimal_dag = get_dag(pauli_tracker, nodes_to_include, pauli_tracker.optimal_dag_density, verbose)
    end

    if pauli_tracker.layering_optimization == "Time"
        verbose && println("Calculating time optimal layering...")

        output_nodes = asg.stitching_properties.graph_output_nodes
        reverse_dag = get_reversed_dag(optimal_dag, verbose)

        pauli_tracker.layering =
            longest_path_layering(optimal_dag, reverse_dag, pauli_tracker.n_nodes, nodes_to_include, verbose)
    elseif pauli_tracker.layering_optimization == "Space"
        verbose && println("Calculating space optimized layering...")

        sparse_dag = get_dag(pauli_tracker, nodes_to_include, 1, verbose)
        reverse_dag = get_reversed_dag(sparse_dag, verbose)

        pauli_tracker.layering =
            variable_num_qubits(sparse_dag, reverse_dag, optimal_dag, asg, 1, nodes_to_include, verbose)
    elseif pauli_tracker.layering_optimization == "Variable"
        verbose && println("Calculating layering with $(pauli_tracker.max_num_qubits) qubits...")

        sparse_dag = get_simple_measurement_dag(pauli_tracker, nodes_to_include, 1, verbose)
        reverse_dag = get_reversed_dag(sparse_dag)

        pauli_tracker.layering = variable_num_qubits(
            sparse_dag,
            reverse_dag,
            optimal_dag,
            asg,
            pauli_tracker.max_num_qubits,
            nodes_to_include,
            verbose,
        )
    else
        error("Invalid layering optimization.")
    end

    verbose && println("Layering complete.")
end

"""
A depth first search which returns the nodes in the order that they are
visited. This is used to find a topological  ordering of a graph quickly
when the ordering does not matter.
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
    layers (Vector{Vector{Qubit}}): The layer of each node in the DAG.
"""
function longest_path_layering(measurement_dag, reverse_measurent_dag, n_nodes, nodes_to_include::Vector{Qubit}, verbose::Bool=false)
    longest_path = zeros(Qubit, n_nodes)

    sorted_nodes = depth_first_sort(reverse_measurent_dag, n_nodes, nodes_to_include)
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
    reverse_measurent_dag::Vector{Vector{Qubit}},
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
    remaining_node_degrees = [length(asg.edge_data[node]) for node in 1:asg.n_nodes]

    if verbose
        println("Performing topological sort via Kahn's Algorithm...")
        total_length = length(in_degree)
        counter = dispcnt = 0
        start_time = time()
    end

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
            possible_node_cost = remaining_node_degrees[possible_node]
            if possible_node_cost < min_node_cost
                node = possible_node
                min_pos = pos
                min_node_cost = possible_node_cost
            end
            if min_node_cost < 1
                break
            end
        end
        deleteat!(queue, min_pos)

        push!(ordering, node)
        for neighbor in reverse_measurent_dag[node]
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0
                push!(queue, neighbor)
            end
        end
        for neighbor in asg.edge_data[node]
            remaining_node_degrees[neighbor] -= 1
        end

        # Show progress in real time
        if verbose && dispcnt >= 1000
            counter += 1
            dispcnt += 1
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
the ASG adding nodes to the DAG. This is done by first finding a topological
ordering of the DAG which minimizes which minimizes the number of qubits.
Next, we combine layers of the DAG such that that minimum number of qubits
is not increased.
"""
function variable_num_qubits(measurement_dag, reverse_measurent_dag, optimal_dag, asg, num_qubits::Int, nodes_to_include::Vector{Qubit}, verbose::Bool=false)
    space_optimized = num_qubits == 1
    sorted_nodes = kahns_algorithm(measurement_dag, reverse_measurent_dag, asg.n_nodes, nodes_to_include, asg, verbose)

    # create a layering that is just the topological sort
    ordering_layering = []
    for node in sorted_nodes
        push!(ordering_layering, [node])
    end
    min_logical_qubits = get_num_logical_qubits(ordering_layering, asg)

    if space_optimized
        num_qubits = min_logical_qubits
    elseif num_qubits < min_logical_qubits
        @warn "Cannot fit circuit onto $num_qubits qubits. Setting num qubits to $min_logical_qubits."
    end

    curr_physical_nodes = get_neighborhood(ordering_layering[1], asg)
    measured_nodes = Set{Qubit}([])

    curr_layer = Vector{Qubit}([sorted_nodes[1]])
    layering = Vector{Vector{Qubit}}([])
    for new_node_to_add in VerboseIterator(
        sorted_nodes[2:end],
        verbose,
        "Combining adjacent timesteps without increasing qubit number...",
    )
        new_neighborhood_to_add = setdiff(get_neighborhood(new_node_to_add, asg), measured_nodes)
        union!(curr_physical_nodes, new_neighborhood_to_add)

        if length(curr_physical_nodes) <= num_qubits && isempty(intersect(optimal_dag[new_node_to_add], curr_physical_nodes))
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