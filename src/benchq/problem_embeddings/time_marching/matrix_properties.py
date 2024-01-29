from math import ceil

import numpy as np


def get_kappa(matrix_norm: float, time_interval: float) -> float:
    """Bounds the value of the matrix Xi condition number.
    kappa <= exp(2||p(A)||),
    where ||p(A)|| <= time_interval * ||A|| for time independent matrix A.

    Args:
        matrix_norm (float): Frobenius norm of a matrix A.
        time_interval (float): time interval of the differential equation.

    Returns:
        kappa (float): the condition number of Xi.
    """
    return np.exp(2 * time_interval * matrix_norm)


def get_degree(kappa: float, epsilon: float) -> int:
    """Calculates an estimation of the degree of an approximating polynomial
    such that the polynomial is epsilon-close to the desired function f(x) = 1/x
    (matrix inversion problems).

    The formula is given by the equations (35)-(36) as described in the paper
    by Y. Dong, X. Meng, K. B. Whaley, and L. Lin.
    "Efficient Phase Factor Evaluation in Quantum Signal Processing".
    https://arxiv.org/pdf/2002.11649.pdf

    Note that in this implementation the degree of polynomial is divided
    by the factor of 3 to reflect a result of a possible improvements
    by Remez algorithm: https://en.wikipedia.org/wiki/Remez_algorithm

    Args:
        kappa (float): the condition number of a matrix to be approximated
            by a polynomial.
        epsilon (float): a desired precision of the approximation
            (truncation error).

    Returns:
        degree (int): the degree of approximating polynomial.
    """

    b = ceil(kappa**2 * np.log(kappa / epsilon))
    degree = 2 * ceil(np.sqrt(b * np.log(4 * b / epsilon))) + 1

    return ceil(degree / 3)


def get_num_of_grid_points(matrix_norm: float, epsilon: float, beta: float) -> int:
    """Computes the bound for the number of grid points to approximate
    the countour integral.

    The formula is derived from the equation (62) as desribed in the paper
    S. Takahira, A. Ohashi, T. Sogabe, and T. S. Usuda.
    "Quantum algorithm for matrix functions by Cauchy’s integral formula."
    https://www.rintonpress.com/journals/doi/QIC20.1-2-2.html

    Args:
        matrix_norm (float): Frobenius norm of a matrix A.
        epsilon (float): a desired precision of the approximation.
        beta (float): bounding parameter of the matrix.

    Returns:
        num_points (int): the number of grid points.
    """

    f = (1 - 1 / beta) * matrix_norm / np.exp(matrix_norm)
    r = beta / matrix_norm
    num_points = max(1 / (1 - 1 / beta), 1 / (1 - r)) * np.log(8 / f / epsilon + 1)

    return int(num_points)
