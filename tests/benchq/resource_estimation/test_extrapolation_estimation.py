import numpy as np
import pytest
from orquestra.quantum.circuits import CNOT, RZ, Circuit, H

from benchq.data_structures import ErrorBudget, QuantumProgram
from benchq.data_structures.hardware_architecture_models import BasicArchitectureModel
from benchq.resource_estimation.graph import (
    ExtrapolationResourceEstimator,
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_custom_extrapolation_pipeline,
    run_custom_resource_estimation_pipeline,
    simplify_rotations,
    synthesize_clifford_t,
)
from benchq.vizualization_tools import plot_extrapolations


@pytest.fixture(params=[False, True])
def use_delayed_gate_synthesis(request):
    return request.param


def _get_transformers(use_delayed_gate_synthesis, error_budget):
    if not use_delayed_gate_synthesis:
        transformers = [
            synthesize_clifford_t(error_budget),
            create_big_graph_from_subcircuits(
                delayed_gate_synthesis=use_delayed_gate_synthesis,
            ),
        ]
    else:
        transformers = [
            simplify_rotations,
            create_big_graph_from_subcircuits(
                delayed_gate_synthesis=use_delayed_gate_synthesis,
            ),
        ]
    return transformers


@pytest.mark.parametrize(
    "quantum_program,steps_to_extrapolate_from,n_measurement_steps_fit_type",
    [
        (
            QuantumProgram(
                [
                    Circuit([H(0), RZ(np.pi / 14)(0), CNOT(0, 1)]),
                    Circuit([H(0), H(1), RZ(np.pi / 14)(0)]),
                ],
                5,
                lambda x: [0] + [1] * x + [0],
            ),
            [1, 2, 3, 4],
            "logarithmic",
        ),
        (
            QuantumProgram(
                [
                    Circuit([H(0), RZ(np.pi / 14)(0), CNOT(0, 1)]),
                    Circuit([H(0), H(1), RZ(np.pi / 14)(0)]),
                ],
                1000,
                lambda x: [0] + [1] * x + [0],
            ),
            [1, 2, 3, 5],
            "logarithmic",
        ),
        (
            QuantumProgram(
                [
                    Circuit([H(0), RZ(np.pi / 14)(0), CNOT(0, 1)]),
                    Circuit([H(0), H(1), RZ(np.pi / 14)(0)]),
                    Circuit([H(0), H(1), CNOT(0, 1)]),
                ],
                100,
                lambda x: [0] + [1, 2] * x + [0],
            ),
            [1, 2, 3, 5, 7, 10, 15, 25],
            "linear",
        ),
    ],
)
def test_get_resource_estimations_for_program_gives_correct_results(
    quantum_program,
    steps_to_extrapolate_from,
    use_delayed_gate_synthesis,
    n_measurement_steps_fit_type,
):
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
    error_budget = ErrorBudget(
        ultimate_failure_tolerance=1e-2, circuit_generation_weight=0
    )
    transformers = _get_transformers(use_delayed_gate_synthesis, error_budget)

    extrapolated_resource_estimates = run_custom_extrapolation_pipeline(
        quantum_program,
        error_budget,
        estimator=ExtrapolationResourceEstimator(
            architecture_model,
            steps_to_extrapolate_from,
            n_measurement_steps_fit_type=n_measurement_steps_fit_type,
        ),
        transformers=transformers,
    )
    gsc_resource_estimates = run_custom_resource_estimation_pipeline(
        quantum_program,
        error_budget,
        estimator=GraphResourceEstimator(architecture_model),
        transformers=transformers,
    )

    attributes_to_compare_harshly = [
        "n_nodes",
        "synthesis_multiplier",
        "total_time",
        "n_physical_qubits",
    ]
    for attribute in attributes_to_compare_harshly:
        assert np.isclose(
            getattr(extrapolated_resource_estimates, attribute),
            getattr(gsc_resource_estimates, attribute),
            rtol=1e-2,
        )
    # assert that the number of measurement steps grows with the steps
    attributes_to_compare_loosely = [
        "n_logical_qubits",
        "code_distance",
        "n_measurement_steps",
    ]
    for attribute in attributes_to_compare_loosely:
        assert (
            getattr(extrapolated_resource_estimates, attribute)
            - getattr(
                extrapolated_resource_estimates.data_used_to_extrapolate[-1], attribute
            )
            > -3  # allow for fits that might be a bit off
        )


def test_better_architecture_does_not_require_more_resources(
    use_delayed_gate_synthesis,
):
    low_noise_architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-4,
        physical_gate_time_in_seconds=1e-6,
    )
    high_noise_architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
    error_budget = ErrorBudget(
        ultimate_failure_tolerance=1e-2, circuit_generation_weight=0
    )
    transformers = _get_transformers(use_delayed_gate_synthesis, error_budget)

    circuit = Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    quantum_program = QuantumProgram(
        subroutines=[circuit],
        steps=100,
        calculate_subroutine_sequence=lambda x: [0] * x,
    )
    low_noise_resource_estimates = run_custom_extrapolation_pipeline(
        quantum_program,
        error_budget,
        estimator=ExtrapolationResourceEstimator(
            low_noise_architecture_model, [1, 2, 3, 4]
        ),
        transformers=transformers,
    )

    high_noise_resource_estimates = run_custom_extrapolation_pipeline(
        quantum_program,
        error_budget,
        estimator=ExtrapolationResourceEstimator(
            high_noise_architecture_model, [1, 2, 3, 4]
        ),
        transformers=transformers,
    )

    assert (
        low_noise_resource_estimates.n_physical_qubits
        <= high_noise_resource_estimates.n_physical_qubits
    )
    assert (
        low_noise_resource_estimates.code_distance
        <= high_noise_resource_estimates.code_distance
    )
    assert (
        low_noise_resource_estimates.total_time
        <= high_noise_resource_estimates.total_time
    )


def test_higher_error_budget_does_not_require_more_resources(
    use_delayed_gate_synthesis,
):
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
    low_failure_tolerance = 1e-3
    high_failure_tolerance = 1e-2

    low_error_budget = ErrorBudget(
        ultimate_failure_tolerance=low_failure_tolerance, circuit_generation_weight=0
    )
    high_error_budget = ErrorBudget(
        ultimate_failure_tolerance=high_failure_tolerance, circuit_generation_weight=0
    )
    low_error_transformers = _get_transformers(
        use_delayed_gate_synthesis, low_error_budget
    )
    high_error_transformers = _get_transformers(
        use_delayed_gate_synthesis, high_error_budget
    )

    circuit = Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    quantum_program = QuantumProgram(
        subroutines=[circuit],
        steps=100,
        calculate_subroutine_sequence=lambda x: [0] * x,
    )
    low_error_resource_estimates = run_custom_extrapolation_pipeline(
        quantum_program,
        low_error_budget,
        estimator=ExtrapolationResourceEstimator(architecture_model, [1, 2, 3, 4]),
        transformers=low_error_transformers,
    )

    high_error_resource_estimates = run_custom_extrapolation_pipeline(
        quantum_program,
        high_error_budget,
        estimator=ExtrapolationResourceEstimator(architecture_model, [1, 2, 3, 4]),
        transformers=high_error_transformers,
    )

    assert (
        high_error_resource_estimates.n_physical_qubits
        <= low_error_resource_estimates.n_physical_qubits
    )
    assert (
        high_error_resource_estimates.code_distance
        <= low_error_resource_estimates.code_distance
    )
    assert (
        high_error_resource_estimates.total_time
        <= low_error_resource_estimates.total_time
    )
