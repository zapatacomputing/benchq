###############################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
###############################################################################
# A convex optimization tool to solve for the coefficients in Chebyshev expansions
# using Python cvxpy package, and as described in
# "Time-marching based quantum solvers for time-dependent linear differential equations"
# (https://arxiv.org/abs/2208.06941)
from typing import Tuple

import cvxpy as cp
import numpy as np


def optimize_chebyshev_coeff(
    error: float, delta: float, gamma_prime: float, maxiter=1e3
) -> Tuple[np.ndarray, float, int]:
    """Solve a convex optimization problem for the coefficients in Chebyshev expansion
    such that the Chebyshev odd-degree polynomial approximates the desired
    function with a smallest degree possible.

    The convex optimization problem is solved only in the interval containing
    singular values of a block-encoded matrix.
    The implementation is based on the procedure as described in (Section 2.3) and
    (Appendix C) in the research papar (https://arxiv.org/abs/2208.06941).

    The optimization stops when the error or maximum number of iteration reached,
    whatever occurs first.

    Args:
        error (float): desired precision on the solution of the convex optimization
        problem. The error is the L_inf norn ('max(abs())').
        delta (float): is the overshooting parameter that arises from Gibbs phenomenon.
            Define: delta = 1/time_interval.
        gamma_prime (float): an amplification factor.
        maxiter (int): maximum number of iterations, optional stopping criteria.

    Returns:
        chebyshev_coeff (np.ndarray): coefficients of the expansion
            in terms of Chebyshev functions.
        epsilon (float): actual precision on the solution.
        degree (int): degree of approximating polynomial.
    """

    def chebychev_expansion(x, coeff):
        """Function that approximates a desired one using Chebyshev polynomials."""
        return [
            sum(
                coeff[k] * np.cos((2 * k + 1) * np.arccos(xi))
                for k in range((degree - 1) // 2)
            )
            for xi in x
        ]

    def exact_func(x):
        """Function we are trying to approximate."""
        return (1 - delta) * gamma_prime * x

    grid_points = 500
    mesh_size = 10000
    constraints_const = max(0.999, 1 - 0.1 * delta)
    # roots of Chebyshev's polynomial
    cheb_roots = [-np.cos(np.pi * j / (grid_points - 1)) for j in range(grid_points)]
    # non-zero roots to force interval constraints
    cheb_roots_reduced = [
        root for root in cheb_roots if root >= 0 and root <= 1 / gamma_prime
    ]

    degree = 3
    epsilon = 1.0
    iter_step = 0
    while True:
        coeff_k = cp.Variable((degree - 1) // 2)  # variables to optimize for
        approximation = cp.hstack(
            [
                cp.sum(
                    [
                        coeff_k[k] * np.cos((2 * k + 1) * np.arccos(cheb_root))
                        for k in range((degree - 1) // 2)
                    ]
                )
                for cheb_root in cheb_roots_reduced
            ]
        )
        # vectorizing constraints
        norm_constraint = []
        for cheb_root in cheb_roots:
            single = cp.sum(
                [
                    coeff_k[k] * np.cos((2 * k + 1) * np.arccos(cheb_root))
                    for k in range((degree - 1) // 2)
                ]
            )
            norm_constraint.append(cp.norm(single, "inf") <= constraints_const)

        target_val = cp.hstack(
            [exact_func(cheb_root) for cheb_root in cheb_roots_reduced]
        )
        objective = cp.Minimize(cp.norm(target_val - approximation, "inf"))
        problem = cp.Problem(objective, norm_constraint)
        problem.solve()

        if problem.status == "optimal":
            approximation_coeffs = coeff_k.value
            x = np.linspace(-1 / gamma_prime, 1 / gamma_prime, mesh_size)
            y_act = np.array([exact_func(xi) for xi in x])
            y_appr = np.array(chebychev_expansion(x, approximation_coeffs))
            epsilon = float(np.linalg.norm(y_act - y_appr, ord=np.inf))
            if epsilon <= error:
                print("Accuracy is reached.")
                return approximation_coeffs, epsilon, degree
            elif iter_step > maxiter:
                print("Max iterations is reached.")
                return approximation_coeffs, epsilon, degree
        else:
            raise Exception("Problem is not feasible.")
        degree += 2
        iter_step += 1
