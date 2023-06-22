#####################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
"""Tools for the Fourier-Filtered Low-Depth Ground State Energy Estimation (FF-LD-GSEE) algorithm (arXiv:2209.06811v2)."""

import numpy as np


def _get_sigma(
    alpha: float, energy_gap: float, lam: float, eta: float, DE: float
) -> float:
    """Get the standard deviation of the Gaussian convolution function (Eq. 15 of arXiv:2209.06811v2)."""
    epsilon = DE / lam
    delta = epsilon**alpha * energy_gap ** (1 - alpha)
    return min(
        0.9 * delta / (np.sqrt(2 * np.log(9 * delta * epsilon ** (-1) * eta ** (-1)))),
        0.2 * delta,
    )


def _get_epsilon_1(epsilon: float, eta: float, sigma: float) -> float:
    """Get the error with respect to the convolution function (Eq. 28 of arXiv:2209.06811v2)."""
    return 0.1 * epsilon * eta / (np.sqrt(2 * np.pi) * sigma**3)


def get_ldgsee_num_iterations(sigma: float, epsilon_1: float) -> float:
    """Get the number of iterations for the FF-LD-GSEE algorithm (Eq. 34 of arXiv:2209.06811v2)."""
    return (
        np.pi ** (-1)
        * sigma ** (-1)
        * np.sqrt(2 * np.log(8 * np.pi ** (-1) * epsilon_1 ** (-1) * sigma ** (-2)))
    )


def get_ldgsee_num_circuit_repetitions(
    epsilon: float, sigma: float, epsilon_1: float, failure_probability: float
) -> float:
    """Get the number of circuit repetitions for the FF-LD-GSEE algorithm."""

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
