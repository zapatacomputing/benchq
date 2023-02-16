################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import numpy as np
from openfermion.resource_estimates import sf
from openfermion.resource_estimates.surface_code_compilation.physical_costing import (
    cost_estimator,
)


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


def get_qpe_resource_estimates_from_mean_field_object(
    mean_field_object,
    target_accuracy=0.001,
    bits_precision_state_prep=10,
):

    # Set rank in order to satisfy
    # rank + 1 > bL where
    # bL = nL + bits_precision_state_prep + 2
    initial_rank = 4
    nL = np.ceil(np.log2(initial_rank + 1))
    rank = int(nL + bits_precision_state_prep + 2)

    (
        sf_total_toffoli_cost,
        sf_logical_qubits,
    ) = model_toffoli_and_qubit_cost_from_single_factorized_mean_field_object(
        mean_field_object, rank, target_accuracy, bits_precision_state_prep
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
