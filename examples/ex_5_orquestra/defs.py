"""
Workflow & task defs.

To run this on Orquestra see the ``run.py`` script in the same directory.
"""

import os

from orquestra import sdk

from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.data_structures import BasicArchitectureModel, ErrorBudget
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.resource_estimation.azure import AzureResourceEstimator
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_custom_resource_estimation_pipeline,
    simplify_rotations,
)

task_deps = [sdk.PythonImports("pyscf==2.2.0", "openfermionpyscf==0.5")]
ms_task_deps = [
    sdk.PythonImports(
        "pyscf==2.2.0",
        "openfermionpyscf==0.5",
        "azure-quantum==0.28.262328b1",
        "pyqir==0.8.0",
        "qiskit_qir==0.3.1",
        "qiskit_ionq==0.3.10",
    )
]
standard_task = sdk.task(
    source_import=sdk.GitImport.infer(),
    dependency_imports=task_deps,
    resources=sdk.Resources(memory="4Gi"),
)

task_with_julia = sdk.task(
    source_import=sdk.GitImport.infer(),
    dependency_imports=task_deps,
    custom_image="mstechly/ta2-julia-test",
)

ms_task = sdk.task(source_import=sdk.GitImport.infer(), dependency_imports=ms_task_deps)


@standard_task
def get_algorithm(operator, evolution_time, error_budget):
    algorithm = qsp_time_evolution_algorithm(
        operator, evolution_time, error_budget.total_failure_tolerance
    )
    return algorithm


@standard_task
def get_operator(problem_size):
    return get_vlasov_hamiltonian(N=problem_size, k=2.0, alpha=0.6, nu=0)


@ms_task
def gsc_estimates(algorithm, architecture_model):
    return run_custom_resource_estimation_pipeline(
        algorithm,
        estimator=GraphResourceEstimator(hw_model=architecture_model),
        transformers=[
            simplify_rotations,
            create_big_graph_from_subcircuits(),
        ],
    )


@ms_task
def azure_estimates(algorithm, architecture_model):
    try:
        os.environ["AZURE_CLIENT_ID"] = sdk.secrets.get("AZURE-CLIENT-ID")
        os.environ["AZURE_TENANT_ID"] = sdk.secrets.get("AZURE-TENANT-ID")
        os.environ["AZURE_CLIENT_SECRET"] = sdk.secrets.get("AZURE-CLIENT-SECRET")
        os.environ["AZURE_RESOURCE_ID"] = sdk.secrets.get("AZURE-RESOURCE-ID")
    except sdk.exceptions.NotFoundError as e:
        print(
            "Cannot load the Azure secrets for execution on cluster, "
            "assuming code is running locally"
        )
        print("Original error message:", e)

    return run_custom_resource_estimation_pipeline(
        algorithm,
        estimator=AzureResourceEstimator(),
        transformers=[],
    )


@sdk.workflow
def example_workflow():
    evolution_time = 5.0
    error_budget = ErrorBudget.from_even_split(total_failure_tolerance=1e-3)
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )

    results = []

    for problem_size in [2]:
        operator = get_operator(problem_size)

        algorithm = get_algorithm(operator, evolution_time, error_budget)

        results.append(azure_estimates(algorithm, architecture_model))
        results.append(gsc_estimates(algorithm, architecture_model))

    return results
