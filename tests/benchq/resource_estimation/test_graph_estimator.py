import os
from dataclasses import replace

import numpy as np
import pytest
from orquestra.quantum.circuits import CNOT, RX, RY, RZ, Circuit, H, T

from benchq.compilation import get_algorithmic_graph_from_ruby_slippers_with_hyperparams
from benchq.data_structures import (
    BASIC_SC_ARCHITECTURE_MODEL,
    AlgorithmImplementation,
    DecoderModel,
    ErrorBudget,
    QuantumProgram,
    get_program_from_circuit,
)
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_custom_resource_estimation_pipeline,
    synthesize_clifford_t,
    transpile_to_native_gates,
)

fast_ruby_slippers = get_algorithmic_graph_from_ruby_slippers_with_hyperparams(
    max_graph_size=10,
    decomposition_strategy=0,
)


@pytest.fixture(params=["time", "space"])
def optimization(request):
    return request.param


@pytest.fixture(params=[True, False])
def use_delayed_gate_synthesis(request):
    return request.param


def _get_transformers(use_delayed_gate_synthesis, error_budget):
    if use_delayed_gate_synthesis:
        transformers = [
            synthesize_clifford_t(error_budget),
            create_big_graph_from_subcircuits(fast_ruby_slippers),
        ]
    else:
        transformers = [
            transpile_to_native_gates,
            create_big_graph_from_subcircuits(fast_ruby_slippers),
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
            {"n_measurement_steps": 4, "n_nodes": 4, "n_logical_qubits": 2},
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
    quantum_program, expected_results, optimization, use_delayed_gate_synthesis
):
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL

    # set circuit generation weight to 0
    error_budget = ErrorBudget.from_weights(1e-3, 0, 1, 1)
    algorithm_implementation = AlgorithmImplementation(quantum_program, error_budget, 1)

    transformers = _get_transformers(use_delayed_gate_synthesis, error_budget)
    gsc_resource_estimates = run_custom_resource_estimation_pipeline(
        algorithm_implementation,
        estimator=GraphResourceEstimator(architecture_model),
        transformers=transformers,
    )

    # Extract only keys that we want to compare
    test_results = {
        "n_measurement_steps": gsc_resource_estimates.extra.n_measurement_steps,
        "n_nodes": gsc_resource_estimates.extra.n_nodes,
        "n_logical_qubits": gsc_resource_estimates.n_logical_qubits,
    }
    for field in test_results.keys():
        assert test_results[field] == expected_results[field]

    # Note that error_budget is a bound for the sum of the gate synthesis error and
    # logical error. Therefore the expression below is a loose upper bound for the
    # logical error rate.
    assert (
        gsc_resource_estimates.logical_error_rate < error_budget.total_failure_tolerance
    )


def test_better_architecture_does_not_require_more_resources(
    optimization,
    use_delayed_gate_synthesis,
):
    low_noise_architecture_model = BASIC_SC_ARCHITECTURE_MODEL

    high_noise_architecture_model = replace(
        BASIC_SC_ARCHITECTURE_MODEL, physical_qubit_error_rate=1e-2
    )

    # set algorithm failure tolerance to 0
    error_budget = ErrorBudget.from_weights(1e-2, 0, 1, 1)

    transformers = _get_transformers(use_delayed_gate_synthesis, error_budget)

    quantum_program = get_program_from_circuit(
        Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    )
    algorithm_implementation = AlgorithmImplementation(quantum_program, error_budget, 1)
    low_noise_resource_estimates = run_custom_resource_estimation_pipeline(
        algorithm_implementation,
        estimator=GraphResourceEstimator(
            low_noise_architecture_model, optimization=optimization
        ),
        transformers=transformers,
    )

    high_noise_resource_estimates = run_custom_resource_estimation_pipeline(
        algorithm_implementation,
        estimator=GraphResourceEstimator(
            high_noise_architecture_model, optimization=optimization
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
        low_noise_resource_estimates.total_time_in_seconds
        <= high_noise_resource_estimates.total_time_in_seconds
    )


def test_higher_error_budget_does_not_require_more_resources(
    optimization,
    use_delayed_gate_synthesis,
):
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL
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
    algorithm_implementation_low_error_budget = AlgorithmImplementation(
        quantum_program, low_error_budget, 1
    )
    algorithm_implementation_high_error_budget = AlgorithmImplementation(
        quantum_program, high_error_budget, 1
    )

    low_error_resource_estimates = run_custom_resource_estimation_pipeline(
        algorithm_implementation_low_error_budget,
        estimator=GraphResourceEstimator(architecture_model, optimization=optimization),
        transformers=low_error_transformers,
    )

    high_error_resource_estimates = run_custom_resource_estimation_pipeline(
        algorithm_implementation_high_error_budget,
        estimator=GraphResourceEstimator(architecture_model, optimization=optimization),
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


def test_get_resource_estimations_for_program_accounts_for_decoder(optimization):
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL
    # set circuit generation weight to 0
    error_budget = ErrorBudget.from_weights(1e-3, 0, 1, 1)
    quantum_program = get_program_from_circuit(
        Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    )
    algorithm_implementation = AlgorithmImplementation(quantum_program, error_budget, 1)

    transformers = _get_transformers(True, error_budget)
    gsc_resource_estimates_no_decoder = run_custom_resource_estimation_pipeline(
        algorithm_implementation,
        estimator=GraphResourceEstimator(architecture_model, decoder_model=None),
        transformers=transformers,
    )

    file_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "data_structures"
    )
    file_path = os.path.join(file_dir, "decoder_test_data.csv")

    decoder = DecoderModel.from_csv(file_path)
    gsc_resource_estimates_with_decoder = run_custom_resource_estimation_pipeline(
        algorithm_implementation,
        estimator=GraphResourceEstimator(architecture_model, decoder_model=decoder),
        transformers=transformers,
    )

    assert gsc_resource_estimates_no_decoder.decoder_info is None
    assert gsc_resource_estimates_with_decoder.decoder_info is not None
    assert gsc_resource_estimates_with_decoder.decoder_info is not None
