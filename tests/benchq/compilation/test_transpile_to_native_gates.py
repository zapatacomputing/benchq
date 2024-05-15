import numpy as np
import pytest
from orquestra.quantum.circuits import (
    CNOT,
    CZ,
    RX,
    RY,
    RZ,
    SX,
    U3,
    Circuit,
    Dagger,
    H,
    I,
    S,
    T,
    X,
    Z,
)

from benchq.compilation.circuits import compile_to_native_gates

TOFFOLI_DECOMPOSITION = [
    H(2),
    CNOT(1, 2),
    T.dagger(2),
    CNOT(0, 2),
    T(2),
    CNOT(1, 2),
    T.dagger(2),
    CNOT(0, 2),
    T(1),
    T(2),
    H(2),
    CNOT(0, 1),
    T.dagger(1),
    T(0),
    CNOT(0, 1),
]

CCZ_DECOMPOSITION = [
    CNOT(1, 2),
    T.dagger(2),
    CNOT(0, 2),
    T(2),
    CNOT(1, 2),
    T.dagger(2),
    CNOT(0, 2),
    T(1),
    T(2),
    CNOT(0, 1),
    T.dagger(1),
    T(0),
    CNOT(0, 1),
]


@pytest.mark.parametrize(
    "input_circuit,output_circuit",
    [
        (Circuit([RZ(np.pi / 5)(0)]), Circuit([RZ(np.pi / 5)(0)])),
        (
            Circuit([RX(np.pi / 5)(0)]),
            Circuit([H(0), RZ(np.pi / 5)(0), H(0)]),
        ),
        (
            Circuit([RY(np.pi / 5)(0)]),
            Circuit([S(0), H(0), RZ(np.pi / 5)(0), H(0), Dagger(S)(0)]),
        ),
        (
            Circuit([U3(np.pi / 5, np.pi / 6, np.pi / 7)(0)]),
            Circuit(
                reversed(
                    [
                        RZ(np.pi / 5)(0),
                        Z(0),
                        SX(0),
                        RZ(np.pi / 6)(0),
                        Z(0),
                        SX(0),
                        RZ(np.pi / 7)(0),
                    ]
                )
            ),
        ),
        (
            Circuit([X.controlled(2)(0, 1, 2)]),
            Circuit(TOFFOLI_DECOMPOSITION),
        ),
        (
            Circuit([CNOT.controlled(1)(0, 1, 2)]),
            Circuit(TOFFOLI_DECOMPOSITION),
        ),
        (
            Circuit([Z.controlled(2)(0, 1, 2)]),
            Circuit(CCZ_DECOMPOSITION),
        ),
        (
            Circuit([CZ.controlled(1)(0, 1, 2)]),
            Circuit(CCZ_DECOMPOSITION),
        ),
    ],
)
def test_simplify_rotation_handles_rotation_gates(input_circuit, output_circuit):
    simplified_circuit = compile_to_native_gates(input_circuit)
    assert simplified_circuit == output_circuit


@pytest.mark.parametrize(
    "angle,output_gates",
    [
        (0, [I]),
        (np.pi / 4, [T]),
        (np.pi / 2, [S]),
        (3 * np.pi / 4, [S, T]),
        (np.pi, [Z]),
        (-np.pi / 4, [Dagger(T)]),
        (-np.pi / 2, [Dagger(S)]),
        (-3 * np.pi / 4, [Dagger(S), Dagger(T)]),
        (-np.pi, [Z]),
    ],
)
def test_simplify_rotation_handles_special_angles(angle, output_gates):
    qubit_id = 0
    circuit = Circuit([RZ(angle)(qubit_id)])
    simplified_circuit = compile_to_native_gates(circuit)
    assert simplified_circuit == Circuit(
        [output_gate(qubit_id) for output_gate in output_gates]
    )
