import time
from copy import copy
from typing import Callable, Sequence, Tuple

import networkx as nx
from dataclasses import dataclass

from ...algorithms.data_structures import ErrorBudget, GraphPartition
from ...compilation import (
    get_algorithmic_graph_from_ruby_slippers,
    pyliqtr_transpile_to_clifford_t,
)
from ...compilation import transpile_to_native_gates as _transpile_to_native_gates
from ...problem_embeddings.quantum_program import (
    QuantumProgram,
    get_program_from_circuit,
)
from orquestra import sdk
from ..resource_info import GraphData

from .graph_estimator import substrate_scheduler, remove_isolated_nodes_from_graph


def _distribute_transpilation_failure_tolerance(
    program: QuantumProgram, total_transpilation_failure_tolerance: float
) -> Sequence[float]:
    n_rots_per_subroutine = [
        program.count_operations_in_subroutine(i, ["RX", "RY", "RZ"])
        for i in range(len(program.subroutines))
    ]
    # Not using program n_rotation_gates because we already computed partial
    # counts for subroutines.
    n_total_rots = sum(
        n_rotations * multi
        for n_rotations, multi in zip(n_rots_per_subroutine, program.multiplicities)
    )

    return (
        [0 for _ in program.subroutines]
        if n_total_rots == 0
        else [
            total_transpilation_failure_tolerance * count / n_total_rots
            for count in n_rots_per_subroutine
        ]
    )


def synthesize_clifford_t(
    error_budget: ErrorBudget,
) -> Callable[[QuantumProgram], QuantumProgram]:
    def _transformer(program: QuantumProgram) -> QuantumProgram:
        tolerances = _distribute_transpilation_failure_tolerance(
            program, error_budget.transpilation_failure_tolerance
        )
        circuits = [
            pyliqtr_transpile_to_clifford_t(circuit, circuit_precision=tolerance)
            for circuit, tolerance in zip(program.subroutines, tolerances)
        ]
        return program.replace_circuits(circuits)

    return _transformer


def transpile_to_native_gates(program: QuantumProgram) -> QuantumProgram:
    print("Transpiling to native gates...")
    start = time.time()
    circuits = [_transpile_to_native_gates(circuit) for circuit in program.subroutines]
    print(f"Transpiled in {time.time() - start} seconds.")
    return QuantumProgram(
        circuits,
        steps=program.steps,
        calculate_subroutine_sequence=program.calculate_subroutine_sequence,
    )


@dataclass
class DistributedGraphCreationOutputWrapper:
    num_logical_qubits: int
    num_graph_preparation_tocks: int
    num_consumption_tocks: int
    num_nodes: int


# @sdk.task(
#     dependency_imports=[sdk.PythonImports("benchq[dev]")],
#     custom_image="hub.stage.nexus.orquestra.io/zapatacomputing/benchq-ce:3eec2c8-sdk0.60.0",
# )
@sdk.task(
    source_import=sdk.GithubImport(
        "zapatacomputing/benchq",
        git_ref="faster-kahns-algo",
    ),
    custom_image="hub.nexus.orquestra.io/zapatacomputing/benchq-ce:3eec2c8-sdk0.60.0",
)
def distributed_graph_creation(circuit, graph_production_method):
    graph, num_consumption_tocks, num_logical_qubits = graph_production_method(circuit)

    compiler = substrate_scheduler(graph, "fast")
    n_measurement_steps = len(compiler.measurement_steps)

    output = DistributedGraphCreationOutputWrapper(
        num_logical_qubits,
        n_measurement_steps,
        num_consumption_tocks,
        graph.number_of_nodes(),
    )

    return output


@sdk.task(
    source_import=sdk.GithubImport(
        "zapatacomputing/benchq",
        git_ref="faster-kahns-algo",
    ),
    custom_image="hub.nexus.orquestra.io/zapatacomputing/benchq-ce:3eec2c8-sdk0.60.0",
)
def get_full_graph_data(program, *graph_data_list):
    graph_data_list = list(graph_data_list)

    num_logical_qubits = 0
    num_measurement_steps = 0
    num_nodes = 0
    for subroutine in program.calculate_subroutine_sequence(program.steps):
        num_logical_qubits = max(
            graph_data_list[subroutine].num_logical_qubits, num_logical_qubits
        )
        num_measurement_steps += (
            graph_data_list[subroutine].num_graph_preparation_tocks
            + graph_data_list[subroutine].num_consumption_tocks
        )
        num_nodes += graph_data_list[subroutine].num_nodes

    return GraphData(
        max_graph_degree=num_logical_qubits,
        n_nodes=num_nodes,
        n_t_gates=program.n_t_gates,
        n_rotation_gates=program.n_rotation_gates,
        n_measurement_steps=num_measurement_steps,
    )


def create_graphs_for_subcircuits(
    graph_production_method=get_algorithmic_graph_from_ruby_slippers,
    destination="local",
    config_name="darpa-ta1",
    workspace_id="darpa-phase-ii-gsc-resource-estimates-8a7c3b",
    project_id="migration",
    num_cores=3,
) -> Callable[[QuantumProgram], GraphPartition]:

    @sdk.workflow(resources=sdk.Resources(cpu=str(num_cores), memory="16Gi"))
    def graph_wf(program: QuantumProgram) -> GraphPartition:
        graph_data_list = [
            distributed_graph_creation(circuit, graph_production_method)
            for circuit in program.subroutines
        ]

        return get_full_graph_data(program, *graph_data_list)

    def _transformer(program: QuantumProgram) -> GraphPartition:
        print("Beginning compilation...")
        if destination == "debug":
            wf_run = graph_wf(program).run("in_process")
        elif destination == "local":
            wf_run = graph_wf(program).run("ray")
        elif destination == "remote":
            wf_run = graph_wf(program).run(
                config_name,
                workspace_id=workspace_id,
                project_id=project_id,
            )
        graph_data = wf_run.get_results(wait=True)
        print("Compilation complete.")

        return graph_data

    return _transformer


def create_big_graph_from_subcircuits(
    graph_production_method=get_algorithmic_graph_from_ruby_slippers,
) -> Callable[[QuantumProgram], GraphPartition]:
    def _transformer(program: QuantumProgram) -> GraphPartition:
        print("Beginning compilation...")
        big_circuit = program.full_circuit
        new_program = get_program_from_circuit(big_circuit)
        graph = graph_production_method(big_circuit)
        print("Compilation complete.")
        return GraphPartition(new_program, [graph])

    return _transformer
