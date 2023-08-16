###############################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
###############################################################################

from math import ceil

import numpy as np
import pytest
from orquestra.integrations.qiskit.conversions import export_to_qiskit
from orquestra.quantum.circuits import ZZ, Circuit
from qiskit import Aer, execute

from benchq.algorithms.lde_solver import (
    get_degree,
    get_kappa,
    get_num_of_grid_points,
    get_prep_int,
    inverse_blockencoding,
)


@pytest.mark.parametrize(
    "kappa, epsilon, expected_result",
    [
        (1, 1e-1, 3),
        (1, 1e-3, 7),
        (10, 1e-3, 80),
        (10, 1e-6, 128),
        (20, 1e-6, 269),
        (30, 1e-6, 415),
        (40, 1e-6, 564),
        (10, 1e-14, 254),
        (20, 1e-14, 521),
    ],
)
def test_get_degree(kappa, epsilon, expected_result):
    result = get_degree(kappa, epsilon)
    assert result == expected_result


@pytest.mark.parametrize(
    "matrix_norm, beta, epsilon, expected_result",
    [
        (0.7280109889280519, 1.3, 1e-3, {"gates": ["RZ", "H", "CNOT"], "qubits": 6}),
        (0.1, 2.0, 1e-1, {"gates": ["RZ", "H", "CNOT"], "qubits": 4}),
        (1.0, 1.3, 1e-6, {"gates": ["RZ", "H", "CNOT"], "qubits": 7}),
        (0.561, 1.1, 1e-12, {"gates": ["RZ", "H", "CNOT"], "qubits": 9}),
    ],
)
def test_get_prep_int_circuit(matrix_norm, beta, epsilon, expected_result):

    circuit, circuit_prime = get_prep_int(matrix_norm, beta, epsilon)
    gate_names = [gate_op.gate.name for gate_op in circuit.operations]
    gate_names_prime = [gate_op.gate.name for gate_op in circuit_prime.operations]

    assert isinstance(circuit, Circuit)
    assert isinstance(circuit_prime, Circuit)
    assert circuit.n_qubits == expected_result["qubits"]
    assert circuit_prime.n_qubits == expected_result["qubits"]
    assert all(gate in expected_result["gates"] for gate in gate_names)
    assert all(gate in expected_result["gates"] for gate in gate_names_prime)


@pytest.mark.parametrize(
    "k, num_qubits, beta, matrix_norm, epsilon",
    [
        (49, 6, 1.3, 0.7280109889280519, 1e-3),
        (79, 7, 1.3, 0.7280109889280519, 1e-6),
        (19, 5, 1.5, 0.5166236541235796, 1e-1),
    ],
)
def test_get_prep_int_amplitudes(k, num_qubits, beta, matrix_norm, epsilon):
    # test if the amplitudes were encoded correctly
    z_k = [beta * np.exp(2 * np.pi * 1.0j * i / k) for i in range(k)]
    unnorm_state = np.sqrt(z_k * np.exp(z_k))
    norm_state = unnorm_state / np.linalg.norm(unnorm_state)
    coef_int_expected = np.pad(norm_state, (0, 2**num_qubits - k))

    unnorm_state_prime = np.conjugate(unnorm_state)
    norm_state_prime = unnorm_state_prime / np.linalg.norm(unnorm_state_prime)
    coef_int_prime_expected = np.pad(norm_state_prime, (0, 2**num_qubits - k))

    circuit, circuit_prime = get_prep_int(matrix_norm, beta, epsilon)
    circuit, circuit_prime = export_to_qiskit(circuit), export_to_qiskit(circuit_prime)
    backend = Aer.get_backend("statevector_simulator")
    actual_state = execute(circuit, backend).result().get_statevector()
    actual_state_prime = execute(circuit_prime, backend).result().get_statevector()

    assert np.allclose(np.abs(coef_int_expected), np.abs(actual_state))
    assert np.allclose(np.abs(coef_int_prime_expected), np.abs(actual_state_prime))


def construct_dummy_cir():
    """Define an arbitrary gate to test with
    instead of matrix block encoding.
    """
    custom_cir = Circuit([ZZ(0.1)(0, 1)])
    norm = np.linalg.norm(custom_cir.to_unitary(), "fro")
    return norm, custom_cir


@pytest.mark.parametrize(
    "beta, epsilon, time",
    [
        (1.3, 1e-3, 0.1),
    ],
)
def test_inverse_blockencoding(beta, epsilon, time):
    matrix_norm, dummy_circuit = construct_dummy_cir()
    kappa = get_kappa(matrix_norm, time)
    K = get_num_of_grid_points(matrix_norm, epsilon, beta)
    total_qubits = dummy_circuit.n_qubits + ceil(np.log2(K)) + 2
    sel_inv = inverse_blockencoding(dummy_circuit, matrix_norm, time, beta, epsilon)

    # Note: the expected number of the 'custom_matrix' repetitions is 1 less than
    # the degree of the approximating polynomial because of the
    # QSP construction procedure.
    expected_num_of_custom_gates = get_degree(kappa, epsilon) - 1
    actual_num_of_custom_gates = sum(
        1
        for op in sel_inv.operations
        if op.gate.name == "Control" and op.gate.wrapped_gate.name == "ZZ"
    )

    assert isinstance(sel_inv, Circuit)
    assert sel_inv.n_qubits == total_qubits
    assert expected_num_of_custom_gates == actual_num_of_custom_gates
