###############################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
###############################################################################

import pytest

from benchq.algorithms.lde_solver import get_degree


@pytest.mark.parametrize(
    "kappa, epsilon, expected_result",
    [
        (1, 1e-1, 3),
        (1, 1e-3, 7),
        (10, 1e-3, 80),
        (10, 1e-6, 128),
        (20, 1e-6, 269),
        (30, 1e-6, 415),
        (40, 1e-6, 564),
        (10, 1e-14, 254),
        (20, 1e-14, 521),
    ],
)
def test_get_degree(kappa, epsilon, expected_result):
    result = get_degree(kappa, epsilon)
    assert result == expected_result
