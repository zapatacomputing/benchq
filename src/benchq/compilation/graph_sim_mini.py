################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
from typing import List, Set, Tuple

from orquestra.quantum.circuits import Circuit

from .graph_sim_data import cz_table, decomposition_lookup_table, multiply_lco


def get_vertices(circuit: Circuit) -> List[Tuple[int, Set[int]]]:
    """Get the vertices of a graph state corresponding to enacting the given circuit
    on the |0> state. Also gives the local clifford operation on each node.

    Args:
        circuit (Circuit): circuit to get the graph state for

    Raises:
        ValueError: if an unsupported gate is encountered

    Returns:
        List[Tuple[int, Set[int]]]: list of tuples of the form
            (local clifford operation, adjacency list) corresponding to each node
            in the graph state
    """
    lco = [10 for _ in range(circuit.n_qubits)]  # local clifford operation on each node
    adj: List[Set[int]] = [set() for _ in range(circuit.n_qubits)]  # adjacency list

    for op in circuit.operations:
        index = op.qubit_indices[0]
        if op.gate.name in ["I", "X", "Y", "Z"]:
            # these gates do not change the graph
            continue
        elif op.gate.name == "H":
            lco[index] = multiply_lco[10, lco[index]]
        elif op.gate.name == "S":
            lco[index] = multiply_lco[6, lco[index]]
        elif op.gate.name == "S_Dagger":
            lco[index] = multiply_lco[5, lco[index]]
        elif op.gate.name == "CZ":
            cz(lco, adj, op.qubit_indices[0], op.qubit_indices[1])
        elif op.gate.name == "CNOT":
            # CNOT = (I \otimes H) CZ (I \otimes H)
            index = op.qubit_indices[1]
            lco[index] = multiply_lco[10, lco[index]]
            cz(lco, adj, op.qubit_indices[0], op.qubit_indices[1])
            lco[index] = multiply_lco[10, lco[index]]
        else:
            raise ValueError("Unknown gate: {}".format(op.gate.name))

    return list(zip(lco, adj))


def cz(lco: List[int], adj: List[Set[int]], vertex_1: int, vertex_2: int) -> None:
    """Apply a CZ gate to the graph on the given vertices.

    Args:
        lco (List[int]): local clifford operation on each node
        adj (List[Set[int]]): adjacency list describing the graph state
        vertex_1 (int): vertex to enact the CZ gate on
        vertex_2 (int): vertex to enact the CZ gate on
    """
    if adj[vertex_1] - {vertex_2}:
        remove_lco(lco, adj, vertex_1, vertex_2)
    if adj[vertex_2] - {vertex_1}:
        remove_lco(lco, adj, vertex_2, vertex_1)
    if adj[vertex_1] - {vertex_2}:
        remove_lco(lco, adj, vertex_1, vertex_2)

    connected = vertex_1 in adj[vertex_2] or vertex_2 in adj[vertex_1]
    table_nums = cz_table[int(connected), lco[vertex_1], lco[vertex_2]]

    if connected != table_nums[0]:
        toggle_edge(adj, vertex_1, vertex_2)
    lco[vertex_1] = table_nums[1]
    lco[vertex_2] = table_nums[2]


def remove_lco(lco: List[int], adj: List[Set[int]], v: int, avoid: int) -> None:
    """Remove all local clifford operations on a vertex v. Needs use of a neighbor
    of v, but if we wish to avoid using a particular neighbor, we can specify it.

    Args:
        lco (List[int]): local clifford operations on each node
        adj (List[Set[int]]): adjacency list describing the graph state
        v (int): index of the vertex to remove local clifford operations from
        avoid (int): index of a neighbor of v to avoid using
    """
    if other_neighbors := adj[v] - {avoid}:
        vb = other_neighbors.pop()
    else:
        vb = avoid

    for factor in reversed(decomposition_lookup_table[lco[v]]):
        if factor == "U":
            local_complement(lco, adj, v)
        else:
            local_complement(lco, adj, vb)


def local_complement(lco: List[int], adj: List[Set[int]], v: int) -> None:
    """Take the local complement of a vertex v.

    Args:
        lco (List[int]): local clifford operations on each node
        adj (List[Set[int]]): adjacency list describing the graph state
        v (int): index node to take the local complement of
    """
    neighbors = list(adj[v])
    for i in range(len(neighbors)):
        for j in range(i + 1, len(neighbors)):
            toggle_edge(adj, neighbors[i], neighbors[j])

    lco[v] = multiply_lco[lco[v], 14]
    for i in adj[v]:
        lco[i] = multiply_lco[lco[i], 6]


def toggle_edge(adj: List[Set[int]], vertex_1: int, vertex_2: int) -> None:
    """If vertices vertex_1 and vertex_2 are connected, we remove the edge.
    Otherwise, add it.

    Args:
        adj (List[Set[int]]): adjacency list describing the graph state
        vertex_1 (int): index of vertex to be connected or disconnected
        vertex_2 (int): index of vertex to be connected or disconnected
    """
    #
    if vertex_2 in adj[vertex_1] or vertex_1 in adj[vertex_2]:
        adj[vertex_1].remove(vertex_2)
        adj[vertex_2].remove(vertex_1)
    else:
        adj[vertex_1].add(vertex_2)
        adj[vertex_2].add(vertex_1)
