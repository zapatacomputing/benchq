"""
Workflow & task defs.

To run this on Orquestra see the ``run.py`` script in the same directory.
"""

import os

import mlflow
import urllib3
from orquestra import sdk

from benchq.algorithms.data_structures import ErrorBudget
from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.compilation.graph_states import get_implementation_compiler
from benchq.mlflow.data_logging import (
    log_input_objects_to_mlflow,
    log_resource_info_to_mlflow,
)
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.quantum_hardware_modeling.hardware_architecture_models import (
    BASIC_SC_ARCHITECTURE_MODEL,
)
from benchq.resource_estimators.graph_estimator import GraphResourceEstimator

task_deps = [
    sdk.PythonImports("pyscf==2.2.0", "openfermionpyscf==0.5"),
    sdk.GithubImport("zapatacomputing/benchq", git_ref="main"),
]
gsc_task_deps = [
    sdk.PythonImports(
        "pyscf==2.2.0",
        "mlflow>=2.3.2",
    ),
    sdk.GithubImport("zapatacomputing/benchq", git_ref="main"),
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
def gsc_estimates(algorithm, logical_architecture_model, hardware_architecture_model):
    estimator = GraphResourceEstimator()
    implementation_compiler = get_implementation_compiler()
    resource_info = estimator.compile_and_estimate(
        algorithm,
        implementation_compiler,
        logical_architecture_model,
        hardware_architecture_model,
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
            hardware_architecture_model,
        )
        log_resource_info_to_mlflow(resource_info)

    return resource_info


@sdk.workflow
def mlflow_example_workflow():
    evolution_time = 5.0
    error_budget = ErrorBudget.from_even_split(total_failure_tolerance=1e-3)
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL

    results = []

    for problem_size in [2, 3, 4]:
        operator = get_operator(problem_size)

        algorithm = get_algorithm(operator, evolution_time, error_budget)

        resource_info = gsc_estimates(algorithm, architecture_model)

        results.append(resource_info)

    return results
