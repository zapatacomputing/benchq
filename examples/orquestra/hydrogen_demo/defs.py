"""
Workflow & task defs.

To run this on Orquestra see the ``run.py`` script in the same directory.
"""
import time

from orquestra import sdk
from orquestra.quantum.evolution import time_evolution

from benchq import BasicArchitectureModel
from benchq.compilation import get_algorithmic_graph, pyliqtr_transpile_to_clifford_t
from benchq.problem_ingestion import generate_jw_qubit_hamiltonian_from_mol_data
from benchq.resource_estimation.graph_compilation import (
    get_resource_estimations_for_graph,
)
from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)

task_deps = [sdk.PythonImports("pyscf==2.1.0", "openfermionpyscf==0.5")]
standard_task = sdk.task(source_import=sdk.GitImport.infer(),
                         dependency_imports=task_deps)

task_with_julia = sdk.task(
    source_import=sdk.GitImport.infer(), dependency_imports=task_deps, custom_image="mstechly/ta2-julia-test"
)


@standard_task
def get_operator(n_hydrogens):
    return generate_jw_qubit_hamiltonian_from_mol_data(
        generate_hydrogen_chain_instance(n_hydrogens)
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
    for n_hydrogens in [3]:
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
        mol_data = generate_hydrogen_chain_instance(n_hydrogens)

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
