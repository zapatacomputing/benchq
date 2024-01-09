"""
Workflow & task defs.

To run this on Orquestra see the ``run.py`` script in the same directory.
"""

import os

from orquestra import sdk

from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.algorithms.data_structures import ErrorBudget
from benchq.quantum_hardware_modeling.hardware_architecture_models import (
    BASIC_SC_ARCHITECTURE_MODEL,
)
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.resource_estimators.azure_estimator import (
    AzureResourceEstimator,
)
from benchq.resource_estimators.graph_estimators import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_custom_resource_estimation_pipeline,
    transpile_to_native_gates,
)

task_deps = [
    sdk.PythonImports("pyscf==2.2.0"),
    sdk.GithubImport("zapatacomputing/benchq", git_ref="main"),
]
ms_task_deps = [
    sdk.PythonImports(
        "pyscf==2.2.0",
        "azure-quantum==0.28.262328b1",
    ),
    sdk.GithubImport("zapatacomputing/benchq", git_ref="main"),
]

standard_task = sdk.task(
    source_import=sdk.InlineImport(),
    dependency_imports=task_deps,
    resources=sdk.Resources(memory="4Gi"),
)

task_with_julia = sdk.task(
    source_import=sdk.InlineImport(),
    dependency_imports=task_deps,
    custom_image="hub.nexus.orquestra.io/users/james.clark/benchq-ce:0.51.0",
)

ms_task = sdk.task(source_import=sdk.InlineImport(), dependency_imports=ms_task_deps)


@standard_task
def get_algorithm(operator, evolution_time, error_budget):
    algorithm = qsp_time_evolution_algorithm(
        operator, evolution_time, error_budget.total_failure_tolerance
    )
    return algorithm


@standard_task
def get_operator(problem_size):
    return get_vlasov_hamiltonian(N=problem_size, k=2.0, alpha=0.6, nu=0)


@task_with_julia
def gsc_estimates(algorithm, architecture_model):
    return run_custom_resource_estimation_pipeline(
        algorithm,
        estimator=GraphResourceEstimator(hw_model=architecture_model),
        transformers=[
            transpile_to_native_gates,
            create_big_graph_from_subcircuits(),
        ],
    )


@ms_task
def azure_estimates(algorithm, architecture_model):
    try:
        os.environ["AZURE_CLIENT_ID"] = sdk.secrets.get(
            "AZURE-CLIENT-ID",
            workspace_id="mlflow-benchq-testing-dd0cb1",
            config_name="darpa-benchmarking",
        )
        os.environ["AZURE_TENANT_ID"] = sdk.secrets.get(
            "AZURE-TENANT-ID",
            workspace_id="mlflow-benchq-testing-dd0cb1",
            config_name="darpa-benchmarking",
        )
        os.environ["AZURE_CLIENT_SECRET"] = sdk.secrets.get(
            "AZURE-CLIENT-SECRET",
            workspace_id="mlflow-benchq-testing-dd0cb1",
            config_name="darpa-benchmarking",
        )
        os.environ["AZURE_RESOURCE_ID"] = sdk.secrets.get(
            "AZURE-RESOURCE-ID",
            workspace_id="mlflow-benchq-testing-dd0cb1",
            config_name="darpa-benchmarking",
        )
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
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL

    results = []

    for problem_size in [2]:
        operator = get_operator(problem_size)

        algorithm = get_algorithm(operator, evolution_time, error_budget)

        results.append(azure_estimates(algorithm, architecture_model))
        results.append(gsc_estimates(algorithm, architecture_model))

    return results
