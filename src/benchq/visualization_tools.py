################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
from typing import List, Optional

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.optimize import minimize

from .resource_estimators.resource_info import (
    ExtrapolatedGraphResourceInfo,
    ResourceInfo,
)


def plot_graph_state_with_measurement_steps(
    graph_state_graph,
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
    info: ExtrapolatedGraphResourceInfo,
    steps_to_extrapolate_from: List[int],
    n_measurement_steps_fit_type: str = "logarithmic",
    exact_info: Optional[ResourceInfo] = None,
):
    """Here we allow one to inspect the fits given by extrapolating a problem
    from a smaller number of steps. If exact_info is provided, we also plot the
    exact values for the problem size in green. The extrapolated point is plotted
    in black. The points used to extrapolate are plotted in blue. The fit is plotted
    in red. If the green or black dot is below the red line on the "n_nodes" plot,
    then we are using a 20-to-4 magic state distillation factory and the "n_nodes"
    was cut in 4 to compensate. This is fine because the original number of nodes
    (without the division by 4) will always follow the red line.
    """
    figure, axis = plt.subplots(3, 1)
    figure.tight_layout(pad=1.5)

    for i, property in enumerate(
        ["max_graph_degree", "n_measurement_steps", "n_nodes"]
    ):
        x = np.array(steps_to_extrapolate_from)
        y = np.array(
            [getattr(d, property) for d in info.extra.data_used_to_extrapolate]
        )

        # logarithmic extrapolation
        if (
            property == "n_measurement_steps"
            and n_measurement_steps_fit_type == "logarithmic"
        ):
            m, c, r_squared = _get_logarithmic_extrapolation(x, y)

            all_x = np.arange(1, info.extra.steps_to_extrapolate_to + 1, 1)
            axis[i].plot(
                all_x,
                m * np.log(all_x) + c,
                "r",
                label="fitted line",
            )
        else:
            m, c, r_squared = _get_linear_extrapolation(x, y)
            axis[i].plot(
                [0, info.extra.steps_to_extrapolate_to],
                [c, m * info.extra.steps_to_extrapolate_to + c],
                "r",
                label="fitted line",
            )

        axis[i].plot(x, y, "bo")
        axis[i].plot(
            [info.extra.steps_to_extrapolate_to],
            [getattr(info.extra, property)],
            "ko",
        )
        if exact_info is not None:
            axis[i].plot(
                [info.extra.steps_to_extrapolate_to],
                [getattr(exact_info.extra, property)],
                "go",
            )

        axis[i].plot([], [], " ", label="r_squared: " + str(r_squared))
        axis[i].legend()
        axis[i].set_title(property)

    plt.show()


def _get_logarithmic_extrapolation(x, y):
    x = np.array(x)
    y = np.array(y)

    def _logarithmic_objective(params):
        a, b = params
        y_pred = a * np.log(x) + b
        error = y_pred - y
        return np.sum(error**2)

    a_opt, b_opt = _extrapolate(x, y, _logarithmic_objective)

    # Calculate R-squared value
    y_mean = np.mean(y)
    total_sum_of_squares = np.sum((y - y_mean) ** 2)
    residual_sum_of_squares = np.sum((y - (a_opt * np.log(x) + b_opt)) ** 2)
    r_squared = 1 - (residual_sum_of_squares / total_sum_of_squares)

    return a_opt, b_opt, r_squared


def _get_linear_extrapolation(x, y):
    x = np.array(x)
    y = np.array(y)

    def _linear_objective(params):
        a, b = params
        y_pred = a * x + b
        error = y_pred - y
        return np.sum(error**2)

    a_opt, b_opt = _extrapolate(x, y, _linear_objective)

    # Calculate R-squared value
    y_mean = np.mean(y)
    total_sum_of_squares = np.sum((y - y_mean) ** 2)
    residual_sum_of_squares = np.sum((y - (a_opt * x + b_opt)) ** 2)
    r_squared = 1 - (residual_sum_of_squares / total_sum_of_squares)

    return a_opt, b_opt, r_squared


def _extrapolate(x, y, objective):
    # Define the constraint that the slope (a) must be greater than zero
    def slope_constraint(params):
        a, _ = params
        return a

    # Perform the optimization
    initial_guess = [1.0, 1.0]
    bounds = [(0, None), (None, None)]
    constraints = {"type": "ineq", "fun": slope_constraint}
    result = minimize(objective, initial_guess, bounds=bounds, constraints=constraints)

    # Extrapolated to desired point
    a_opt, b_opt = result.x

    return a_opt, b_opt
