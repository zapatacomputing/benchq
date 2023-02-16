################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
"""
Objectives:

1. Have a "benchq" script, which takes in a circuit and outputs a resource estimate
    - Prototype, but needs to make sense in principle.
    - Well defined I/Os


2. Have a "darpa-1.5" script, which creates a circuit from an application instance.
    - This is mostly for completeness and illustratory purposes
    - Software can be quite crappy
"""
import logging
import time

import networkx as nx
from graph_state_generation.optimizers import (
    approximate_static_stabilizer_reduction,
    fast_maximal_independent_set_stabilizer_reduction,
    greedy_stabilizer_measurement_scheduler,
    random_mapper,
)
from graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler
from qiskit.circuit import QuantumCircuit

from benchq import BasicArchitectureModel
from benchq.compilation import get_algorithmic_graph, pyliqtr_transpile_to_clifford_t
from benchq.resource_estimation.graph_compilation import get_resource_estimations_for_graph


def main(file_name="h_chain_circuit.qasm"):
    # Uncomment to see Jabalizer output
    # logging.getLogger().setLevel(logging.INFO)

    qiskit_circuit = QuantumCircuit.from_qasm_file(file_name)

    # TA 2 part: FTQC compilation
    synthesis_accuracy = 1e-10
    clifford_t_circuit = pyliqtr_transpile_to_clifford_t(
        qiskit_circuit, synthesis_accuracy
    )
    graph = get_algorithmic_graph(clifford_t_circuit)

    # substrate scheduler
    connected_graph = graph.copy()
    connected_graph.remove_nodes_from(list(nx.isolates(graph)))  # remove isolated nodes
    connected_graph = nx.convert_node_labels_to_integers(connected_graph)

    scheduler_only_compiler = TwoRowSubstrateScheduler(
        connected_graph, stabilizer_scheduler=greedy_stabilizer_measurement_scheduler
    )
    scheduler_only_compiler.run()
    print(
        "Number of measurements required after substrate scheduler:"
        + str(scheduler_only_compiler.measurement_steps)
    )

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


if __name__ == "__main__":
    main()
