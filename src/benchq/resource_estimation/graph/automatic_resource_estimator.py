# WARNING! This feature is still in development and is untested. Use at your own risk.

from functools import partial
from typing import Any, Optional

import numpy as np

from ...data_structures import (
    AlgorithmImplementation,
    DecoderModel,
    QuantumProgram,
    ResourceInfo,
)
from ...data_structures.hardware_architecture_models import BasicArchitectureModel
from .default_pipelines import (
    run_fast_extrapolation_estimate,
    run_fast_graph_estimate,
    run_precise_extrapolation_estimate,
    run_precise_graph_estimate,
)
from .graph_estimator import GraphResourceEstimator

LARGEST_GRAPH_TOLERANCE = 1e8
DEFAULT_STEPS_TO_EXTRAPOLATE_FROM = [1, 2, 3]


def automatic_resource_estimator(
    algorithm_implementation: AlgorithmImplementation,
    hardware_model: BasicArchitectureModel,
    decoder_model: Optional[DecoderModel] = None,
) -> ResourceInfo:
    """Pick the appropriate resource estimator based on the size of the program.

    Currently chooses between GraphResourceEstimator and
    ExtrapolationResourceEstimator and whether or not to use delayed gate synthesis
    in the following order:
        1. GraphResourceEstimator without delayed gate synthesis
        2. GraphResourceEstimator with delayed gate synthesis
        3. ExtrapolationResourceEstimator without delayed gate synthesis
        4. ExtrapolationResourceEstimator with delayed gate synthesis


    Args:
        program (QuantumProgram): program to estimate resources for
        error_budget (ErrorBudget): budget for the error the program can tolerate
        delayed_gate_synthesis (bool, optional): whether or not to decompose.
            The gates into clifford + T before creating graph. Defaults to False.

    Raises:
        ValueError: if the problem is too big to estimate resources for

    Returns:
        GraphResourceEstimator: an appropriate resource estimator for the problem
    """
    pipeline: Any = None
    assert isinstance(algorithm_implementation.program, QuantumProgram)

    prev_steps = algorithm_implementation.program.steps
    algorithm_implementation.program.steps = max(DEFAULT_STEPS_TO_EXTRAPOLATE_FROM)
    if (
        estimate_full_graph_size(algorithm_implementation, True)
        < LARGEST_GRAPH_TOLERANCE
    ):
        pipeline = partial(
            run_fast_extrapolation_estimate,
            steps_to_extrapolate_from=DEFAULT_STEPS_TO_EXTRAPOLATE_FROM,
        )
    elif (
        estimate_full_graph_size(algorithm_implementation, False)
        < LARGEST_GRAPH_TOLERANCE
    ):
        pipeline = partial(
            run_precise_extrapolation_estimate,
            steps_to_extrapolate_from=DEFAULT_STEPS_TO_EXTRAPOLATE_FROM,
        )

    algorithm_implementation.program.steps = prev_steps
    if (
        estimate_full_graph_size(algorithm_implementation, True)
        < LARGEST_GRAPH_TOLERANCE
    ):
        pipeline = run_fast_graph_estimate
    if (
        estimate_full_graph_size(algorithm_implementation, False)
        < LARGEST_GRAPH_TOLERANCE
    ):
        pipeline = run_precise_graph_estimate

    if pipeline is not None:
        return pipeline(
            algorithm_implementation,
            hardware_model,
            decoder_model=decoder_model,
        )
    else:
        raise ValueError(
            "Problem size too large for resource estimation. "
            "Try reducing the size of each of your steps in the program. "
            "If you are creating a program from a circuit, consider breaking "
            "the program up into steps."
        )


def estimate_full_graph_size(
    algorithm_implementation: AlgorithmImplementation, delayed_gate_synthesis=False
) -> int:
    full_graph_size = algorithm_implementation.program.n_t_gates

    if not delayed_gate_synthesis:
        full_graph_size += (
            algorithm_implementation.program.n_rotation_gates
            * GraphResourceEstimator.SYNTHESIS_SCALING
            * np.log2(
                1
                / algorithm_implementation.error_budget.transpilation_failure_tolerance
            )
        )
    else:
        full_graph_size += algorithm_implementation.program.n_rotation_gates

    return full_graph_size
