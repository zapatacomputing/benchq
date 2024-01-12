################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import time

import networkx as nx
from orquestra.quantum.circuits import (
    Circuit,
    CNOT,
    CZ,
    H,
    S,
    T,
    X,
    Y,
    Z,
    I,
    RZ,
    Dagger,
)


from .initialize_julia import jl


def get_nx_graph_from_rbs_adj_list(adj: list) -> nx.Graph:
    graph = nx.empty_graph(len(adj))
    for vertex_id, neighbors in enumerate(adj):
        for neighbor in neighbors:
            graph.add_edge(vertex_id, neighbor)

    return graph


def get_algorithmic_graph_from_ruby_slippers(circuit: Circuit) -> nx.Graph:
    lco, adj, _ = jl.run_ruby_slippers(circuit, True)

    print("getting networkx graph from vertices")
    start = time.time()
    graph = get_nx_graph_from_rbs_adj_list(adj)
    end = time.time()
    print("time: ", end - start)

    return graph


def get_ruby_slippers_compiler(
    verbose=True,
    max_graph_size=1e7,
    teleportation_threshold=40,
    min_neighbors=6,
    teleportation_distance=4,
    max_num_neighbors_to_search=1e5,
    decomposition_strategy=1,
):
    def _run_compiler(circuit: Circuit) -> nx.Graph:
        lco, adj, _ = jl.run_ruby_slippers(
            circuit,
            verbose,
            max_graph_size,
            teleportation_threshold,
            teleportation_distance,
            min_neighbors,
            max_num_neighbors_to_search,
            decomposition_strategy,
        )

        print("getting networkx graph from vertices")
        start = time.time()
        graph = get_nx_graph_from_rbs_adj_list(adj)
        end = time.time()
        print("time: ", end - start)

        return graph

    return _run_compiler


def get_algorithmic_graph_from_Jabalizer(circuit: Circuit) -> nx.Graph:
    svec, op_seq, icm_output, data_qubits_map = jl.run_jabalizer(circuit)
    return create_graph_from_stabilizers(svec)


def create_graph_from_stabilizers(svec):
    G = nx.Graph()
    siz = len(svec)
    for i in range(siz):
        z = svec[i].Z
        for j in range(i + 1, siz):
            if z[j]:
                G.add_edge(i, j)
    return G


def get_algorithmic_graph_and_icm_output(circuit):
    svec, op_seq, icm_output, data_qubits_map = jl.run_jabalizer(circuit)
    return create_graph_from_stabilizers(svec), op_seq, icm_output, data_qubits_map


def icmop_to_circuit(icmop):
    """Converts an ICMOp to an Orquestra Circuit"""
    gate_map = {
        1: I,
        2: X,
        3: Y,
        4: Z,
        7: X,
        8: Y,
        9: Z,
        10: CZ,
        11: CNOT,
        12: T,
        13: Dagger(T),
        14: RZ,
    }

    circuit = Circuit()
    for op in icmop:
        gate_type = gate_map[op[0]]
        qubits = (
            [op[1], op[2]] if op[2] != 0 else [op[1]]
        )  # Check if there's a second qubit
        params = [op[3]] if op[3] != 0 else []  # Check if there's an angle parameter
        gate = gate_type(*qubits, *params)
        circuit.operations.append(gate)

    return circuit
