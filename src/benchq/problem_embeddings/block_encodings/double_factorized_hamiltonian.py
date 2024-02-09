################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################

from typing import Tuple

import numpy as np
from openfermion.resource_estimates import df

from benchq.problem_ingestion.molecular_hamiltonians import compute_lambda_df

from ..qpe import _get_double_factorized_qpe_info


def get_double_factorized_hamiltonian_block_encoding(
    h1: np.ndarray,
    eri: np.ndarray,
    threshold: float,
    bits_precision_state_prep: int = 10,
    bits_precision_rotation: int = 20,
) -> Tuple[int, int, float]:
    """Get the Toffoli count, qubit cost, and the one-norm for the block encoding of
    double factorized hamiltonian as described in PRX Quantum 2, 030305. This function
    works by getting the full cost of double factorized qpe and then deducing the cost
    of the block encoding from that.

    Args:
        h1: Matrix elements of the one-body operator that includes kinetic
            energy operator and electorn-nuclear Coulomb operator.
        eri: Four-dimensional array containing electron-repulsion
            integrals.
        threshold: Threshold for the factorization.
        allowable_phase_estimation_error: Allowable error in phase estimation.
            Corresponds to epsilon_QPE in the paper.
        bits_precision_coefficients: The number of bits for the representation of
            the coefficients. Corresponds to aleph_1 and aleph_2 in the paper.
        bits_precision_rotations: The number of bits of precision for rotation angles.
            Corresponds to beth in the paper.

    Returns:
        A tuple containing:
            The number of Toffolis required for a controlled implementation of the block
                encoding.
            The number of qubits required for the controlled block encoding (including
                the control qubit).
            The one-norm of the block encoding, corresponding to lambda in the paper.
                Note that this has the same units as the entries of h1 and eri.
    """

    # In the df.compute_cost(...) function below, we set dE = 1 since this input doesn't
    # matter for us. We are only interested in the cost of implementing the quantum walk
    # operator, not the cost of QPE which depends on dE. Recall, dE determines the
    # precision of the QPE output which depends on the number of ancilla qubits in the
    # energy register.

    eri_rr, LR, L, Lxi = df.factorize(eri, threshold)
    lam = compute_lambda_df(h1, eri_rr, LR)

    allowable_phase_estimation_error = 1
    (step_cost, total_cost, num_qubits,) = _get_double_factorized_qpe_info(
        h1,
        eri,
        threshold,
        allowable_phase_estimation_error,
        bits_precision_state_prep,
        bits_precision_rotation,
    )

    # Remove all but one of the ancilla qubits in the QPE energy register.
    iterations = np.ceil(np.pi * lam / (allowable_phase_estimation_error * 2))
    num_qubits_energy_register = 2 * np.ceil(np.log2(iterations)) - 1
    num_qubits = num_qubits - num_qubits_energy_register + 1

    return step_cost, num_qubits, lam
