from copy import deepcopy
from dataclasses import replace
from typing import List

from ...data_structures import (
    AlgorithmImplementation,
    ExtrapolatedGraphResourceInfo,
    QuantumProgram,
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


def run_custom_extrapolation_pipeline(
    algorithm_description: AlgorithmImplementation,
    estimator: ExtrapolationResourceEstimator,
    transformers,
) -> ExtrapolatedGraphResourceInfo:
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

    return estimator.estimate_via_extrapolation(
        algorithm_description,
        small_programs_graph_data,
    )
