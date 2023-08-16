import math

import numpy as np
from orquestra.quantum.circuits import Circuit

from benchq.block_encodings.block_encoding_utils import controlled_clock


def get_add_l(L) -> Circuit:
    size = math.ceil(math.log2(L)) + 1
    add_l_circuit = Circuit(n_qubits=size)
    for _ in range(L):
        add_l_circuit += controlled_clock(size)
    return add_l_circuit


def get_add_dagger(L) -> Circuit:
    size = math.ceil(math.log2(L)) + 1
    add_dagger_circuit = controlled_clock(size, direction="backward")
    return add_dagger_circuit
