"""
Workflow & task defs.

To run this on Orquestra see the ``run.py`` script in the same directory.
"""
from orquestra import sdk

import time
from orquestra.quantum.evolution import time_evolution

from benchq import BasicArchitectureModel
from benchq.compilation import get_algorithmic_graph, pyliqtr_transpile_to_clifford_t
from benchq.problem_ingestion import (
    generate_jw_qubit_hamiltonian_from_mol_data,
    generate_mol_data_for_h_chain,
)
from benchq.resource_estimation.graph_compilation import (
    get_resource_estimations_for_graph,
)

standard_task = sdk.task(
    source_import=sdk.GitImport.infer(),
    # source_import=sdk.GitImport(
    #     repo_url="git@github.com:zapatacomputing/proto-benchq.git",
    #     git_ref="mstechly/workflows",
    # ),
    # dependency_imports=[
    #     sdk.GitImport(
    #         repo_url="git@github.com:zapatacomputing/proto-benchq.git",
    #         git_ref="mstechly/workflows",
    #     ),
    # ],
)

task_with_julia = sdk.task(
    source_import=sdk.GitImport.infer(),
    # source_import=sdk.GitImport(
    #     repo_url="git@github.com:zapatacomputing/proto-benchq.git",
    #     git_ref="mstechly/workflows",
    # ),
    custom_image="mstechly/ta2-julia-test"
    # dependency_imports=[
    #     sdk.GitImport(
    #         repo_url="git@github.com:zapatacomputing/proto-benchq.git",
    #         git_ref="mstechly/workflows",
    #     ),
    # ],
)


@standard_task
def get_operator(n_hydrogens):
    return generate_jw_qubit_hamiltonian_from_mol_data(
        generate_mol_data_for_h_chain(n_hydrogens)
    )


@standard_task
def time_evolution_task(operator, time):
    return time_evolution(operator, time)


@standard_task
def transpile_to_clifford_t(circuit, synthesis_accuracy):
    return pyliqtr_transpile_to_clifford_t(circuit, synthesis_accuracy)


@task_with_julia
def get_algorithmic_graph_task(circuit):
    return get_algorithmic_graph(circuit)


@standard_task
def get_resource_estimations_for_graph_task(
    graph, architecture_model, synthesis_accuracy
):
    return get_resource_estimations_for_graph(
        graph, architecture_model, synthesis_accuracy
    )


@sdk.workflow
def hydrogen_workflow():
    synthesis_accuracy = 1e-7
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-5,
        physical_gate_time_in_seconds=1e-8,
    )
    workflow_results = []
    for n_hydrogens in [1]:
        operator = get_operator(n_hydrogens)
        evolution_time = 1
        circuit = time_evolution_task(operator, evolution_time)

        clifford_t_circuit = transpile_to_clifford_t(circuit, synthesis_accuracy)
        graph = get_algorithmic_graph_task(clifford_t_circuit)
        resource_estimates = get_resource_estimations_for_graph_task(
            graph, architecture_model, synthesis_accuracy
        )
        workflow_results.append(resource_estimates)

    return workflow_results


def original_main():
    for n_hydrogens in [1]:

        # TA 1 part: specify the core computational capability

        # Generate instance
        mol_data = generate_mol_data_for_h_chain(n_hydrogens)

        # Convert instance to core computational problem instance
        operator = generate_jw_qubit_hamiltonian_from_mol_data(mol_data)
        print("Number of hydrogen atoms:", n_hydrogens)
        print("Number of qubits:", operator.n_qubits)

        # TA 1.5 part: model algorithmic circuit
        start = time.time()
        circuit = time_evolution(operator, time=1)
        end = time.time()
        print("Circuit generation time:", end - start)

        # TA 2 part: FTQC compilation

        synthesis_accuracy = 1e-10
        clifford_t_circuit = pyliqtr_transpile_to_clifford_t(
            circuit, synthesis_accuracy
        )
        graph = get_algorithmic_graph(clifford_t_circuit)

        # TA 2 part: model hardware resources
        architecture_model = BasicArchitectureModel(
            physical_gate_error_rate=1e-3,
            physical_gate_time_in_seconds=1e-6,
        )
        synthesis_accuracy = 1e-3
        start = time.time()
        resource_estimates = get_resource_estimations_for_graph(
            len(graph.nodes), architecture_model, synthesis_accuracy
        )
        end = time.time()
        print("Resource estimation time:", end - start)
        print(resource_estimates)
