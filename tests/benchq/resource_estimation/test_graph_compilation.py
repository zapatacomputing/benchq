from dataclasses import asdict

import numpy as np
import pytest
from orquestra.quantum.circuits import CNOT, RX, RY, RZ, Circuit, H, T

from benchq.data_structures.hardware_architecture_models import BasicArchitectureModel
from benchq.data_structures.quantum_program import QuantumProgram
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_resource_estimation_pipeline,
    simplify_rotations,
    synthesize_clifford_t,
)


@pytest.fixture(params=[True, False])
def use_synthesis(request):
    return request.param


def _get_transformers(use_synthesis, error_budget):
    if use_synthesis:
        transformers = [
            synthesize_clifford_t(error_budget),
            create_big_graph_from_subcircuits(synthesized=use_synthesis),
        ]
    else:
        transformers = [
            simplify_rotations,
            create_big_graph_from_subcircuits(synthesized=use_synthesis),
        ]
    return transformers


@pytest.mark.parametrize(
    "quantum_program,expected_results",
    [
        (
            QuantumProgram(
                [Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])], 1, lambda x: [0]
            ),
            {"n_measurement_steps": 3, "n_nodes": 3, "max_graph_degree": 2},
        ),
        # (
        #     QuantumProgram(
        #         [Circuit([RX(np.pi / 4)(0), RY(np.pi / 4)(0), CNOT(0, 1)])],
        #         1,
        #         lambda _: [0],
        #     ),
        #     {"n_measurement_steps": 3, "n_nodes": 4, "max_graph_degree": 2},
        # ),
        (
            QuantumProgram(
                [Circuit([H(0)] + [CNOT(i, i + 1) for i in range(3)])],
                1,
                lambda _: [0],
            ),
            {"n_measurement_steps": 4, "n_nodes": 4, "max_graph_degree": 3},
        ),
        (
            QuantumProgram(
                [Circuit([H(0)] + [CNOT(i, i + 1) for i in range(3)] + [T(1), T(2)])],
                1,
                lambda _: [0],
            ),
            {"n_measurement_steps": 6, "n_nodes": 6, "max_graph_degree": 5},
        ),
        # (
        #     QuantumProgram(
        #         [Circuit([H(0), T(0), CNOT(0, 1), T(2), CNOT(2, 3)])],
        #         1,
        #         lambda _: [0],
        #     ),
        #     {"n_measurement_steps": 3, "n_nodes": 3, "max_graph_degree": 2},
        # ),
    ],
)
def test_get_resource_estimations_for_program_gives_correct_results(
    quantum_program, expected_results, use_synthesis
):
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
    error_budget = {
        "qsp_required_precision": 1e-3,
        "tolerable_circuit_error_rate": 1e-2,
        "total_error": 1e-2,
        "synthesis_error_rate": 0.5,
        "ec_error_rate": 0.5,
    }
    transformers = _get_transformers(use_synthesis, error_budget)
    gsc_resource_estimates = run_resource_estimation_pipeline(
        quantum_program,
        error_budget,
        estimator=GraphResourceEstimator(architecture_model),
        transformers=transformers,
    )

    for key in expected_results.keys():
        assert asdict(gsc_resource_estimates)[key] == expected_results[key]

    # Note that error_budget is a bound for the sum of the gate synthesis error and
    # logical error. Therefore the expression below is a loose upper bound for the
    # logical error rate.
    assert (
        asdict(gsc_resource_estimates)["logical_error_rate"]
        < error_budget["tolerable_circuit_error_rate"]
    )


def test_better_architecture_does_not_require_more_resources(use_synthesis):
    low_noise_architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-4,
        physical_gate_time_in_seconds=1e-6,
    )
    high_noise_architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
    error_budget = {
        "qsp_required_precision": 1e-3,
        "tolerable_circuit_error_rate": 1e-2,
        "total_error": 1e-2,
        "synthesis_error_rate": 0.5,
        "ec_error_rate": 0.5,
    }
    transformers = _get_transformers(use_synthesis, error_budget)

    circuit = Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    quantum_program = QuantumProgram(
        subroutines=[circuit], steps=1, calculate_subroutine_sequence=lambda x: [0]
    )
    low_noise_resource_estimates = run_resource_estimation_pipeline(
        quantum_program,
        error_budget,
        estimator=GraphResourceEstimator(low_noise_architecture_model),
        transformers=transformers,
    )

    high_noise_resource_estimates = run_resource_estimation_pipeline(
        quantum_program,
        error_budget,
        estimator=GraphResourceEstimator(high_noise_architecture_model),
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


def test_higher_error_budget_does_not_require_more_resources(use_synthesis):
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
    low_failure_rate = 1e-3
    high_failure_rate = 1e-2

    low_error_budget = {
        "qsp_required_precision": 1e-3,
        "tolerable_circuit_error_rate": low_failure_rate,
        "total_error": low_failure_rate,
        "synthesis_error_rate": 0.5,
        "ec_error_rate": 0.5,
    }
    high_error_budget = {
        "qsp_required_precision": 1e-3,
        "tolerable_circuit_error_rate": high_failure_rate,
        "total_error": high_failure_rate,
        "synthesis_error_rate": 0.5,
        "ec_error_rate": 0.5,
    }
    low_error_transformers = _get_transformers(use_synthesis, low_error_budget)
    high_error_transformers = _get_transformers(use_synthesis, high_error_budget)

    circuit = Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    quantum_program = QuantumProgram(
        subroutines=[circuit], steps=1, calculate_subroutine_sequence=lambda x: [0]
    )
    low_error_resource_estimates = run_resource_estimation_pipeline(
        quantum_program,
        low_error_budget,
        estimator=GraphResourceEstimator(architecture_model),
        transformers=low_error_transformers,
    )

    high_error_resource_estimates = run_resource_estimation_pipeline(
        quantum_program,
        high_error_budget,
        estimator=GraphResourceEstimator(architecture_model),
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
