from copy import deepcopy

from ...data_structures import AlgorithmDescription, QuantumProgram
from .extrapolation_estimator import (
    ExtrapolatedResourceInfo,
    ExtrapolationResourceEstimator,
)


def run_custom_resource_estimation_pipeline(
    algorithm_description: AlgorithmDescription,
    estimator,
    transformers,
):
    program = algorithm_description.program
    for transformer in transformers:
        assert isinstance(algorithm_description.program, QuantumProgram)
        program = transformer(program)

    return estimator.estimate(algorithm_description)


def run_custom_extrapolation_pipeline(
    algorithm_description: AlgorithmDescription,
    estimator: ExtrapolationResourceEstimator,
    transformers,
) -> ExtrapolatedResourceInfo:
    small_programs_resource_info = []
    for i in estimator.steps_to_extrapolate_from:
        # create copy of program for each number of steps
        small_algorithm_description = deepcopy(algorithm_description)

        small_algorithm_description.error_budget.synthesis_failure_tolerance
        small_algorithm_description.program.n_rotation_gates

        for transformer in transformers:
            assert isinstance(small_algorithm_description.program, QuantumProgram)
            small_algorithm_description.program.steps = i
            small_algorithm_description.program = transformer(
                small_algorithm_description.program
            )

        resource_info = estimator.estimate(small_algorithm_description)
        small_programs_resource_info.append(resource_info)

    return estimator.estimate_via_extrapolation(
        algorithm_description,
        small_programs_resource_info,
    )
