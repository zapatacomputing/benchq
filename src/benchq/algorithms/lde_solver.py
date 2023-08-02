###############################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
###############################################################################
from math import ceil
from typing import Tuple

import numpy as np
from orquestra.integrations.qiskit.conversions import (
    export_to_qiskit,
    import_from_qiskit,
)
from orquestra.quantum.circuits import PHASE, RZ, SX, Circuit, X

from .lin_and_dong_qsp import build_qsp_circuit


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
    such that the polynomial is epsilon-close to the desired function.
    For the matrix inversion problem, the function to be approximated is 1/x.

    The formula is given by the equations (35)-(36) as described in the paper
    by Y. Dong, X. Meng, K. B. Whaley, and L. Lin.
    "Efficient Phase Factor Evaluation in Quantum Signal Processing".
    https://arxiv.org/pdf/2002.11649.pdf

    Note that in this implementation the degree of polynomial is devided
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


def get_prep(grid_point: int, k: int, beta: float) -> Tuple[Circuit, Circuit]:
    """Constructs unitaries that prepare states COEF_k and COEF_k_prime
        corresponding to the z_k.

    Args:
        grid_point (int): a current grid point of out the total k points.
        k (int): The number of the grid points to approximate the countour
            integral.
        beta (float): bounding parameter of the matrix.

    Returns:
        prep, prep_prime (Circuit): unitary corresponding to
            PREP and PREP_prime.
    """

    alpha = beta / 2.0
    theta = np.arcsin(np.sqrt((alpha) / (beta + alpha)))  # theta/2
    prep = Circuit()
    prep_prime = Circuit()
    phi = np.pi * grid_point / k

    # decompose using U3
    prep += PHASE(-3 * phi / 2 - theta / 2 - np.pi / 2)(0)
    prep += RZ(-phi + np.pi)(0)  # P gate
    prep += SX.dagger(0)
    prep += RZ(2 * theta + np.pi)(0)
    prep += SX(0)

    prep_prime += PHASE(-3 * phi / 2 - theta / 2 - np.pi / 2)(0)
    prep_prime += RZ(phi + np.pi)(0)
    prep_prime += SX.dagger(0)
    prep_prime += RZ(-2 * theta + np.pi)(0)
    prep_prime += SX(0)

    return prep, prep_prime


def control_prep(k: int, beta: float) -> Tuple[Circuit, Circuit]:
    """Constructs the control-PREP and control-PREP_prime unitaries.

    Args:
        k (int): The numper of the grid points to approximate
            the countour integral.
        beta (float): bounding parameter of the matrix.

    Returns:
        c_prep, c_prep_prime (Circuit): control-unitaries of
            PREP and PREP_prime.
    """

    if k <= 0:
        raise ValueError("The number of grid points should be non-negative.")

    n_controlled_qubits = int(np.ceil(np.log2(k)))
    c_prep = Circuit()
    c_prep_prime = Circuit()

    for grid_point in range(k):
        binary = bin(grid_point)[2::]
        reversed_bin = binary[::-1]
        ones = [ind for ind, digit in enumerate(reversed_bin) if digit == "1"]

        c_prep += Circuit([X(i) for i in range(n_controlled_qubits) if i not in ones])
        c_prep_prime += Circuit(
            [X(i) for i in range(n_controlled_qubits) if i not in ones]
        )

        prep, prep_prime = get_prep(grid_point, k, beta)
        for qubit in range(n_controlled_qubits):
            prep = prep.controlled(qubit)
            prep_prime = prep_prime.controlled(qubit)

        c_prep += prep
        c_prep_prime += prep_prime
        c_prep += Circuit([X(i) for i in range(n_controlled_qubits) if i not in ones])
        c_prep_prime += Circuit(
            [X(i) for i in range(n_controlled_qubits) if i not in ones]
        )

    return c_prep, c_prep_prime


def inverse_blockencoding(
    be_matrix: Circuit, matrix_norm: float, time: float, beta: float, epsilon: float
) -> Circuit:
    """Construct SEL_inv, an inverse of block encoding, utilizing the QSP.

    Args:
        be_matrix (Circuit): the block encoding of a matrix.
        matrix_norm (float): the norm of the matrix that is
            to be block encoded.
        time (float): the time interval one seeks solution
            for a differntial equation.
        beta (float): a bounding parameter of the matrix.
        epsilon (float): an accuracy for the polynomial approximation.

        Returns:
            sel_inverse (Circuit): an instance of oqquestra quantum circuit
                representing the inverse of block encoding.
    """

    # number of grid points
    k = get_num_of_grid_points(matrix_norm, epsilon, beta)
    kappa = get_kappa(matrix_norm, time)
    num_phis = get_degree(kappa, epsilon)
    # generate arbitrary phases
    phi_seq = np.linspace(-np.pi, np.pi, num_phis)

    prep, prep_prime = control_prep(k=k, beta=beta)
    prep_prime_dag = prep_prime.inverse()
    grid_qubits = ceil(np.log2(k)) + 1

    # contruct the circuit representing SEL
    sel = Circuit()
    sel += prep
    shifted_be_matrix = Circuit(
        [
            op.gate(*[qubit + grid_qubits for qubit in op.qubit_indices])
            for op in be_matrix.operations
        ]
    )
    shifted_be_matrix = shifted_be_matrix.controlled(grid_qubits - 1)
    sel += shifted_be_matrix
    sel += prep_prime_dag

    # Construct QSP circuit in Qiskit
    qsp_qubits = sel.n_qubits + 1
    qiskit_sel = export_to_qiskit(sel)
    sel_inverse = build_qsp_circuit(qsp_qubits, qiskit_sel, phi_seq, realpart=True)

    return import_from_qiskit(sel_inverse)
