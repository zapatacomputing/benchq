################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
from functools import singledispatch

from cirq.circuits import Circuit as CirqCircuit
from orquestra.integrations.cirq.conversions import export_to_cirq, import_from_cirq
from orquestra.integrations.forest.conversions import (
    export_to_pyquil,
    import_from_pyquil,
)
from orquestra.integrations.qiskit.conversions import (
    export_to_qiskit,
    import_from_qiskit,
)
from orquestra.quantum.circuits import Circuit as OrquestraCircuit
from orquestra.quantum.evolution import time_evolution as old_time_evolution
from orquestra.quantum.operators import PauliRepresentation
from pyquil.quil import Program as PyquilCircuit
from qiskit.circuit import QuantumCircuit as QiskitCircuit


@singledispatch
def import_circuit(circuit):
    """imports a circuit from a supported quantum framework."""
    raise NotImplementedError(f"Circuit type {type(circuit)} not supported")


@import_circuit.register
def _(circuit: QiskitCircuit):
    return import_from_qiskit(circuit)


@import_circuit.register
def _(circuit: CirqCircuit):
    return import_from_cirq(circuit)


@import_circuit.register
def _(circuit: PyquilCircuit):
    return import_from_pyquil(circuit)


@import_circuit.register
def _(circuit: OrquestraCircuit):
    return circuit


def export_circuit(circuit_type, circuit: OrquestraCircuit):
    """Exports a circuit to a supported quantum framework."""
    if circuit_type == OrquestraCircuit:
        return circuit
    elif circuit_type == QiskitCircuit:
        return export_to_qiskit(circuit)
    elif circuit_type == CirqCircuit:
        return export_to_cirq(circuit)
    elif circuit_type == PyquilCircuit:
        return export_to_pyquil(circuit)
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
