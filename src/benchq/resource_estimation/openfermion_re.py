################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
import numpy as np
import pyscf
from openfermion.resource_estimates import sf
from openfermion.resource_estimates.surface_code_compilation.physical_costing import (
    cost_estimator,
)
from typing import Dict, Any
import pyscf


def model_toffoli_and_qubit_cost_from_single_factorized_mean_field_object(
    mean_field_object, rank, DE, CHI
):
    num_orb = len(mean_field_object.mo_coeff)
    num_spinorb = num_orb * 2

    # First, up: lambda and CCSD(T)
    eri_rr, LR = sf.factorize(mean_field_object._eri, rank)
    lam = sf.compute_lambda(mean_field_object, LR)

    # now do costing
    stps1 = sf.compute_cost(num_spinorb, lam, DE, L=rank, chi=CHI, stps=20000)[0]

    _, sf_total_toffoli_cost, sf_logical_qubits = sf.compute_cost(
        num_spinorb, lam, DE, L=rank, chi=CHI, stps=stps1
    )
    return sf_total_toffoli_cost, sf_logical_qubits


def _get_unsymmetrized_eri(meanfield_object: pyscf.scf.hf.SCF) -> np.ndarray:
    """Get the ERI for molecular orbitals in the S1 symmetry representation.

    Args:
        meanfield_object: A PySCF mean field object.

    Returns:
        The ERI in the S1 symmetry representation."""

    eri = pyscf.ao2mo.kernel(meanfield_object.mol, meanfield_object.mo_coeff)
    return pyscf.ao2mo.restore("s1", eri, meanfield_object.mol.nao_nr())


def get_qpe_resource_estimates_from_mean_field_object(
    meanfield_object: pyscf.scf.hf.SCF,
    rank: int,
    target_accuracy: float = 0.001,
    bits_precision_state_prep: int = 10,
) -> Dict[str, Any]:

    # ERI must be represented using S1 permutation symmetry.
    if not meanfield_object._eri.shape == (meanfield_object._eri.shape[0],) * 4:
        meanfield_object._eri = _get_unsymmetrized_eri(meanfield_object)

    if not np.allclose(
        np.transpose(meanfield_object._eri, (2, 3, 0, 1)), meanfield_object._eri
    ):
        raise ValueError("ERI do not have (ij | kl) == (kl | ij) symmetry.")


    (
        sf_total_toffoli_cost,
        sf_logical_qubits,
    ) = model_toffoli_and_qubit_cost_from_single_factorized_mean_field_object(
        meanfield_object, rank, target_accuracy, bits_precision_state_prep
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

    physical_qubit_count = best_cost.physical_qubit_count
    duration = best_cost.duration
    print("Number of physical qubits is:", physical_qubit_count)
    print("Runtime in hours is:", duration.seconds / 3600)
    return {
        # "logical_error_rate": final_logical_error_rate,
        "total_time": duration.seconds,
        "physical_qubit_count": physical_qubit_count,
        # "min_viable_distance": min_viable_distance,
        # "synthesis_error_rate": synthesis_error_rate,
        # "resources_in_cells": resources_in_cells,
    }
