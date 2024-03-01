"""Workflow and task definitions.

To run this on Orquestra or locally use ``run.py`` script in the same directory.
"""

from dataclasses import replace
from typing import List

from orquestra import sdk

from benchq.algorithms.data_structures import (
    AlgorithmImplementation,
    ErrorBudget,
    GraphPartition,
)
from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.quantum_hardware_modeling import (
    BASIC_ION_TRAP_ARCHITECTURE_MODEL,
    BASIC_SC_ARCHITECTURE_MODEL,
    BasicArchitectureModel,
)
from benchq.resource_estimators.graph_estimators import (
    GraphResourceEstimator,
    create_graph_from_full_circuit,
    compile_to_native_gates,
)
from benchq.resource_estimators.resource_info import GraphResourceInfo

task_deps = [
    sdk.PythonImports(
        "pyscf==2.2.0", "openfermionpyscf==0.5", "stim==1.10", "juliapkg"
    ),
    sdk.GithubImport(
        "zapatacomputing/benchq",
    ),
]

task = sdk.task(
    source_import=sdk.InlineImport(),
    dependency_imports=task_deps,
    resources=sdk.Resources(memory="4Gi"),
    custom_image="hub.nexus.orquestra.io/users/james.clark/benchq-ce:0.50.0",
)


@task
def get_algorithm_implementation(
    problem_size: int, evolution_time: float, error_budget: ErrorBudget
) -> AlgorithmImplementation:
    """Task producing algorithm implementation.

    The produced algorithm is QSP time evolution algorithm, with given evolution
    time and error budget. The operator used is vlasov_hamiltonian of given size.
    """
    return qsp_time_evolution_algorithm(
        hamiltonian=get_vlasov_hamiltonian(N=problem_size, k=2.0, alpha=0.0, nu=0),
        time=evolution_time,
        failure_tolerance=error_budget.total_failure_tolerance,
    )


@task
def compile(
    algorithm_implementation: AlgorithmImplementation,
) -> AlgorithmImplementation:
    """Transpile algorithm implementation into a graph representationp.

    The transpilation has two steps:

    1. Simplifying rotations
    2. Converting the QuantumProgram of the algorithm into a graph representation.
    """
    compiled_algorithm = replace(
        algorithm_implementation,
        program=create_graph_from_full_circuit()(
            compile_to_native_gates(algorithm_implementation.program)
        ),
    )

    if not isinstance(compiled_algorithm.program, GraphPartition):
        raise TypeError(
            f"Expected AlgorithmImplementation[GraphPartition],"
            f"got {type(compiled_algorithm)}"
        )

    return compiled_algorithm


@task
def estimate_resources(
    algorithm_implementation: AlgorithmImplementation,
    architecture_model: BasicArchitectureModel,
) -> GraphResourceInfo:
    """Estimate resources for algorithm impl., assuming given architecture_model."""
    return GraphResourceEstimator(hw_model=architecture_model).estimate(
        algorithm_implementation
    )


@sdk.workflow(resources=sdk.Resources(memory="8Gi", nodes=2))
def estimation_workflow() -> List[GraphResourceInfo]:
    """The workflow for estimating resources.

    The workflow does the following:
    1. Creates algorithm implementation.
    2. Transpiles it into a graph representation.
    3. Defines two architecture models.
    4. Estimates the resources for the constructed algorithm implementation assuming
       the defined hardware models.

    The last step can be parallelized.

    The workflow does not use pieplines defined in benchq, and hence the graph
    compilation is not repeated for each hardware model, bur rather computed
    once and reused.
    """
    algorithm = get_algorithm_implementation(
        problem_size=2,
        evolution_time=5.0,
        error_budget=ErrorBudget.from_even_split(total_failure_tolerance=1e-3),
    )

    architecture_models: List[BasicArchitectureModel] = [
        BASIC_SC_ARCHITECTURE_MODEL,
        BASIC_ION_TRAP_ARCHITECTURE_MODEL,
    ]

    compiled_algorithm = compile(algorithm)

    return [
        estimate_resources(compiled_algorithm, model) for model in architecture_models
    ]
