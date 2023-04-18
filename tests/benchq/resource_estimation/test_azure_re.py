import os

import numpy as np
import pytest
from orquestra.quantum.circuits import CNOT, RX, RY, RZ, Circuit, H, T

from benchq.data_structures import BasicArchitectureModel
from benchq.data_structures.quantum_program import get_program_from_circuit
from benchq.resource_estimation.azure import AzureResourceEstimator

SKIP_AZURE = pytest.mark.skipif(
    os.getenv("BENCHQ_TEST_AZURE") is None,
    reason="Azure tests can only run if BENCHQ_TEST_AZURE env variable is defined",
)


@SKIP_AZURE
@pytest.mark.skip(
    "It looks like Azure does not take information about the hardware into account"
)
def test_better_architecture_does_not_require_more_resources():
    low_quality_architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-4,
        physical_gate_time_in_seconds=1e-6,
    )
    high_quality_architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-9,
    )
    error_budget = {
        "total_error": 1e-3,
        "synthesis_error_rate": 0.5,
        "ec_error_rate": 0.5,
    }

    quantum_program = get_program_from_circuit(
        Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    )
    low_quality_azure_re = AzureResourceEstimator(
        hw_model=low_quality_architecture_model
    )
    high_quality_azure_re = AzureResourceEstimator(
        hw_model=high_quality_architecture_model
    )
    low_quality_resource_estimates = low_quality_azure_re.estimate(
        quantum_program, error_budget
    )
    high_quality_resource_estimates = high_quality_azure_re.estimate(
        quantum_program, error_budget
    )
    assert (
        low_quality_resource_estimates.physical_qubit_count
        < high_quality_resource_estimates.physical_qubit_count
    )
    assert (
        low_quality_resource_estimates.distance
        <= high_quality_resource_estimates.distance
    )
    assert (
        low_quality_resource_estimates.total_time
        < high_quality_resource_estimates.total_time
    )


@SKIP_AZURE
def test_higher_error_budget_requires_less_resources():
    low_failure_rate = 1e-5
    high_failure_rate = 1e-3

    low_error_budget = {
        "total_error": low_failure_rate,
        "synthesis_error_rate": 0.5,
        "ec_error_rate": 0.5,
    }
    high_error_budget = {
        "total_error": high_failure_rate,
        "synthesis_error_rate": 0.5,
        "ec_error_rate": 0.5,
    }
    quantum_program = get_program_from_circuit(
        Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    )
    azure_re = AzureResourceEstimator()

    low_budget_resource_estimates = azure_re.estimate(quantum_program, low_error_budget)
    high_budget_resource_estimates = azure_re.estimate(
        quantum_program, high_error_budget
    )

    assert (
        low_budget_resource_estimates.physical_qubit_count
        > high_budget_resource_estimates.physical_qubit_count
    )
    assert (
        low_budget_resource_estimates.distance
        >= high_budget_resource_estimates.distance
    )
    assert (
        low_budget_resource_estimates.total_time
        > high_budget_resource_estimates.total_time
    )
