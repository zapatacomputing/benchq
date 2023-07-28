################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import time

import networkx as nx

from . import jl


def get_algorithmic_graph_from_graph_sim_mini(circuit):
    lco, adj = jl.run_graph_sim_mini(circuit)

    print("getting networkx graph from vertices")
    start = time.time()
    graph = nx.empty_graph(len(adj))
    for vertex_id, neighbors in enumerate(adj):
        for neighbor in neighbors:
            graph.add_edge(vertex_id, neighbor)
    end = time.time()
    print("time: ", end - start)

    return graph


def get_algorithmic_graph_from_Jabalizer(circuit):
    svec, op_seq, icm_output, data_qubits_map = jl.run_jabalizer(circuit)
    # use dummy graph for quick resource estimate as we are just trying to
    # benchmark Jabalizer here
    dummy_graph = nx.path_graph(len(svec))
    return dummy_graph


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
