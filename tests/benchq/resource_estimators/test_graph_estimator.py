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


@pytest.mark.parametrize(
    "quantum_program,optimization,expected_results",
    [
        (
            QuantumProgram(
                [Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])], 1, lambda x: [0]
            ),
            "Space",
            {"code_distance": 9, "n_logical_qubits": 5},
        ),
        (
            QuantumProgram.from_circuit(
                Circuit([RX(np.pi / 4)(0), RY(np.pi / 4)(0), CNOT(0, 1)])
            ),
            "Space",
            {"code_distance": 9, "n_logical_qubits": 5},
        ),
        (
            QuantumProgram.from_circuit(
                Circuit([H(0)] + [CNOT(i, i + 1) for i in range(3)])
            ),
            "Space",
            {"code_distance": 9, "n_logical_qubits": 5},
        ),
        (
            QuantumProgram.from_circuit(
                Circuit([H(0)] + [CNOT(i, i + 1) for i in range(3)] + [T(1), T(2)])
            ),
            "Space",
            {"code_distance": 9, "n_logical_qubits": 5},
        ),
        (
            QuantumProgram.from_circuit(
                Circuit([H(0), T(0), CNOT(0, 1), T(2), CNOT(2, 3)])
            ),
            "Space",
            {"code_distance": 9, "n_logical_qubits": 5},
        ),
        (
            QuantumProgram(
                [Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])], 1, lambda x: [0]
            ),
            "Time",
            {"code_distance": 7, "n_logical_qubits": 6},
        ),
        (
            QuantumProgram.from_circuit(
                Circuit([RX(np.pi / 4)(0), RY(np.pi / 4)(0), CNOT(0, 1)])
            ),
            "Time",
            {"code_distance": 9, "n_logical_qubits": 7},
        ),
        (
            QuantumProgram.from_circuit(
                Circuit([H(0)] + [CNOT(i, i + 1) for i in range(3)])
            ),
            "Time",
            {"code_distance": 7, "n_logical_qubits": 8},
        ),
        (
            QuantumProgram.from_circuit(
                Circuit([H(0)] + [CNOT(i, i + 1) for i in range(3)] + [T(1), T(2)])
            ),
            "Time",
            {"code_distance": 9, "n_logical_qubits": 13},
        ),
        (
            QuantumProgram.from_circuit(
                Circuit([H(0), T(0), CNOT(0, 1), T(2), CNOT(2, 3)])
            ),
            "Time",
            {"code_distance": 9, "n_logical_qubits": 12},
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
    low_noise_architecture_model = BASIC_ION_TRAP_ARCHITECTURE_MODEL

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


@pytest.mark.parametrize(
    "gsc_info,optimization,expected_results",
    [
        (
            GSCInfo(
                4,
                2,
                [3, 5],
                [0, 0],
                [0, 0],
            ),
            "Time",
            {"number_of_magic_state_factories": 0, "number_of_data_qubits": 4},
        ),
        (
            GSCInfo(
                5,
                2,
                [3, 5],
                [0, 7],
                [0, 1],
            ),
            "Time",
            {"number_of_magic_state_factories": 8, "number_of_data_qubits": 5},
        ),
        (
            GSCInfo(
                5,
                2,
                [3, 5],
                [0, 7],
                [0, 2],
            ),
            "Space",
            {"number_of_magic_state_factories": 1, "number_of_data_qubits": 5},
        ),
    ],
)
def test_get_resource_estimations_for_program_accounts_for_spatial_resources(
    gsc_info, optimization, expected_results
):

    dummy_circuit = Circuit()

    dummy_quantum_program = QuantumProgram(
        [dummy_circuit, dummy_circuit],
        steps=2,
        calculate_subroutine_sequence=lambda x: [0, 1],
    )

    # Initialize Graph Resource Estimator
    estimator = GraphResourceEstimator(optimization)

    compiled_program = CompiledQuantumProgram.from_program(
        dummy_quantum_program, [gsc_info, gsc_info]
    )

    magic_state_factory = None
    data_and_bus_code_distance = None
    n_t_gates_per_rotation = None

    logical_architecture_resource_info = (
        estimator.get_bus_architecture_resource_breakdown(
            compiled_program,
            data_and_bus_code_distance,
            magic_state_factory,
            n_t_gates_per_rotation,
        )
    )

    number_of_magic_state_factories = (
        logical_architecture_resource_info.num_magic_state_factories
    )

    number_of_data_qubits = logical_architecture_resource_info.num_logical_data_qubits

    # Check that the number of magic state factories is correct
    assert (
        number_of_magic_state_factories
        == expected_results["number_of_magic_state_factories"]
    )
    assert number_of_data_qubits == expected_results["number_of_data_qubits"]


# Test for the time optimal cycle allocation functionality
@pytest.mark.parametrize(
    "gsc_info,optimization,cycles_per_layer",
    [
        (
            GSCInfo(
                4,
                3,
                [3, 5, 1],
                [0, 7, 1],
                [0, 0, 1],
            ),
            "Time",
            [9 * 3, 9 * 5 + 9 * 2, +27 + 9 * 2 + (27 + 9 * 2) * (30 - 1)],
        ),
        (
            GSCInfo(
                4,
                3,
                [3, 5, 1],
                [0, 7, 1],
                [0, 0, 1],
            ),
            "Space",
            [
                9 * 3,
                9 * 5 + 9 * 2 + (27 + 9 * 2) * (7 - 1),
                +27 + 9 * 2 + (27 + 9 * 2) * 30,
            ],
        ),
    ],
)
def test_get_cycle_allocation(gsc_info, optimization, cycles_per_layer):

    distillation_time_in_cycles = 27
    n_t_gates_per_rotation = 30
    data_and_bus_code_distance = 9

    dummy_circuit = Circuit()

    def calculate_subroutine_sequence(x):
        return [0, 1]

    dummy_quantum_program = QuantumProgram(
        [dummy_circuit, dummy_circuit],
        steps=2,
        calculate_subroutine_sequence=calculate_subroutine_sequence,
    )

    # Initialize Graph Resource Estimator
    estimator = GraphResourceEstimator(optimization)

    compiled_program = CompiledQuantumProgram.from_program(
        dummy_quantum_program, [gsc_info, gsc_info]
    )

    time_allocation = estimator.get_cycle_allocation(
        compiled_program,
        distillation_time_in_cycles,
        n_t_gates_per_rotation,
        data_and_bus_code_distance,
    )

    # Check that the number of cycles is correct
    assert time_allocation.total == sum(cycles_per_layer) * len(
        calculate_subroutine_sequence(0)
    )
