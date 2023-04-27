################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
Basic example of how to perform resource estimation of a circuit from a QASM file.
"""

from orquestra.integrations.qiskit.conversions import import_from_qiskit
from qiskit.circuit import QuantumCircuit

from benchq import BasicArchitectureModel
from benchq.data_structures import ErrorBudget, get_program_from_circuit
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_resource_estimation_pipeline,
    simplify_rotations,
    synthesize_clifford_t,
)


def main(file_name):
    # Uncomment to see extra debug output
    # logging.getLogger().setLevel(logging.INFO)

    # We can load a circuit from a QASM file using qiskit
    qiskit_circuit = QuantumCircuit.from_qasm_file(file_name)
    # In order to perform resource estimation we need to translate it to a
    # benchq program.
    quantum_program = get_program_from_circuit(import_from_qiskit(qiskit_circuit))

    # Error budget is used to define what should be the failure rate of running
    # the whole calculation. It also allows to set relative weights for different
    # parts of the calculation, such as gate synthesis or circuit generation.
    error_budget = ErrorBudget(ultimate_failure_tolerance=1e-3)

    # Architecture model is used to define the hardware model.
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )

    # Here we run the resource estimation pipeline.
    # In this case before performing estimation we use the following transformers:
    # 1. Simplify rotations – it is a simple transpilation that removes redundant
    # rotations from the circuit, such as RZ(0) or RZ(2pi) and replaces RX and RY
    # gates with RZs
    # 2. Gate synthesis – replaces all RZ gates with Clifford+T gates
    # 3. Create big graph from subcircuits – this transformer is used to create
    # a graph from subcircuits. It is needed to perform resource estimation using
    # the graph resource estimator. In this case we use delayed gate synthesis, as
    # we have already performed gate synthesis in the previous step.
    gsc_resource_estimates = run_resource_estimation_pipeline(
        quantum_program,
        error_budget,
        estimator=GraphResourceEstimator(architecture_model),
        transformers=[
            simplify_rotations,
            synthesize_clifford_t(error_budget),
            create_big_graph_from_subcircuits(delayed_gate_synthesis=False),
        ],
    )
    print("Resource estimation results:")
    print(gsc_resource_estimates)


if __name__ == "__main__":
    main("data/example_circuit.qasm")
