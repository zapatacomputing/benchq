import os
from dataclasses import asdict

import numpy as np
import pytest
from orquestra.quantum.circuits import CNOT, RX, RY, RZ, Circuit, H, T

from benchq.data_structures import (
    AlgorithmImplementation,
    BasicArchitectureModel,
    DecoderModel,
    ErrorBudget,
    QuantumProgram,
    get_program_from_circuit,
)
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_custom_resource_estimation_pipeline,
    simplify_rotations,
    synthesize_clifford_t,
)


@pytest.fixture(params=[True, False])
def use_delayed_gate_synthesis(request):
    return request.param


def _get_transformers(use_delayed_gate_synthesis, error_budget):
    if use_delayed_gate_synthesis:
        transformers = [
            synthesize_clifford_t(error_budget),
            create_big_graph_from_subcircuits(),
        ]
    else:
        transformers = [
            simplify_rotations,
            create_big_graph_from_subcircuits(),
        ]
    return transformers


@pytest.mark.parametrize(
    "quantum_program,expected_results",
    [
        (
            QuantumProgram(
                [Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])], 1, lambda x: [0]
            ),
            {"n_measurement_steps": 3, "n_nodes": 3, "n_logical_qubits": 2},
        ),
        (
            get_program_from_circuit(
                Circuit([RX(np.pi / 4)(0), RY(np.pi / 4)(0), CNOT(0, 1)])
            ),
            {"n_measurement_steps": 4, "n_nodes": 4, "n_logical_qubits": 3},
        ),
        (
            get_program_from_circuit(
                Circuit([H(0)] + [CNOT(i, i + 1) for i in range(3)])
            ),
            {"n_measurement_steps": 4, "n_nodes": 4, "n_logical_qubits": 3},
        ),
        (
            get_program_from_circuit(
                Circuit([H(0)] + [CNOT(i, i + 1) for i in range(3)] + [T(1), T(2)])
            ),
            {"n_measurement_steps": 6, "n_nodes": 6, "n_logical_qubits": 5},
        ),
        (
            get_program_from_circuit(
                Circuit([H(0), T(0), CNOT(0, 1), T(2), CNOT(2, 3)])
            ),
            {"n_measurement_steps": 3, "n_nodes": 6, "n_logical_qubits": 2},
        ),
    ],
)
def test_get_resource_estimations_for_program_gives_correct_results(
    quantum_program, expected_results, use_delayed_gate_synthesis
):
    architecture_model = BasicArchitectureModel(
        physical_t_gate_error_rate=1e-3,
        surface_code_cycle_time_in_seconds=1e-6,
    )
    # set circuit generation weight to 0
    error_budget = ErrorBudget.from_weights(1e-3, 0, 1, 1)
    algorithm_description = AlgorithmImplementation(quantum_program, error_budget, 1)

    transformers = _get_transformers(use_delayed_gate_synthesis, error_budget)
    gsc_resource_estimates = asdict(
        run_custom_resource_estimation_pipeline(
            algorithm_description,
            estimator=GraphResourceEstimator(architecture_model),
            transformers=transformers,
        )
    )

    # Extract only keys that we want to compare
    assert {
        key: gsc_resource_estimates[key] for key in expected_results
    } == expected_results

    # Note that error_budget is a bound for the sum of the gate synthesis error and
    # logical error. Therefore the expression below is a loose upper bound for the
    # logical error rate.
    assert (
        gsc_resource_estimates["logical_error_rate"]
        < error_budget.total_failure_tolerance
    )


def test_better_architecture_does_not_require_more_resources(
    use_delayed_gate_synthesis,
):
    low_noise_architecture_model = BasicArchitectureModel(
        physical_t_gate_error_rate=1e-4,
        surface_code_cycle_time_in_seconds=1e-6,
    )
    high_noise_architecture_model = BasicArchitectureModel(
        physical_t_gate_error_rate=1e-3,
        surface_code_cycle_time_in_seconds=1e-6,
    )
    error_budget = ErrorBudget.from_weights(
        total_failure_tolerance=1e-2, circuit_generation_weight=0
    )
    transformers = _get_transformers(use_delayed_gate_synthesis, error_budget)

    quantum_program = get_program_from_circuit(
        Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    )
    algorithm_description = AlgorithmImplementation(quantum_program, error_budget, 1)
    low_noise_resource_estimates = run_custom_resource_estimation_pipeline(
        algorithm_description,
        estimator=GraphResourceEstimator(low_noise_architecture_model),
        transformers=transformers,
    )

    high_noise_resource_estimates = run_custom_resource_estimation_pipeline(
        algorithm_description,
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
        low_noise_resource_estimates.total_time_in_seconds
        <= high_noise_resource_estimates.total_time_in_seconds
    )


def test_higher_error_budget_does_not_require_more_resources(
    use_delayed_gate_synthesis,
):
    architecture_model = BasicArchitectureModel(
        physical_t_gate_error_rate=1e-3,
        surface_code_cycle_time_in_seconds=1e-6,
    )
    low_failure_tolerance = 1e-3
    high_failure_tolerance = 1e-2

    # set circuit generation weight to 0
    low_error_budget = ErrorBudget.from_weights(low_failure_tolerance, 0, 1, 1)
    high_error_budget = ErrorBudget.from_weights(high_failure_tolerance, 0, 1, 1)

    low_error_transformers = _get_transformers(
        use_delayed_gate_synthesis, low_error_budget
    )
    high_error_transformers = _get_transformers(
        use_delayed_gate_synthesis, high_error_budget
    )

    quantum_program = get_program_from_circuit(
        Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    )
    algorithm_description_low_error_budget = AlgorithmImplementation(
        quantum_program, low_error_budget, 1
    )
    algorithm_description_high_error_budget = AlgorithmImplementation(
        quantum_program, high_error_budget, 1
    )

    low_error_resource_estimates = run_custom_resource_estimation_pipeline(
        algorithm_description_low_error_budget,
        estimator=GraphResourceEstimator(architecture_model),
        transformers=low_error_transformers,
    )

    high_error_resource_estimates = run_custom_resource_estimation_pipeline(
        algorithm_description_high_error_budget,
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
        high_error_resource_estimates.total_time_in_seconds
        <= low_error_resource_estimates.total_time_in_seconds
    )


def test_get_resource_estimations_for_program_accounts_for_decoder():
    architecture_model = BasicArchitectureModel(
        physical_t_gate_error_rate=1e-3,
        surface_code_cycle_time_in_seconds=1e-6,
    )
    # set circuit generation weight to 0
    error_budget = ErrorBudget.from_weights(1e-3, 0, 1, 1)
    quantum_program = get_program_from_circuit(
        Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    )
    algorithm_description = AlgorithmImplementation(quantum_program, error_budget, 1)

    transformers = _get_transformers(True, error_budget)
    gsc_resource_estimates_no_decoder = run_custom_resource_estimation_pipeline(
        algorithm_description,
        estimator=GraphResourceEstimator(architecture_model, decoder_model=None),
        transformers=transformers,
    )

    file_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "data_structures"
    )
    file_path = os.path.join(file_dir, "decoder_test_data.csv")

    decoder = DecoderModel.from_csv(file_path)
    gsc_resource_estimates_with_decoder = run_custom_resource_estimation_pipeline(
        algorithm_description,
        estimator=GraphResourceEstimator(architecture_model, decoder_model=decoder),
        transformers=transformers,
    )

    assert gsc_resource_estimates_no_decoder.max_decodable_distance is None
    assert gsc_resource_estimates_no_decoder.decoder_area is None
    assert gsc_resource_estimates_no_decoder.decoder_total_energy_consumption is None
    assert gsc_resource_estimates_no_decoder.decoder_power is None

    assert gsc_resource_estimates_with_decoder.max_decodable_distance is not None
    assert gsc_resource_estimates_with_decoder.decoder_area is not None
    assert (
        gsc_resource_estimates_with_decoder.decoder_total_energy_consumption is not None
    )
    assert gsc_resource_estimates_with_decoder.decoder_power is not None
