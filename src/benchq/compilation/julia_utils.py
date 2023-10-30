################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import time

import networkx as nx
from orquestra.quantum.circuits import Circuit

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
