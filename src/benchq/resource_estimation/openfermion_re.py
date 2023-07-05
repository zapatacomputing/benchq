################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
from typing import Tuple

import numpy as np
from openfermion.resource_estimates import sf, df
from openfermion.resource_estimates.surface_code_compilation.physical_costing import (
    AlgorithmParameters,
    CostEstimate,
    cost_estimator,
)

from benchq.data_structures.resource_info import OpenFermionResourceInfo
from benchq.resource_estimation._compute_lambda import (
    compute_lambda_sf,
    compute_lambda_df,
)


def get_single_factorized_qpe_toffoli_and_qubit_cost(
    h1: np.ndarray,
    eri: np.ndarray,
    rank: int,
    allowable_phase_estimation_error: float,
    bits_precision_state_prep: float,
) -> Tuple[int, int]:
    """Get the number of Toffoli gates and logical qubits for single factorized QPE.

    See get_single_factorized_qpe_resource_estimate for descriptions of arguments.

    Returns:
        The number of Toffoli gates and logical qubits.
    """
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
        chi=bits_precision_state_prep,
        stps=20000,
    )[0]

    _, sf_total_toffoli_cost, sf_logical_qubits = sf.compute_cost(
        num_spinorb,
        lam,
        allowable_phase_estimation_error,
        L=rank,
        chi=bits_precision_state_prep,
        stps=stps1,
    )
    return sf_total_toffoli_cost, sf_logical_qubits


def get_double_factorized_qpe_toffoli_and_qubit_cost(
    h1: np.ndarray,
    eri: np.ndarray,
    threshold: float,
    allowable_phase_estimation_error: float,
    bits_precision_state_prep: int = 10,
    bits_precision_rotation: int = 20,
) -> Tuple[int, int]:
    """Get the number of Toffoli gates and logical qubits for double factorized QPE.
    """
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
        bits_precision_state_prep,
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
        bits_precision_state_prep,
        bits_precision_rotation,
        stps=initial_step_cost,
        verbose=False,
    )

    return step_cost, total_cost, ancilla_cost


def get_toffoli_and_qubit_cost_for_double_factorized_block_encoding(
    h1: np.ndarray,
    eri: np.ndarray,
    threshold: float,
    allowable_phase_estimation_error: float,
    bits_precision_state_prep: int = 10,
    bits_precision_rotation: int = 20,
) -> Tuple[int, int]:
    """Get the Toffoli and qubit cost for the double factorized block encoding.

    Args:

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

    eri_rr, LR, L, Lxi = df.factorize(eri, threshold)
    lam = compute_lambda_df(h1, eri_rr, LR)

    allowable_phase_estimation_error = 1
    (
        step_cost,
        total_cost,
        ancilla_cost,
    ) = get_double_factorized_qpe_toffoli_and_qubit_cost(
        h1,
        eri,
        threshold,
        allowable_phase_estimation_error,
        bits_precision_state_prep,
        bits_precision_rotation,
    )

    # Now, we will remove the ancilla qubits in the energy register in QPE, and only add one using Guoming's algorithm.
    # The number of steps in Heisenberg-Limited QPE, i.e., 2^m.
    iters = np.ceil(np.pi * lam / (allowable_phase_estimation_error * 2))

    # Number of control qubits in the energy register
    m = 2 * np.ceil(np.log2(iters)) - 1

    ancilla_cost = ancilla_cost - m

    return step_cost, ancilla_cost


def get_single_factorized_qpe_resource_estimate(
    h1: np.ndarray,
    eri: np.ndarray,
    rank: int,
    allowable_phase_estimation_error: float = 0.001,
    bits_precision_state_prep: int = 10,
) -> OpenFermionResourceInfo:
    """Get the estimated resources for single factorized QPE as described in PRX Quantum
    2, 030305.

    Args:
        h1 (np.ndarray): Matrix elements of the one-body operator that includes kinetic
            energy operator and electorn-nuclear Coulomb operator.
        eri (np.ndarray): Four-dimensional array containing electron-repulsion
            integrals.
        rank (int): Rank of the factorization.
        allowable_phase_estimation_error (float): Allowable error in phase estimation.
            Corresponds to epsilon_QPE in the paper.
        bits_precision_state_prep (float): The number of bits for the representation of
            the coefficients. Corresponds to aleph_1 and aleph_2 in the paper.

    Returns:
        A dictionary containing the estimated time and physical qubit requirements.
    """

    if not np.allclose(np.transpose(eri, (2, 3, 0, 1)), eri):
        raise ValueError("ERI do not have (ij | kl) == (kl | ij) symmetry.")

    (
        sf_total_toffoli_cost,
        sf_logical_qubits,
    ) = get_single_factorized_qpe_toffoli_and_qubit_cost(
        h1, eri, rank, allowable_phase_estimation_error, bits_precision_state_prep
    )
    print("Number of Toffoli's is:", sf_total_toffoli_cost)
    print("Number of logical qubits is:", sf_logical_qubits)

    # Model physical costs
    best_cost, best_params = cost_estimator(
        sf_logical_qubits,
        sf_total_toffoli_cost,
        physical_error_rate=1.0e-3,
        portion_of_bounding_box=1.0,
    )

    return _openfermion_result_to_resource_info(best_cost, best_params)


def _openfermion_result_to_resource_info(
    cost: CostEstimate, algorithm_parameters: AlgorithmParameters
) -> OpenFermionResourceInfo:
    return OpenFermionResourceInfo(
        n_physical_qubits=cost.physical_qubit_count,
        n_logical_qubits=algorithm_parameters.max_allocated_logical_qubits,
        total_time_in_seconds=cost.duration.seconds,
        code_distance=algorithm_parameters.logical_data_qubit_distance,
        logical_error_rate=cost.algorithm_failure_probability,
        decoder_info=None,
        widget_name=algorithm_parameters.magic_state_factory.details,
        extra=algorithm_parameters,
    )
