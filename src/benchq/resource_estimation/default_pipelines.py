from functools import partial
from typing import Any, List, Optional

import numpy as np

from ..compilation import get_algorithmic_graph_from_ruby_slippers
from ..data_structures import (
    AlgorithmImplementation,
    DecoderModel,
    ExtrapolatedGraphResourceInfo,
    QuantumProgram,
    ResourceInfo,
)
from ..data_structures.hardware_architecture_models import BasicArchitectureModel
from .graph.customizable_pipelines import (
    run_custom_extrapolation_pipeline,
    run_custom_resource_estimation_pipeline,
)
from .graph.extrapolation_estimator import ExtrapolationResourceEstimator
from .graph.graph_estimator import GraphResourceEstimator
from .graph.transformers import (
    create_big_graph_from_subcircuits,
    synthesize_clifford_t,
    transpile_to_native_gates,
)
from .openfermion_re import get_physical_cost

LARGEST_GRAPH_TOLERANCE = 1e8
DEFAULT_STEPS_TO_EXTRAPOLATE_FROM = [1, 2, 3]


def run_precise_graph_estimate(
    algorithm_implementation: AlgorithmImplementation,
    hardware_model: BasicArchitectureModel,
    decoder_model: Optional[DecoderModel] = None,
) -> ResourceInfo:
    """Run a slow resource estimate with the lowest amount of resources.

    Run a resource estimate by creating a full graph of the full Clifford + T circuit
    that the algorithm implements and then running the resource estimator on that
    graph. This is the slowest way to run a resource estimate, but it is also the most
    accurate one and gives the least amount of resources needed to run the algorithm.

    Args:
        algorithm_implementation (AlgorithmImplementation): The algorithm to estimate
            resources for.
        hardware_model (BasicArchitectureModel): The hardware model to estimate
            resources for.
        decoder_model (Optional[DecoderModel], optional): The decoder model to
            run the algorithm with. Defaults to None and returns no estimate in
            that case.

    Returns:
        ResourceInfo: The resources required to run the algorithm.
    """
    estimator = GraphResourceEstimator(hardware_model, decoder_model=decoder_model)

    return run_custom_resource_estimation_pipeline(
        algorithm_implementation,
        estimator,
        transformers=[
            transpile_to_native_gates,
            synthesize_clifford_t(algorithm_implementation.error_budget),
            create_big_graph_from_subcircuits(),
        ],
    )


def run_fast_graph_estimate(
    algorithm_implementation: AlgorithmImplementation,
    hardware_model: BasicArchitectureModel,
    decoder_model: Optional[DecoderModel] = None,
) -> ResourceInfo:
    """Run a slow resource estimate that's faster than the precise one.

    Run a resource estimate by creating a full graph of the full circuit which is
    not decomposed into Clifford + T gates. This is faster than the precise graph
    estimate, but it gives a higher estimate of the resources needed to run the
    algorithm because the substrate scheduler is not allowed to optimize over the
    full circuit.

    Args:
        algorithm_implementation (AlgorithmImplementation): The algorithm to estimate
            resources for.
        hardware_model (BasicArchitectureModel): The hardware model to estimate
            resources for.
        decoder_model (Optional[DecoderModel], optional): The decoder model to
            run the algorithm with. Defaults to None and returns no estimate in
            that case.

    Returns:
        ResourceInfo: The resources required to run the algorithm.
    """
    estimator = GraphResourceEstimator(hardware_model, decoder_model=decoder_model)

    return run_custom_resource_estimation_pipeline(
        algorithm_implementation,
        estimator,
        transformers=[
            transpile_to_native_gates,
            create_big_graph_from_subcircuits(
                graph_production_method=get_algorithmic_graph_from_ruby_slippers,
            ),
        ],
    )


def run_precise_extrapolation_estimate(
    algorithm_implementation: AlgorithmImplementation,
    hardware_model: BasicArchitectureModel,
    steps_to_extrapolate_from: List[int],
    decoder_model: Optional[DecoderModel] = None,
    n_measurement_steps_fit_type: str = "logarithmic",
) -> ExtrapolatedGraphResourceInfo:
    """Run a faster resource estimate that's based on extrapolating from smaller
    circuits.

    Run a resource estimate by creating a part graph created by of the full
    Clifford + T circuit. This might be useful for some smaller problem instances
    and can give smaller resource estimates than the fast graph estimate.

    Args:
        algorithm_implementation (AlgorithmImplementation): The algorithm to estimate
            resources for.
        hardware_model (BasicArchitectureModel): The hardware model to estimate
            resources for.
        decoder_model (Optional[DecoderModel], optional): The decoder model to
            run the algorithm with. Defaults to None and returns no estimate in
            that case.

    Returns:
        ResourceInfo: The resources required to run the algorithm.
    """
    estimator = ExtrapolationResourceEstimator(
        hardware_model,
        steps_to_extrapolate_from,
        decoder_model=decoder_model,
        n_measurement_steps_fit_type=n_measurement_steps_fit_type,
    )

    return run_custom_extrapolation_pipeline(
        algorithm_implementation,
        estimator,
        transformers=[
            transpile_to_native_gates,
            synthesize_clifford_t(algorithm_implementation.error_budget),
            create_big_graph_from_subcircuits(),
        ],
    )


def run_fast_extrapolation_estimate(
    algorithm_implementation: AlgorithmImplementation,
    hardware_model: BasicArchitectureModel,
    steps_to_extrapolate_from: List[int],
    decoder_model: Optional[DecoderModel] = None,
    n_measurement_steps_fit_type: str = "logarithmic",
) -> ExtrapolatedGraphResourceInfo:
    """The fastest resource estimate method, but also the least accurate one.

    Run a resource estimate by creating a part graph created by of the full
    circuit with rotations not decomposed to Clifford + T. This gives us the
    furthest reach possible, but will likely overestimate the resources needed
    to run the algorithm.

    Args:
        algorithm_implementation (AlgorithmImplementation): The algorithm to estimate
            resources for.
        hardware_model (BasicArchitectureModel): The hardware model to estimate
            resources for.
        decoder_model (Optional[DecoderModel], optional): The decoder model to
            run the algorithm with. Defaults to None and returns no estimate in
            that case.

    Returns:
        ResourceInfo: The resources required to run the algorithm.
    """
    estimator = ExtrapolationResourceEstimator(
        hardware_model,
        steps_to_extrapolate_from,
        decoder_model=decoder_model,
        n_measurement_steps_fit_type=n_measurement_steps_fit_type,
    )

    return run_custom_extrapolation_pipeline(
        algorithm_implementation,
        estimator,
        transformers=[
            transpile_to_native_gates,
            create_big_graph_from_subcircuits(
                graph_production_method=get_algorithmic_graph_from_ruby_slippers,
            ),
        ],
    )


def run_footprint_analysis_pipeline(
    algorithm_implementation: AlgorithmImplementation,
    hardware_model: BasicArchitectureModel,
    decoder_model: Optional[DecoderModel] = None,
):
    dummy_estimator = GraphResourceEstimator(
        hardware_model, decoder_model=decoder_model
    )

    algorithm_implementation.program = transpile_to_native_gates(
        algorithm_implementation.program
    )

    total_t_gates = dummy_estimator.get_n_total_t_gates(
        algorithm_implementation.program.n_t_gates,
        algorithm_implementation.program.n_rotation_gates,
        algorithm_implementation.error_budget.transpilation_failure_tolerance,
    )

    hardware_failure_tolerance = (
        algorithm_implementation.error_budget.hardware_failure_tolerance
    )

    return get_physical_cost(
        algorithm_implementation.program.num_data_qubits,
        num_t=total_t_gates,
        architecture_model=hardware_model,
        hardware_failure_tolerance=hardware_failure_tolerance,
        decoder_model=decoder_model,
    )


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
