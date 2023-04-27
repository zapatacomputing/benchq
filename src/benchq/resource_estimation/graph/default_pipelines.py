from typing import List, Optional

from ...compilation import get_algorithmic_graph_from_Jabalizer
from ...data_structures import AlgorithmDescription, DecoderModel
from ...data_structures.hardware_architecture_models import BasicArchitectureModel
from .customizable_pipelines import (
    run_custom_extrapolation_pipeline,
    run_custom_resource_estimation_pipeline,
)
from .extrapolation_estimator import ExtrapolationResourceEstimator
from .graph_estimator import GraphResourceEstimator
from .transformers import create_big_graph_from_subcircuits, synthesize_clifford_t


def run_estimate_using_graph_estimator_without_delayed_gate_synthesis(
    algorithm_description: AlgorithmDescription,
    hardware_model: BasicArchitectureModel,
    decoder_model: Optional[DecoderModel] = None,
):
    estimator = GraphResourceEstimator(hardware_model, decoder_model=decoder_model)

    return run_custom_resource_estimation_pipeline(
        algorithm_description,
        estimator,
        transformers=[
            synthesize_clifford_t(algorithm_description.error_budget),
            create_big_graph_from_subcircuits(delayed_gate_synthesis=False),
        ],
    )


def run_estimate_using_graph_estimator_with_delayed_gate_synthesis(
    algorithm_description: AlgorithmDescription,
    hardware_model: BasicArchitectureModel,
    decoder_model: Optional[DecoderModel] = None,
):
    estimator = GraphResourceEstimator(hardware_model, decoder_model=decoder_model)

    return run_custom_resource_estimation_pipeline(
        algorithm_description,
        estimator,
        transformers=[
            create_big_graph_from_subcircuits(
                delayed_gate_synthesis=True,
                graph_production_method=get_algorithmic_graph_from_Jabalizer,
            )
        ],
    )


def run_estimate_using_extrapolation_estimator_without_delayed_gate_synthesis(
    algorithm_description: AlgorithmDescription,
    hardware_model: BasicArchitectureModel,
    steps_to_extrapolate_from: List[int],
    decoder_model: Optional[DecoderModel] = None,
    n_measurement_steps_fit_type: str = "logarithmic",
):
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
            create_big_graph_from_subcircuits(delayed_gate_synthesis=False),
        ],
    )


def run_estimate_using_extrapolation_estimator_with_delayed_gate_synthesis(
    algorithm_description: AlgorithmDescription,
    hardware_model: BasicArchitectureModel,
    steps_to_extrapolate_from: List[int],
    decoder_model: Optional[DecoderModel] = None,
    n_measurement_steps_fit_type: str = "logarithmic",
):
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
                delayed_gate_synthesis=True,
                graph_production_method=get_algorithmic_graph_from_Jabalizer,
            )
        ],
    )
