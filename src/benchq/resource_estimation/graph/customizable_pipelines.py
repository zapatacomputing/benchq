from copy import copy
from dataclasses import replace

from ...data_structures import AlgorithmImplementation, QuantumProgram
from .extrapolation_estimator import (
    ExtrapolatedResourceInfo,
    ExtrapolationResourceEstimator,
)


def run_custom_resource_estimation_pipeline(
    algorithm_description: AlgorithmImplementation,
    estimator,
    transformers,
):
    internal_algorthm_description = copy(algorithm_description)

    for transformer in transformers:
        # all transformers give back QuantumPrograms except the last one
        assert isinstance(internal_algorthm_description.program, QuantumProgram)
        internal_algorthm_description.program = transformer(
            internal_algorthm_description.program
        )

    return estimator.estimate(internal_algorthm_description)


def run_custom_extrapolation_pipeline(
    algorithm_description: AlgorithmImplementation,
    estimator: ExtrapolationResourceEstimator,
    transformers,
) -> ExtrapolatedResourceInfo:
    synthesis_accuracy_for_each_rotation = 1 - (
        1 - algorithm_description.error_budget.synthesis_failure_tolerance
    ) ** (1 / algorithm_description.program.n_rotation_gates)

    internal_algorthm_description = copy(algorithm_description)

    small_programs_resource_info = []
    for i in estimator.steps_to_extrapolate_from:
        # create copy of program for each number of steps
        small_algorithm_description = copy(algorithm_description)
        small_algorithm_description.error_budget = replace(
            algorithm_description.error_budget,
            synthesis_failure_tolerance=synthesis_accuracy_for_each_rotation
            * small_algorithm_description.program.n_rotation_gates,
        )

        for transformer in transformers:
            # all transformers give back QuantumPrograms except the last one
            assert isinstance(small_algorithm_description.program, QuantumProgram)
            small_algorithm_description.program.steps = i
            small_algorithm_description.program = transformer(
                small_algorithm_description.program
            )

        resource_info = estimator.estimate(small_algorithm_description)
        small_programs_resource_info.append(resource_info)

    # get rid of graph compilation step
    for transformer in transformers[:-1]:
        internal_algorthm_description.program = transformer(
            internal_algorthm_description.program
        )

    return estimator.estimate_via_extrapolation(
        internal_algorthm_description,
        small_programs_resource_info,
    )
