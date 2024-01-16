from functools import partial
from typing import List, Optional

import numpy as np

from ..algorithms.data_structures import AlgorithmImplementation
from ..compilation import get_algorithmic_graph_from_ruby_slippers
from ..decoder_modeling import DecoderModel
from ..problem_embeddings.quantum_program import QuantumProgram
from ..quantum_hardware_modeling.hardware_architecture_models import (
    BasicArchitectureModel,
)
from .footprint_estimators.openfermion_estimator import footprint_estimator
from .graph_estimators.customizable_pipelines import (
    get_custom_extrapolated_estimate,
    get_custom_resource_estimation,
)
from .graph_estimators.extrapolation_estimator import ExtrapolationResourceEstimator
from .graph_estimators.graph_estimator import GraphResourceEstimator
from .graph_estimators.transformers import (
    create_big_graph_from_subcircuits,
    synthesize_clifford_t,
    transpile_to_native_gates,
)
from .resource_info import ExtrapolatedGraphResourceInfo, ResourceInfo

DEFAULT_STEPS_TO_EXTRAPOLATE_FROM = [1, 2, 3]


def get_precise_graph_estimate(
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

    return get_custom_resource_estimation(
        algorithm_implementation,
        estimator,
        transformers=[
            transpile_to_native_gates,
            synthesize_clifford_t(algorithm_implementation.error_budget),
            create_big_graph_from_subcircuits(),
        ],
    )


def get_fast_graph_estimate(
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

    return get_custom_resource_estimation(
        algorithm_implementation,
        estimator,
        transformers=[
            transpile_to_native_gates,
            create_big_graph_from_subcircuits(
                graph_production_method=get_algorithmic_graph_from_ruby_slippers,
            ),
        ],
    )


def get_precise_extrapolation_estimate(
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

    return get_custom_extrapolated_estimate(
        algorithm_implementation,
        estimator,
        transformers=[
            transpile_to_native_gates,
            synthesize_clifford_t(algorithm_implementation.error_budget),
            create_big_graph_from_subcircuits(),
        ],
    )


def get_fast_extrapolation_estimate(
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

    return get_custom_extrapolated_estimate(
        algorithm_implementation,
        estimator,
        transformers=[
            transpile_to_native_gates,
            create_big_graph_from_subcircuits(
                graph_production_method=get_algorithmic_graph_from_ruby_slippers,
            ),
        ],
    )


def get_footprint_estimate(
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

    return footprint_estimator(
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

    Currently, chooses between GraphResourceEstimator and
    ExtrapolationResourceEstimator and whether to use delayed gate synthesis
    in the following order:
        1. GraphResourceEstimator without delayed gate synthesis
        2. ExtrapolationResourceEstimator without delayed gate synthesis
        3. GraphResourceEstimator with delayed gate synthesis
        4. ExtrapolationResourceEstimator with delayed gate synthesis
        5. Footprint estimator as a last-ditch effort

    Decision is based on graph complexity, which is roughly the number
    of remove_sqs operations one needs to do. Check out Ruby slippers compiler
    for more details on remove_sqs.

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
    assert isinstance(algorithm_implementation.program, QuantumProgram)
    initial_number_of_steps = algorithm_implementation.program.steps

    graph_size = estimate_full_graph_size(algorithm_implementation, False)
    reduced_graph_size = estimate_full_graph_size(algorithm_implementation, True)

    # Changing number of steps impacts estimated graph size for extrapolation
    algorithm_implementation.program.steps = max(DEFAULT_STEPS_TO_EXTRAPOLATE_FROM)

    extrapolaed_graph_size = estimate_full_graph_size(algorithm_implementation, False)
    small_extrapolated_graph_size = estimate_full_graph_size(
        algorithm_implementation, True
    )

    algorithm_implementation.program.steps = initial_number_of_steps

    if graph_size < 1e7:
        pipeline = get_precise_graph_estimate
        print("Using precise graph estimator")
    elif extrapolaed_graph_size < 1e7:
        pipeline = partial(
            get_precise_extrapolation_estimate,
            steps_to_extrapolate_from=DEFAULT_STEPS_TO_EXTRAPOLATE_FROM,
        )
        print("Using precise extrapolation graph estimator")
    elif reduced_graph_size < 1e7:
        pipeline = get_fast_graph_estimate
        print("Using fast graph estimator")
    elif small_extrapolated_graph_size < 1e7:
        pipeline = partial(
            get_fast_extrapolation_estimate,
            steps_to_extrapolate_from=DEFAULT_STEPS_TO_EXTRAPOLATE_FROM,
        )
        print("Using fast extrapolation graph estimator")
    else:
        pipeline = get_footprint_estimate
        print("Using footprint analysis estimator")

    return pipeline(
        algorithm_implementation,
        hardware_model,
        decoder_model=decoder_model,
    )


def estimate_full_graph_size(
    algorithm_implementation: AlgorithmImplementation, delayed_gate_synthesis=False
) -> int:
    graph_complexity = (
        algorithm_implementation.program.n_t_gates
        + algorithm_implementation.program.n_c_gates * 2
    )

    if not delayed_gate_synthesis:
        graph_complexity += (
            algorithm_implementation.program.n_rotation_gates
            * GraphResourceEstimator.SYNTHESIS_SCALING
            * np.log2(
                1
                / algorithm_implementation.error_budget.transpilation_failure_tolerance
            )
        )
    else:
        graph_complexity += algorithm_implementation.program.n_rotation_gates

    return graph_complexity
