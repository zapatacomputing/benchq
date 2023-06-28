import numpy as np
import pytest

from benchq.algorithms.ld_gsee import (
    get_ldgsee_num_circuit_repetitions,
    get_ldgsee_num_iterations,
)


@pytest.mark.parametrize(
    "alpha,delta_true,eta,epsilon,expected_result",
    [
        (1, 1, 1, 1, 5 / np.pi * np.sqrt(2 * np.log(16 * np.sqrt(2 / np.pi)))),
        (1, 10, 1, 10, 1 / 2 / np.pi * np.sqrt(2 * np.log(16 * np.sqrt(2 / np.pi)))),
    ],
)
def test_get_ldgsee_num_iterations(alpha, delta_true, eta, epsilon, expected_result):
    assert np.isclose(
        get_ldgsee_num_iterations(alpha, delta_true, eta, epsilon), expected_result
    )


@pytest.mark.parametrize(
    "alpha,delta_true,eta,epsilon,failure_probability,expected_result",
    [
        (1, 1, 1, 1, 1, 128 / np.pi * np.log(4 * 2)),
        (1, 10, 1, 10, 1, 128 / np.pi * np.log(4 * 2)),
    ],
)
def test_get_ldgsee_num_circuit_repetitions(
    alpha, delta_true, eta, epsilon, failure_probability, expected_result
):
    assert np.isclose(
        get_ldgsee_num_circuit_repetitions(
            alpha, delta_true, eta, epsilon, failure_probability
        ),
        expected_result,
    )
