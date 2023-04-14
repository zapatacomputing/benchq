################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
from math import ceil, floor
from typing import List

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from .resource_estimation.graph.extrapolation_estimator import ExtrapolatedResourceInfo


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


def plot_extrapolations(
    info: ExtrapolatedResourceInfo,
    steps_to_extrapolate_from: List[int],
):
    """Here we allow one to inspect the fits given by extrapolating a problem
    from a smaller number of steps.
    """
    figure, axis = plt.subplots(3, 1)
    figure.tight_layout(pad=1.5)

    for i, property in enumerate(
        ["n_logical_qubits", "n_nodes", "n_measurement_steps"]
    ):
        x = np.array(steps_to_extrapolate_from)
        y = np.array([getattr(d, property) for d in info.data_used_to_extrapolate])

        # logarithmic extrapolation
        if property == "n_measurement_steps":
            x = np.log(x)

        coeffs, sum_of_residuals, _, _, _ = np.polyfit(x, y, 1, full=True)
        r_squared = 1 - (sum_of_residuals[0] / (len(y) * np.var(y)))
        m, c = coeffs

        # logarithmic extrapolation
        if property == "n_measurement_steps":
            x = np.exp(x)  # rescale the x values for plotting
            extrapolated_point = ceil(m * np.log(info.steps_to_extrapolate_to) + c)

            axis[i].plot(x, y, "o")
            all_x = np.arange(1, info.steps_to_extrapolate_to, 1)
            axis[i].plot(
                all_x,
                m * np.log(all_x) + c,
                "r",
                label="fitted line",
            )
            axis[i].plot(
                [info.steps_to_extrapolate_to],
                [extrapolated_point],
                "ko",
            )
            plt.yticks(range(floor(min(y)), extrapolated_point + 1))
        else:
            extrapolated_point = ceil(m * info.steps_to_extrapolate_to + c)

            axis[i].plot(x, y, "o")
            axis[i].plot(
                [0, info.steps_to_extrapolate_to],
                [c, m * info.steps_to_extrapolate_to + c],
                "r",
                label="fitted line",
            )
            axis[i].plot(
                [info.steps_to_extrapolate_to],
                [extrapolated_point],
                "ko",
            )
            plt.yticks(range(floor(min(y)) - 1, extrapolated_point + 1))

        axis[i].plot([], [], " ", label="r_squared: " + str(r_squared))
        axis[i].legend()
        axis[i].set_title(property)
        axis[i].ticklabel_format(useOffset=False)
        axis[i].yaxis.set_major_formatter(plt.FormatStrFormatter("%d"))
    plt.show()
