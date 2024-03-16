################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
Get the number of logical qubits in the circuit. This is done by finding
the maximum number of physical qubits which are connected to each other
through the conditional Pauli operators at each layer of the pauli tracker.
"""
function get_num_logical_qubits(layering, asg, optimization, verbose=false)
    if optimization == "Space"
        neighborhod_degree = 1
    elseif optimization == "Time"
        neighborhod_degree = 2
    elseif optimization == "Variable"
        neighborhod_degree = 1
    else
        throw(ArgumentError("Invalid optimization type."))
    end

    curr_physical_nodes = get_neighborhood(layering[1], asg, neighborhod_degree)
    n_logical_qubits = length(curr_physical_nodes)
    measured_nodes = Set{Qubit}([])

    for i in VerboseIterator(1:length(layering)-1, verbose, "Calculating number of logical qubits...")
        union!(measured_nodes, layering[i])
        added_nodes = layering[i+1]

        setdiff!(curr_physical_nodes, layering[i])
        new_nodes_to_add = setdiff(get_neighborhood(added_nodes, asg, neighborhod_degree), measured_nodes)
        union!(curr_physical_nodes, new_nodes_to_add)

        n_logical_qubits = max(n_logical_qubits, length(curr_physical_nodes))
    end

    return n_logical_qubits
end

function get_neighborhood(centers, asg, distance=1)
    neighborhood = Set{Qubit}([])
    if distance == 0
        return centers
    end
    for center in centers
        for neighbor in asg.edge_data[center]
            push!(neighborhood, neighbor)
        end
    end

    return get_neighborhood(union(neighborhood, centers), asg, distance - 1)
end

function get_n_measurement_steps(pauli_tracker::PauliTracker)
    return length(pauli_tracker.layering)
end


"""
Get the lower bound for the number of logical qubits in the circuit. This is done by finding
the maximum number of nodes which are in the neighborhod of a node, yet must be measured after
that node. We know that when we measure the node at the center of the neighborhood, all of the
nodes which are measured after that must be realized as logical qubits. The function will print
out the bound as well as histogram of the bounds for each node.

Attributes:
    dag (Vector{Vector{Qubit}}): The DAG representing the order in which the qubits must be measured.
    asg (AbstractStateGraph): The state graph representing the connectivity of the qubits.
    nodes_to_include (Vector{Qubit}): The nodes which should be included in the DAG.
    depth (Int): The depth to which the successors of each node should be calculated.
    verbose (Bool): Whether to print the progress of the function.

Returns:
    nothing
"""
function print_lower_bound_for_n_logical_qubits(dag, asg, nodes_to_include, depth=5, verbose=false)
    bounds = [0 for _ in 1:asg.n_nodes]
    reverse_dag = get_reversed_dag(dag)
    for qubit in VerboseIterator(nodes_to_include, verbose, "Calculating logical qubit lower bound...")
        successors = get_all_successors(reverse_dag, qubit, depth)
        bounds[qubit] = length(intersect(asg.edge_data[qubit], successors))
    end
    println("Lower bound on logical qubits with this DAG and ASG: ", maximum(bounds))
    println("Number of nodes with each bound: ", bounds_histogram(bounds))
end

function get_all_successors(dag, qubit, depth)

    @memoize function get_successors(qubit, depth)
        if depth == 0
            return Set{Qubit}()
        end

        successors = Set{Qubit}(dag[qubit])
        for node in dag[qubit]
            union!(successors, get_successors(node, depth - 1))
        end

        return successors
    end

    return get_successors(qubit, depth)
end

function bounds_histogram(bounds)
    hist = Dict{Int,Int}()
    for bound in bounds
        hist[bound] = get(hist, bound, 0) + 1
    end
    return hist
end