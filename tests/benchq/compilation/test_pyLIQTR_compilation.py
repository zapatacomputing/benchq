################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
import numpy as np
import pytest
from cirq.circuits.circuit import Circuit as CirqCircuit
from cirq.devices.line_qubit import LineQubit
from cirq.ops.common_gates import CNOT as CirqCNOT
from cirq.ops.common_gates import H as CirqH
from numpy import linalg as LA
from orquestra.quantum.circuits import CNOT as OrquestraCNOT
from orquestra.quantum.circuits import RX, RZ
from orquestra.quantum.circuits import Circuit as OrquestraCircuit
from orquestra.quantum.circuits import H as OrquestraH
from qiskit.circuit import QuantumCircuit as QiskitCircuit

from benchq.compilation.circuits import pyliqtr_transpile_to_clifford_t

two_qubit_qiskit_circuit = QiskitCircuit(2)
two_qubit_qiskit_circuit.cx(0, 1)
two_qubit_qiskit_circuit.h(0)


@pytest.mark.parametrize(
    "circuit",
    [
        two_qubit_qiskit_circuit,
        CirqCircuit([CirqCNOT(LineQubit(0), LineQubit(1)), CirqH(LineQubit(0))]),
    ],
)
def test_clifford_circuit_produces_correct_output(circuit):
    """Tests that clifford circuits are unchanged"""
    assert pyliqtr_transpile_to_clifford_t(
        circuit, gate_precision=0.001
    ) == OrquestraCircuit([OrquestraCNOT(0, 1), OrquestraH(0)])


@pytest.mark.parametrize("gate_precision", [1e-3, 1e-6, 1e-10, 1.2e-6])
@pytest.mark.parametrize(
    "circuit",
    [
        OrquestraCircuit([RZ(0.1)(0)]),
        OrquestraCircuit([RZ(0.1)(0), OrquestraCNOT(0, 1), RX(0.3)(0)]),
    ],
)
def test_non_clifford_gates_compile(circuit, gate_precision):
    target_unitary = circuit.to_unitary()
    compiled_circuit = pyliqtr_transpile_to_clifford_t(
        circuit, gate_precision=gate_precision
    )
    compiled_unitary = compiled_circuit.to_unitary()
    distance_from_target = (
        LA.norm(mod_out_phase(target_unitary) - mod_out_phase(compiled_unitary), 2) / 2
    )  # normalize with 2 because we are using the 2 norm rather than diamond norm
    assert distance_from_target < gate_precision ** (1 / len(circuit.operations))


@pytest.mark.parametrize(
    "circuit, gate_precision, circuit_precision",
    [(OrquestraCircuit([RZ(0.1)(0)]), 1e-3, 1e-3)],
)
def test_user_cant_specify_both_gate_and_circuit_precision(
    circuit, gate_precision, circuit_precision
):
    with pytest.raises(ValueError):
        pyliqtr_transpile_to_clifford_t(
            circuit, gate_precision=gate_precision, circuit_precision=circuit_precision
        )


@pytest.mark.parametrize(
    "circuit, gate_precision, circuit_precision",
    [(OrquestraCircuit([RZ(0.1)(0)]), None, None)],
)
def test_user_didnt_specify_either_gate_or_circuit_precision(
    circuit, gate_precision, circuit_precision
):
    with pytest.raises(ValueError):
        pyliqtr_transpile_to_clifford_t(
            circuit, gate_precision=gate_precision, circuit_precision=circuit_precision
        )


def mod_out_phase(matrix):
    return matrix / np.exp(1j * np.angle(matrix[0][0]))
