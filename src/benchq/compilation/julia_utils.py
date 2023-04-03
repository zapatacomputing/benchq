################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import time
from typing import List, Set, Tuple

import networkx as nx

from . import jl


def get_algorithmic_graph_from_Jabalizer(circuit):
    jl.run_jabalizer(circuit)
    return nx.read_adjlist("adjacency_list.nxl")


def get_algorithmic_graph_from_graph_sim_mini(circuit):
    lco, adj = jl.run_graph_sim_mini(circuit)

    print("getting networkx graph from vertices")
    start = time.time()
    edges = []
    for vertex, neighbors in enumerate(adj):
        for neighbor in neighbors:
            edges.append(vertex, neighbor)
    graph = get_networkx_graph_from_vertices(list(zip(lco, adj)))
    end = time.time()
    print("time: ", end - start)

    return graph


def get_networkx_graph_from_vertices(vertices: List[Tuple[int, Set[int]]]) -> nx.Graph:
    """Convert the vertices of a graph to a networkx graph.

    Args:
        vertices (list(tuple(int, set(int)))): list of vertices of the graph state
            of the form (lco, neighbors).

        Returns:
            nx.Graph: the networkx graph with those vertices
    """
    G = nx.empty_graph(len(vertices))
    for vertex_id, vertex in enumerate(vertices):
        for neighbor in vertex[1]:
            G.add_edge(vertex_id, neighbor)
    return G
