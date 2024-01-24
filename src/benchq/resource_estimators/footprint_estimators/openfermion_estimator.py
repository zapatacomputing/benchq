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
from typing import Iterable, Optional

from ...decoder_modeling.decoder_resource_estimator import get_decoder_info
from ...magic_state_distillation import MagicStateFactory
from ...magic_state_distillation.autoccz_factories import iter_all_openfermion_factories
from ...quantum_hardware_modeling import (
    BASIC_SC_ARCHITECTURE_MODEL,
    BasicArchitectureModel,
)
from ...quantum_hardware_modeling.fowler_surface_code import (
    logical_cell_error_rate,
    physical_qubits_per_logical_qubit,
)
from ..resource_info import OpenFermionExtra, OpenFermionResourceInfo


@dataclasses.dataclass(frozen=True, unsafe_hash=True)
class CostEstimate:
    physical_qubit_count: int
    duration: float
    algorithm_failure_probability: float
    magic_state_factory_name: str


@dataclasses.dataclass(frozen=True, unsafe_hash=True)
class AlgorithmParameters:
    physical_error_rate: float
    surface_code_cycle_time: float
    logical_data_qubit_distance: int
    magic_state_factory: MagicStateFactory
    max_allocated_logical_qubits: int
    factory_count: int
    routing_overhead_proportion: float
    toffoli_count: int = 0
    t_count: int = 0
    proportion_of_bounding_box: float = 1


def _estimate_cost(params: AlgorithmParameters) -> CostEstimate:
    """Determine algorithm single-shot layout and costs for given params.

    ASSUMES:
        - There is enough routing area to get needed data qubits to the
            factories as fast as the factories run.
        - The bottleneck time cost is waiting for magic states.
    """
    if params.t_count == 0 and params.toffoli_count == 0:
        raise ValueError("Circuit must contain T gates and/or Toffoli gates.")

    n_logical_qubits_used_for_computation = int(
        math.ceil(
            params.max_allocated_logical_qubits
            * (1 + params.routing_overhead_proportion)
        )
    )
    n_physical_qubits_used_for_computation = (
        n_logical_qubits_used_for_computation
        * physical_qubits_per_logical_qubit(params.logical_data_qubit_distance)
    )

    n_physical_qubits_used_for_distillation = (
        params.factory_count * params.magic_state_factory.qubits
    )

    n_total_distillations = params.toffoli_count + math.ceil(params.t_count / 2)

    total_distillation_cycles = int(
        n_total_distillations
        / params.factory_count
        * params.magic_state_factory.distillation_time_in_cycles
    )
    distillation_failure = (
        params.magic_state_factory.distilled_magic_state_error_rate
        * n_total_distillations
    )

    V_computation = (
        params.proportion_of_bounding_box
        * n_physical_qubits_used_for_computation
        * total_distillation_cycles
    )
    data_failure = (
        logical_cell_error_rate(
            params.logical_data_qubit_distance,
            physical_qubit_error_rate=params.physical_error_rate,
        )
        * V_computation
    )

    return CostEstimate(
        physical_qubit_count=n_physical_qubits_used_for_computation
        + n_physical_qubits_used_for_distillation,
        duration=total_distillation_cycles * params.surface_code_cycle_time,
        algorithm_failure_probability=min(1.0, data_failure + distillation_failure),
        magic_state_factory_name=params.magic_state_factory.name,
    )


def _cost_estimator(
    num_logical_qubits: int,
    num_toffoli: int = 0,
    num_t: int = 0,
    surface_code_cycle_time: float = 1e-6,
    physical_error_rate: float = 1.0e-3,
    portion_of_bounding_box: float = 1.0,
    routing_overhead_proportion: float = 0.5,
    hardware_failure_tolerance: float = 1e-3,
    factory_count: int = 4,
    magic_state_factory_iterator: Optional[Iterable[MagicStateFactory]] = None,
):
    """
    Produce best cost in terms of physical qubits and real run time based on
    number of toffoli, number of logical qubits, and physical error rate.
    """
    if num_t == 0 and num_toffoli == 0:
        raise ValueError("Circuit must contain T gates and/or Toffoli gates.")
    if magic_state_factory_iterator is None:
        magic_state_factory_iterator = iter_all_openfermion_factories(
            physical_error_rate
        )

    best_cost = None
    best_params = None
    for factory in magic_state_factory_iterator:
        for logical_data_qubit_distance in range(7, 101, 2):
            params = AlgorithmParameters(
                physical_error_rate=physical_error_rate,
                surface_code_cycle_time=surface_code_cycle_time,
                logical_data_qubit_distance=logical_data_qubit_distance,
                magic_state_factory=factory,
                toffoli_count=num_toffoli,
                t_count=num_t,
                max_allocated_logical_qubits=num_logical_qubits,
                factory_count=factory_count,
                routing_overhead_proportion=routing_overhead_proportion,
                proportion_of_bounding_box=portion_of_bounding_box,
            )

            cost = _estimate_cost(params)

            if cost.algorithm_failure_probability <= hardware_failure_tolerance:
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
            "Failed to find parameters that yield an acceptable failure probability. "
            "You must decrease the number of T gates and/or Toffolis in your circuit"
        )

    return best_cost, best_params


def footprint_estimator(
    num_logical_qubits: int,
    num_toffoli: int = 0,
    num_t: int = 0,
    architecture_model: BasicArchitectureModel = BASIC_SC_ARCHITECTURE_MODEL,
    routing_overhead_proportion=0.5,
    hardware_failure_tolerance=1e-3,
    factory_count: int = 4,
    magic_state_factory_iterator: Optional[Iterable[MagicStateFactory]] = None,
    decoder_model=None,
) -> OpenFermionResourceInfo:
    """Get the estimated resources for single factorized QPE as described in PRX Quantum
    2, 030305.

    Args:
        num_toffoli: The number of Toffoli gates required.
        num_logical_qubits: The number of logical qubits required.
    Returns:
        The estimated physical qubits, runtime, and other resource estimation info.
    """

    best_cost, best_params = _cost_estimator(
        num_logical_qubits,
        num_toffoli=num_toffoli,
        num_t=num_t,
        physical_error_rate=architecture_model.physical_qubit_error_rate,
        surface_code_cycle_time=architecture_model.surface_code_cycle_time_in_seconds,
        routing_overhead_proportion=routing_overhead_proportion,
        hardware_failure_tolerance=hardware_failure_tolerance,
        factory_count=factory_count,
        magic_state_factory_iterator=magic_state_factory_iterator,
    )

    decoder_info = get_decoder_info(
        architecture_model,
        decoder_model,
        best_params.logical_data_qubit_distance,
        best_cost.physical_qubit_count * best_cost.duration,
        best_params.max_allocated_logical_qubits,
    )

    resource_info = OpenFermionResourceInfo(
        n_physical_qubits=best_cost.physical_qubit_count,
        n_logical_qubits=best_params.max_allocated_logical_qubits,
        total_time_in_seconds=best_cost.duration,
        code_distance=best_params.logical_data_qubit_distance,
        logical_error_rate=best_cost.algorithm_failure_probability,
        decoder_info=decoder_info,
        routing_to_measurement_volume_ratio=best_params.routing_overhead_proportion,
        magic_state_factory_name=best_params.magic_state_factory.name,
        extra=OpenFermionExtra(
            fail_rate_msFactory=best_params.magic_state_factory.distilled_magic_state_error_rate,  # noqa: E501
            rounds_magicstateFactory=best_params.magic_state_factory.distillation_time_in_cycles,  # noqa: E501
            physical_qubit_error_rate=best_params.physical_error_rate,
            scc_time=best_params.surface_code_cycle_time,
        ),
    )

    return resource_info
