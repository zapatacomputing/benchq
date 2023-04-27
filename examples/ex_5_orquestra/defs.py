"""
Workflow & task defs.

To run this on Orquestra see the ``run.py`` script in the same directory.
"""
import time

from orquestra import sdk
from orquestra.quantum.evolution import time_evolution

from benchq.compilation import (
    get_algorithmic_graph_from_Jabalizer,
    pyliqtr_transpile_to_clifford_t,
)
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_resource_estimation_pipeline,
    simplify_rotations,
)
from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm

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
    source_import=sdk.GitImport.infer(), dependency_imports=task_deps
)

task_with_julia = sdk.task(
    source_import=sdk.GitImport.infer(),
    dependency_imports=task_deps,
    custom_image="mstechly/ta2-julia-test",
)

ms_task = sdk.task(source_import=sdk.GitImport.infer(), dependency_imports=ms_task_deps)


@standard_task
def get_program(operator, evolution_time, error_budget):
    algorithm = qsp_time_evolution_algorithm(
        operator, evolution_time, error_budget.circuit_generation_weight
    )
    return algorithm.program


@standard_task
def get_operator(problem_size):
    return get_vlasov_hamiltonian(N=problem_size, k=2.0, alpha=0.6, nu=0)


@standard_task
def time_evolution_task(operator, time):
    return time_evolution(operator, time)


@standard_task
def transpile_to_clifford_t(circuit, circuit_precision):
    return pyliqtr_transpile_to_clifford_t(circuit, circuit_precision=circuit_precision)


@task_with_julia
def get_algorithmic_graph_task(circuit):
    return get_algorithmic_graph_from_Jabalizer(circuit)


@standard_task
def get_resource_estimations_for_graph_task(
    graph, architecture_model, synthesis_accuracy
):
    return get_resource_estimations_for_graph(
        graph, architecture_model, synthesis_accuracy
    )


@ms_task
def gsc_estimates(program, error_budget, architecture_model):
    return run_resource_estimation_pipeline(
        program,
        error_budget,
        estimator=GraphResourceEstimator(hw_model=architecture_model),
        transformers=[
            simplify_rotations,
            create_big_graph_from_subcircuits(delayed_gate_synthesis=True),
        ],
    )


from orquestra import sdk
import os
from benchq.data_structures import ErrorBudget, BasicArchitectureModel
from benchq.resource_estimation.azure import AzureResourceEstimator
from benchq.resource_estimation.graph import run_resource_estimation_pipeline
from orquestra.sdk.exceptions import NotFoundError


@ms_task
def azure_estimates(program, error_budget, architecture_model):
    try:
        os.environ["AZURE_CLIENT_ID"] = sdk.secrets.get("AZURE-CLIENT-ID")
        os.environ["AZURE_TENANT_ID"] = sdk.secrets.get("AZURE-TENANT-ID")
        os.environ["AZURE_CLIENT_SECRET"] = sdk.secrets.get("AZURE-CLIENT-SECRET")
        os.environ["AZURE_RESOURCE_ID"] = sdk.secrets.get("AZURE-RESOURCE-ID")
    except NotFoundError as e:
        print("Cannot load the Azure secrets, assuming code is running locally")
        print("Original error message:", e)

    return run_resource_estimation_pipeline(
        program,
        error_budget,
        estimator=AzureResourceEstimator(),
        transformers=[],
    )


@sdk.workflow
def example_workflow():

    evolution_time = 5.0
    error_budget = ErrorBudget(ultimate_failure_tolerance=1e-3)
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )

    results = []

    for problem_size in [2]:
        operator = get_operator(problem_size)

        program = get_program(operator, evolution_time, error_budget)

        results.append(azure_estimates(program, error_budget, architecture_model))
        results.append(gsc_estimates(program, error_budget, architecture_model))

    return results
