################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
Basic example of how to perform resource estimation of a circuit from a QASM file.
WARNING: This example requires the pyscf extra. run `pip install benchq[pyscf]`
to install the extra.
"""

import os

from qiskit.circuit import QuantumCircuit

from benchq.algorithms.data_structures import AlgorithmImplementation, ErrorBudget
from benchq.compilation.graph_states import get_ruby_slippers_circuit_compiler
from benchq.compilation.graph_states.implementation_compiler import (
    get_implementation_compiler,
)
from benchq.logical_architecture_modeling.graph_based_logical_architectures import (
    AllToAllArchitectureModel,
    TwoRowBusArchitectureModel,
)
from benchq.quantum_hardware_modeling import BASIC_SC_ARCHITECTURE_MODEL
from benchq.resource_estimators.graph_estimator import GraphResourceEstimator


def main(file_name):
    # Uncomment to see extra debug output
    # logging.getLogger().setLevel(logging.INFO)

    # We can load a circuit from a QASM file using qiskit
    qiskit_circuit = QuantumCircuit.from_qasm_file(file_name)

    # Error budget is used to define what should be the failure rate of running
    # the whole calculation. It also allows to set relative weights for different
    # parts of the calculation, such as gate synthesis or circuit generation.
    error_budget = ErrorBudget.from_even_split(total_failure_tolerance=1e-3)

    # algorithm implementation encapsulates the how the algorithm is implemented
    # including the program, the number of times the program must be repeated,
    # and the error budget which will be used in the circuit.
    algorithm_implementation = AlgorithmImplementation.from_circuit(
        qiskit_circuit, error_budget, 1
    )

    # Here we run the resource estimation pipeline:
    # Architecture model is used to define the hardware model.
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL
    # Create the estimator object, we can optimize for "Time" or "Space"
    estimator = GraphResourceEstimator(optimization="Time", verbose=True)
    # Use the default compiler
    compiler = get_implementation_compiler(
        circuit_compiler=get_ruby_slippers_circuit_compiler(),
        destination="single-thread",
    )

    all_to_all_architecture = AllToAllArchitectureModel()

    # Put all the pieces together to get a resource estimate
    gsc_resource_estimates = estimator.compile_and_estimate(
        algorithm_implementation,
        compiler,
        all_to_all_architecture,
        architecture_model,
    )
    print("Resource estimation results:")
    print(gsc_resource_estimates)


if __name__ == "__main__":
    current_directory = os.path.dirname(__file__)
    main(current_directory + "/data/ghz_circuit.qasm")
