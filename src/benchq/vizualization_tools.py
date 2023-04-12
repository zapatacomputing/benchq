################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def plot_graph_state_with_measurement_steps(
    graph_state_graph,
    measurement_steps,
    cmap=plt.cm.rainbow,
    name="measurement_steps_plot",
):
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


def plot_linear_extrapolation(x, y, steps_to_extrapolate_to):
    coeffs, sum_of_residuals, _, _, _ = np.polyfit(x, y, 1, full=True)
    r_squared = 1 - (sum_of_residuals[0] / (len(y) * np.var(y)))
    m, c = coeffs
    plt.plot(x, y, "o")
    plt.plot(
        [0, steps_to_extrapolate_to],
        [c, m * steps_to_extrapolate_to + c],
        "r",
        label="fitted line",
    )
    plt.legend()
    plt.show()
    return r_squared
