################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
"""
Copy of example 1 with added code to demonstrate logging params and metrics to mlflow
"""

import mlflow
from orquestra.integrations.qiskit.conversions import import_from_qiskit
from qiskit.circuit import QuantumCircuit

from benchq.algorithms.data_structures import AlgorithmImplementation, ErrorBudget
from benchq.mlflow.data_logging import (
    log_input_objects_to_mlflow,
    log_resource_info_to_mlflow,
)
from benchq.problem_embeddings import QuantumProgram
from benchq.quantum_hardware_modeling import BASIC_SC_ARCHITECTURE_MODEL
from benchq.resource_estimators.graph_estimators import (
    GraphResourceEstimator,
    create_graph_from_full_circuit,
    get_custom_resource_estimation,
    transpile_to_clifford_t,
    compile_to_native_gates,
)


def main(file_name, total_failure_tolerance=1e-3):
    # Uncomment to see extra debug output
    # logging.getLogger().setLevel(logging.INFO)

    # We can load a circuit from a QASM file using qiskit
    qiskit_circuit = QuantumCircuit.from_qasm_file(file_name)
    # In order to perform resource estimation we need to translate it to a
    # benchq program.
    quantum_program = QuantumProgram.from_circuit(import_from_qiskit(qiskit_circuit))

    # Error budget is used to define what should be the failure rate of running
    # the whole calculation. It also allows to set relative weights for different
    # parts of the calculation, such as gate synthesis or circuit generation.
    error_budget = ErrorBudget.from_even_split(
        total_failure_tolerance=total_failure_tolerance
    )

    # algorithm implementation encapsulates the how the algorithm is implemented
    # including the program, the number of times the program must be repeated,
    # and the error budget which will be used in the circuit.
    algorithm_implementation = AlgorithmImplementation(quantum_program, error_budget, 1)

    # Architecture model is used to define the hardware model.
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL

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
    gsc_resource_estimates = get_custom_resource_estimation(
        algorithm_implementation,
        estimator=GraphResourceEstimator(architecture_model),
        transformers=[
            compile_to_native_gates,
            transpile_to_clifford_t(error_budget),
            create_graph_from_full_circuit(),
        ],
    )

    # mlflow.set_tracking_uri("http://127.0.0.1:5000")
    with mlflow.start_run():
        log_input_objects_to_mlflow(
            algorithm_implementation,
            "simple qiskit circuit",
            BASIC_SC_ARCHITECTURE_MODEL,
        )
        log_resource_info_to_mlflow(gsc_resource_estimates)


if __name__ == "__main__":
    for i in range(5):
        main("data/example_circuit.qasm", 10 ** (-i))
