################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
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

from orquestra.integrations.qiskit.conversions import import_from_qiskit
from qiskit.circuit import QuantumCircuit

from benchq import BasicArchitectureModel
from benchq.compilation import (
    get_algorithmic_graph,
    pyliqtr_transpile_to_clifford_t,
    simplify_rotations,
)
from benchq.resource_estimation.graph_compilation import (
    get_resource_estimations_for_graph,
)
from benchq.resource_estimation.graph_compilation_rotations import (
    get_resource_estimations_for_graph as get_resource_estimations_for_graph_with_rotations,
)

# This demo shows how to get resource estimation for a circuit in two ways:
# First, with explicit transpilation of rotations into Clifford + T
# Second, without the transpilation, with passing rotations through Jabalizer.


def main(file_name="circuits/h_chain_circuit.qasm"):
    # Uncomment to see Jabalizer output
    # logging.getLogger().setLevel(logging.INFO)
    # TA 2 part: model hardware resources
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
    qiskit_circuit = QuantumCircuit.from_qasm_file(file_name)
    # TA 2 part: FTQC compilation
    # synthesis_accuracy = 1e-1
    synthesis_accuracy = 1e-2
    # synthesis_accuracy = 0.01
    # breakpoint()
    clifford_t_circuit = pyliqtr_transpile_to_clifford_t(
        qiskit_circuit, synthesis_accuracy
    )
    graph = get_algorithmic_graph(clifford_t_circuit)

    logical_error_rate = 1e-3
    start = time.time()
    resource_estimates = get_resource_estimations_for_graph(
        graph, architecture_model, logical_error_rate, plot=True
    )
    end = time.time()
    print("Resource estimation time FULL:", end - start)
    print(resource_estimates)

    circuit_with_rotations = import_from_qiskit(qiskit_circuit)
    circuit_with_rotations_2 = simplify_rotations(circuit_with_rotations)

    graph = get_algorithmic_graph(circuit_with_rotations_2)
    start = time.time()
    resource_estimates = get_resource_estimations_for_graph_with_rotations(
        graph, architecture_model, logical_error_rate, plot=True
    )
    end = time.time()
    print("Resource estimation time ROTATIONS:", end - start)
    print(resource_estimates)


if __name__ == "__main__":
    main()
