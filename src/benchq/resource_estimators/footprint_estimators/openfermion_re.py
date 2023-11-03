################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################

from typing import Tuple

import numpy as np
from openfermion.resource_estimates import df, sf

from benchq.problem_ingestion.block_encodings.utils._compute_lambda import (
    compute_lambda_df,
    compute_lambda_sf,
)


def _validate_eri(eri: np.ndarray):
    """Validate that the ERI tensor has the symmetries required for factorization."""
    if not np.allclose(np.transpose(eri, (2, 3, 0, 1)), eri):
        raise ValueError("ERI do not have (ij | kl) == (kl | ij) symmetry.")


def get_single_factorized_qpe_toffoli_and_qubit_cost(
    h1: np.ndarray,
    eri: np.ndarray,
    rank: int,
    allowable_phase_estimation_error: float = 0.001,
    bits_precision_coefficients: float = 10,
) -> Tuple[int, int]:
    """Get the number of Toffoli gates and logical qubits for single factorized QPE as
    described in PRX Quantum 2, 030305.

    Args:
        h1: Matrix elements of the one-body operator that includes kinetic
            energy operator and electorn-nuclear Coulomb operator.
        eri: Four-dimensional array containing electron-repulsion
            integrals.
        rank: Rank of the factorization.
        allowable_phase_estimation_error: Allowable error in phase estimation.
            Corresponds to epsilon_QPE in the paper.
        bits_precision_coefficients: The number of bits for the representation of
            the coefficients. Corresponds to aleph_1 and aleph_2 in the paper.

    Returns:
        A tuple containing the number of Toffoli gates and number of logical qubits.
    """

    _validate_eri(eri)
    num_orb = h1.shape[0]
    num_spinorb = num_orb * 2

    # First, up: lambda and CCSD(T)
    eri_rr, LR = sf.factorize(eri, rank)
    lam = compute_lambda_sf(h1, eri_rr, LR)

    # now do costing
    stps1 = sf.compute_cost(
        num_spinorb,
        lam,
        allowable_phase_estimation_error,
        L=rank,
        chi=bits_precision_coefficients,
        stps=20000,
    )[0]

    _, sf_total_toffoli_cost, sf_logical_qubits = sf.compute_cost(
        num_spinorb,
        lam,
        allowable_phase_estimation_error,
        L=rank,
        chi=bits_precision_coefficients,
        stps=stps1,
    )
    return sf_total_toffoli_cost, sf_logical_qubits


def _get_double_factorized_qpe_info(
    h1: np.ndarray,
    eri: np.ndarray,
    threshold: float,
    allowable_phase_estimation_error: float = 0.001,
    bits_precision_coefficients: int = 10,
    bits_precision_rotation: int = 20,
):
    """Get information about the double factorized QPE algorithm.

    Args: See get_double_factorized_qpe_toffoli_and_qubit_cost.

    Returns:
        Tuple containing the number of Toffoli gates per iteration, total number of
            Tofolli gates, and total number of qubits.
    """

    _validate_eri(eri)
    num_orb = h1.shape[0]
    num_spinorb = num_orb * 2

    eri_rr, LR, L, Lxi = df.factorize(eri, threshold)
    lam = compute_lambda_df(h1, eri_rr, LR)

    initial_step_cost, _, _ = df.compute_cost(
        num_spinorb,
        lam,
        allowable_phase_estimation_error,
        L,
        Lxi,
        bits_precision_coefficients,
        bits_precision_rotation,
        stps=20000,
        verbose=False,
    )

    step_cost, total_cost, ancilla_cost = df.compute_cost(
        num_spinorb,
        lam,
        allowable_phase_estimation_error,
        L,
        Lxi,
        bits_precision_coefficients,
        bits_precision_rotation,
        stps=initial_step_cost,
        verbose=False,
    )

    return step_cost, total_cost, ancilla_cost


def get_double_factorized_qpe_toffoli_and_qubit_cost(
    h1: np.ndarray,
    eri: np.ndarray,
    threshold: float,
    allowable_phase_estimation_error: float = 0.001,
    bits_precision_coefficients: int = 10,
    bits_precision_rotation: int = 20,
) -> Tuple[int, int]:
    """Get the number of Toffoli gates and logical qubits for double factorized QPE as
    described in PRX Quantum 2, 030305.

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
        A tuple containing the number of Toffoli gates and number of logical qubits.
    """
    step_cost, total_cost, ancilla_cost = _get_double_factorized_qpe_info(
        h1,
        eri,
        threshold,
        allowable_phase_estimation_error,
        bits_precision_coefficients,
        bits_precision_rotation,
    )

    return total_cost, ancilla_cost


def get_double_factorized_block_encoding_info(
    h1: np.ndarray,
    eri: np.ndarray,
    threshold: float,
    bits_precision_state_prep: int = 10,
    bits_precision_rotation: int = 20,
) -> Tuple[int, int, float]:
    """Get the Toffoli count, qubit cost, and the one-norm for the double factorized
    block encoding as described in PRX Quantum 2, 030305.

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
