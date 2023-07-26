################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
import datetime
from typing import Tuple

import numpy as np
from openfermion.resource_estimates import df, sf
from openfermion.resource_estimates.molecule import pyscf_to_cas


from benchq.data_structures.resource_info import OpenFermionResourceInfo
from benchq.data_structures import SubroutineModel
from benchq.resource_estimation._compute_lambda import (
    compute_lambda_df,
    compute_lambda_sf,
)
from benchq.resource_estimation.footprint_analysis import (
    AlgorithmParameters,
    CostEstimate,
    cost_estimator,
)


def _validate_eri(eri: np.ndarray):
    """Validate that the ERI tensor has the symmetries required for factorization."""
    if not np.allclose(np.transpose(eri, (2, 3, 0, 1)), eri):
        raise ValueError("ERI do not have (ij | kl) == (kl | ij) symmetry.")


def get_integrals_from_hamiltonian_instance(hamiltonian_instance):
    mean_field_object = hamiltonian_instance.get_active_space_meanfield_object()
    h1, eri_full, _, _, _ = pyscf_to_cas(mean_field_object)
    return h1, eri_full


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


def get_single_factorized_be_subnormalization(
    h1: np.ndarray,
    eri: np.ndarray,
    rank: int,
) -> int:
    """Get the subnormalization for single factorized block encoding as
    described in PRX Quantum 2, 030305.

    Args:
        h1: Matrix elements of the one-body operator that includes kinetic
            energy operator and electorn-nuclear Coulomb operator.
        eri: Four-dimensional array containing electron-repulsion
            integrals.
        rank: Rank of the factorization.

    Returns:
        The single factorization block encoding subnormalization.
    """

    _validate_eri(eri)
    num_orb = h1.shape[0]
    num_spinorb = num_orb * 2

    eri_rr, LR = sf.factorize(eri, rank)
    subnormalization = compute_lambda_sf(h1, eri_rr, LR)
    return subnormalization


class SFHamiltonianBlockEncoding(SubroutineModel):
    def __init__(
        self,
        task_name="hamiltonian_block_encoding",
        requirements=None,
        toffoli_gate=SubroutineModel("toffoli_gate"),
    ):
        super().__init__(task_name, requirements, toffoli_gate=toffoli_gate)

    def set_requirements(self, hamiltonian, failure_tolerance):
        args = locals()
        args.pop("self")
        args = {k: v for k, v in args.items() if not k.startswith("__")}
        super().set_requirements(**args)

    def populate_requirements_for_subroutines(self):
        h1, eri_full = get_integrals_from_hamiltonian_instance(
            self.requirements["hamiltonian"]
        )
        rank = choose_rank_for_sf(h1, eri_full)
        toffoli_gate_cost, _ = get_single_factorized_qpe_toffoli_and_qubit_cost(
            h1,
            eri_full,
            rank,
        )
        self.toffoli_gate.number_of_times_called = toffoli_gate_cost
        self.toffoli_gate.set_requirements(
            failure_tolerance=self.requirements["failure_tolerance"] / toffoli_gate_cost
        )

    def get_subnormalization(self, hamiltonian_instance):
        # Implementation for single factorized Hamiltonian
        # Here, I'm assuming it to be similar to the double factorized case
        # You may need to adjust the function to properly compute the subnormalization
        h1, eri_full = get_integrals_from_hamiltonian_instance(hamiltonian_instance)
        rank = choose_rank_for_sf(h1, eri_full)
        return get_single_factorized_be_subnormalization(h1, eri_full, rank)


def choose_rank_for_sf(
    h1: np.ndarray,
    eri: np.ndarray,
):
    return 20


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
        threshold:
        allowable_phase_estimation_error: Allowable error in phase estimation.
            Corresponds to epsilon_QPE in the paper.
        bits_precision_coefficients: The number of bits for the representation of
            the coefficients. Corresponds to aleph_1 and aleph_2 in the paper.
        bits_precision_rotations: The number of bits of precision for rotation angles.
            Corresponds to beth in the paper.

    Returns:
        A tuple containing the number of Toffoli gates and number of logical qubits.
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

    return total_cost, ancilla_cost


def get_double_factorized_be_toffoli_and_qubit_cost(
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
        threshold:
        allowable_phase_estimation_error: Allowable error in phase estimation.
            Corresponds to epsilon_QPE in the paper.
        bits_precision_coefficients: The number of bits for the representation of
            the coefficients. Corresponds to aleph_1 and aleph_2 in the paper.
        bits_precision_rotations: The number of bits of precision for rotation angles.
            Corresponds to beth in the paper.

    Returns:
        A tuple containing the number of Toffoli gates and number of logical qubits.
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

    return step_cost, ancilla_cost


def get_double_factorized_be_subnormalization(
    h1: np.ndarray,
    eri: np.ndarray,
    threshold: float,
) -> int:
    """Get the subnormalization for double factorized block encoding as
    described in PRX Quantum 2, 030305.

    Args:
        h1: Matrix elements of the one-body operator that includes kinetic
            energy operator and electorn-nuclear Coulomb operator.
        eri: Four-dimensional array containing electron-repulsion
            integrals.
        threshold:

    Returns:
        The double factorization block encoding subnormalization.
    """

    _validate_eri(eri)
    num_orb = h1.shape[0]
    num_spinorb = num_orb * 2

    eri_rr, LR, L, Lxi = df.factorize(eri, threshold)
    subnormalization = compute_lambda_df(h1, eri_rr, LR)
    return subnormalization


def choose_threshold_for_df(
    h1: np.ndarray,
    eri: np.ndarray,
):
    return 1e-6


class DFHamiltonianBlockEncoding(SubroutineModel):
    def __init__(
        self,
        task_name="hamiltonian_block_encoding",
        requirements=None,
        toffoli_gate=SubroutineModel("toffoli_gate"),
    ):
        super().__init__(task_name, requirements, toffoli_gate=toffoli_gate)

    def set_requirements(self, hamiltonian, failure_tolerance):
        args = locals()
        # Clean up the args dictionary before setting requirements
        args.pop("self")
        args = {k: v for k, v in args.items() if not k.startswith("__")}
        super().set_requirements(**args)

    def populate_requirements_for_subroutines(self):
        # self.requirements["hamiltonian"]
        h1, eri_full = get_integrals_from_hamiltonian_instance(
            self.requirements["hamiltonian"]
        )
        truncation_threshold = choose_threshold_for_df(h1, eri_full)
        toffoli_gate_cost, _ = get_double_factorized_be_toffoli_and_qubit_cost(
            h1,
            eri_full,
            truncation_threshold,
        )
        self.toffoli_gate.number_of_times_called = toffoli_gate_cost
        self.toffoli_gate.set_requirements(
            failure_tolerance=self.requirements["failure_tolerance"] / toffoli_gate_cost
        )

    def get_subnormalization(self, hamiltonian_instance):
        h1, eri_full = get_integrals_from_hamiltonian_instance(hamiltonian_instance)
        truncation_threshold = choose_threshold_for_df(h1, eri_full)
        return get_double_factorized_be_subnormalization(
            h1, eri_full, truncation_threshold
        )


def get_physical_cost(
    num_logical_qubits: int,
    num_toffoli: int,
    surface_code_cycle_time: datetime.timedelta = datetime.timedelta(microseconds=1),
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
        num_toffoli,
        surface_code_cycle_time=surface_code_cycle_time,
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
        total_time_in_seconds=cost.duration.total_seconds(),
        code_distance=algorithm_parameters.logical_data_qubit_distance,
        logical_error_rate=cost.algorithm_failure_probability,
        decoder_info=None,
        widget_name=algorithm_parameters.magic_state_factory.details,
        extra=algorithm_parameters,
    )


class QubitizedQuantumPhaseEstimation(SubroutineModel):
    def __init__(
        self,
        task_name="phase_estimation",
        requirements=None,
        hamiltonian_block_encoding=None,
    ):
        super().__init__(
            task_name,
            requirements,
            hamiltonian_block_encoding=hamiltonian_block_encoding
            if hamiltonian_block_encoding is not None
            else SubroutineModel("hamiltonian_block_encoding"),
        )

    def set_requirements(
        self,
        precision,
        failure_tolerance,
        hamiltonian,
    ):
        args = locals()
        # Clean up the args dictionary before setting requirements
        args.pop("self")
        args = {k: v for k, v in args.items() if not k.startswith("__")}
        super().set_requirements(**args)

    def populate_requirements_for_subroutines(self):
        # Compute subnormalization of block encoding if the get_subnormalization method is available
        if hasattr(self.hamiltonian_block_encoding, "get_subnormalization"):
            subnormalization = self.hamiltonian_block_encoding.get_subnormalization(
                self.requirements["hamiltonian"]
            )
            n_block_encodings = np.ceil(
                np.pi * subnormalization / (self.requirements["precision"] * 2)
            )
        else:
            n_block_encodings = None
            print(
                "Warning: No subroutine for the Hamiltonian block encoding task has been provided that has a get_subnormalization method."
            )

        self.hamiltonian_block_encoding.number_of_times_called = n_block_encodings

        if n_block_encodings:
            be_failure_tolerance = self.requirements["failure_tolerance"]
        else:
            be_failure_tolerance = None
        self.hamiltonian_block_encoding.set_requirements(
            hamiltonian=self.requirements["hamiltonian"],
            failure_tolerance=be_failure_tolerance,
        )
