from copy import deepcopy
from dataclasses import replace
from typing import List

from ...data_structures import (
    AlgorithmImplementation,
    ExtrapolatedGraphData,
    ExtrapolatedGraphResourceInfo,
    QuantumProgram,
)
from ...data_structures.hardware_architecture_models import (
    BASIC_ION_TRAP_ARCHITECTURE_MODEL,
)
from .extrapolation_estimator import ExtrapolationResourceEstimator
from .graph_estimator import GraphData, GraphPartition


def run_custom_resource_estimation_pipeline(
    algorithm_description: AlgorithmImplementation,
    estimator,
    transformers,
):
    for transformer in transformers:
        # all transformers give back QuantumPrograms except the last one
        assert isinstance(algorithm_description.program, QuantumProgram)
        algorithm_description = replace(
            algorithm_description, program=transformer(algorithm_description.program)
        )

    return estimator.estimate(algorithm_description)


def _create_extrapolated_graph_data(
    algorithm_description: AlgorithmImplementation,
    estimator: ExtrapolationResourceEstimator,
    transformers,
) -> ExtrapolatedGraphData:
    synthesis_accuracy_for_each_rotation = 1 - (
        1 - algorithm_description.error_budget.transpilation_failure_tolerance
    ) ** (1 / algorithm_description.program.n_rotation_gates)

    small_programs_graph_data: List[GraphData] = []
    for i in estimator.steps_to_extrapolate_from:
        # create copy of program for each number of steps
        small_algorithm_description = deepcopy(algorithm_description)
        small_algorithm_description.error_budget = replace(
            algorithm_description.error_budget,
            transpilation_failure_tolerance=synthesis_accuracy_for_each_rotation
            * small_algorithm_description.program.n_rotation_gates,
        )

        for transformer in transformers:
            # all transformers give back QuantumPrograms except the last one
            assert isinstance(small_algorithm_description.program, QuantumProgram)
            small_algorithm_description.program.steps = i
            small_algorithm_description.program = transformer(
                small_algorithm_description.program
            )

        assert isinstance(small_algorithm_description.program, GraphPartition)
        graph_data = estimator._get_graph_data_for_single_graph(
            small_algorithm_description.program
        )
        small_programs_graph_data.append(graph_data)

    # get rid of graph compilation step
    for transformer in transformers[:-1]:
        algorithm_description = replace(
            algorithm_description, program=transformer(algorithm_description.program)
        )

    return estimator.get_extrapolated_graph_data(
        small_programs_graph_data, algorithm_description.program
    )


def create_extrapolated_graph_data_pipeline(
    algorithm_description: AlgorithmImplementation,
    steps_to_extrapolate_from,
    decoder_model,
    transformers,
):
    # the architecture model doesn't matter for extrapolating graph data
    dummy_extrapolation_estimator = ExtrapolationResourceEstimator(
        BASIC_ION_TRAP_ARCHITECTURE_MODEL(),
        steps_to_extrapolate_from,
        decoder_model=decoder_model,
    )
    return _create_extrapolated_graph_data(
        algorithm_description,
        estimator=dummy_extrapolation_estimator,
        transformers=transformers,
    )


def run_custom_extrapolation_pipeline(
    algorithm_description: AlgorithmImplementation,
    estimator: ExtrapolationResourceEstimator,
    transformers,
) -> ExtrapolatedGraphResourceInfo:
    extrapolated_graph_data = _create_extrapolated_graph_data(
        algorithm_description, estimator, transformers
    )

    return estimator.estimate_given_extrapolation_data(
        algorithm_description,
        extrapolated_graph_data,
    )
