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


def plot_linear_extrapolations(
    ExtrapolatedResourceInfo, steps_to_extrapolate_from, steps_to_extrapolate_to
):
    figure, axis = plt.subplots(3, 1)
    figure.tight_layout(pad=1.5)

    for i, property in enumerate(
        ["n_logical_qubits", "n_nodes", "n_measurement_steps"]
    ):
        x = steps_to_extrapolate_from
        y = np.array(
            [
                getattr(d, property)
                for d in ExtrapolatedResourceInfo.data_used_to_extrapolate
            ]
        )

        # logarithmic extrapolation
        if property == "n_measurement_steps":
            x = np.log(x)

        coeffs, sum_of_residuals, _, _, _ = np.polyfit(x, y, 1, full=True)
        r_squared = 1 - (sum_of_residuals[0] / (len(y) * np.var(y)))
        m, c = coeffs

        axis[i].plot(x, y, "o")
        axis[i].plot(
            [0, steps_to_extrapolate_to],
            [c, m * steps_to_extrapolate_to + c],
            "r",
            label="fitted line",
        )
        axis[i].plot(
            [steps_to_extrapolate_to],
            [m * steps_to_extrapolate_to + c],
            "ko",
        )
        axis[i].plot([], [], " ", label="r_squared: " + str(r_squared))
        axis[i].legend()
        axis[i].set_title(property)
        axis[i].ticklabel_format(useOffset=False)
        axis[i].yaxis.set_major_formatter(plt.FormatStrFormatter("%d"))
    plt.show()
