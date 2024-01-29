import os

import numpy as np
import pytest
from orquestra.quantum.circuits import CNOT, RZ, Circuit, H

from benchq.algorithms.data_structures import AlgorithmImplementation, ErrorBudget
from benchq.problem_embeddings.quantum_program import get_program_from_circuit
from benchq.quantum_hardware_modeling.hardware_architecture_models import IONTrapModel
from benchq.resource_estimators.azure_estimator import AzureResourceEstimator

SKIP_AZURE = pytest.mark.skipif(
    os.getenv("BENCHQ_TEST_AZURE") is None,
    reason="Azure tests can only run if BENCHQ_TEST_AZURE env variable is defined",
)


@SKIP_AZURE
@pytest.mark.skip(
    "It looks like Azure does not take information about the hardware into account"
)
def test_better_architecture_does_not_require_more_resources() -> None:
    low_quality_architecture_model = IONTrapModel(
        physical_qubit_error_rate=1e-4,
        surface_code_cycle_time_in_seconds=1e-6,
    )
    high_quality_architecture_model = IONTrapModel(
        physical_qubit_error_rate=1e-3,
        surface_code_cycle_time_in_seconds=1e-9,
    )

    # set circuit generation weight to 0
    error_budget = ErrorBudget.from_weights(1e-3, 0, 1, 1)

    quantum_program = get_program_from_circuit(
        Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    )

    alg_impl = AlgorithmImplementation(
        program=quantum_program, error_budget=error_budget, n_shots=1
    )

    low_quality_azure_re = AzureResourceEstimator(
        hw_model=low_quality_architecture_model
    )
    high_quality_azure_re = AzureResourceEstimator(
        hw_model=high_quality_architecture_model
    )
    low_quality_resource_estimates = low_quality_azure_re.estimate(alg_impl)

    high_quality_resource_estimates = high_quality_azure_re.estimate(alg_impl)

    assert (
        low_quality_resource_estimates.n_physical_qubits
        < high_quality_resource_estimates.n_physical_qubits
    )
    assert (
        low_quality_resource_estimates.code_distance
        <= high_quality_resource_estimates.code_distance
    )
    assert (
        low_quality_resource_estimates.total_time_in_seconds
        < high_quality_resource_estimates.total_time_in_seconds
    )


@SKIP_AZURE
def test_higher_error_budget_requires_less_resources() -> None:
    low_failure_tolerance = 1e-5
    high_failure_tolerance = 1e-3

    quantum_program = get_program_from_circuit(
        Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    )

    # set circuit generation weight to 0
    low_error_budget_impl = AlgorithmImplementation(
        program=quantum_program,
        error_budget=ErrorBudget.from_weights(low_failure_tolerance, 0, 1, 1),
        n_shots=1,
    )

    high_error_budget_impl = AlgorithmImplementation(
        program=quantum_program,
        error_budget=ErrorBudget.from_weights(high_failure_tolerance, 0, 1, 1),
        n_shots=1,
    )
    azure_re = AzureResourceEstimator()

    low_budget_resource_estimates = azure_re.estimate(low_error_budget_impl)
    high_budget_resource_estimates = azure_re.estimate(high_error_budget_impl)

    assert (
        low_budget_resource_estimates.n_physical_qubits
        > high_budget_resource_estimates.n_physical_qubits
    )
    assert (
        low_budget_resource_estimates.code_distance
        >= high_budget_resource_estimates.code_distance
    )
    assert (
        low_budget_resource_estimates.total_time_in_seconds
        > high_budget_resource_estimates.total_time_in_seconds
    )
