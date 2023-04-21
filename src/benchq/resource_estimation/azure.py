################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import os
import warnings
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Optional

from azure.quantum.qiskit import AzureQuantumProvider
from orquestra.integrations.qiskit.conversions import export_to_qiskit
from orquestra.quantum.circuits import Circuit
from qiskit.tools.monitor import job_monitor

from ..data_structures import BasicArchitectureModel, ErrorBudget, QuantumProgram


@dataclass
class AzureResourceInfo:
    physical_qubit_count: int
    logical_qubit_count: int
    total_time: float
    depth: int
    distance: int
    cycle_time: float
    logical_error_rate: float
    raw_data: dict


def _azure_result_to_resource_info(job_results: dict) -> AzureResourceInfo:
    return AzureResourceInfo(
        physical_qubit_count=job_results["physicalCounts"]["physicalQubits"],
        logical_qubit_count=job_results["physicalCounts"]["breakdown"][
            "algorithmicLogicalQubits"
        ],
        total_time=job_results["physicalCounts"]["runtime_in_s"],
        depth=job_results["physicalCounts"]["breakdown"]["algorithmicLogicalDepth"],
        distance=job_results["logicalQubit"]["codeDistance"],
        cycle_time=job_results["logicalQubit"]["logicalCycleTime"],
        logical_error_rate=job_results["errorBudget"]["logical"],
        raw_data=job_results,
    )


class AzureResourceEstimator:
    """Class that interfaces between Bench-Q and Azure QRE.

    It allows to use Azure QRE to estimate the resources required to run
    a given quantum program.

    Requires having Azure credentials set up in the environment.

    Args:
        hw_model: Describes the architecture that should be used for resource
            estimation. If None, default architecture provided by QRE is used.
            Defaults to None.
        use_full_circuit: If True, recreates the whole circuit from QuantumProgram.
            Defaults to True.

    """

    def __init__(
        self,
        hw_model: Optional[BasicArchitectureModel] = None,
        use_full_circuit: bool = True,
    ):
        if hw_model is not None:
            warnings.warn(
                "Supplying hardware model to AzureResourceEstimator is "
                "currently broken."
            )
        self.hw_model = hw_model
        self.use_full_circuit = use_full_circuit

    def estimate(
        self, program: QuantumProgram, error_budget: Optional[ErrorBudget] = None
    ) -> AzureResourceInfo:
        azure_error_budget: Dict[str, float] = {}
        if error_budget is not None:
            azure_error_budget = {}
            azure_error_budget["rotations"] = error_budget.synthesis_failure_tolerance
            remaining_error = error_budget.ec_failure_tolerance
            azure_error_budget["logical"] = remaining_error / 2
            azure_error_budget["tstates"] = remaining_error / 2
        if self.use_full_circuit:
            circuit = program.full_circuit
            return self._estimate_resources_for_circuit(circuit, azure_error_budget)
        else:
            raise NotImplementedError(
                "Resource estimation for Quantum Programs which are not consisting "
                "of a single circuit is not implemented yet."
            )

    def _estimate_resources_for_circuit(
        self, circuit: Circuit, error_budget: Dict[str, float]
    ) -> AzureResourceInfo:
        if self.hw_model is not None:
            gate_time = self.hw_model.physical_gate_time_in_seconds
            gate_time_string = f"{int(gate_time * 1e9)} ns"
            qubitParams = {
                "name": "custom gate-based",
                "instructionSet": "GateBased",
                "oneQubitGateTime": gate_time_string,
                # "oneQubitMeasurementTime": "30 μs",
                "oneQubitGateErrorRate": self.hw_model.physical_gate_error_rate,
                # "tStateErrorRate": 1e-3
            }
        else:
            qubitParams = None

        qiskit_circuit = export_to_qiskit(circuit)
        provider = AzureQuantumProvider(
            resource_id=os.getenv("AZURE_RESOURCE_ID"), location="East US"
        )

        backend = provider.get_backend("microsoft.estimator")
        if qubitParams is None:
            job = backend.run(qiskit_circuit, errorBudget=error_budget)
        else:
            job = backend.run(
                qiskit_circuit, qubitParams=qubitParams, errorBudget=error_budget
            )

        job_monitor(job)
        job_results = job.result().data()
        del job_results["reportData"]
        job_results["physicalCounts"]["runtime_in_s"] = (
            job_results["physicalCounts"]["runtime"] / 1e9
        )
        return _azure_result_to_resource_info(job_results)
