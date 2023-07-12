from typing import Tuple

import numpy as np
from orquestra.quantum.circuits import PHASE, RZ, SX, Circuit, X


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
