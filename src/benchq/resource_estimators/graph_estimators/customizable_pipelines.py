from copy import deepcopy
from dataclasses import replace
from inspect import signature
from typing import List

from ...algorithms.data_structures.algorithm_implementation import (
    AlgorithmImplementation,
)
from ...quantum_hardware_modeling.hardware_architecture_models import (
    BASIC_ION_TRAP_ARCHITECTURE_MODEL,
)
from ..resource_info import ExtrapolatedGraphData, ExtrapolatedGraphResourceInfo
from .extrapolation_estimator import ExtrapolationResourceEstimator
from .graph_estimator import GraphData, GraphPartition


def get_custom_resource_estimation(
    algorithm_implementation: AlgorithmImplementation,
    estimator,
    transformers,
):
    for transformer in transformers:
        algorithm_implementation = replace(
            algorithm_implementation,
            program=transformer(algorithm_implementation.program),
        )

    return estimator.estimate(algorithm_implementation)


def _get_extrapolated_graph_data(
    algorithm_implementation: AlgorithmImplementation,
    estimator: ExtrapolationResourceEstimator,
    transformers,
) -> ExtrapolatedGraphData:
    synthesis_accuracy_for_each_rotation = 1 - (
        1 - algorithm_implementation.error_budget.transpilation_failure_tolerance
    ) ** (1 / algorithm_implementation.program.n_rotation_gates)

    small_programs_graph_data: List[GraphData] = []
    for i in estimator.steps_to_extrapolate_from:
        print(f"Creating graph data for {i} steps...")

        # create copy of program for each number of steps
        small_algorithm_implementation = deepcopy(algorithm_implementation)
        small_algorithm_implementation.error_budget = replace(
            algorithm_implementation.error_budget,
            transpilation_failure_tolerance=synthesis_accuracy_for_each_rotation
            * small_algorithm_implementation.program.n_rotation_gates,
        )

        for transformer in transformers:
            small_algorithm_implementation.program.steps = i
            small_algorithm_implementation.program = transformer(
                small_algorithm_implementation.program
            )

        graph_data = estimator._get_graph_data_for_single_graph(
            small_algorithm_implementation.program
        )
        small_programs_graph_data.append(graph_data)

    # get transformers which are used before graph creation
    circuit_transformers = []
    for transformer in transformers:
        # This is a little hacky, would prefer to use a protocol here.
        if signature(transformer).return_annotation is GraphPartition:
            break
        circuit_transformers.append(transformer)

    for transformer in circuit_transformers:
        algorithm_implementation = replace(
            algorithm_implementation,
            program=transformer(algorithm_implementation.program),
        )

    return estimator.get_extrapolated_graph_data(
        small_programs_graph_data, algorithm_implementation.program
    )


def get_extrapolated_graph_data(
    algorithm_implementation: AlgorithmImplementation,
    steps_to_extrapolate_from,
    decoder_model,
    transformers,
):
    # the architecture model doesn't matter for extrapolating graph data
    dummy_extrapolation_estimator = ExtrapolationResourceEstimator(
        BASIC_ION_TRAP_ARCHITECTURE_MODEL,
        steps_to_extrapolate_from,
        decoder_model=decoder_model,
    )
    return _get_extrapolated_graph_data(
        algorithm_implementation,
        estimator=dummy_extrapolation_estimator,
        transformers=transformers,
    )


def get_custom_extrapolated_estimate(
    algorithm_implementation: AlgorithmImplementation,
    estimator: ExtrapolationResourceEstimator,
    transformers,
) -> ExtrapolatedGraphResourceInfo:
    extrapolated_graph_data = _get_extrapolated_graph_data(
        algorithm_implementation, estimator, transformers
    )

    return estimator.estimate_given_extrapolation_data(
        algorithm_implementation,
        extrapolated_graph_data,
    )
