import time
from copy import copy
from typing import Callable, Sequence, Tuple

import networkx as nx

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


def create_graphs_for_subcircuits(
    graph_production_method=get_algorithmic_graph_from_ruby_slippers,
) -> Callable[[QuantumProgram], GraphPartition]:
    def _transformer(program: QuantumProgram) -> GraphPartition:
        graphs_list = [
            graph_production_method(circuit) for circuit in program.subroutines
        ]
        return GraphPartition(program, graphs_list)

    return _transformer


def create_big_graph_from_subcircuits(
    graph_production_method=get_algorithmic_graph_from_ruby_slippers,
) -> Callable[[QuantumProgram], GraphPartition]:
    def _transformer(program: QuantumProgram) -> GraphPartition:
        print("Creating big graph from subcircuits...")
        big_circuit = program.full_circuit
        new_program = get_program_from_circuit(big_circuit)
        graph = graph_production_method(big_circuit)
        return GraphPartition(new_program, [graph])

    return _transformer


def remove_isolated_nodes(graph_partition: GraphPartition) -> GraphPartition:
    """Sometimes our circuits can generate a lot of extra nodes because of how
    RESET is implemented. This transformer removes these nodes from the
    graph to prevent them from influencing the costing. There are 3 known sources
    of isolated nodes:
        1. Unneeded resets at the beginning of the circuit.
        2. Decomposing rotations into gates sometimes gives bare nodes if a
             T gate is placed after a reset. (most concerning)
        3. Consecutive reset gates happening later on in the circuit.

    Args:
        graph_partition (GraphPartition): graph partition to remove the isoated
            nodes of.

    Returns:
        GraphPartition: input graph partition with isolated nodes removed.
    """
    print("Removing isolated nodes from graph...")
    start = time.time()
    new_graphs = []
    total_nodes_removed = 0
    for graph in graph_partition.subgraphs:
        n_nodes_removed, graph = remove_isolated_nodes_from_graph(graph)

        total_nodes_removed += n_nodes_removed
        new_graphs.append(graph)

    print(
        f"Removed {total_nodes_removed} isolated nodes "
        f"in {time.time() - start} seconds."
    )
    return GraphPartition(graph_partition.program, new_graphs)


def remove_isolated_nodes_from_graph(graph: nx.Graph) -> Tuple[int, nx.Graph]:
    cleaned_graph = copy(graph)
    isolated_nodes = list(nx.isolates(cleaned_graph))
    n_nodes_removed = len(isolated_nodes)

    cleaned_graph.remove_nodes_from(isolated_nodes)
    cleaned_graph = nx.convert_node_labels_to_integers(cleaned_graph)

    return n_nodes_removed, cleaned_graph
