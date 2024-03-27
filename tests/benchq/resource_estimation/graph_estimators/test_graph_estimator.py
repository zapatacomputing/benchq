import os
from dataclasses import replace

import numpy as np
import pytest
from orquestra.quantum.circuits import CNOT, RX, RY, RZ, Circuit, H, T

from benchq.algorithms.data_structures import AlgorithmImplementation, ErrorBudget
from benchq.compilation.graph_states import (
    get_implementation_compiler,
    get_ruby_slippers_circuit_compiler,
)
from benchq.compilation.graph_states.compiled_data_structures import GSCInfo
from benchq.decoder_modeling import DecoderModel
from benchq.problem_embeddings.quantum_program import QuantumProgram
from benchq.quantum_hardware_modeling import (
    BASIC_ION_TRAP_ARCHITECTURE_MODEL,
    BASIC_SC_ARCHITECTURE_MODEL,
    DETAILED_ION_TRAP_ARCHITECTURE_MODEL,
)
from benchq.resource_estimators.graph_estimator import GraphResourceEstimator

fast_ruby_slippers = get_implementation_compiler(
    circuit_compiler=get_ruby_slippers_circuit_compiler(
        takes_graph_input=False,
        gives_graph_output=False,
        max_graph_size=10,
        decomposition_strategy=0,
    )
)


@pytest.fixture(params=["Time", "Space"])
def optimization(request):
    return request.param


@pytest.fixture(params=[True, False])
def transpile_to_clifford_t(request):
    return request.param


@pytest.mark.parametrize(
    "architecture_model, supports_hardware_resources",
    [
        (BASIC_SC_ARCHITECTURE_MODEL, False),
        (BASIC_ION_TRAP_ARCHITECTURE_MODEL, False),
        (DETAILED_ION_TRAP_ARCHITECTURE_MODEL, True),
    ],
)
def test_resource_estimations_returns_results_for_different_architectures(
    optimization,
    architecture_model,
    supports_hardware_resources,
    transpile_to_clifford_t,
):
    # set circuit generation weight to 0
    error_budget = ErrorBudget.from_weights(1e-3, 0, 1, 1)
    quantum_program = QuantumProgram(
        [Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])], 1, lambda x: [0]
    )
    algorithm_implementation = AlgorithmImplementation(quantum_program, error_budget, 1)
    if transpile_to_clifford_t:
        algorithm_implementation = algorithm_implementation.transpile_to_clifford_t()

    estimator = GraphResourceEstimator(optimization)
    gsc_resource_estimates = estimator.compile_and_estimate(
        algorithm_implementation,
        fast_ruby_slippers,
        architecture_model,
    )

    assert gsc_resource_estimates
    if supports_hardware_resources:
        assert gsc_resource_estimates.hardware_resource_info is not None
    else:
        assert gsc_resource_estimates.hardware_resource_info is None


# GSCInfo(
#     num_logical_qubits,
#     num_layers,
#     graph_creation_tocks_per_layer,
#     t_states_per_layer,
#     rotations_per_layer,
# )


@pytest.mark.parametrize(
    "quantum_program,optimization,expected_results",
    [
        (
            QuantumProgram(
                [Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])], 1, lambda x: [0]
            ),
            "Space",
            {"code_distance": 8, "n_logical_qubits": 4},
        ),
        (
            QuantumProgram.from_circuit(
                Circuit([RX(np.pi / 4)(0), RY(np.pi / 4)(0), CNOT(0, 1)])
            ),
            "Space",
            {"code_distance": 9, "n_logical_qubits": 4},
        ),
        (
            QuantumProgram.from_circuit(
                Circuit([H(0)] + [CNOT(i, i + 1) for i in range(3)])
            ),
            "Space",
            {"code_distance": 9, "n_logical_qubits": 4},
        ),
        (
            QuantumProgram.from_circuit(
                Circuit([H(0)] + [CNOT(i, i + 1) for i in range(3)] + [T(1), T(2)])
            ),
            "Space",
            {"code_distance": 9, "n_logical_qubits": 4},
        ),
        (
            QuantumProgram.from_circuit(
                Circuit([H(0), T(0), CNOT(0, 1), T(2), CNOT(2, 3)])
            ),
            "Space",
            {"code_distance": 8, "n_logical_qubits": 4},
        ),
        (
            QuantumProgram(
                [Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])], 1, lambda x: [0]
            ),
            "Time",
            {"code_distance": 10, "n_logical_qubits": 18},
        ),
        (
            QuantumProgram.from_circuit(
                Circuit([RX(np.pi / 4)(0), RY(np.pi / 4)(0), CNOT(0, 1)])
            ),
            "Time",
            {"code_distance": 10, "n_logical_qubits": 18},
        ),
        (
            QuantumProgram.from_circuit(
                Circuit([H(0)] + [CNOT(i, i + 1) for i in range(3)])
            ),
            "Time",
            {"code_distance": 10, "n_logical_qubits": 24},
        ),
        (
            QuantumProgram.from_circuit(
                Circuit([H(0)] + [CNOT(i, i + 1) for i in range(3)] + [T(1), T(2)])
            ),
            "Time",
            {"code_distance": 10, "n_logical_qubits": 36},
        ),
        (
            QuantumProgram.from_circuit(
                Circuit([H(0), T(0), CNOT(0, 1), T(2), CNOT(2, 3)])
            ),
            "Time",
            {"code_distance": 10, "n_logical_qubits": 36},
        ),
    ],
)
def test_get_resource_estimations_for_program_gives_correct_results(
    quantum_program, expected_results, transpile_to_clifford_t, optimization
):
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL

    # set circuit generation weight to 0
    error_budget = ErrorBudget.from_weights(1e-3, 0, 1, 1)
    algorithm_implementation = AlgorithmImplementation(quantum_program, error_budget, 1)
    if transpile_to_clifford_t:
        algorithm_implementation = algorithm_implementation.transpile_to_clifford_t()
    estimator = GraphResourceEstimator(optimization)

    resource_estimates = estimator.compile_and_estimate(
        algorithm_implementation,
        fast_ruby_slippers,
        architecture_model,
    )

    assert resource_estimates.code_distance == expected_results["code_distance"]
    assert resource_estimates.n_logical_qubits == expected_results["n_logical_qubits"]


def test_better_architecture_does_not_require_more_resources(
    optimization,
    transpile_to_clifford_t,
):
    low_noise_architecture_model = BASIC_SC_ARCHITECTURE_MODEL

    high_noise_architecture_model = replace(
        BASIC_SC_ARCHITECTURE_MODEL, physical_qubit_error_rate=1e-2
    )

    # set algorithm failure tolerance to 0
    error_budget = ErrorBudget.from_weights(1e-2, 0, 1, 1)

    quantum_program = QuantumProgram.from_circuit(
        Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    )
    algorithm_implementation = AlgorithmImplementation(quantum_program, error_budget, 1)
    estimator = GraphResourceEstimator(optimization)

    low_noise_resource_estimates = estimator.compile_and_estimate(
        algorithm_implementation,
        fast_ruby_slippers,
        low_noise_architecture_model,
    )

    high_noise_resource_estimates = estimator.compile_and_estimate(
        algorithm_implementation,
        fast_ruby_slippers,
        high_noise_architecture_model,
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
    transpile_to_clifford_t,
):
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL
    low_failure_tolerance = 1e-3
    high_failure_tolerance = 1e-2

    # set circuit generation weight to 0
    low_error_budget = ErrorBudget.from_weights(low_failure_tolerance, 0, 1, 1)
    high_error_budget = ErrorBudget.from_weights(high_failure_tolerance, 0, 1, 1)

    quantum_program = QuantumProgram.from_circuit(
        Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    )
    algorithm_implementation_low_error_budget = AlgorithmImplementation(
        quantum_program, low_error_budget, 1
    )
    algorithm_implementation_high_error_budget = AlgorithmImplementation(
        quantum_program, high_error_budget, 1
    )
    if transpile_to_clifford_t:
        algorithm_implementation_low_error_budget = (
            algorithm_implementation_low_error_budget.transpile_to_clifford_t()
        )
        algorithm_implementation_high_error_budget = (
            algorithm_implementation_high_error_budget.transpile_to_clifford_t()
        )

    estimator = GraphResourceEstimator(optimization)

    low_error_resource_estimates = estimator.compile_and_estimate(
        algorithm_implementation_low_error_budget,
        fast_ruby_slippers,
        architecture_model,
    )

    high_error_resource_estimates = estimator.compile_and_estimate(
        algorithm_implementation_high_error_budget,
        fast_ruby_slippers,
        architecture_model,
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
    quantum_program = QuantumProgram.from_circuit(
        Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    )
    algorithm_implementation = AlgorithmImplementation(quantum_program, error_budget, 1)
    estimator = GraphResourceEstimator(optimization)

    gsc_resource_estimates_no_decoder = estimator.compile_and_estimate(
        algorithm_implementation,
        fast_ruby_slippers,
        architecture_model,
    )

    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "decoder_test_data.csv"
    )

    decoder = DecoderModel.from_csv(file_path)
    gsc_resource_estimates_with_decoder = estimator.compile_and_estimate(
        algorithm_implementation,
        fast_ruby_slippers,
        architecture_model,
        decoder_model=decoder,
    )

    assert gsc_resource_estimates_no_decoder.decoder_info is None
    assert gsc_resource_estimates_with_decoder.decoder_info is not None
