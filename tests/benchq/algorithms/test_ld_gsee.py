import numpy as np
import pytest

from benchq.algorithms.ld_gsee import (
    get_epsilon_1,
    get_ldgsee_num_circuit_repetitions,
    get_ldgsee_num_iterations,
    get_ldgsee_num_qubits,
    get_sigma,
)


def test_get_sigma_scales_with_energy():
    alpha = 0.5
    eta = 1
    epsilon = 1
    delta_true = 1
    scale_factor = 10
    assert np.isclose(
        get_sigma(alpha, scale_factor * delta_true, eta, scale_factor * epsilon),
        scale_factor * get_sigma(alpha, delta_true, eta, epsilon),
    )


@pytest.mark.parametrize(
    "num_block_encoding_qubits,expected_result", [(1, 2), (2, 3), (3, 4)]
)
def test_get_ldgsee_num_circuit_qubits(num_block_encoding_qubits, expected_result):
    assert get_ldgsee_num_qubits(num_block_encoding_qubits) == expected_result
