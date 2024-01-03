################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################

import warnings
from typing import Tuple

import numpy as np

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    # openfermion throws deprecation warning thru pyscf and numpy
    # Could be fixed by using old setuptools, but there would be dependency conflict
    from openfermion.resource_estimates import df, sf

from benchq.data_structures import (
    BASIC_SC_ARCHITECTURE_MODEL,
    BasicArchitectureModel,
    DetailedArchitectureModel,
)
from benchq.data_structures.resource_info import (
    OpenFermionExtra,
    OpenFermionResourceInfo,
)
from benchq.resource_estimation._compute_lambda import (
    compute_lambda_df,
    compute_lambda_sf,
)
from benchq.resource_estimation._footprint_analysis import (
    AlgorithmParameters,
    CostEstimate,
    cost_estimator,
)
from benchq.resource_estimation.decoder_resource_estimator import get_decoder_info


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


def get_physical_cost(
    num_logical_qubits: int,
    num_toffoli: int = 0,
    num_t: int = 0,
    architecture_model: BasicArchitectureModel = BASIC_SC_ARCHITECTURE_MODEL,
    routing_overhead_proportion=0.5,
    hardware_failure_tolerance=1e-3,
    decoder_model=None,
    factory_count: int = 4,
) -> OpenFermionResourceInfo:
    """Get the estimated resources for single factorized QPE as described in PRX Quantum
    2, 030305.

    Args:
        num_toffoli: The number of Toffoli gates required.
        num_logical_qubits: The number of logical qubits required.
    Returns:
        The estimated physical qubits, runtime, and other resource estimation info.
    """

    best_cost, best_params = cost_estimator(
        num_logical_qubits,
        num_toffoli=num_toffoli,
        num_t=num_t,
        physical_error_rate=architecture_model.physical_qubit_error_rate,
        surface_code_cycle_time=architecture_model.surface_code_cycle_time_in_seconds,
        routing_overhead_proportion=routing_overhead_proportion,
        hardware_failure_tolerance=hardware_failure_tolerance,
        factory_count=factory_count,
    )

    decoder_info = get_decoder_info(
        architecture_model,
        decoder_model,
        best_params.logical_data_qubit_distance,
        best_cost.physical_qubit_count * best_cost.duration,
        best_params.max_allocated_logical_qubits,
    )

    resource_info = _openfermion_result_to_resource_info(
        best_cost, best_params, decoder_info
    )
    if isinstance(architecture_model, DetailedArchitectureModel):
        resource_info.hardware_resource_info = (
            architecture_model.get_hardware_resource_estimates(resource_info)
        )

    return resource_info


def _openfermion_result_to_resource_info(
    cost: CostEstimate, algorithm_parameters: AlgorithmParameters, decoder_info=None
) -> OpenFermionResourceInfo:
    return OpenFermionResourceInfo(
        n_physical_qubits=cost.physical_qubit_count,
        n_logical_qubits=algorithm_parameters.max_allocated_logical_qubits,
        total_time_in_seconds=cost.duration,
        code_distance=algorithm_parameters.logical_data_qubit_distance,
        logical_error_rate=cost.algorithm_failure_probability,
        decoder_info=decoder_info,
        routing_to_measurement_volume_ratio=algorithm_parameters.routing_overhead_proportion,  # noqa
        widget_name=algorithm_parameters.widget.details,
        extra=OpenFermionExtra(
            fail_rate_msFactory=algorithm_parameters.widget.failure_rate,
            rounds_magicstateFactory=algorithm_parameters.widget.distillation_time_in_cycles,  # noqa
            physical_qubit_error_rate=algorithm_parameters.physical_error_rate,
            scc_time=algorithm_parameters.surface_code_cycle_time,
        ),
    )
