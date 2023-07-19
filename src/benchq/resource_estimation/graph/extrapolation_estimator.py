from dataclasses import replace
from math import ceil
from typing import List, Optional

import numpy as np
from scipy.optimize import minimize

from ...data_structures import (
    AlgorithmImplementation,
    BasicArchitectureModel,
    DecoderModel,
    ExtrapolatedGraphData,
    ExtrapolatedGraphResourceInfo,
    QuantumProgram,
)
from .graph_estimator import GraphData, GraphResourceEstimator


class ExtrapolationResourceEstimator(GraphResourceEstimator):
    def __init__(
        self,
        hw_model: BasicArchitectureModel,
        steps_to_extrapolate_from: List[int],
        decoder_model: Optional[DecoderModel] = None,
        optimization: str = "space",
        substrate_scheduler_preset: str = "fast",
        n_measurement_steps_fit_type: str = "logarithmic",
    ):
        super().__init__(
            hw_model, decoder_model, optimization, substrate_scheduler_preset
        )
        self.steps_to_extrapolate_from = steps_to_extrapolate_from
        self.n_measurement_steps_fit_type = n_measurement_steps_fit_type

    def get_extrapolated_graph_data(
        self,
        data: List[GraphData],
        program: QuantumProgram,
    ) -> ExtrapolatedGraphData:
        steps_to_extrapolate_to = program.steps

        max_graph_degree, max_graph_degree_r_squared = _get_linear_extrapolation(
            self.steps_to_extrapolate_from,
            np.array([d.max_graph_degree for d in data]),
            steps_to_extrapolate_to,
        )
        # sometimes the n_measurement_steps is logarithmic, sometimes it's linear.
        # we need to check which one is better by inspecting the fit
        if self.n_measurement_steps_fit_type == "logarithmic":
            (
                n_measurement_steps,
                n_measurement_steps_r_squared,
            ) = _get_logarithmic_extrapolation(
                self.steps_to_extrapolate_from,
                np.array([d.n_measurement_steps for d in data]),
                steps_to_extrapolate_to,
            )
        elif self.n_measurement_steps_fit_type == "linear":
            (
                n_measurement_steps,
                n_measurement_steps_r_squared,
            ) = _get_linear_extrapolation(
                self.steps_to_extrapolate_from,
                np.array([d.n_measurement_steps for d in data]),
                steps_to_extrapolate_to,
            )
        else:
            raise ValueError(
                "n_measurement_steps_fit_type must be either 'logarithmic' or 'linear'"
                f", not {self.n_measurement_steps_fit_type}"
            )

        return ExtrapolatedGraphData(
            max_graph_degree=max_graph_degree,
            n_measurement_steps=n_measurement_steps,
            n_nodes=program.n_t_gates + program.n_rotation_gates,
            n_t_gates=program.n_t_gates,
            n_rotation_gates=program.n_rotation_gates,
            n_logical_qubits_r_squared=max_graph_degree_r_squared,
            n_measurement_steps_r_squared=n_measurement_steps_r_squared,
            data_used_to_extrapolate=data,
            steps_to_extrapolate_to=steps_to_extrapolate_to,
        )

    def estimate_given_extrapolation_data(
        self,
        algorithm_description: AlgorithmImplementation,
        extrapolated_info: ExtrapolatedGraphData,
    ):
        assert isinstance(algorithm_description.program, QuantumProgram)
        resource_info = self.estimate_resources_from_graph_data(
            extrapolated_info, algorithm_description
        )
        info = ExtrapolatedGraphResourceInfo(
            n_logical_qubits=resource_info.n_logical_qubits,
            extra=replace(extrapolated_info, n_nodes=resource_info.extra.n_nodes),
            code_distance=resource_info.code_distance,
            logical_error_rate=resource_info.logical_error_rate,
            total_time_in_seconds=resource_info.total_time_in_seconds,
            n_physical_qubits=resource_info.n_physical_qubits,
            decoder_info=resource_info.decoder_info,
            widget_name=resource_info.widget_name,
        )
        return info


def _get_logarithmic_extrapolation(x, y, steps_to_extrapolate_to):
    x = np.array(x)
    y = np.array(y)

    def _logarithmic_objective(params):
        a, b = params
        y_pred = a * np.log(x) + b
        error = y_pred - y
        return np.sum(error**2)

    a_opt, b_opt = _extrapolate(x, y, steps_to_extrapolate_to, _logarithmic_objective)

    extrapolated_point = ceil(a_opt * np.log(steps_to_extrapolate_to) + b_opt)

    # Calculate R-squared value
    y_mean = np.mean(y)
    total_sum_of_squares = np.sum((y - y_mean) ** 2)
    residual_sum_of_squares = np.sum((y - (a_opt * np.log(x) + b_opt)) ** 2)
    r_squared = 1 - (residual_sum_of_squares / total_sum_of_squares)

    return extrapolated_point, r_squared


def _get_linear_extrapolation(x, y, steps_to_extrapolate_to):
    x = np.array(x)
    y = np.array(y)

    def _linear_objective(params):
        a, b = params
        y_pred = a * x + b
        error = y_pred - y
        return np.sum(error**2)

    a_opt, b_opt = _extrapolate(x, y, steps_to_extrapolate_to, _linear_objective)

    extrapolated_point = ceil(a_opt * steps_to_extrapolate_to + b_opt)

    # Calculate R-squared value
    y_mean = np.mean(y)
    total_sum_of_squares = np.sum((y - y_mean) ** 2)
    residual_sum_of_squares = np.sum((y - (a_opt * x + b_opt)) ** 2)
    r_squared = 1 - (residual_sum_of_squares / total_sum_of_squares)

    return extrapolated_point, r_squared


def _extrapolate(x, y, steps_to_extrapolate_to, objective):
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
