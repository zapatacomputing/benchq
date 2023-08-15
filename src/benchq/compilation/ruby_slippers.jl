################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
#=
This module contains functions for getting the graph state corresponding to a
state generated by a circuit using a graph state simulator (graph_sim) from the paper
"Fast simulation of stabilizer circuits using a graph state representation" by Simon
Anders, Hans J. Briegel. https://arxiv.org/abs/quant-ph/0504117". We have modified
the algorithm to ignore paulis.

Many of the modules have a no_teleport version. This is to denote that the compiler
does not use teleportation in these cases and is more or less just it's predicessor,
a graph simulator for stabilizer states.
=#

using PythonCall
using StatsBase

include("graph_sim_data.jl")

const AdjList = Set{Int32}

const Qubit = UInt32

struct ICMOp
    code::UInt8
    qubit1::Qubit
    qubit2::Qubit

    ICMOp(name, qubit) = new(name, qubit, 0)
    ICMOp(name, qubit1, qubit2) = new(name, qubit1, qubit2)
end

struct RubySlippersHyperparams
    teleportation_threshold::UInt16
    teleportation_distance::UInt8
    min_neighbors::UInt8
    max_num_neighbors_to_search::UInt32
    decomposition_strategy::UInt8
end

default_hyperparams = RubySlippersHyperparams(40, 4, 6, 1e5, 1)


"""
Converts a given circuit in Clifford + T form to icm form and simulates the icm
circuit using the graph sim mini simulator. Returns the adjacency list of the graph
state created by the icm circuit along with the single qubit operations on each vertex.
teleportation_threshold, min_neighbors, teleportation_distance, and  max_num_neighbors_to_search
are metaparameters which can be optimized to speed up the simulation.

Args:
    circuit::Circuit                  circuit to be simulated
    max_graph_size::Int               maximum number of nodes in the graph state
    teleportation_threshold::Int      max node degree allowed before state is teleported
    teleportation_distance::Int       number of teleportations to do when state is teleported
    min_neighbors::Int                stop searching for neighbor with low degree if
                                        neighbor has at least this many neighbors
    max_num_neighbors_to_search::Int  max number of neighbors to search through when finding
                                        a neighbor with low degree
    decomposition_strategy::Int       strategy for decomposing non-clifford gate
                                        0: keep current qubit as data qubit
                                        1: teleport data to new qubit which becomes data qubit

Returns:
    adj::Vector{AdjList}              adjacency list describing the graph state
    lco::Vector{UInt8}                  local clifford operations on each node
"""
function run_ruby_slippers(
    circuit,
    verbose=false,
    max_graph_size=nothing,
    teleportation_threshold=40,
    teleportation_distance=4,
    min_neighbors=6,
    max_num_neighbors_to_search=1e5,
    decomposition_strategy=1,
)
    # params which can be optimized to speed up computation
    hyperparams = RubySlippersHyperparams(
        teleportation_threshold,
        teleportation_distance,
        min_neighbors,
        max_num_neighbors_to_search,
        decomposition_strategy,
    )

    if max_graph_size === nothing
        max_graph_size = get_max_n_nodes(circuit, hyperparams.teleportation_distance)
    else
        max_graph_size = pyconvert(UInt32, max_graph_size)
    end

    if verbose
        print("get_graph_state_data:\t")
        (lco, adj) = @time get_graph_state_data(circuit, true, max_graph_size, hyperparams)
    else
        (lco, adj) = get_graph_state_data(circuit, false, max_graph_size, hyperparams)
    end

    return pylist(lco), python_adjlist!(adj)
end

function get_max_n_nodes(circuit, teleportation_distance)
    supported_ops = get_op_list()

    n_magic_state_injection_teleports = 0
    n_ruby_slippers_teleports = 0

    for op in circuit.operations
        if occursin("ResetOperation", pyconvert(String, op.__str__()))
            n_magic_state_injection_teleports += 1
            continue
        else
            op_index = get_op_index(supported_ops, op)
            if double_qubit_op(op_index)
                n_ruby_slippers_teleports += 2
            elseif decompose_op(op_index)
                n_magic_state_injection_teleports += 1
                n_ruby_slippers_teleports += 1
            end
        end
    end

    return convert(UInt32, n_magic_state_injection_teleports +
                           n_ruby_slippers_teleports * teleportation_distance +
                           pyconvert(Int, circuit.n_qubits))
end

"""
Get the vertices of a graph state corresponding to enacting the given circuit
on the |0> state. Also gives the local clifford operation on each node.

Args:
    circuit (Circuit): orquestra circuit circuit to get the graph state for
    verbose (Bool): whether to print progress
    hyperparams (Dict): metaparameters for the ruby slippers algorithm see
                        description in run_ruby_slippers for more details

Raises:
    ValueError: if an unsupported gate is encountered

Returns:
    Vector{UInt8}: the list of local clifford operations on each node
    Vector{AdjList}:   the adjacency list describing the graph corresponding to the graph state
"""
function get_graph_state_data(
    circuit,
    verbose::Bool=false,
    max_graph_size::UInt32=1e8,
    hyperparams::RubySlippersHyperparams=default_hyperparams,
)
    n_qubits = pyconvert(Int, circuit.n_qubits)
    ops = circuit.operations

    lco = fill(H_code, max_graph_size)   # local clifford operation on each node
    adj = [AdjList() for _ = 1:max_graph_size]  # adjacency list
    if verbose
        println("Memory for data structures allocated")
    end


    data_qubits = [Qubit(i) for i = 1:n_qubits]
    curr_qubits = [n_qubits] # make this a list so it can be modified in place
    supported_ops = get_op_list()

    if verbose
        total_length = length(ops)
        counter = dispcnt = 0
        start_time = time()
        erase = "        \b\b\b\b\b\b\b\b"
    end

    for (i, op) in enumerate(ops)
        if verbose
            counter += 1
            if (dispcnt += 1) >= 1000
                percent = round(Int, 100 * counter / total_length)
                elapsed = round(time() - start_time, digits=2)
                print("\r$(percent)% ($counter) completed in $erase$(elapsed)s")
                dispcnt = 0
            end
        end

        if occursin("ResetOperation", pyconvert(String, op.__str__()))
            curr_qubits[1] += 1
            data_qubits[get_qubit_1(op)] = curr_qubits[1]
            continue
        else
            # Decomposes gates into the icm format.
            # Reference: https://arxiv.org/abs/1509.02004
            op_index = get_op_index(supported_ops, op)
            if single_qubit_op(op_index)
                icm_op = ICMOp(code_list[op_index], data_qubits[get_qubit_1(op)])
            elseif double_qubit_op(op_index)
                icm_op = ICMOp(
                    code_list[op_index],
                    data_qubits[get_qubit_1(op)],
                    data_qubits[get_qubit_2(op)],
                )
            elseif decompose_op(op_index)
                # Note: these are currently all single qubit gates
                original_qubit = get_qubit_1(op)
                compiled_qubit = data_qubits[original_qubit]
                curr_qubits[1] += 1
                if hyperparams.decomposition_strategy == 0
                    data_qubits[original_qubit] = curr_qubits[1]
                end
                icm_op = ICMOp(CNOT_code, compiled_qubit, curr_qubits[1])
            end
        end

        # apply the icm_op to the circuit, thereby creating the graph
        op_code = icm_op.code
        qubit_1 = icm_op.qubit1
        if op_code == H_code
            lco[qubit_1] = multiply_h(lco[qubit_1])
        elseif op_code == S_code
            lco[qubit_1] = multiply_s(lco[qubit_1])
        elseif op_code == CNOT_code
            # CNOT = (I ⊗ H) CZ (I ⊗ H)
            qubit_2 = icm_op.qubit2
            lco[qubit_2] = multiply_h(lco[qubit_2])
            cz(lco, adj, qubit_1, qubit_2, data_qubits, curr_qubits, hyperparams)
            lco[qubit_2] = multiply_h(lco[qubit_2])
        elseif op_code == CZ_code
            cz(lco, adj, qubit_1, icm_op.qubit2, data_qubits, curr_qubits, hyperparams)
        elseif !pauli_op(op_code)
            error("Unrecognized gate code $op_code encountered")
        end
    end

    if verbose
        elapsed = round(time() - start_time, digits=2)
        println("\r100% ($counter) completed in $erase$(elapsed)s")
    end

    # get rid of excess space in the data structures
    resize!(lco, curr_qubits[1])
    resize!(adj, curr_qubits[1])

    return lco, adj
end

"""Unpacks the values in the cz table and updates the lco values)"""
@inline function update_lco(table, lco, vertex_1, vertex_2)
    # Get the packed value from the table
    val = table[lco[vertex_1], lco[vertex_2]]
    # The code for the first vertex is stored in the top nibble
    # and the second in the bottom nibble
    lco[vertex_1] = (val >> 4) & 0x7
    lco[vertex_2] = val & 0x7
    # return if the top bit is set, which indicates if it is isolated or connected
    (val & 0x80) != 0x00
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
    lco::Vector{UInt8}      local clifford operation on each node
    adj::Vector{AdjList}  adjacency list describing the graph state
    vertex_1::Int         vertex to enact the CZ gate on
    vertex_2::Int         vertex to enact the CZ gate on
"""
function cz(lco, adj, vertex_1, vertex_2, data_qubits, curr_qubits, hyperparams)
    lst1, lst2 = adj[vertex_1], adj[vertex_2]

    if length(adj[vertex_1]) >= hyperparams.teleportation_threshold
        vertex_1 = teleportation!(
            lco,
            adj,
            vertex_1,
            data_qubits,
            curr_qubits,
            hyperparams,
            hyperparams.teleportation_distance,
        )
    end
    if length(adj[vertex_2]) >= hyperparams.teleportation_threshold
        vertex_2 = teleportation!(
            lco,
            adj,
            vertex_2,
            data_qubits,
            curr_qubits,
            hyperparams,
            hyperparams.teleportation_distance,
        )
    end


    if check_almost_isolated(lst1, vertex_2)
        check_almost_isolated(lst2, vertex_1) ||
            remove_lco!(lco, adj, vertex_2, vertex_1, data_qubits, curr_qubits, hyperparams)
        # if you don't remove vertex_2 from lst1, then you don't need to check again
    else
        remove_lco!(lco, adj, vertex_1, vertex_2, data_qubits, curr_qubits, hyperparams)
        if !check_almost_isolated(lst2, vertex_1)
            remove_lco!(lco, adj, vertex_2, vertex_1, data_qubits, curr_qubits, hyperparams)
            # recheck the adjacency list of vertex_1, because it might have been removed
            check_almost_isolated(lst1, vertex_2) || remove_lco!(
                lco,
                adj,
                vertex_1,
                vertex_2,
                data_qubits,
                curr_qubits,
                hyperparams,
            )
        end
    end
    if vertex_2 in lst1
        update_lco(cz_connected, lco, vertex_1, vertex_2) ||
            remove_edge!(adj, vertex_1, vertex_2)
    else
        update_lco(cz_isolated, lco, vertex_1, vertex_2) &&
            add_edge!(adj, vertex_1, vertex_2)
    end
end

function cz_no_teleport(lco, adj, vertex_1, vertex_2, data_qubits, curr_qubits, hyperparams)
    lst1, lst2 = adj[vertex_1], adj[vertex_2]

    if check_almost_isolated(lst1, vertex_2)
        check_almost_isolated(lst2, vertex_1) || remove_lco_no_teleport!(
            lco,
            adj,
            vertex_2,
            vertex_1,
            data_qubits,
            curr_qubits,
            hyperparams,
        )
        # if you don't remove vertex_2 from lst1, then you don't need to check again
    else
        remove_lco_no_teleport!(
            lco,
            adj,
            vertex_1,
            vertex_2,
            data_qubits,
            curr_qubits,
            hyperparams,
        )
        if !check_almost_isolated(lst2, vertex_1)
            remove_lco_no_teleport!(
                lco,
                adj,
                vertex_2,
                vertex_1,
                data_qubits,
                curr_qubits,
                hyperparams,
            )
            # recheck the adjacency list of vertex_1, because it might have been removed
            check_almost_isolated(lst1, vertex_2) || remove_lco_no_teleport!(
                lco,
                adj,
                vertex_1,
                vertex_2,
                data_qubits,
                curr_qubits,
                hyperparams,
            )
        end
    end

    if vertex_2 in lst1
        update_lco(cz_connected, lco, vertex_1, vertex_2) ||
            remove_edge!(adj, vertex_1, vertex_2)
    else
        update_lco(cz_isolated, lco, vertex_1, vertex_2) &&
            add_edge!(adj, vertex_1, vertex_2)
    end
end


"""
Select a neighbor to use when removing a local clifford operation.

The return value be set to avoid if there are no neighbors or avoid is the only neighbor,
otherwise it returns the neighbor with the fewest neighbors (or the first one that
it finds with less than min_neighbors)
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
            # stop search if  super small neighborhood is found
            num_neighbors = length(adj[neighbor])
            num_neighbors < hyperparams.min_neighbors && return neighbor
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
Remove all local clifford operations on a vertex v that do not commute
with CZ. Needs use of a neighbor of v, but if we wish to avoid using
a particular neighbor, we can specify it.

Args:
    lco::Vector{UInt8}      local clifford operations on each node
    adj::Vector{AdjList}  adjacency list describing the graph state
    v::Int                index of the vertex to remove local clifford operations from
    avoid::Int            index of a neighbor of v to avoid using
"""
function remove_lco!(lco, adj, v, avoid, data_qubits, curr_qubits, hyperparams)
    code = lco[v]
    if code == Pauli_code || code == S_code
    elseif code == SQRT_X_code
        local_complement!(lco, adj, v, data_qubits, curr_qubits, hyperparams)
    else
        if code == SH_code
            local_complement!(lco, adj, v, data_qubits, curr_qubits, hyperparams)
            vb = get_neighbor(adj, v, avoid, hyperparams)
            # Cannot use teleportation becase vb wouldn't be a neighbor of v
            local_complement_no_teleport!(lco, adj, vb, data_qubits, curr_qubits)
        else # code == H_code || code == HS_code
            # almost all calls to remove_lco!() will end up here
            vb = get_neighbor(adj, v, avoid, hyperparams)
            local_complement_no_teleport!(lco, adj, vb, data_qubits, curr_qubits)
            local_complement_no_teleport!(lco, adj, v, data_qubits, curr_qubits)
        end
    end
end

function remove_lco_no_teleport!(lco, adj, v, avoid, data_qubits, curr_qubits, hyperparams)
    code = lco[v]
    if code == Pauli_code || code == S_code
    elseif code == SQRT_X_code
        local_complement_no_teleport!(lco, adj, v, data_qubits, curr_qubits)
    else
        if code == SH_code
            local_complement_no_teleport!(lco, adj, v, data_qubits, curr_qubits)
            vb = get_neighbor(adj, v, avoid, hyperparams)
            # Cannot use teleportation becase vb wouldn't be a neighbor of v
            local_complement_no_teleport!(lco, adj, vb, data_qubits, curr_qubits)
        else # code == H_code || code == HS_code
            # almost all calls to remove_lco!() will end up here
            vb = get_neighbor(adj, v, avoid, hyperparams)
            local_complement_no_teleport!(lco, adj, vb, data_qubits, curr_qubits)
            local_complement_no_teleport!(lco, adj, v, data_qubits, curr_qubits)
        end
    end
end


"""
Take the local complement of a vertex v.

Args:
    lco::Vector{UInt8}      local clifford operations on each node
    adj::Vector{AdjList}  adjacency list describing the graph state
    v::Int                index node to take the local complement of
"""
function local_complement!(lco, adj, v, data_qubits, curr_qubits, hyperparams)

    if length(adj[v]) >= hyperparams.teleportation_threshold
        v = teleportation!(
            lco,
            adj,
            v,
            data_qubits,
            curr_qubits,
            hyperparams,
            hyperparams.teleportation_distance,
        )
    end

    local_complement_no_teleport!(lco, adj, v, data_qubits, curr_qubits)
end

function local_complement_no_teleport!(lco, adj, v, data_qubits, curr_qubits)
    neighbors = collect(adj[v])
    len = length(neighbors)
    for i = 1:len
        neighbor = neighbors[i]
        for j = i+1:len
            toggle_edge!(adj, neighbor, neighbors[j])
        end
    end
    lco[v] = multiply_by_sqrt_x(lco[v])
    for i in adj[v]
        lco[i] = multiply_by_s(lco[i])
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
    # if insorted(vertex_2, adj[vertex_1])
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
    lco::Vector{UInt8}      local clifford operations on each node
    adj::Vector{AdjList}  adjacency list describing the graph state
    oz_qubit::Int         index of the qubit to teleport
    data_qubits::Dict       map from qubit indices to vertex indices
    curr_qubits::Int      number of qubits in the graph state
"""
function teleportation!(
    lco,
    adj,
    oz_qubit,
    data_qubits,
    curr_qubits,
    hyperparams,
    curr_teleportation_distance,
)
    slippers_qubit = Qubit(curr_qubits[1] + 1) # facilitates teleportation
    kansas_qubit = Qubit(curr_qubits[1] + 2) # qubit we teleport to
    curr_qubits[1] += 2

    # prepare bell state
    adj[slippers_qubit] = AdjList([kansas_qubit])
    adj[kansas_qubit] = AdjList([slippers_qubit])
    lco[slippers_qubit] = SH_code
    lco[kansas_qubit] = S_code

    # teleport
    lco[slippers_qubit] = multiply_h(lco[slippers_qubit])
    cz_no_teleport(
        lco,
        adj,
        oz_qubit,
        slippers_qubit,
        data_qubits,
        curr_qubits,
        hyperparams,
    )
    lco[slippers_qubit] = multiply_h(lco[slippers_qubit])
    lco[oz_qubit] = multiply_h(lco[oz_qubit])


    # update qubit map if needed
    for (i, qubit) in enumerate(data_qubits)
        if qubit == oz_qubit
            data_qubits[i] = kansas_qubit
        end
    end

    # peform multiple teleportations if we need distance > 2
    if curr_teleportation_distance > 2
        return teleportation!(
            lco,
            adj,
            kansas_qubit,
            data_qubits,
            curr_qubits,
            hyperparams,
            curr_teleportation_distance - 2,
        )
    end

    return kansas_qubit
end


#=
Some small utils for converting from python objects to Julia
=#

"""Get qubit index of python operation"""
get_qubit_1(op) = pyconvert(Int, op.qubit_indices[0]) + 1 # +1 because Julia is 1-indexed
get_qubit_2(op) = pyconvert(Int, op.qubit_indices[1]) + 1

"""Get Python version of op_list of to speed up getting index"""
get_op_list() = pylist(op_list)

"""Get index of operation name"""
get_op_index(op_list, op) = pyconvert(Int, op_list.index(op.gate.name)) + 1

pauli_op(index) = 0 <= index < 5 # i.e. I, X, Y, Z
single_qubit_op(index) = index < 8   # Paulis, H, S, S_Dagger
double_qubit_op(index) = 7 < index < 10  # CZ, CNOT
decompose_op(index) = index > 9 # T, T_Dagger, RX, RY, RZ

"""
Destructively convert this to a Python adjacency list
"""
function python_adjlist!(adj)
    pylist([pylist(adj[i] .- 1) for i = 1:length(adj)])
end
