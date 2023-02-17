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
import time

from benchq import BasicArchitectureModel
from benchq.compilation import get_algorithmic_graph, pyliqtr_transpile_to_clifford_t
from benchq.resource_estimation.graph_compilation import (
    get_resource_estimations_for_graph,
)
from qiskit.circuit import QuantumCircuit


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

    # TA 2 part: model hardware resources
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
    synthesis_accuracy = 1e-3
    start = time.time()
    resource_estimates = get_resource_estimations_for_graph(
        graph, architecture_model, synthesis_accuracy, verbose=True
    )
    end = time.time()
    print("Resource estimation time:", end - start)
    print(resource_estimates)


if __name__ == "__main__":
    main()
