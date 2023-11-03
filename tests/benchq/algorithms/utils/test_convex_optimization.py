###############################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
###############################################################################
import pytest

from benchq.problem_embedding.qsp.get_qsp_polynomial import optimize_chebyshev_coeff


@pytest.mark.parametrize(
    "error, delta, gamma_prime, degree_expected",
    [
        (0.01, 0.05, 5, 25),
        (1, 0.05, 5, 3),
    ],
)
def test_convex_optimization(error, delta, gamma_prime, degree_expected):
    _, _, degree = optimize_chebyshev_coeff(error, delta, gamma_prime)
    assert degree_expected == degree
