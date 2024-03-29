################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from copy import copy
from typing import Tuple


def plot_graph_state_with_measurement_steps(
    asg,
    measurement_steps,
    cmap=plt.cm.rainbow,
    name="extrapolation_plot",
):
    """Plot a graph state with the measurement steps highlighted in different
    colors. The measurement steps are given as a list of lists of nodes. Each
    list of nodes is a measurement step. The nodes are given as a list of
    tuples. Each tuple is a node and a measurement basis. The node is an
    integer and the measurement basis is a string. The graph state is given as
    a networkx graph. The nodes are integers and the edges are tuples of
    integers. The cmap is the color map to use for the measurement steps.
    Note: Only works when substrate scheduler is run in "fast" mode."""
    graph_state_graph = nx.Graph()
    for node, neighbors in enumerate(asg["edge_data"]):
        for neighbor in neighbors:
            graph_state_graph.add_edge(node, neighbor)
    _, graph_state_graph = remove_isolated_nodes_from_graph(graph_state_graph)

    node_measurement_groupings = [
        [node[0] for node in row] for row in measurement_steps
    ]
    colors = cmap(np.linspace(0, 1, len(node_measurement_groupings)))
    color_map = []
    for node in graph_state_graph:
        for i, group in enumerate(node_measurement_groupings):
            if int(node) in group:
                color_map.append(colors[i])
                break

    nx.draw(graph_state_graph, node_color=color_map, node_size=10)
    # uncomment following lines to save graph image as well as show it
    # plt.savefig(name + ".pdf")
    # plt.clf()
    plt.show()


def remove_isolated_nodes_from_graph(graph: nx.Graph) -> Tuple[int, nx.Graph]:
    cleaned_graph = copy(graph)
    isolated_nodes = list(nx.isolates(cleaned_graph))
    n_nodes_removed = len(isolated_nodes)

    cleaned_graph.remove_nodes_from(isolated_nodes)
    cleaned_graph = nx.convert_node_labels_to_integers(cleaned_graph)

    return n_nodes_removed, cleaned_graph
