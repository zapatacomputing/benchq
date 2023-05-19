from dataclasses import dataclass, replace
from math import ceil
from typing import List, Optional

import numpy as np

from ...data_structures import (
    AlgorithmImplementation,
    BasicArchitectureModel,
    DecoderModel,
    ExtrapolatedGraphData,
    ExtrapolatedGraphResourceInfo,
    QuantumProgram,
    ResourceInfo,
)
from .graph_estimator import GraphResourceEstimator


class ExtrapolationResourceEstimator(GraphResourceEstimator):
    def __init__(
        self,
        hw_model: BasicArchitectureModel,
        steps_to_extrapolate_from: List[int],
        decoder_model: Optional[DecoderModel] = None,
        optimization: str = "time",
        distillation_widget: str = "(15-to-1)_7,3,3",
        n_measurement_steps_fit_type: str = "logarithmic",
    ):
        super().__init__(hw_model, decoder_model, distillation_widget, optimization)
        self.steps_to_extrapolate_from = steps_to_extrapolate_from
        self.n_measurement_steps_fit_type = n_measurement_steps_fit_type

    def _get_extrapolated_graph_data(
        self,
        data: List[ResourceInfo],
        program: QuantumProgram,
    ) -> ExtrapolatedGraphData:
        steps_to_extrapolate_to = program.steps

        max_graph_degree, max_graph_degree_r_squared = _get_linear_extrapolation(
            self.steps_to_extrapolate_from,
            np.array([d.n_logical_qubits for d in data]),
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
                np.array([d.extra.n_measurement_steps for d in data]),
                steps_to_extrapolate_to,
            )
        elif self.n_measurement_steps_fit_type == "linear":
            (
                n_measurement_steps,
                n_measurement_steps_r_squared,
            ) = _get_linear_extrapolation(
                self.steps_to_extrapolate_from,
                np.array([d.extra.n_measurement_steps for d in data]),
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

    def estimate_via_extrapolation(
        self,
        algorithm_description: AlgorithmImplementation,
        data: List[ResourceInfo],
    ):
        assert isinstance(algorithm_description.program, QuantumProgram)
        extrapolated_info = self._get_extrapolated_graph_data(
            data, algorithm_description.program
        )
        resource_info = self.estimate_resources_from_graph_data(
            extrapolated_info, algorithm_description
        )
        return ExtrapolatedGraphResourceInfo(
            n_logical_qubits=resource_info.n_logical_qubits,
            extra=replace(
                extrapolated_info, n_nodes=algorithm_description.program.n_nodes
            ),
            code_distance=resource_info.code_distance,
            logical_error_rate=resource_info.logical_error_rate,
            total_time_in_seconds=resource_info.total_time_in_seconds,
            n_physical_qubits=resource_info.n_physical_qubits,
            decoder_info=resource_info.decoder_info,
        )


def _get_linear_extrapolation(x, y, steps_to_extrapolate_to):
    coeffs, sum_of_residuals, _, _, _ = np.polyfit(x, y, 1, full=True)
    r_squared = 1 - (sum_of_residuals[0] / (len(y) * np.var(y)))
    m, c = coeffs

    # get rid of floating point errors
    rounded_point = round(m * steps_to_extrapolate_to + c, 5)
    return ceil(rounded_point), r_squared


def _get_logarithmic_extrapolation(x, y, steps_to_extrapolate_to):
    log_x = np.log(x)
    coeffs, sum_of_residuals, _, _, _ = np.polyfit(log_x, y, 1, full=True)
    r_squared = 1 - (sum_of_residuals[0] / (len(y) * np.var(y)))
    m, c = coeffs

    # get rid of floating point errors
    rounded_point = m * np.log(steps_to_extrapolate_to) + c
    return ceil(rounded_point), r_squared
