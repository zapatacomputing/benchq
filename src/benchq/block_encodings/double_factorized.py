from typing import Tuple
from openfermion.resource_estimates import df
import numpy as np


def get_toffoli_and_qubit_cost_for_double_factorized_block_encoding(
    n: int,
    lam: float,
    dE: float,
    L: int,
    Lxi: int,
    chi: int,
    beta: int,
    verbose: bool = False,
) -> Tuple[int, int]:
    """Get the Toffoli and qubit cost for the double factorized block encoding.
    
    Args:
        n: the number of spin-orbitals
        lam: the lambda-value for the Hamiltonian
        dE: allowable error in phase estimation
        L: the rank of the first decomposition
        Lxi: the total number of eigenvectors
        chi: equivalent to aleph_1 and aleph_2 in the document, the
            number of bits for the representation of the coefficients
        beta: equivalent to beth in the document, the number of bits
            for the rotations
        stps: an approximate number of steps to choose the precision of
            single qubit rotations in preparation of the equal superpositn state
        verbose: do additional printing of intermediates?
    
    Returns:
        A tuple whose first element is the number of Toffolis required for a controlled
            implementation of the block encoding, and whose second element is the number
            of qubits required for the block encoding (not including the qubit) it would
            typically be controlled on.
        """

    # In the df.compute_cost(...) function below, we set dE = 1 since this input doesn't
    # matter for us. We are only interested in the cost of implementing the quantum walk
    # operator, not the cost of QPE which depends on dE. Recall, dE determines the
    # precision of the QPE output which depends on the number of ancilla qubits in the
    # energy register.

    dE = 1
    initial_step_cost, _, _ = df.compute_cost(
        n, lam, dE, L, Lxi, chi, beta, stps=20000, verbose=False
    )

    step_cost, total_cost, ancilla_cost = df.compute_cost(
        n, lam, dE, L, Lxi, chi, beta, stps=initial_step_cost, verbose=False
    )

    # Now, we will remove the ancilla qubits in the energy register in QPE, and only add one using Guoming's algorithm.
    # The number of steps in Heisenberg-Limited QPE, i.e., 2^m.
    iters = np.ceil(np.pi * lam / (dE * 2))

    # Number of control qubits in the energy register
    m = 2 * np.ceil(np.log2(iters)) - 1

    ancilla_cost = ancilla_cost - m

    return step_cost, ancilla_cost
