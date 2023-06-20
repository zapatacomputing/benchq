################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
from functools import singledispatch
from typing import Optional

from cirq.circuits import Circuit as CirqCircuit
from orquestra.integrations.cirq.conversions import export_to_cirq, import_from_cirq
from orquestra.integrations.qiskit.conversions import (
    export_to_qiskit,
    import_from_qiskit,
)
from orquestra.quantum.circuits import Circuit as OrquestraCircuit
from orquestra.quantum.evolution import time_evolution as old_time_evolution
from orquestra.quantum.operators import PauliRepresentation
from qiskit.circuit import QuantumCircuit as QiskitCircuit


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


def time_evolution(
    hamiltonian: PauliRepresentation,
    time: float,
    method: str = "Trotter",
    trotter_order: int = 1,
    circuit_type: type = OrquestraCircuit,
) -> OrquestraCircuit:
    """Time evolution of a quantum circuit.

    Args:
        circuit: The quantum circuit to evolve.
        hamiltonian: The Hamiltonian to evolve the circuit with.
        time: The time to evolve the circuit for.
        num_time_slices: The number of time slices to use.
        evolution_type: The type of evolution to perform. Defaults to "unitary".
        backend: The backend to use for the evolution. Defaults to None.
        **kwargs: Additional keyword arguments to pass to the backend.

    Returns:
        The evolved quantum circuit.
    """
    return export_circuit(
        circuit_type,
        old_time_evolution(
            hamiltonian,
            time,
            method,
            trotter_order,
        ),
    )
