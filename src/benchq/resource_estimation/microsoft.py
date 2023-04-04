################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import os

from azure.quantum.qiskit import AzureQuantumProvider
from orquestra.integrations.qiskit.conversions import export_to_qiskit
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import RGQFTMultiplier
from qiskit.tools.monitor import job_monitor

from ..data_structures import QuantumProgram


def get_resource_estimations_for_circuit(
    circuit, architecture_model=None, error_budget=None
):
    qiskit_circuit = export_to_qiskit(circuit)

    if architecture_model is not None:
        gate_time = architecture_model.physical_gate_time_in_seconds
        gate_time_string = f"{int(gate_time * 1e9)} ns"
        qubit = {
            "name": "slow gate-based",
            "oneQubitGateTime": gate_time_string,
            # "oneQubitMeasurementTime": "30 μs",
            "oneQubitGateErrorRate": architecture_model.physical_gate_error_rate,
            # "tStateErrorRate": 1e-3
        }

    provider = AzureQuantumProvider(
        resource_id=os.getenv("AZURE_RESOURCE_ID"), location="East US"
    )

    backend = provider.get_backend("microsoft.estimator")

    if architecture_model is None and error_budget is None:
        job = backend.run(qiskit_circuit)
    else:
        job = backend.run(qiskit_circuit, qubit=qubit, errorBudget=error_budget)

    job_monitor(job)
    full_results = job.result().data()
    del full_results["reportData"]
    full_results["physicalCounts"]["runtime_in_s"] = (
        full_results["physicalCounts"]["runtime"] / 10e9
    )
    return full_results


def get_resource_estimations_for_program(
    quantum_program: QuantumProgram, error_budget: float, architecture_model
):
    """_summary_

    Args:
        quantum_program: _description_
        error_budget: _description_
    """
    total_multiplicity = sum(quantum_program.multiplicities)
    # TA 2 part: Microsoft estimation
    all_ms_results = []
    for mult, circuit in zip(
        quantum_program.multiplicities, quantum_program.subroutines
    ):
        ms_results = get_resource_estimations_for_circuit(
            circuit,
            architecture_model=architecture_model,
            error_budget=error_budget * mult / total_multiplicity,
        )
        all_ms_results.append(ms_results)
    return _combine_estimates(all_ms_results, quantum_program.multiplicities)


def _combine_estimates(estimates_per_subroutine, subroutine_multiplicities):
    combined_resource_estimates = {
        "total_time": 0,
        "number_of_physical_qubits": [],
        "logical_error_rate": [],
        "distance": [],
        "number_of_logical_qubits": [],
        "cycle_time": [],
        "depth": [],
        "T_state_error_rate": [],
    }
    for re, mult in zip(estimates_per_subroutine, subroutine_multiplicities):
        combined_resource_estimates["total_time"] += (
            re["physicalCounts"]["runtime_in_s"] * mult
        )
        combined_resource_estimates["number_of_physical_qubits"].append(
            re["physicalCounts"]["physicalQubits"]
        )
        combined_resource_estimates["logical_error_rate"].append(
            re["errorBudget"]["logical"]
        )
        combined_resource_estimates["distance"].append(
            re["logicalQubit"]["codeDistance"]
        )
        combined_resource_estimates["number_of_logical_qubits"].append(
            re["physicalCounts"]["breakdown"]["algorithmicLogicalQubits"]
        )
        combined_resource_estimates["cycle_time"].append(
            re["logicalQubit"]["logicalCycleTime"]
        )
        combined_resource_estimates["depth"].append(
            re["physicalCounts"]["breakdown"]["algorithmicLogicalDepth"]
        )
        combined_resource_estimates["T_state_error_rate"].append(
            re["physicalCounts"]["breakdown"]["requiredLogicalTstateErrorRate"]
        )

    return combined_resource_estimates
