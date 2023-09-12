#   Copyright 2017 The OpenFermion Developers
#   Modifications copyright 2023 Zapata Computing, Inc. for purposes
#   of giving users more control over physical costing parameters.
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import dataclasses
import math
from typing import Iterator, Tuple


@dataclasses.dataclass(frozen=True, unsafe_hash=True)
class MagicStateFactory:
    details: str
    physical_qubit_footprint: int
    distillation_time_in_tocks: int
    failure_rate: float


@dataclasses.dataclass(frozen=True, unsafe_hash=True)
class CostEstimate:
    physical_qubit_count: int
    duration: float
    algorithm_failure_probability: float


@dataclasses.dataclass(frozen=True, unsafe_hash=True)
class AlgorithmParameters:
    physical_error_rate: float
    surface_code_cycle_time: float
    logical_data_qubit_distance: int
    widget: MagicStateFactory
    max_allocated_logical_qubits: int
    factory_count: int
    routing_overhead_proportion: float
    toffoli_count: int = 0
    t_count: int = 0
    proportion_of_bounding_box: float = 1

    def estimate_cost(self) -> CostEstimate:
        """Determine algorithm single-shot layout and costs for given params.

        ASSUMES:
            - There is enough routing area to get needed data qubits to the
                factories as fast as the factories run.
            - The bottleneck time cost is waiting for magic states.
        """
        if self.t_count == 0 and self.toffoli_count == 0:
            raise ValueError(
                "Cannot accommodate circuits having no T gates and Toffoli gates."
            )

        n_logical_qubits_used_for_computation = int(
            math.ceil(
                self.max_allocated_logical_qubits
                * (1 + self.routing_overhead_proportion)
            )
        )
        n_physical_qubits_used_for_computation = (
            n_logical_qubits_used_for_computation
            * _physical_qubits_per_logical_qubit(self.logical_data_qubit_distance)
        )

        n_physical_qubits_used_for_distillation = (
            self.factory_count * self.widget.physical_qubit_footprint
        )

        total_distillation_tocks = int(
            (self.toffoli_count + math.ceil(self.t_count / 2))
            / self.factory_count
            * self.widget.distillation_time_in_tocks
        )

        distillation_failure = self.widget.failure_rate * (
            math.ceil(self.t_count / 2) + self.toffoli_count
        )

        V_computation = (
            self.proportion_of_bounding_box
            * n_physical_qubits_used_for_computation
            * total_distillation_tocks
        )
        data_failure = (
            _logical_cell_error_rate(
                self.logical_data_qubit_distance,
                physical_qubit_error_rate=self.physical_error_rate,
            )
            * V_computation
        )

        return CostEstimate(
            physical_qubit_count=n_physical_qubits_used_for_computation
            + n_physical_qubits_used_for_distillation,
            duration=total_distillation_tocks * self.surface_code_cycle_time,
            algorithm_failure_probability=min(1.0, data_failure + distillation_failure),
        )


def _logical_cell_error_rate(
    code_distance: int, physical_qubit_error_rate: float
) -> float:
    return 0.1 * (100 * physical_qubit_error_rate) ** ((code_distance + 1) / 2)


def _get_total_logical_failure_rate(
    code_distance: int, physical_qubit_error_rate: float, logical_st_volume: int
) -> float:
    return logical_st_volume * _logical_cell_error_rate(
        code_distance, physical_qubit_error_rate
    )


def iter_known_factories(
    physical_error_rate: float, num_toffoli: int, num_t: int
) -> Iterator[MagicStateFactory]:
    error_msg = "Cannot accommodate circuits having no T gates and Toffoli gates."

    if num_t == 0 and num_toffoli == 0:
        raise ValueError(error_msg)
    yield from iter_auto_ccz_factories(physical_error_rate)


def _autoccz_or_t_factory_dimensions(
    l1_distance: int, l2_distance: int
) -> Tuple[int, int, float]:
    """Determine the width, height, depth of the magic state factory."""
    t1_height = 4 * l1_distance / l2_distance
    t1_width = 8 * l1_distance / l2_distance
    t1_depth = 5.75 * l1_distance / l2_distance

    ccz_depth = 5
    ccz_height = 6
    ccz_width = 3
    storage_width = 2 * l1_distance / l2_distance

    ccz_rate = 1 / ccz_depth
    t1_rate = 1 / t1_depth
    t1_factories = int(math.ceil((ccz_rate * 8) / t1_rate))
    t1_factory_column_height = t1_height * math.ceil(t1_factories / 2)

    width = int(math.ceil(t1_width * 2 + ccz_width + storage_width))
    height = int(math.ceil(max(ccz_height, t1_factory_column_height)))
    depth = max(ccz_depth, t1_depth)

    return width, height, depth


def iter_auto_ccz_factories(physical_error_rate: float) -> Iterator[MagicStateFactory]:
    for l1_distance in range(5, 25, 2):
        for l2_distance in range(l1_distance + 2, 41, 2):
            w, h, d = _autoccz_or_t_factory_dimensions(
                l1_distance=l1_distance, l2_distance=l2_distance
            )
            f_ccz = _compute_autoccz_distillation_error(
                l1_distance=l1_distance,
                l2_distance=l2_distance,
                physical_error_rate=physical_error_rate,
            )

            yield MagicStateFactory(
                details=f"AutoCCZ({physical_error_rate=},{l1_distance=},{l2_distance=}",
                physical_qubit_footprint=w
                * h
                * _physical_qubits_per_logical_qubit(l2_distance),
                distillation_time_in_tocks=int(d * l2_distance),
                failure_rate=float(f_ccz),
            )


def _compute_autoccz_distillation_error(
    l1_distance: int, l2_distance: int, physical_error_rate: float
) -> float:
    # Level 0
    L0_distance = l1_distance // 2
    L0_distillation_error = physical_error_rate
    L0_topological_error = _get_total_logical_failure_rate(
        logical_st_volume=100,  # Estimated 100 for T injection.
        code_distance=L0_distance,
        physical_qubit_error_rate=physical_error_rate,
    )
    L0_total_T_error = L0_distillation_error + L0_topological_error

    # Level 1
    L1_topological_error = _get_total_logical_failure_rate(
        logical_st_volume=1100,  # Estimated 1000 for factory, 100 for T injection.
        code_distance=l1_distance,
        physical_qubit_error_rate=physical_error_rate,
    )
    L1_distillation_error = 35 * L0_total_T_error**3
    L1_total_T_error = L1_distillation_error + L1_topological_error

    # Level 2
    L2_topological_error = _get_total_logical_failure_rate(
        logical_st_volume=1000,  # Estimated 1000 for factory.
        code_distance=l2_distance,
        physical_qubit_error_rate=physical_error_rate,
    )
    L2_distillation_error = 28 * L1_total_T_error**2
    L2_total_CCZ_or_2T_error = L2_topological_error + L2_distillation_error

    return L2_total_CCZ_or_2T_error


def _physical_qubits_per_logical_qubit(code_distance: int) -> int:
    return (code_distance + 1) ** 2 * 2


def cost_estimator(
    num_logical_qubits,
    num_toffoli=0,
    num_t=0,
    surface_code_cycle_time=1e-6,
    physical_error_rate=1.0e-3,
    portion_of_bounding_box=1.0,
    routing_overhead_proportion=0.5,
    hardware_failure_tolerance=1e-3,
):
    """
    Produce best cost in terms of physical qubits and real run time based on
    number of toffoli, number of logical qubits, and physical error rate.
    """

    best_cost = None
    best_params = None
    for factory in iter_known_factories(
        physical_error_rate=physical_error_rate, num_toffoli=num_toffoli, num_t=num_t
    ):
        for logical_data_qubit_distance in range(7, 101, 2):
            params = AlgorithmParameters(
                physical_error_rate=physical_error_rate,
                surface_code_cycle_time=surface_code_cycle_time,
                logical_data_qubit_distance=logical_data_qubit_distance,
                widget=factory,
                toffoli_count=num_toffoli,
                t_count=num_t,
                max_allocated_logical_qubits=num_logical_qubits,
                factory_count=4,
                routing_overhead_proportion=routing_overhead_proportion,
                proportion_of_bounding_box=portion_of_bounding_box,
            )
            cost = params.estimate_cost()
            if cost.algorithm_failure_probability < hardware_failure_tolerance:
                # optimize for smallest spacetime volume
                if (
                    best_cost is None
                    or cost.physical_qubit_count * cost.duration
                    < best_cost.physical_qubit_count * best_cost.duration
                ):
                    best_cost = cost
                    best_params = params

    if best_cost is None:
        raise RuntimeError(
            "Failed to find parameters that yield an acceptable failure probability."
        )

    return best_cost, best_params
