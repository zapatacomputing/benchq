import numpy as np
import pytest
from orquestra.quantum.circuits import RX, RY, RZ, Circuit, Dagger, H, I, S, T, Z

from benchq.compilation import simplify_rotations


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
    ],
)
def test_simplify_rotation_handles_rotation_gates(input_circuit, output_circuit):
    simplified_circuit = simplify_rotations(input_circuit)
    assert simplified_circuit == output_circuit


@pytest.mark.parametrize(
    "angle,output_gate",
    [
        (0, I),
        (np.pi / 4, T),
        (np.pi / 2, S),
        (np.pi, Z),
        (-np.pi / 4, Dagger(T)),
        (-np.pi / 2, Dagger(S)),
        (-np.pi, Z),
    ],
)
def test_simplify_rotation_handles_special_angles(angle, output_gate):
    qubit_id = 0
    circuit = Circuit([RZ(angle)(qubit_id)])
    simplified_circuit = simplify_rotations(circuit)
    assert simplified_circuit == Circuit([output_gate(qubit_id)])
