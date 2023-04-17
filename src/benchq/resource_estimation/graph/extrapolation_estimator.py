from dataclasses import dataclass
from math import ceil
from typing import List, Optional

import numpy as np

from ...data_structures import BasicArchitectureModel, DecoderModel
from .graph_estimator import GraphData, GraphResourceEstimator, ResourceInfo


@dataclass
class ExtrapolatedGraphData(GraphData):
    max_graph_degree_r_squared: float
    n_measurement_steps_r_squared: float
    n_nodes_r_squared: float


@dataclass
class ExtrapolatedResourceInfo(ResourceInfo):
    n_logical_qubits_r_squared: float
    n_measurement_steps_r_squared: float
    n_nodes_r_squared: float
    data_used_to_extrapolate: List[ResourceInfo]
    steps_to_extrapolate_to: int

    def __repr__(self):
        new_necessary_info = [
            "n_logical_qubits_r_squared",
            "n_measurement_steps_r_squared",
            "n_nodes_r_squared",
        ]
        inherited_necessary_info = super().__repr__() + "\n"

        return inherited_necessary_info + "\n".join(
            f"{info}: {getattr(self, info)}" for info in new_necessary_info
        )


class ExtrapolationResourceEstimator(GraphResourceEstimator):
    def __init__(
        self,
        hw_model: BasicArchitectureModel,
        steps_to_extrapolate_from: List[int],
        decoder_model: Optional[DecoderModel] = None,
        n_measurement_steps_fit_type: str = "logarithmic",
    ):
        self.hw_model = hw_model
        self.steps_to_extrapolate_from = steps_to_extrapolate_from
        self.decoder_model = decoder_model
        self.n_measurement_steps_fit_type = n_measurement_steps_fit_type

    def _get_extrapolated_graph_data(
        self, data: List[ResourceInfo], steps_to_extrapolate_to: int
    ) -> ExtrapolatedGraphData:

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

        n_nodes, n_nodes_r_squared = _get_linear_extrapolation(
            self.steps_to_extrapolate_from,
            np.array([d.n_nodes for d in data]),
            steps_to_extrapolate_to,
        )

        return ExtrapolatedGraphData(
            max_graph_degree=max_graph_degree,
            n_measurement_steps=n_measurement_steps,
            n_nodes=n_nodes,
            max_graph_degree_r_squared=max_graph_degree_r_squared,
            n_measurement_steps_r_squared=n_measurement_steps_r_squared,
            n_nodes_r_squared=n_nodes_r_squared,
        )

    def estimate_via_extrapolation(
        self,
        data: List[ResourceInfo],
        error_budget,
        delayed_gate_synthesis: bool,
        steps_to_extrapolate_to: int,
    ):
        extrapolated_info = self._get_extrapolated_graph_data(
            data, steps_to_extrapolate_to
        )
        resource_info = self._estimate_resources_from_graph_data(
            extrapolated_info, delayed_gate_synthesis, error_budget
        )
        return ExtrapolatedResourceInfo(
            n_logical_qubits=resource_info.n_logical_qubits,
            n_measurement_steps=resource_info.n_measurement_steps,
            n_nodes=resource_info.n_nodes,
            synthesis_multiplier=resource_info.synthesis_multiplier,
            code_distance=resource_info.code_distance,
            logical_error_rate=resource_info.logical_error_rate,
            total_time=resource_info.total_time,
            n_physical_qubits=resource_info.n_physical_qubits,
            decoder_power=resource_info.decoder_power,
            decoder_area=resource_info.decoder_area,
            max_decodable_distance=resource_info.max_decodable_distance,
            n_logical_qubits_r_squared=extrapolated_info.max_graph_degree_r_squared,
            n_measurement_steps_r_squared=extrapolated_info.n_measurement_steps_r_squared,  # noqa: E501
            n_nodes_r_squared=extrapolated_info.n_nodes_r_squared,
            data_used_to_extrapolate=data,
            steps_to_extrapolate_to=steps_to_extrapolate_to,
        )


def _get_linear_extrapolation(x, y, steps_to_extrapolate_to):
    coeffs, sum_of_residuals, _, _, _ = np.polyfit(x, y, 1, full=True)
    r_squared = 1 - (sum_of_residuals[0] / (len(y) * np.var(y)))
    m, c = coeffs
    return ceil(m * steps_to_extrapolate_to + c), r_squared


def _get_logarithmic_extrapolation(x, y, steps_to_extrapolate_to):
    log_x = np.log(x)
    coeffs, sum_of_residuals, _, _, _ = np.polyfit(log_x, y, 1, full=True)
    r_squared = 1 - (sum_of_residuals[0] / (len(y) * np.var(y)))
    m, c = coeffs
    return ceil(m * np.log(steps_to_extrapolate_to) + c), r_squared
