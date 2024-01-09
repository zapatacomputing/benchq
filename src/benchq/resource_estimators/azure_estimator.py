################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import os
import warnings
from typing import Dict, Optional

from azure.quantum.qiskit import AzureQuantumProvider
from orquestra.integrations.qiskit.conversions import export_to_qiskit
from orquestra.quantum.circuits import Circuit
from qiskit.tools.monitor import job_monitor

from ..algorithms.data_structures import AlgorithmImplementation
from ..quantum_hardware_modeling import BasicArchitectureModel
from .resource_info import AzureExtra, AzureResourceInfo


def _azure_result_to_resource_info(job_results: dict) -> AzureResourceInfo:
    return AzureResourceInfo(
        n_physical_qubits=job_results["physicalCounts"]["physicalQubits"],
        n_logical_qubits=job_results["physicalCounts"]["breakdown"][
            "algorithmicLogicalQubits"
        ],
        total_time_in_seconds=job_results["physicalCounts"]["runtime_in_s"],
        code_distance=job_results["logicalQubit"]["codeDistance"],
        logical_error_rate=job_results["errorBudget"]["logical"],
        decoder_info=None,
        magic_state_factory_name="default",
        routing_to_measurement_volume_ratio=0,
        extra=AzureExtra(
            cycle_time=job_results["logicalQubit"]["logicalCycleTime"],
            depth=job_results["physicalCounts"]["breakdown"]["algorithmicLogicalDepth"],
            raw_data=job_results,
        ),
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
        self,
        algorithm: AlgorithmImplementation,
    ) -> AzureResourceInfo:
        azure_error_budget: Dict[str, float] = {}
        if algorithm.error_budget is not None:
            azure_error_budget = {}
            azure_error_budget[
                "rotations"
            ] = algorithm.error_budget.transpilation_failure_tolerance
            remaining_error = algorithm.error_budget.hardware_failure_tolerance
            azure_error_budget["logical"] = remaining_error / 2
            azure_error_budget["tstates"] = remaining_error / 2
        if self.use_full_circuit:
            circuit = algorithm.program.full_circuit
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
            gate_time = self.hw_model.surface_code_cycle_time_in_seconds
            gate_time_string = f"{int(gate_time * 1e9)} ns"
            qubitParams = {
                "name": "custom gate-based",
                "instructionSet": "GateBased",
                "oneQubitGateTime": gate_time_string,
                # "oneQubitMeasurementTime": "30 μs",
                "oneQubitGateErrorRate": (self.hw_model.physical_qubit_error_rate),
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
