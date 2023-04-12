from copy import deepcopy

from ...data_structures import QuantumProgram
from .extrapolation_estimator import ExtrapolationResourceEstimator


def run_resource_estimation_pipeline(
    program,
    error_budget,
    estimator,
    transformers,
):
    for transformer in transformers:
        program = transformer(program)
    return estimator.estimate(program, error_budget)


def run_extrapolation_pipeline(
    program: QuantumProgram,
    error_budget,
    estimator: ExtrapolationResourceEstimator,
    transformers,
):
    small_programs_resource_info = []
    for i in estimator.steps_to_extrapolate_from:
        # create copy of program for each number of steps
        small_program = deepcopy(program)
        small_program.steps = i

        for transformer in transformers:
            small_program = transformer(small_program)
        resource_info = estimator.estimate(small_program, error_budget)
        small_programs_resource_info.append(resource_info)

    return estimator.estimate_via_extrapolation(
        small_programs_resource_info,
        error_budget,
        small_program.delayed_gate_synthesis,
        program.steps,
    )
