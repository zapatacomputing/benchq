"""
Workflow & task defs.

To run this on Orquestra see the ``run.py`` script in the same directory.
"""

import mlflow

import os
import urllib3

from orquestra import sdk

from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.data_structures import ErrorBudget
from benchq.data_structures.hardware_architecture_models import IONTrapModel
from benchq.problem_ingestion import get_vlasov_hamiltonian

from benchq.mlflow.data_logging import (
    log_input_objects_to_mlflow,
    log_resource_info_to_mlflow,
)
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_custom_resource_estimation_pipeline,
    transpile_to_native_gates,
)

task_deps = [
    sdk.PythonImports("pyscf==2.2.0", "openfermionpyscf==0.5", "juliacall"),
    sdk.GithubImport("zapatacomputing/benchq", git_ref="mlflow-demo"),
]
gsc_task_deps = [
    sdk.PythonImports(
        "pyscf==2.2.0",
        "mlflow>=2.3.2",
        "stim==1.10",
    ),
    sdk.GithubImport("zapatacomputing/benchq", git_ref="mlflow-demo"),
]
standard_task = sdk.task(
    source_import=sdk.InlineImport(),
    dependency_imports=task_deps,
    resources=sdk.Resources(memory="4Gi"),
)

gsc_task = sdk.task(
    source_import=sdk.InlineImport(),
    dependency_imports=gsc_task_deps,
    custom_image="hub.nexus.orquestra.io/users/james.clark/benchq-ce:0.51.0",
)


@standard_task
def get_algorithm(operator, evolution_time, error_budget):
    algorithm = qsp_time_evolution_algorithm(
        operator, evolution_time, error_budget.total_failure_tolerance
    )
    return algorithm


@standard_task
def get_operator(problem_size):
    return get_vlasov_hamiltonian(N=problem_size, k=2.0, alpha=0.6, nu=0)


@gsc_task
def gsc_estimates(algorithm, architecture_model):

    resource_info = run_custom_resource_estimation_pipeline(
        algorithm,
        estimator=GraphResourceEstimator(hw_model=architecture_model),
        transformers=[
            transpile_to_native_gates,
            create_big_graph_from_subcircuits(),
        ],
    )

    f = open(os.environ["ORQUESTRA_PASSPORT_FILE"], "r")
    os.environ["MLFLOW_TRACKING_TOKEN"] = f.read()
    urllib3.disable_warnings()
    mlflow.set_tracking_uri("http://mlflow:8080")  # for remote orquestra

    # mlflow.set_tracking_uri("http://127.0.0.1:5000")  # for local testing

    mlflow.set_experiment("mlflow demo2")
    with mlflow.start_run():
        log_input_objects_to_mlflow(
            algorithm,
            "qsp_time_evolution_algorithm",
            architecture_model,
        )
        log_resource_info_to_mlflow(resource_info)

    return resource_info


@sdk.workflow
def mlflow_example_workflow():
    evolution_time = 5.0
    error_budget = ErrorBudget.from_even_split(total_failure_tolerance=1e-3)
    architecture_model = IONTrapModel(
        physical_qubit_error_rate=1e-3,
        surface_code_cycle_time_in_seconds=1e-6,
    )

    results = []

    for problem_size in [2, 3, 4]:
        operator = get_operator(problem_size)

        algorithm = get_algorithm(operator, evolution_time, error_budget)

        resource_info = gsc_estimates(algorithm, architecture_model)

        results.append(resource_info)

    return results
