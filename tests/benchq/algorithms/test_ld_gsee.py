################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
import numpy as np
import pytest

from benchq.algorithms.ld_gsee import (
    get_ld_gsee_max_evolution_time,
    get_ld_gsee_num_circuit_repetitions,
)


@pytest.mark.parametrize(
    "alpha,energy_gap,square_overlap,precision,expected_result",
    [
        (1, 1, 1, 1, 5 / np.pi * np.sqrt(2 * np.log(16 * np.sqrt(2 / np.pi)))),
        (1, 10, 1, 10, 1 / 2 / np.pi * np.sqrt(2 * np.log(16 * np.sqrt(2 / np.pi)))),
    ],
)
def test_get_ld_gsee_num_iterations(
    alpha, energy_gap, square_overlap, precision, expected_result
):
    np.testing.assert_allclose(
        get_ld_gsee_max_evolution_time(alpha, energy_gap, square_overlap, precision),
        expected_result,
    )


@pytest.mark.parametrize(
    "alpha,energy_gap,square_overlap,precision,failure_probability,expected_result",
    [
        (1, 1, 1, 1, 1, 128 / np.pi * np.log(4 * 2)),
        (1, 10, 1, 10, 1, 128 / np.pi * np.log(4 * 2)),
    ],
)
def test_get_ld_gsee_num_circuit_repetitions(
    alpha, energy_gap, square_overlap, precision, failure_probability, expected_result
):
    np.testing.assert_allclose(
        get_ld_gsee_num_circuit_repetitions(
            alpha, energy_gap, square_overlap, precision, failure_probability
        ),
        expected_result,
    )
