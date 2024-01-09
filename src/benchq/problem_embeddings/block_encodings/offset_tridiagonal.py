import numpy as np
from orquestra.quantum.circuits import RY, Circuit, H

from .offset_tridiagonal_utils import controlled_clock, x_conj_gate


def get_offset_tridagonal_block_encoding(
    n: int, a: float, b: float, c: float
) -> Circuit:
    """Constructs the block-encoding of the offset tridiagonal matrix with
    parameters a, b, c. The offset tridagonal matrix M looks like:

        [ a  0  c  0       ]
        [ 0  a  0  c       ]
    M = [ b  0  a  . . .   ]
        [ 0  b   .  .  .  c]
        [        .  .  a  0]
        [           b  0  a]

    where 0 <= a <= 0.5, |b| <= .25, and |c| <= .25. The matrix is placed in the
    upper left n x n corner of the matrix provided by the circuit.

    This is based on a translation of the MATLAB code provided by Daan Camps at
    https://github.com/QuantumComputingLab/explicit-block-encodings
    and is explained in the paper by  D. Camps, L. Lin, R. Van Beeumen, C. Yang
    explicit quantum circuits for block encodings of certain sparse matrices. 2022.
    https://doi.org/10.48550/arXiv.2203.10236
    """
    assert 0 <= a <= 0.5
    assert abs(b) <= 0.25
    assert abs(c) <= 0.25

    a, b, c = a * 4, b * 4, c * 4

    D = Circuit([H(1), H(2)])

    theta0 = 2 * np.arccos(a - 1)
    theta1 = 2 * np.arccos(b)
    theta2 = 2 * np.arccos(c)

    OA = Circuit()
    OA += x_conj_gate([1, 2], RY(theta0).controlled(2)(1, 2, 0))
    OA += x_conj_gate([1], RY(theta1).controlled(2)(1, 2, 0))
    OA += x_conj_gate([2], RY(theta2).controlled(2)(1, 2, 0))
    OA += x_conj_gate(
        [1], RY(np.pi - theta1).controlled(n + 3)(*reversed(range(n + 4)))
    )
    OA += x_conj_gate(
        range(2, n + 4),
        RY(np.pi - theta2).controlled(n + 3)(*reversed(range(n + 4))),
    )

    OC = Circuit()
    OC += controlled_clock(n, list(range(3, n + 3)), [2], direction="forward")
    OC += controlled_clock(n, list(range(3, n + 3)), [1], direction="backward")

    circuit = Circuit()
    circuit += D
    circuit += OA
    circuit += OC
    circuit += D

    return circuit
