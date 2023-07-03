from typing import Iterable

import numpy as np
from orquestra.quantum.circuits import (
    CNOT,
    RZ,
    SX,
    Circuit,
    ControlledGate,
    Dagger,
    GateOperation,
    H,
    I,
    S,
    T,
    Z,
)
from orquestra.quantum.decompositions import decompose_orquestra_circuit
from orquestra.quantum.decompositions._decomposition import DecompositionRule

from ..conversions._circuit_translations import import_circuit


def transpile_to_native_gates(circuit) -> Circuit:
    """Traspile common gates to clifford + RZ gates.
    Changes RX, RY, and U3 to RZ. Changes CCX to T gates.
    Also, translates rotations with some characteristic angles
    (-pi, -pi/2, -pi/4, 0, pi/4, pi/2, pi) to simpler gates.
    """
    circuit = import_circuit(circuit)
    return decompose_orquestra_circuit(
        circuit,
        [CCZtoT(), U3toRZ(), RXtoRZ(), RYtoRZ(), DecomposeStandardRZ()],
    )


class DecomposeStandardRZ(DecompositionRule[GateOperation]):
    """Decomposes RZ with characteristic angles to regular gates."""

    def predicate(self, operation: GateOperation) -> bool:
        if not isinstance(operation, GateOperation):
            return False
        special_angles = [
            0,
            np.pi / 4,
            np.pi / 2,
            3 * np.pi / 4,
            np.pi,
            -np.pi / 4,
            -np.pi / 2,
            -3 * np.pi / 4,
            -np.pi,
        ]
        theta = float(operation.params[0]) if len(operation.params) > 0 else None  # type: ignore # noqa: E501
        return bool(
            (operation.gate.name in ["RZ"] and np.isclose(theta, special_angles).any())  # type: ignore # noqa: E501
        )

    def production(self, operation: GateOperation) -> Iterable[GateOperation]:
        theta = float(operation.params[0])  # type: ignore
        if np.isclose(theta, 0):
            return [I(*operation.qubit_indices)]
        elif np.isclose(theta, np.pi / 4):
            return [T(*operation.qubit_indices)]
        elif np.isclose(theta, np.pi / 2):
            return [S(*operation.qubit_indices)]
        elif np.isclose(theta, 3 * np.pi / 4):
            return [S(*operation.qubit_indices), T(*operation.qubit_indices)]
        elif np.isclose(theta, np.pi) or np.isclose(theta, -np.pi):
            return [Z(*operation.qubit_indices)]
        elif np.isclose(theta, -np.pi / 4):
            return [Dagger(T)(*operation.qubit_indices)]
        elif np.isclose(theta, -np.pi / 2):
            return [Dagger(S)(*operation.qubit_indices)]
        elif np.isclose(theta, -3 * np.pi / 4):
            return [
                Dagger(S)(*operation.qubit_indices),
                Dagger(T)(*operation.qubit_indices),
            ]
        else:
            raise RuntimeError(
                "This shouldn't happen! It means there's a bug in "
                "DecomposeStandardRZ function."
            )


class RXtoRZ(DecompositionRule[GateOperation]):
    """Decomposition of RX to RZ gate."""

    def predicate(self, operation: GateOperation) -> bool:
        if not isinstance(operation, GateOperation):
            return False
        # Only decompose U3 and its controlled version
        return (
            operation.gate.name == "RX"
            or isinstance(operation.gate, ControlledGate)
            and operation.gate.wrapped_gate.name == "RX"
        )

    def production(self, operation: GateOperation) -> Iterable[GateOperation]:
        theta = operation.params[0]

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
        if not isinstance(operation, GateOperation):
            return False
        # Only decompose U3 and its controlled version
        return (
            operation.gate.name == "RY"
            or isinstance(operation.gate, ControlledGate)
            and operation.gate.wrapped_gate.name == "RY"
        )

    def production(self, operation: GateOperation) -> Iterable[GateOperation]:
        theta = operation.params[0]

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


class U3toRZ(DecompositionRule[GateOperation]):
    """Decomposition of U3 into RX and RZ gates."""

    def predicate(self, operation: GateOperation) -> bool:
        if not isinstance(operation, GateOperation):
            return False
        # Only decompose U3 and its controlled version
        return (
            operation.gate.name == "U3"
            or isinstance(operation.gate, ControlledGate)
            and operation.gate.wrapped_gate.name == "U3"
        )

    def production(self, operation: GateOperation) -> Iterable[GateOperation]:
        theta = operation.params[0]
        phi = operation.params[1]
        lam = operation.params[2]

        # ignore global phase as it's not relevant to gsc
        gate_decomposition = [
            RZ(phi),
            Z,
            SX,
            RZ(theta),
            Z,
            SX,
            RZ(lam),
        ]

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


class CCZtoT(DecompositionRule[GateOperation]):
    """Decomposition of U3 into RX and RZ gates."""

    def predicate(self, operation: GateOperation) -> bool:
        if not isinstance(operation, GateOperation):
            return False
        # Only decompose CCZ
        if operation.gate.name == "Control":
            assert isinstance(operation.gate, ControlledGate)
            if (
                operation.gate.wrapped_gate.name == "X"
                and operation.gate.num_control_qubits == 2
            ) or (
                operation.gate.wrapped_gate.name == "CNOT"
                and operation.gate.num_control_qubits == 1
            ):
                return True

        return False

    def production(self, operation: GateOperation) -> Iterable[GateOperation]:
        qubit_1, qubit_2, qubit_3 = operation.qubit_indices

        gate_operation_decomposition = [
            H(qubit_3),
            CNOT(qubit_2, qubit_3),
            T.dagger(qubit_3),
            CNOT(qubit_1, qubit_3),
            T(qubit_3),
            CNOT(qubit_2, qubit_3),
            T.dagger(qubit_3),
            CNOT(qubit_1, qubit_3),
            T(qubit_2),
            T(qubit_3),
            H(qubit_3),
            CNOT(qubit_1, qubit_2),
            T.dagger(qubit_2),
            T(qubit_1),
            CNOT(qubit_1, qubit_2),
        ]

        return reversed(gate_operation_decomposition)
