import os
import pathlib
import re
import subprocess
from typing import Iterable

import numpy as np
from orquestra.quantum.circuits import (
    RZ,
    Circuit,
    ControlledGate,
    Dagger,
    GateOperation,
    H,
    S,
    T,
    Z,
    I,
)
from orquestra.quantum.decompositions import decompose_orquestra_circuit
from orquestra.quantum.decompositions._decomposition import DecompositionRule

from ..conversions._circuit_translations import import_circuit


def simplify_rotations(circuit) -> Circuit:
    """Changes RX and RY to RZ.
    Also, translates rotations with some characteristic angles (-pi, -pi/2, -pi/4, 0, pi/4, pi/2, pi) to simpler gates
    """
    circuit = import_circuit(circuit)
    return decompose_orquestra_circuit(
        circuit, [RXtoRZ(), RYtoRZ(), DecomposeStandardRZ()]
    )


class DecomposeRZNaively(DecompositionRule[GateOperation]):
    """Decomposes RZ with characteristic angles to regular gates."""

    def predicate(self, operation: GateOperation) -> bool:
        return operation.gate.name in ["RZ"]

    def production(self, operation: GateOperation) -> Iterable[GateOperation]:
        q_index = operation.qubit_indices[0]
        return [H(q_index), T(q_index), S(q_index), H(q_index), T(q_index), H(q_index)]


class DecomposeStandardRZ(DecompositionRule[GateOperation]):
    """Decomposes RZ with characteristic angles to regular gates."""

    def predicate(self, operation: GateOperation) -> bool:
        special_angles = [
            0,
            np.pi / 4,
            np.pi / 2,
            np.pi,
            -np.pi / 4,
            -np.pi / 2,
            -np.pi,
        ]
        return (
            operation.gate.name in ["RZ"]
            and np.isclose(operation.params[0], special_angles).any()
        )

    def production(self, operation: GateOperation) -> Iterable[GateOperation]:
        theta = operation.params[0]
        if np.isclose(theta, 0):
            return [I(*operation.qubit_indices)]
        elif np.isclose(theta, np.pi / 4):
            return [T(*operation.qubit_indices)]
        elif np.isclose(theta, np.pi / 2):
            return [S(*operation.qubit_indices)]
        elif np.isclose(theta, np.pi) or np.isclose(theta, -np.pi):
            return [Z(*operation.qubit_indices)]
        elif np.isclose(theta, -np.pi / 4):
            return [Dagger(T)(*operation.qubit_indices)]
        elif np.isclose(theta, -np.pi / 2):
            return [Dagger(S)(*operation.qubit_indices)]
        else:
            raise Exception(
                "This shouldn't happen! It means there's a bug in DecomposeStandardRZ function."
            )


class RXtoRZ(DecompositionRule[GateOperation]):
    """Decomposition of RX to RZ gate."""

    def predicate(self, operation: GateOperation) -> bool:
        # Only decompose U3 and its controlled version
        return (
            operation.gate.name == "RX"
            or isinstance(operation.gate, ControlledGate)
            and operation.gate.wrapped_gate.name == "RX"
        )

    def production(self, operation: GateOperation) -> Iterable[GateOperation]:
        theta = operation.params

        gate_decomposition = [H, RZ(theta), H]

        def preprocess_gate(gate):
            return (
                gate.controlled(operation.gate.num_control_qubits)
                if operation.gate.name == "Control"
                else gate
            )

        gate_operation_decomposition = [
            preprocess_gate(gate)(*operation.qubit_indices)
            for gate in gate_decomposition
        ]

        return reversed(gate_operation_decomposition)


class RYtoRZ(DecompositionRule[GateOperation]):
    """Decomposition of RY to RZ gate."""

    def predicate(self, operation: GateOperation) -> bool:
        # Only decompose U3 and its controlled version
        return (
            operation.gate.name == "RY"
            or isinstance(operation.gate, ControlledGate)
            and operation.gate.wrapped_gate.name == "RY"
        )

    def production(self, operation: GateOperation) -> Iterable[GateOperation]:
        theta = operation.params

        gate_decomposition = [Dagger(S), H, RZ(theta), H, S]

        def preprocess_gate(gate):
            return (
                gate.controlled(operation.gate.num_control_qubits)
                if operation.gate.name == "Control"
                else gate
            )

        gate_operation_decomposition = [
            preprocess_gate(gate)(*operation.qubit_indices)
            for gate in gate_decomposition
        ]

        return reversed(gate_operation_decomposition)
