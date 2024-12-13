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
from benchq.compilation.graph_states.compiled_data_structures import (
    CompiledQuantumProgram,
    GSCInfo,
)
from benchq.decoder_modeling import DecoderModel
from benchq.logical_architecture_modeling.graph_based_logical_architectures import (
    TwoRowBusArchitectureModel,
)
from benchq.problem_embeddings.quantum_program import QuantumProgram
from benchq.quantum_hardware_modeling import (
    BASIC_ION_TRAP_ARCHITECTURE_MODEL,
    BASIC_SC_ARCHITECTURE_MODEL,
    DETAILED_ION_TRAP_ARCHITECTURE_MODEL,
)
from benchq.resource_estimators.graph_estimator import GraphResourceEstimator
from benchq.resource_estimators.resource_info import (
    LogicalArchitectureResourceInfo,
    MagicStateFactoryInfo,
)

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
def test_resource_estimations_returns_results_for_different_hardware_architectures(
    optimization,
    architecture_model,
    supports_hardware_resources,
    transpile_to_clifford_t,
):

    logical_architecture_model = TwoRowBusArchitectureModel()

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
        logical_architecture_model,
        architecture_model,
    )

    assert gsc_resource_estimates
    if supports_hardware_resources:
        assert gsc_resource_estimates.hardware_resource_info is not None
    else:
        assert gsc_resource_estimates.hardware_resource_info is None


@pytest.mark.parametrize(
    "quantum_program,optimization,expected_results",
    [
        # (
        #     QuantumProgram(
        #         [Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])], 1, lambda x: [0]
        #     ),
        #     "Space",
        #     {"code_distance": 9, "n_logical_qubits": 5},
        # ),
        # (
        #     QuantumProgram.from_circuit(
        #         Circuit([RX(np.pi / 4)(0), RY(np.pi / 4)(0), CNOT(0, 1)])
        #     ),
        #     "Space",
        #     {"code_distance": 9, "n_logical_qubits": 5},
        # ),
        # (
        #     QuantumProgram.from_circuit(
        #         Circuit([H(0)] + [CNOT(i, i + 1) for i in range(3)])
        #     ),
        #     "Space",
        #     {"code_distance": 9, "n_logical_qubits": 5},
        # ),
        # (
        #     QuantumProgram.from_circuit(
        #         Circuit([H(0)] + [CNOT(i, i + 1) for i in range(3)] + [T(1), T(2)])
        #     ),
        #     "Space",
        #     {"code_distance": 9, "n_logical_qubits": 5},
        # ),
        # (
        #     QuantumProgram.from_circuit(
        #         Circuit([H(0), T(0), CNOT(0, 1), T(2), CNOT(2, 3)])
        #     ),
        #     "Space",
        #     {"code_distance": 9, "n_logical_qubits": 5},
        # ),
        # (
        #     QuantumProgram(
        #         [Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])], 1, lambda x: [0]
        #     ),
        #     "Time",
        #     {"code_distance": 7, "n_logical_qubits": 6},
        # ),
        # (
        #     QuantumProgram.from_circuit(
        #         Circuit([RX(np.pi / 4)(0), RY(np.pi / 4)(0), CNOT(0, 1)])
        #     ),
        #     "Time",
        #     {"code_distance": 11, "n_logical_qubits": 7},
        # ),
        # (
        #     QuantumProgram.from_circuit(
        #         Circuit([H(0)] + [CNOT(i, i + 1) for i in range(3)])
        #     ),
        #     "Time",
        #     {"code_distance": 7, "n_logical_qubits": 8},
        # ),
        # (
        #     QuantumProgram.from_circuit(
        #         Circuit([H(0)] + [CNOT(i, i + 1) for i in range(3)] + [T(1), T(2)])
        #     ),
        #     "Time",
        #     {"code_distance": 9, "n_logical_qubits": 13},
        # ),
        (
            QuantumProgram.from_circuit(
                Circuit([H(0), T(0), RY(np.pi / 4)(0), CNOT(0, 1), T(2), CNOT(2, 3)])
            ),
            "Time",
            {"code_distance": 11, "n_logical_qubits": 11},
        ),
    ],
)
def test_get_resource_estimations_for_program_gives_correct_results(
    quantum_program, expected_results, transpile_to_clifford_t, optimization
):
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL
    logical_architecture_model = TwoRowBusArchitectureModel()

    # set circuit generation weight to 0
    error_budget = ErrorBudget.from_weights(1e-3, 0, 1, 1)
    algorithm_implementation = AlgorithmImplementation(quantum_program, error_budget, 1)
    if transpile_to_clifford_t:
        algorithm_implementation = algorithm_implementation.transpile_to_clifford_t()
    estimator = GraphResourceEstimator(optimization)

    resource_estimates = estimator.compile_and_estimate(
        algorithm_implementation,
        fast_ruby_slippers,
        logical_architecture_model,
        architecture_model,
    )

    obtained_log_arch_info = resource_estimates.logical_architecture_resource_info

    assert (
        obtained_log_arch_info.data_and_bus_code_distance  # type: ignore
        == expected_results["code_distance"]
    )
    assert (
        obtained_log_arch_info.num_logical_qubits  # type: ignore
        == expected_results["n_logical_qubits"]
    )


def test_better_hardware_architecture_does_not_require_more_resources(
    optimization,
    transpile_to_clifford_t,
):
    low_noise_architecture_model = BASIC_ION_TRAP_ARCHITECTURE_MODEL
    logical_architecture_model = TwoRowBusArchitectureModel()

    high_noise_architecture_model = replace(
        BASIC_ION_TRAP_ARCHITECTURE_MODEL, physical_qubit_error_rate=1e-3
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
        logical_architecture_model,
        low_noise_architecture_model,
    )

    high_noise_resource_estimates = estimator.compile_and_estimate(
        algorithm_implementation,
        fast_ruby_slippers,
        logical_architecture_model,
        high_noise_architecture_model,
    )

    low_noise_re = low_noise_resource_estimates.logical_architecture_resource_info
    high_noise_re = high_noise_resource_estimates.logical_architecture_resource_info

    assert (
        low_noise_resource_estimates.n_physical_qubits  # type: ignore
        <= high_noise_resource_estimates.n_physical_qubits  # type: ignore
    )
    assert (
        low_noise_re.data_and_bus_code_distance  # type: ignore
        <= high_noise_re.data_and_bus_code_distance  # type: ignore
    )
    assert (
        low_noise_resource_estimates.total_time_in_seconds  # type: ignore
        <= high_noise_resource_estimates.total_time_in_seconds  # type: ignore
    )


def test_higher_error_budget_does_not_require_more_resources(
    optimization,
    transpile_to_clifford_t,
):
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL
    low_failure_tolerance = 1e-3
    high_failure_tolerance = 1e-2

    logical_architecture_model = TwoRowBusArchitectureModel()

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
        logical_architecture_model,
        architecture_model,
    )

    high_error_resource_estimates = estimator.compile_and_estimate(
        algorithm_implementation_high_error_budget,
        fast_ruby_slippers,
        logical_architecture_model,
        architecture_model,
    )

    high_re = high_error_resource_estimates.logical_architecture_resource_info
    low_re = low_error_resource_estimates.logical_architecture_resource_info

    assert (
        high_error_resource_estimates.n_physical_qubits  # type: ignore
        <= low_error_resource_estimates.n_physical_qubits
    )

    high_err_distance = high_re.data_and_bus_code_distance  # type: ignore
    low_err_distance = low_re.data_and_bus_code_distance  # type: ignore
    assert high_err_distance <= low_err_distance  # type: ignore
    assert (
        high_error_resource_estimates.total_time_in_seconds  # type: ignore
        <= low_error_resource_estimates.total_time_in_seconds
    )


def test_get_resource_estimations_for_program_accounts_for_decoder(optimization):
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL
    logical_architecture_model = TwoRowBusArchitectureModel()

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
        logical_architecture_model,
        architecture_model,
    )

    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "decoder_test_data.csv"
    )

    decoder = DecoderModel.from_csv(file_path)
    gsc_resource_estimates_with_decoder = estimator.compile_and_estimate(
        algorithm_implementation,
        fast_ruby_slippers,
        logical_architecture_model,
        architecture_model,
        decoder_model=decoder,
    )

    assert gsc_resource_estimates_no_decoder.decoder_info is None
    assert gsc_resource_estimates_with_decoder.decoder_info is not None
