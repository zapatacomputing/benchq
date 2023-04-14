################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import os

from azure.quantum.qiskit import AzureQuantumProvider
from orquestra.integrations.qiskit.conversions import export_to_qiskit
from typing import Optional
from qiskit.tools.monitor import job_monitor
from orquestra.quantum.circuits import Circuit
from dataclasses import dataclass

from ..data_structures import QuantumProgram, BasicArchitectureModel
from collections import Counter


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


class AzureResourceEstimator:
    def __init__(
        self,
        hw_model: Optional[BasicArchitectureModel] = None,
        use_full_circuit: bool = False,
    ):
        self.hw_model = hw_model
        self.use_full_circuit = use_full_circuit

    def estimate(self, program: QuantumProgram, error_budget) -> AzureResourceInfo:
        if error_budget is not None:
            total_error = error_budget["total_error"]
            azure_error_budget = {}
            azure_error_budget["rotations"] = (
                error_budget["synthesis_error_rate"] * total_error
            )
            remaining_error = error_budget["synthesis_error_rate"] * total_error
            azure_error_budget["logical"] = remaining_error / 2
            azure_error_budget["tstates"] = remaining_error / 2
        if self.use_full_circuit:
            circuit = program.full_circuit()
            return self._estimate_resources_for_circuit(circuit, azure_error_budget)
        else:
            raise NotImplementedError(
                "Resource estimation for Quantum Programs which are not consisting "
                "of a single circuit is not implemented yet."
            )

    def _estimate_resources_for_circuit(
        self, circuit: Circuit, error_budget
    ) -> AzureResourceInfo:
        """_summary_

        Args:
            circuit: _description_
            error_budget: _description_

        Returns:
            _description_
        """
        if self.hw_model is not None:
            gate_time = self.hw_model.physical_gate_time_in_seconds
            gate_time_string = f"{int(gate_time * 1e9)} ns"
            qubit = {
                "name": "slow gate-based",
                "oneQubitGateTime": gate_time_string,
                # "oneQubitMeasurementTime": "30 μs",
                "oneQubitGateErrorRate": self.hw_model.physical_gate_error_rate,
                # "tStateErrorRate": 1e-3
            }
        else:
            qubit = None

        qiskit_circuit = export_to_qiskit(circuit)
        provider = AzureQuantumProvider(
            resource_id=os.getenv("AZURE_RESOURCE_ID"), location="East US"
        )

        backend = provider.get_backend("microsoft.estimator")
        job = backend.run(qiskit_circuit, qubit=qubit, errorBudget=error_budget)

        job_monitor(job)
        full_results = job.result().data()
        del full_results["reportData"]
        full_results["physicalCounts"]["runtime_in_s"] = (
            full_results["physicalCounts"]["runtime"] / 1e9
        )
        return full_results
