#####################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
"""Tools for the Fourier-Filtered Low-Depth Ground State Energy Estimation (FF-LD-GSEE) algorithm (arXiv:2209.06811v2)."""

import numpy as np


def get_sigma(
    alpha: float, delta_true: float, eta: float, epsilon: float
) -> float:
    """Get the standard deviation of the Gaussian convolution function (Eq. 15 of
    arXiv:2209.06811v2).

    Arguments:
        alpha: The parameter alpha controlling the tradeoff between circuit repetitions
            and circuit depth. Zero corresponds to the minimum circuit depth, while one
            corresponds to the minimum number of circuit repetitions.
        delta_true: The energy gap of the Hamiltonian.
        lam: The one-norm of the Hamiltonian.
        eta: The square overlap of the initial state with the ground state.
        epsilon: The desired ground state energy accuracy.

    Returns: The standard deviation of the Gaussian convolution function."""
    delta = epsilon**alpha * delta_true ** (1 - alpha)
    return min(
        0.9 * delta / (np.sqrt(2 * np.log(9 * delta * epsilon ** (-1) * eta ** (-1)))),
        0.2 * delta,
    )


def get_epsilon_1(epsilon: float, eta: float, sigma: float) -> float:
    """Get the error with respect to the convolution function (Eq. 28 of
        arXiv:2209.06811v2).

    Arguments:
        epsilon: The error tolerance.
        eta: The error tolerance for the convolution function.
        sigma: The standard deviation of the Gaussian convolution function.

    Returns: The error with respect to the convolution function."""

    return 0.1 * epsilon * eta / (np.sqrt(2 * np.pi) * sigma**3)


def get_ldgsee_num_iterations(sigma: float, epsilon_1: float) -> float:
    """Get the number of iterations for the FF-LD-GSEE algorithm (Eq. 34 of
    arXiv:2209.06811v2).

    Arguments:
        sigma: The standard deviation of the Gaussian convolution function.
        epsilon_1: The error with respect to the convolution function.

    Returns: The estimated number of iterations required by the FF-LD-GSEE algorithm."""
    return (
        np.pi ** (-1)
        * sigma ** (-1)
        * np.sqrt(2 * np.log(8 * np.pi ** (-1) * epsilon_1 ** (-1) * sigma ** (-2)))
    )


def get_ldgsee_num_circuit_repetitions(
    epsilon: float, sigma: float, epsilon_1: float, failure_probability: float
) -> float:
    """Get the number of circuit repetitions for the FF-LD-GSEE algorithm.

    Arguments:
        epsilon: The error tolerance.
        sigma: The standard deviation of the Gaussian convolution function.
        epsilon_1: The error with respect to the convolution function.
        failure_probability: The failure probability.

    Returns: The estimated number of circuit repetitions required by the FF-LD-GSEE
        algorithm.."""

    # number of grid points along the x-axis
    M = np.ceil(sigma / epsilon) + 1

    return (
        (16 / np.pi**2)
        * np.log(4 * M / failure_probability)
        / (sigma**4 * epsilon_1**2)
    )


def get_ldgsee_num_qubits(num_block_encoding_qubits: int) -> int:
    """Get the number of qubits for the FF-LD-GSEE algorithm.

    Arguments:
        num_block_encoding_qubits: The number of logical qubits used for the block encoding.

    Returns: The number of logical qubits for the FF-LD-GSEE algorithm."""
    return num_block_encoding_qubits + 1
