import math

from orquestra.quantum.circuits import Circuit

from benchq.block_encodings.block_encoding_utils import controlled_clock


def get_add_l(L) -> Circuit:
    add_l_circuit = Circuit()
    for _ in range(L):
        size = math.ceil(math.log2(L)) + 1
        add_l_circuit += controlled_clock(size)

    return add_l_circuit


def get_add_dagger(L) -> Circuit:
    add_dagger_circuit = Circuit()
    size = math.ceil(math.log2(L)) + 1
    add_dagger_circuit = controlled_clock(size, direction="backward")
    return add_dagger_circuit
