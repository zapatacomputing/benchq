import math

import numpy as np
import pytest
from orquestra.quantum.circuits import Circuit

from benchq.algorithms.utils.compression_gadget import get_add_dagger, get_add_l
from benchq.block_encodings.block_encoding_utils import controlled_clock


@pytest.mark.parametrize(
    "L, target_unitary",
    [
        (2, np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])),
        (1, np.array([[1, 0], [0, 1]])),
        (
            3,
            np.array(
                [
                    [1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1],
                ]
            ),
        ),
    ],
)
def test_add_l_and_add_dagger(L, target_unitary):
    circuit = get_add_dagger(L)
    size = math.ceil(math.log2(L)) + 1
    get_add_dagger_l = Circuit(n_qubits=size)
    for _ in range(L):
        get_add_dagger_l += circuit
    ckt_add_l = get_add_l(L) + get_add_dagger_l
    test_unitary = ckt_add_l.to_unitary()

    assert np.allclose(test_unitary, target_unitary)


@pytest.mark.parametrize(
    "L, target_unitary",
    [
        (2, np.array([[0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])),
        (1, np.array([[0, 1], [1, 0]])),
        (
            3,
            np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0],
                ]
            ),
        ),
    ],
)
def test_add_l(L, target_unitary):
    circuit = get_add_dagger(L)
    size = math.ceil(math.log2(L)) + 1
    get_add_dagger_l = Circuit(n_qubits=size)
    for _ in range(L):
        get_add_dagger_l += circuit
    get_add_l_plus_one = get_add_l(L) + controlled_clock(size)
    ckt_add_l_plus_one = get_add_l_plus_one + get_add_dagger_l
    test_unitary = ckt_add_l_plus_one.to_unitary()

    assert np.allclose(test_unitary, target_unitary)


@pytest.mark.parametrize(
    "L, target_unitary",
    [
        (2, np.array([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0]])),
        (1, np.array([[0, 1], [1, 0]])),
        (
            3,
            np.array(
                [
                    [0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0],
                ]
            ),
        ),
    ],
)
def test_add_dagger(L, target_unitary):
    circuit = get_add_dagger(L)
    size = math.ceil(math.log2(L)) + 1
    get_add_dagger_l = Circuit(n_qubits=size)
    for _ in range(L):
        get_add_dagger_l += circuit
    get_add_dagger_plus_one = get_add_dagger_l + controlled_clock(
        size, direction="backward"
    )
    ckt_add_l = get_add_l(L) + get_add_dagger_plus_one
    test_unitary = ckt_add_l.to_unitary()

    assert np.allclose(test_unitary, target_unitary)


@pytest.mark.parametrize(
    "L, initial_vector, final_vector",
    [
        (2, np.array([1, 0, 0, 0]), np.array([0, 0, 1, 0])),
        (1, np.array([1, 0]), np.array([1, 0])),
        (
            3,
            np.array([1, 0, 0, 0, 0, 0, 0, 0]),
            np.array([0, 0, 1, 0, 0, 0, 0, 0]),
        ),
    ],
)
def test_controlled_clock_final_state(L, initial_vector, final_vector):
    size = math.ceil(math.log2(L)) + 1
    circuit = controlled_clock(size)
    circuit1 = circuit + controlled_clock(size)
    test_unitary = circuit1.to_unitary()
    exp_final_vector = np.matmul(test_unitary, initial_vector)
    assert np.allclose(exp_final_vector, final_vector)


@pytest.mark.parametrize(
    "L, initial_vector, final_vector",
    [
        (2, np.array([1, 0, 0, 0]), np.array([0, 0, 1, 0])),
        (3, np.array([1, 0, 0, 0, 0, 0, 0, 0]), np.array([0, 0, 0, 1, 0, 0, 0, 0])),
        (1, np.array([1, 0]), np.array([0, 1])),
        (3, np.array([1, 0, 0, 0, 0, 0, 0, 0]), np.array([0, 0, 0, 1, 0, 0, 0, 0])),
        (
            7,
            np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
        ),
    ],
)
def test_add_l_final_state(L, initial_vector, final_vector):
    circuit = get_add_l(L)
    test_unitary = circuit.to_unitary()
    exp_final_vector = np.matmul(test_unitary, initial_vector)
    assert np.allclose(exp_final_vector, final_vector)


@pytest.mark.parametrize(
    "L, initial_vector, final_vector",
    [
        (2, np.array([1, 0, 0, 0]), np.array([0, 0, 0, 1])),
        (1, np.array([1, 0]), np.array([0, 1])),
        (3, np.array([1, 0, 0, 0, 0, 0, 0, 0]), np.array([0, 0, 0, 0, 0, 0, 0, 1])),
    ],
)
def test_add_dagger_final_state(L, initial_vector, final_vector):
    # circuit = get_add_l(L)
    circuit = get_add_dagger(L)
    test_unitary = circuit.to_unitary()
    exp_final_vector = np.matmul(test_unitary, initial_vector)
    assert np.allclose(exp_final_vector, final_vector)


@pytest.mark.parametrize(
    "L, initial_vector, final_vector",
    [
        (2, np.array([1, 0, 0, 0]), np.array([0, 1, 0, 0])),
        (3, np.array([1, 0, 0, 0, 0, 0, 0, 0]), np.array([0, 0, 1, 0, 0, 0, 0, 0])),
        (1, np.array([1, 0]), np.array([1, 0])),
        (3, np.array([1, 0, 0, 0, 0, 0, 0, 0]), np.array([0, 0, 1, 0, 0, 0, 0, 0])),
        (
            7,
            np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            np.array([0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        ),
    ],
)
def test_add_dagger_final_state1(L, initial_vector, final_vector):
    circuit = get_add_l(L) + get_add_dagger(L)
    test_unitary = circuit.to_unitary()
    exp_final_vector = np.matmul(test_unitary, initial_vector)
    assert np.allclose(exp_final_vector, final_vector)


@pytest.mark.parametrize("L", [(1), (2), (8), (16)])
def test_controlled_clock_l_times_and_add_l(L):
    size = math.ceil(math.log2(L)) + 1
    circuit = Circuit(n_qubits=size)
    for _ in range(L):
        circuit += controlled_clock(size)
    circuit_add = get_add_l(L)
    assert np.allclose(circuit.to_unitary(), circuit_add.to_unitary())
