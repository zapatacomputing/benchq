################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
from functools import singledispatch
from typing import Optional, Union

from cirq.circuits import Circuit as CirqCircuit
from orquestra.integrations.cirq.conversions import export_to_cirq, import_from_cirq
from orquestra.integrations.qiskit.conversions import (
    export_to_qiskit,
    import_from_qiskit,
)
from orquestra.quantum.circuits import Circuit as OrquestraCircuit
from qiskit.circuit import QuantumCircuit as QiskitCircuit

SUPPORTED_CIRCUITS = Union[QiskitCircuit, CirqCircuit, OrquestraCircuit]


def _reset_n_qubits_if_needed(
    circuit: OrquestraCircuit, original_n_qubits: Optional[int] = None
):
    return (
        circuit
        if original_n_qubits is None
        else OrquestraCircuit(circuit.operations, n_qubits=original_n_qubits)
    )


@singledispatch
def import_circuit(circuit, original_n_qubits: Optional[int] = None):
    """imports a circuit from a supported quantum framework."""
    raise NotImplementedError(f"Circuit type {type(circuit)} not supported")


@import_circuit.register
def _(circuit: QiskitCircuit, original_n_qubits: Optional[int] = None):
    return _reset_n_qubits_if_needed(import_from_qiskit(circuit), original_n_qubits)


@import_circuit.register
def _(circuit: CirqCircuit, original_n_qubits: Optional[int] = None):
    return _reset_n_qubits_if_needed(import_from_cirq(circuit), original_n_qubits)


@import_circuit.register
def _(circuit: OrquestraCircuit, original_n_qubits: Optional[int] = None):
    return _reset_n_qubits_if_needed(circuit, original_n_qubits)


def export_circuit(circuit_type, circuit: OrquestraCircuit):
    """Exports a circuit to a supported quantum framework."""
    if circuit_type == OrquestraCircuit:
        return circuit
    elif circuit_type == QiskitCircuit:
        return export_to_qiskit(circuit)
    elif circuit_type == CirqCircuit:
        return export_to_cirq(circuit)
    else:
        raise NotImplementedError(f"Circuit type {circuit_type} not supported")
