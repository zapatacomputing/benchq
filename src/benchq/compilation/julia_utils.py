################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import time

import networkx as nx

from . import jl


def get_algorithmic_graph_from_Jabalizer(circuit):
    jl.run_jabalizer(circuit)
    return nx.read_adjlist("adjacency_list.nxl")


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
