################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import time

import networkx as nx

from . import jl


def get_algorithmic_graph_from_ruby_slippers(circuit):
    lco, adj = jl.run_ruby_slippers(circuit, True)

    print("getting networkx graph from vertices")
    start = time.time()
    graph = nx.empty_graph(len(adj))
    for vertex_id, neighbors in enumerate(adj):
        for neighbor in neighbors:
            graph.add_edge(vertex_id, neighbor)
    end = time.time()
    print("time: ", end - start)

    return graph


def get_algorithmic_graph_from_ruby_slippers_with_hyperparams(
    verbose=True,
    max_graph_size=9999999,
    teleportation_threshold=40,
    min_neighbors=6,
    oz_to_kansas_distance=4,
    max_num_neighbors_to_search=99999,
):
    def _run_compiler(circuit):
        lco, adj = jl.run_ruby_slippers(
            circuit,
            verbose,
            max_graph_size,
            teleportation_threshold,
            oz_to_kansas_distance,
            min_neighbors,
            max_num_neighbors_to_search,
        )

        print("getting networkx graph from vertices")
        start = time.time()
        graph = nx.empty_graph(len(adj))
        for vertex_id, neighbors in enumerate(adj):
            for neighbor in neighbors:
                graph.add_edge(vertex_id, neighbor)
        end = time.time()
        print("time: ", end - start)

        return graph

    return _run_compiler


def get_algorithmic_graph_from_Jabalizer(circuit):
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
