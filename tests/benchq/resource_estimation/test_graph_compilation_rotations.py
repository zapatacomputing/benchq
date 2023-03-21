import numpy as np
import pytest
from orquestra.quantum.circuits import CNOT, RX, RY, RZ, Circuit, H, T

from benchq.data_structures.hardware_architecture_models import BasicArchitectureModel
from benchq.data_structures.quantum_program import QuantumProgram
from benchq.resource_estimation.graph_compilation_rotations import (
    get_resource_estimations_for_program,
)


@pytest.mark.parametrize(
    "quantum_program,expected_results",
    [
        (
            QuantumProgram(
                [Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])], 1, lambda x: [0]
            ),
            {"n_measurement_steps": 3, "n_nodes": 3, "max_graph_degree": 2},
        ),
        (
            QuantumProgram(
                [Circuit([RX(np.pi / 4)(0), RY(np.pi / 4)(0), CNOT(0, 1)])],
                1,
                lambda _: [0],
            ),
            {"n_measurement_steps": 3, "n_nodes": 4, "max_graph_degree": 2},
        ),
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
        (
            QuantumProgram(
                [Circuit([H(0), T(0), CNOT(0, 1), T(2), CNOT(2, 3)])],
                1,
                lambda _: [0],
            ),
            {"n_measurement_steps": 3, "n_nodes": 6, "max_graph_degree": 2},
        ),
    ],
)
def test_get_resource_estimations_for_program_gives_correct_results(
    quantum_program, expected_results
):
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
    error_budget = 1e-3
    gsc_resource_estimates = get_resource_estimations_for_program(
        quantum_program,
        error_budget,
        architecture_model,
        plot=True,
    )
    for key in expected_results.keys():
        assert gsc_resource_estimates[key] == expected_results[key]

    # Note that error_budget is a bound for the sum of the gate synthesis error and
    # logical error. Therefore the expression below is a loose upper bound for the
    # logical error rate.
    assert gsc_resource_estimates["logical_error_rate"] < error_budget


def test_better_architecture_does_not_require_more_resources():
    low_noise_architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-4,
        physical_gate_time_in_seconds=1e-6,
    )
    high_noise_architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
    error_budget = 1e-3
    circuit = Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    quantum_program = QuantumProgram(
        subroutines=[circuit], steps=1, calculate_subroutine_sequence=lambda x: [0]
    )
    low_noise_resource_estimates = get_resource_estimations_for_program(
        quantum_program,
        error_budget,
        low_noise_architecture_model,
        plot=True,
    )
    high_noise_resource_estimates = get_resource_estimations_for_program(
        quantum_program,
        error_budget,
        high_noise_architecture_model,
        plot=True,
    )

    assert (
        low_noise_resource_estimates["physical_qubit_count"]
        <= high_noise_resource_estimates["physical_qubit_count"]
    )
    assert (
        low_noise_resource_estimates["min_viable_distance"]
        <= high_noise_resource_estimates["min_viable_distance"]
    )
    assert (
        low_noise_resource_estimates["total_time"]
        <= high_noise_resource_estimates["total_time"]
    )


def test_higher_error_budget_does_not_require_more_resources():
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
    low_error_budget = 1e-3
    high_error_budget = 1e-2
    circuit = Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    quantum_program = QuantumProgram(
        subroutines=[circuit], steps=1, calculate_subroutine_sequence=lambda x: [0]
    )
    low_error_resource_estimates = get_resource_estimations_for_program(
        quantum_program,
        low_error_budget,
        architecture_model,
        plot=True,
    )
    high_error_resource_estimates = get_resource_estimations_for_program(
        quantum_program,
        high_error_budget,
        architecture_model,
        plot=True,
    )

    assert (
        high_error_resource_estimates["physical_qubit_count"]
        <= low_error_resource_estimates["physical_qubit_count"]
    )
    assert (
        high_error_resource_estimates["min_viable_distance"]
        <= low_error_resource_estimates["min_viable_distance"]
    )
    assert (
        high_error_resource_estimates["total_time"]
        <= low_error_resource_estimates["total_time"]
    )
