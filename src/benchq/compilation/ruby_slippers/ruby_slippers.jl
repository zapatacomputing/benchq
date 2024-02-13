################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
#=
This module contains functions for getting the graph state corresponding to a
state generated by a circuit using a graph state simulator (graph_sim) from the paper
"Fast simulation of stabilizer circuits using a graph state representation" by Simon
Anders, Hans J. Briegel. https://arxiv.org/abs/quant-ph/0504117". We have modified
the algorithm to ignore paulis.
=#

using PythonCall
using StatsBase

const Qubit = UInt32
const AdjList = Set{Qubit}
const erase_line = "        \b\b\b\b\b\b\b\b"

include("verbose_iterator.jl")
include("graph_sim_data.jl")
include("../pauli_tracker/pauli_tracker.jl")
include("algorithm_specific_graph.jl")
include("asg_stitching.jl")

"""
Converts a given circuit in Clifford + T form to icm form and simulates the icm
circuit using the graph sim mini simulator. Returns the adjacency list of the graph
state created by the icm circuit along with the single qubit operations on each vertex.
teleportation_threshold, min_neighbor_degree, teleportation_distance, and  max_num_neighbors_to_search
are metaparameters which can be optimized to speed up the simulation. This function
serves as the primary entry point for the Ruby Slippers algorithm via pythoncall.

Args:
    orquestra_circuit::Circuit        circuit to be simulated
    verbose::Bool                     whether to print progress
    takes_graph_input::Bool           whether the circuit takes a graph state as input and thus
                                        can be stitched to a previous graph state.
    gives_graph_output::Bool          whether the circuit gives a graph state as output and thus
                                        can be stitched to a future graph state.
    layering_optimization::String     which layering optimization to use in the pauli tracker.
                                        Options are "ST-Volume", "Time", "Space", "Variable"
    max_num_qubits::Int                  how many gates to put in each layer in the case of "Variable"
    teleportation_threshold::Int      max node degree allowed before state is teleported
    teleportation_distance::Int       number of teleportations to do when state is teleported
    min_neighbor_degree::Int                stop searching for neighbor with low degree if
                                        neighbor has at least this many neighbors
    max_num_neighbors_to_search::Int  max number of neighbors to search through when finding
                                        a neighbor with low degree
    decomposition_strategy::Int       strategy for decomposing non-clifford gate
                                        0: keep current qubit as data qubit
                                        1: teleport data to new qubit which becomes data qubit
    max_graph_size::Int               maximum number of nodes in the graph state
    max_time::Float64                 maximum time to spend compiling the circuit


Returns:
    edge_data::python List[List[int]] adjacency list describing the graph state
    num_consumption_tocks::Int        number of tocks used to consume the graph
    num_logical_qubits::Int           number of logical qubits in the graph state
    proportion::Float64               proportion of the circuit that was compiled
"""
function run_ruby_slippers(
    orquestra_circuit;
    verbose::Bool=true,
    takes_graph_input::Bool=true,
    gives_graph_output::Bool=true,
    layering_optimization::String="ST-Volume",
    max_num_qubits::Int64=1,
    teleportation_threshold::Int64=40,
    teleportation_distance::Int64=4,
    min_neighbor_degree::Int64=6,
    max_num_neighbors_to_search::Int64=100000,
    decomposition_strategy::Int64=0,
    max_time::Float64=1e8,
    max_graph_size=nothing,
)
    if decomposition_strategy == 1
        error("Decomposition strategy 1 is not yet supported")
    end
    # params which can be optimized to speed up computation
    hyperparams = RbSHyperparams(
        teleportation_threshold,
        teleportation_distance,
        min_neighbor_degree,
        max_num_neighbors_to_search,
        decomposition_strategy,
    )

    if max_graph_size === nothing
        max_graph_size = get_max_n_nodes(
            orquestra_circuit,
            hyperparams.teleportation_distance,
            takes_graph_input,
            gives_graph_output,
        )
    else
        max_graph_size = pyconvert(UInt32, max_graph_size)
    end

    if verbose
        (asg, pauli_tracker, proportion) =
            @time get_graph_state_data(
                orquestra_circuit;
                verbose=verbose,
                takes_graph_input=takes_graph_input,
                gives_graph_output=gives_graph_output,
                layering_optimization=layering_optimization,
                max_num_qubits=max_num_qubits,
                hyperparams=hyperparams,
                max_graph_size=max_graph_size,
                max_time=max_time,
            )
    else
        (asg, pauli_tracker, proportion) =
            get_graph_state_data(
                orquestra_circuit;
                verbose=verbose,
                takes_graph_input=takes_graph_input,
                gives_graph_output=gives_graph_output,
                layering_optimization=layering_optimization,
                max_num_qubits=max_num_qubits,
                hyperparams=hyperparams,
                max_graph_size=max_graph_size,
                max_time=max_time,
            )
    end

    if proportion == 1.0
        num_logical_qubits = get_num_logical_qubits(pauli_tracker.layering, asg, verbose)
        num_consumption_tocks = length(pauli_tracker.layering)
        println("True number of consumption tocks: ", num_consumption_tocks)
        println("True number of logical qubits: ", num_logical_qubits)
        return python_asg(asg), num_consumption_tocks, num_logical_qubits, proportion
    else
        # if we did not finish compiling the circuit, return the proportion of the circuit
        return python_asg(asg), 0, 0, proportion
    end
end


"""
Get the maximum number of nodes that the graph could possibly need. Helps to reduce
memory usage when creating the graph state and the pauli tracker.
"""
function get_max_n_nodes(
    orquestra_circuit,
    teleportation_distance,
    takes_graph_input,
    gives_graph_output,
)
    n_qubits = pyconvert(Int, orquestra_circuit.n_qubits)
    supported_ops = get_op_list()

    n_magic_state_injection_teleports = 0
    n_ruby_slippers_teleports = 0

    for op in orquestra_circuit.operations
        if occursin("ResetOperation", pyconvert(String, op.__str__()))
            n_magic_state_injection_teleports += 1
            continue
        else
            op_index = get_op_index(supported_ops, op)
            if double_qubit_op(op_index)
                n_ruby_slippers_teleports += 2
            elseif non_clifford_op(op_index)
                n_magic_state_injection_teleports += 1
                n_ruby_slippers_teleports += 1
            end
        end
    end

    n_projected_nodes = n_magic_state_injection_teleports +
                        n_ruby_slippers_teleports * teleportation_distance +
                        n_qubits

    if takes_graph_input
        n_projected_nodes += BUFFER_SIZE * n_qubits
    end
    if gives_graph_output
        n_projected_nodes += 4 * n_qubits
    end

    return convert(UInt32, n_projected_nodes)
end

"""
Get the vertices of a graph state corresponding to enacting the given circuit
on the |0> state. Also gives the single qubit clifford operation on each node.

Args:
    orquestra_circuit::Circuit   circuit to be simulated
    verbose::Bool                whether to print progress
    takes_graph_input::Bool      whether the circuit takes a graph state as input and thus
                                   can be stitched to a previous graph state.
    gives_graph_output::Bool     whether the circuit gives a graph state as output and thus
                                   can be stitched to a future graph state.
    layering_optimization::Stringwhich layering optimization to use in the pauli tracker.
                                   Options are "ST-Volume", "Time", "Space", "Variable"
    max_num_qubits::Int             how many gates to put in each layer in the case of "Variable"
    hyperparams::RbSHyperparams  metaparameters which can be optimized to speed up the compilation.
    max_graph_size::UInt32       maximum number of nodes in the graph state
    max_time::Float64            maximum time to spend compiling the circuit

Raises:
    ValueError: if an unsupported gate is encountered

Returns:
    Vector{UInt8}: the list of single qubit clifford operations on each node
    Vector{AdjList}:   the adjacency list describing the graph corresponding to the graph state
"""
function get_graph_state_data(
    orquestra_circuit;
    verbose::Bool=true,
    takes_graph_input::Bool=true,
    gives_graph_output::Bool=true,
    manually_stitchable::Bool=false,
    layering_optimization::String="ST-Volume",
    max_num_qubits::Int64=1,
    hyperparams::RbSHyperparams=default_hyperparams,
    max_graph_size::UInt32=UInt32(100000),
    max_time::Float64=1e8,
)
    if hyperparams.decomposition_strategy == 1
        error("Decomposition strategy 1 is not yet supported")
    end

    n_qubits = pyconvert(Int, orquestra_circuit.n_qubits)

    if takes_graph_input
        asg, pauli_tracker = initialize_for_graph_input(max_graph_size, n_qubits, layering_optimization, max_num_qubits)
    else
        asg = AlgorithmSpecificGraphAllZero(max_graph_size, n_qubits)
        pauli_tracker = PauliTracker(n_qubits, layering_optimization, max_num_qubits)
    end

    total_length = length(orquestra_circuit.operations)
    counter = 0
    start_time = time()

    for (counter, orquestra_op) in enumerate(
        VerboseIterator(
            orquestra_circuit.operations,
            verbose,
            "Compiling graph state using Ruby Slippers...",
            true,
        )
    )
        elapsed_time = time() - start_time
        # End early if we have exceeded the max time
        if elapsed_time >= max_time
            delete_excess_asg_space!(asg)
            percent = counter / total_length
            return asg, pauli_tracker, percent
        end

        # Apply current operation
        if occursin("ResetOperation", pyconvert(String, orquestra_op.__str__())) # reset operation
            asg.n_nodes += 1
            asg.stitching_properties.gate_output_nodes[get_qubit_1(orquestra_op)] = asg.n_nodes
            add_new_qubit_to_pauli_tracker!(pauli_tracker)
            continue
        else
            icm_ops = convert_orquestra_op_to_icm_ops(orquestra_op)
            for op in icm_ops
                if op.code in non_clifford_gate_codes
                    apply_non_clifford_gate!(asg, pauli_tracker, op, hyperparams)
                elseif op.code in [I_code, X_code, Y_code, Z_code, H_code, S_code] # single qubit clifford gates
                    op_code = op.code
                    node = asg.stitching_properties.gate_output_nodes[op.qubit1] # node this operation with act on
                    if op_code in [I_code, X_code, Y_code, Z_code]
                        asg.sqp[node] = multiply_sqp[asg.sqp[node], external_to_internal_paulis[op_code]]
                    elseif op_code == H_code
                        multiply_h_from_left(asg, pauli_tracker, node)
                    elseif op_code == S_code
                        multiply_s_from_left(asg, pauli_tracker, node)
                    end
                elseif op.code in [CZ_code, CNOT_code] # two qubit clifford gates
                    op_code = op.code
                    node_1 = asg.stitching_properties.gate_output_nodes[op.qubit1]
                    node_2 = asg.stitching_properties.gate_output_nodes[op.qubit2]
                    if op_code == CNOT_code
                        # CNOT = (I ⊗ H) CZ (I ⊗ H)
                        multiply_h_from_left(asg, pauli_tracker, node_2)
                        cz(asg, node_1, node_2, pauli_tracker, hyperparams)
                        # update node_2 to the new qubit if previous cz teleported it
                        node_2 = asg.stitching_properties.gate_output_nodes[op.qubit2]
                        multiply_h_from_left(asg, pauli_tracker, node_2)
                    elseif op_code == CZ_code
                        cz(asg, node_1, node_2, pauli_tracker, hyperparams)
                    end
                else
                    error("Unsupported gate: $(op.code)")
                end
            end
        end
    end

    # add teleportations at end so we can connect to next buffer
    nodes_to_remove = Set{Qubit}([])
    if gives_graph_output
        add_output_nodes!(asg, pauli_tracker, nodes_to_remove)
    end
    if takes_graph_input
        prune_buffer!(asg, pauli_tracker, n_qubits, nodes_to_remove)
    end

    calculate_layering!(pauli_tracker, asg, nodes_to_remove, verbose)
    delete_excess_asg_space!(asg)

    if manually_stitchable
        verbose && println("Minimizing node labels for manual stitching...")
        asg, pauli_tracker = minimize_node_labels!(asg, pauli_tracker, nodes_to_remove)
    end

    return asg, pauli_tracker, 1.0
end

"""
Implement non-clifford gates via gate teleportation as described in
https://arxiv.org/abs/1509.02004. This is commonly reffered to as the ICM
format.
"""
function apply_non_clifford_gate!(asg, pauli_tracker, op, hyperparams)
    original_qubit = op.qubit1 # qubit the T gate was originally acting on before ICM
    asg.n_nodes += 1
    # println(compiled_qubit, " -> ", asg.n_nodes, " ")
    # TODO: implement different decomposition_strategies with new tracker
    original_node = Qubit(asg.stitching_properties.gate_output_nodes[original_qubit])
    compiled_node = Qubit(asg.n_nodes)
    # add new qubit to be tracked
    add_new_qubit_to_pauli_tracker!(pauli_tracker)
    # apply CX
    multiply_h_from_left(asg, pauli_tracker, compiled_node)
    cz_no_teleport(asg, original_node, compiled_node, pauli_tracker, hyperparams)
    # update original_node to the new qubit if that cz teleported it
    original_node = Qubit(asg.stitching_properties.gate_output_nodes[original_qubit])
    multiply_h_from_left(asg, pauli_tracker, compiled_node)
    # mark compiled qubit as where the data is being stored
    if hyperparams.decomposition_strategy == 0
        asg.stitching_properties.gate_output_nodes[original_qubit] = compiled_node
    end
    # Update pauli Tracker
    add_z_to_pauli_tracker!(pauli_tracker.cond_paulis, original_node, compiled_node)
    if op.code == RZ_code
        add_measurement!(pauli_tracker.measurements, op.code, original_node, op.angle)
    else
        add_measurement!(pauli_tracker.measurements, op.code, original_node)
    end
end

"""
Delete excess parts of the ASG to save space once we have completed
the computation. This is done by resizing the vectors to only contain
the nodes which are actually used in the graph state.
"""
function delete_excess_asg_space!(asg)
    resize!(asg.edge_data, asg.n_nodes)
    resize!(asg.sqs, asg.n_nodes)
    resize!(asg.sqp, asg.n_nodes)
end

"""
Check if a vertex is almost isolated. A vertex is almost isolated if it has no
neighbors or if it has one neighbor and that neighbor is the given vertex.

Args:
    set::AdjList set of neighbors of a vertex
    vertex::Int  vertex to check if it is almost isolated

Returns:
    Bool: whether the vertex is almost isolated
"""
function check_almost_isolated(set, vertex)
    len = length(set)
    return (len == 0) || (len == 1 && vertex in set)
end

"""
Apply a CZ gate to the graph on the given vertices.

Args:
    sqs::Vector{UInt8}      single qubit clifford operation on each node
    adj::Vector{AdjList}  adjacency list describing the graph state
    vertex_1::Int         vertex to enact the CZ gate on
    vertex_2::Int         vertex to enact the CZ gate on
"""
function cz(asg, vertex_1, vertex_2, pauli_tracker, hyperparams)
    if length(asg.edge_data[vertex_1]) >= hyperparams.teleportation_threshold
        distance = hyperparams.teleportation_distance
        vertex_1 = teleportation!(asg, vertex_1, pauli_tracker, hyperparams, distance)
    end
    if length(asg.edge_data[vertex_2]) >= hyperparams.teleportation_threshold
        distance = hyperparams.teleportation_distance
        vertex_2 = teleportation!(asg, vertex_2, pauli_tracker, hyperparams, distance)
    end

    cz_no_teleport(asg, vertex_1, vertex_2, pauli_tracker, hyperparams)
end

function cz_no_teleport(asg, vertex_1, vertex_2, pauli_tracker, hyperparams)
    adj1, adj2 = asg.edge_data[vertex_1], asg.edge_data[vertex_2]

    if !check_almost_isolated(adj1, vertex_2)
        remove_sqs!(asg, vertex_1, vertex_2, hyperparams)
    end
    if !check_almost_isolated(adj2, vertex_1)
        remove_sqs!(asg, vertex_2, vertex_1, hyperparams)
    end
    if !check_almost_isolated(adj1, vertex_2)
        remove_sqs!(asg, vertex_1, vertex_2, hyperparams)
    end

    # Now that the verticies CZ is acting on are either isolated or have sqs = I or S,
    # apply a CZ gate between those two gates. Only requires using lookup table.
    track_conditional_paulis_through_cz(pauli_tracker.cond_paulis, vertex_1, vertex_2)

    connected = vertex_1 in asg.edge_data[vertex_2] || vertex_2 in asg.edge_data[vertex_1]

    clifford_1_table_code = asg.sqp[vertex_1] + 4 * (asg.sqs[vertex_1] - 1)
    clifford_2_table_code = asg.sqp[vertex_2] + 4 * (asg.sqs[vertex_2] - 1)
    table_tuple = cz_table[connected+1][clifford_1_table_code, clifford_2_table_code]

    connected != table_tuple[1] && toggle_edge!(asg.edge_data, vertex_1, vertex_2)
    asg.sqp[vertex_1] = table_tuple[2][1]
    asg.sqs[vertex_1] = table_tuple[2][2]
    asg.sqp[vertex_2] = table_tuple[3][1]
    asg.sqs[vertex_2] = table_tuple[3][2]
end


"""
Remove all single qubit clifford operations on a vertex v that do not
commute with CZ. Needs use of a neighbor of v, but if we wish to avoid
using a particular neighbor, we can specify it.

Args:
    sqs::Vector{UInt8}      single qubit clifford operations on each node
    adj::Vector{AdjList}  adjacency list describing the graph state
    v::Int                index of the vertex to remove single qubit clifford operations from
    avoid::Int            index of a neighbor of v to avoid using
"""
function remove_sqs!(asg, v, avoid, hyperparams)
    code = asg.sqs[v]
    if code == I_code || code == S_code
    elseif code == SQRT_X_code || code == HS_code
        local_complement!(asg, v)
    else # code == H_code || code == SH_code
        # almost all calls to remove_sqs!() will end up here
        neighbor = get_neighbor(asg.edge_data, v, avoid, hyperparams)
        local_complement!(asg, neighbor)
        local_complement!(asg, v)
    end
end

"""
Select a neighbor to use when removing a single qubit clifford operation.

The return value be set to avoid if there are no neighbors or avoid is the only neighbor,
otherwise it returns the neighbor with the fewest neighbors (or the first one that
it finds with less than min_neighbor_degree)
"""
function get_neighbor(adj, v, avoid, hyperparams)
    neighbors_of_v = adj[v]

    # Avoid copying and modifying adjacency vector
    check_almost_isolated(neighbors_of_v, avoid) && return avoid

    smallest_neighborhood_size = typemax(eltype(neighbors_of_v)) # initialize to max possible value
    neighbor_with_smallest_neighborhood = 0
    if length(neighbors_of_v) <= hyperparams.max_num_neighbors_to_search
        neighbors_to_search = neighbors_of_v
    else
        neighbors_to_search = sample(
            collect(neighbors_of_v),
            hyperparams.max_num_neighbors_to_search;
            replace=false
        )
    end

    for neighbor in neighbors_to_search
        if neighbor != avoid
            # stop search if super small neighborhood is found
            num_neighbors = length(adj[neighbor])
            num_neighbors < hyperparams.min_neighbor_degree && return neighbor
            # search for smallest neighborhood
            if num_neighbors < smallest_neighborhood_size
                smallest_neighborhood_size = num_neighbors
                neighbor_with_smallest_neighborhood = neighbor
            end
        end
    end
    return neighbor_with_smallest_neighborhood
end


"""
Take the local complement of a vertex v.

Args:
    sqs::Vector{UInt8}      single qubit clifford operations on each node
    adj::Vector{AdjList}  adjacency list describing the graph state
    v::Int                index node to take the local complement of
"""
function local_complement!(asg, v)
    neighbors = collect(asg.edge_data[v])
    len = length(neighbors)
    multiply_sqrt_x_from_right(asg, v)
    for i = 1:len
        neighbor = neighbors[i]
        multiply_s_dagger_from_right(asg, neighbor)
        for j = i+1:len
            toggle_edge!(asg.edge_data, neighbor, neighbors[j])
        end
    end
end


"""Add an edge between the two vertices given"""
@inline function add_edge!(adj, vertex_1, vertex_2)
    push!(adj[vertex_1], vertex_2)
    push!(adj[vertex_2], vertex_1)
end

"""Remove an edge between the two vertices given"""
@inline function remove_edge!(adj, vertex_1, vertex_2)
    delete!(adj[vertex_1], vertex_2)
    delete!(adj[vertex_2], vertex_1)
end

"""
If vertices vertex_1 and vertex_2 are connected, we remove the edge.
Otherwise, add it.

Args:
    adj::Vector{AdjList}  adjacency list describing the graph state
    vertex_1::Int         index of vertex to be connected or disconnected
    vertex_2::Int         index of vertex to be connected or disconnected
"""
function toggle_edge!(adj, vertex_1, vertex_2)
    if vertex_2 in adj[vertex_1]
        remove_edge!(adj, vertex_1, vertex_2)
    else
        add_edge!(adj, vertex_1, vertex_2)
    end
end

"""
Teleport your "oz qubit" with high degree to a "kansas qubit" with degree 1.
Speeds up computation by avoiding performing local complements on high degree nodes.

Args:
    asg::AlgorithmSpecificGraph       graph state to teleport in
    oz_qubit::Int                     index of the qubit to teleport
    pauli_tracker::PauliTracker       tracker to update with teleportation
    hyperparams::RbSHyperparams       metaparameters which can be optimized to speed up the compilation
    curr_teleportation_distance::Int  number of teleportations to do when state is teleported
                                        multiplied by 2
"""
function teleportation!(
    asg,
    oz_qubit,
    pauli_tracker,
    hyperparams,
    curr_teleportation_distance,
)
    slippers_qubit = Qubit(asg.n_nodes + 1) # facilitates teleportation
    kansas_qubit = Qubit(asg.n_nodes + 2) # qubit we teleport to
    asg.n_nodes += 2
    add_new_qubit_to_pauli_tracker!(pauli_tracker)
    add_new_qubit_to_pauli_tracker!(pauli_tracker)

    # output state of H(slippers_qubit) * CX(slippers_qubit, kansas_qubit_qubit) * H(slippers_qubit)
    asg.sqs[slippers_qubit] = I_code
    asg.sqs[kansas_qubit] = I_code
    asg.edge_data[slippers_qubit] = AdjList(kansas_qubit)
    asg.edge_data[kansas_qubit] = AdjList(slippers_qubit)

    cz_no_teleport(asg, oz_qubit, slippers_qubit, pauli_tracker, hyperparams)
    multiply_h_from_left(asg, pauli_tracker, slippers_qubit)
    multiply_h_from_left(asg, pauli_tracker, oz_qubit)

    add_z_to_pauli_tracker!(pauli_tracker.cond_paulis, oz_qubit, kansas_qubit)
    add_measurement!(pauli_tracker.measurements, H_code, oz_qubit)
    add_x_to_pauli_tracker!(pauli_tracker.cond_paulis, slippers_qubit, kansas_qubit)
    add_measurement!(pauli_tracker.measurements, H_code, slippers_qubit)


    # update qubit map if needed
    for (i, qubit) in enumerate(asg.stitching_properties.gate_output_nodes)
        if qubit == oz_qubit
            asg.stitching_properties.gate_output_nodes[i] = kansas_qubit
        end
    end

    # peform multiple teleportations if we need distance > 2
    if curr_teleportation_distance > 2
        distance = curr_teleportation_distance - 2
        return teleportation!(asg, kansas_qubit, pauli_tracker, hyperparams, distance)
    end

    return kansas_qubit
end
