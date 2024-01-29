import math

import numpy as np
import pytest

from benchq.problem_embeddings.block_encodings.offset_tridiagonal_utils import (
    controlled_clock,
)


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
