################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


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
    for node, neighbors in asg["edge_data"].items():
        for neighbor in neighbors:
            graph_state_graph.add_edge(node, neighbor)

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
