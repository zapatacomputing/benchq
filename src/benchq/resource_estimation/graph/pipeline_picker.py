from functools import partial
from typing import Any, Optional

import numpy as np

from ...data_structures import AlgorithmDescription, DecoderModel, QuantumProgram
from ...data_structures.hardware_architecture_models import BasicArchitectureModel
from .default_pipelines import (
    run_estimate_using_extrapolation_estimator_with_delayed_gate_synthesis,
    run_estimate_using_extrapolation_estimator_without_delayed_gate_synthesis,
    run_estimate_using_graph_estimator_with_delayed_gate_synthesis,
    run_estimate_using_graph_estimator_without_delayed_gate_synthesis,
)
from .graph_estimator import GraphResourceEstimator

LARGEST_GRAPH_TOLERANCE = 1e8
DEFAULT_STEPS_TO_EXTRAPOLATE_FROM = [1, 2, 3]


def automatic_resource_estimator(
    algorithm_description: AlgorithmDescription,
    hardware_model: BasicArchitectureModel,
    decoder_model: Optional[DecoderModel] = None,
):
    return pick_pipeline_by_program_proportions(
        algorithm_description, hardware_model, decoder_model
    )


def pick_pipeline_by_program_proportions(
    algorithm_description: AlgorithmDescription,
    hardware_model: BasicArchitectureModel,
    decoder_model: Optional[DecoderModel] = None,
):
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
    assert isinstance(algorithm_description.program, QuantumProgram)

    prev_steps = algorithm_description.program.steps
    algorithm_description.program.steps = max(DEFAULT_STEPS_TO_EXTRAPOLATE_FROM)
    if estimate_full_graph_size(algorithm_description, True) < LARGEST_GRAPH_TOLERANCE:
        pipeline = partial(
            run_estimate_using_extrapolation_estimator_with_delayed_gate_synthesis,
            steps_to_extrapolate_from=DEFAULT_STEPS_TO_EXTRAPOLATE_FROM,
        )
    elif (
        estimate_full_graph_size(algorithm_description, False) < LARGEST_GRAPH_TOLERANCE
    ):
        pipeline = partial(
            run_estimate_using_extrapolation_estimator_without_delayed_gate_synthesis,
            steps_to_extrapolate_from=DEFAULT_STEPS_TO_EXTRAPOLATE_FROM,
        )

    algorithm_description.program.steps = prev_steps
    if estimate_full_graph_size(algorithm_description, True) < LARGEST_GRAPH_TOLERANCE:
        pipeline = run_estimate_using_graph_estimator_with_delayed_gate_synthesis
    if estimate_full_graph_size(algorithm_description, False) < LARGEST_GRAPH_TOLERANCE:
        pipeline = run_estimate_using_graph_estimator_without_delayed_gate_synthesis

    if pipeline is not None:
        return pipeline(
            algorithm_description,
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
    algorithm_description: AlgorithmDescription, delayed_gate_synthesis=False
):
    full_graph_size = algorithm_description.program.n_t_gates

    if not delayed_gate_synthesis:
        full_graph_size += (
            algorithm_description.program.n_rotation_gates
            * GraphResourceEstimator.SYNTHESIS_SCALING
            * np.log2(
                1 / algorithm_description.error_budget.synthesis_failure_tolerance
            )
        )
    else:
        full_graph_size += algorithm_description.program.n_rotation_gates

    return full_graph_size
