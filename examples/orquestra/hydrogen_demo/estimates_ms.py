################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import time

from benchq import BasicArchitectureModel

from benchq.resource_estimation.microsoft import (
    get_resource_estimations_for_program as msft_re_for_program)

from .defs import get_operator, ms_task, get_program
from orquestra import sdk

@ms_task
def ms_estimate(quantum_program, error_budget: float, architecture_model):
    import os
    os.environ["AZURE_CLIENT_ID"] = sdk.secrets.get("AZURE-CLIENT-ID")
    os.environ["AZURE_TENANT_ID"] = sdk.secrets.get("AZURE-TENANT-ID")
    os.environ["AZURE_CLIENT_SECRET"] = sdk.secrets.get("AZURE-CLIENT-SECRET")
    os.environ["AZURE_RESOURCE_ID"] = sdk.secrets.get("AZURE-RESOURCE-ID")

    return msft_re_for_program(quantum_program, error_budget, architecture_model)

@sdk.workflow
def ms_estimates():
    dt = 0.5  # Integration timestep
    tmax = 5  # Maximal timestep
    sclf = 1
    results = []
    for n_hydrogens in [2]:
        # TA 1 part: specify the core computational capability
        # Generate instance
        # Convert instance to core computational problem instance
        operator = get_operator(n_hydrogens)

        tolerable_circuit_error_rate = 1e-3
        # Allocate half the error budget to QSP precision
        qsp_required_precision = (tolerable_circuit_error_rate / 2)
        remaining_error_budget = tolerable_circuit_error_rate - qsp_required_precision

        architecture_model = BasicArchitectureModel(
            physical_gate_error_rate=1e-3,
            physical_gate_time_in_seconds=1e-6,
        )

        ##### STUFF FOR SUBCIRCUITS
        # TA 1.5 part: model algorithmic circuit
        for mode in ["time_evolution", "gse"]:
            quantum_program = get_program(
                operator, qsp_required_precision, dt, tmax, sclf, mode=mode
            )

            results.append(ms_estimate(
                quantum_program, remaining_error_budget, architecture_model
            ))

    return results
