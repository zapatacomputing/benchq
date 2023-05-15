from typing import List, Optional

from ...compilation import get_algorithmic_graph_from_Jabalizer
from ...data_structures import (
    AlgorithmImplementation,
    DecoderModel,
    ExtrapolatedGraphResourceInfo,
    ResourceInfo,
)
from ...data_structures.hardware_architecture_models import BasicArchitectureModel
from .customizable_pipelines import (
    run_custom_extrapolation_pipeline,
    run_custom_resource_estimation_pipeline,
)
from .extrapolation_estimator import ExtrapolationResourceEstimator
from .graph_estimator import GraphResourceEstimator
from .transformers import create_big_graph_from_subcircuits, synthesize_clifford_t


def run_precise_graph_estimate(
    algorithm_description: AlgorithmImplementation,
    hardware_model: BasicArchitectureModel,
    decoder_model: Optional[DecoderModel] = None,
) -> ResourceInfo:
    """Run a slow resource estimate with the lowest amount of resources.

    Run a resource estimate by creating a full graph of the full Clifford + T circuit
    that the algorithm implements and then running the resource estimator on that
    graph. This is the slowest way to run a resource estimate, but it is also the most
    accurate one and gives the least amount of resources needed to run the algorithm.

    Args:
        algorithm_description (AlgorithmImplementation): The algorithm to estimate
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
        algorithm_description,
        estimator,
        transformers=[
            synthesize_clifford_t(algorithm_description.error_budget),
            create_big_graph_from_subcircuits(),
        ],
    )


def run_fast_graph_estimate(
    algorithm_description: AlgorithmImplementation,
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
        algorithm_description (AlgorithmImplementation): The algorithm to estimate
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
        algorithm_description,
        estimator,
        transformers=[
            create_big_graph_from_subcircuits(
                graph_production_method=get_algorithmic_graph_from_Jabalizer,
            )
        ],
    )


def run_precise_extrapolation_estimate(
    algorithm_description: AlgorithmImplementation,
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
        algorithm_description (AlgorithmImplementation): The algorithm to estimate
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
        algorithm_description,
        estimator,
        transformers=[
            synthesize_clifford_t(algorithm_description.error_budget),
            create_big_graph_from_subcircuits(),
        ],
    )


def run_fast_extrapolation_estimate(
    algorithm_description: AlgorithmImplementation,
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
        algorithm_description (AlgorithmImplementation): The algorithm to estimate
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
        algorithm_description,
        estimator,
        transformers=[
            create_big_graph_from_subcircuits(
                graph_production_method=get_algorithmic_graph_from_Jabalizer,
            )
        ],
    )
