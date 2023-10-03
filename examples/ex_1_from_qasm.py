################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
Basic example of how to perform resource estimation of a circuit from a QASM file.
"""

from orquestra.integrations.qiskit.conversions import import_from_qiskit
from qiskit.circuit import QuantumCircuit

from benchq.data_structures import (
    BASIC_SC_ARCHITECTURE_MODEL,
    AlgorithmImplementation,
    ErrorBudget,
    get_program_from_circuit,
)
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_custom_resource_estimation_pipeline,
    synthesize_clifford_t,
    transpile_to_native_gates,
)
from benchq.compilation.julia_utils import (
    get_ruby_slippers_compiler,
    get_algorithmic_graph_from_Jabalizer,
    get_algorithmic_graph_from_graphsim_mini,
)


def main(file_name):
    # Uncomment to see extra debug output
    # logging.getLogger().setLevel(logging.INFO)

    print("loading circuit...")
    # We can load a circuit from a QASM file using qiskit
    qiskit_circuit = QuantumCircuit.from_qasm_file(file_name)
    # In order to perform resource estimation we need to translate it to a
    # benchq program.
    quantum_program = get_program_from_circuit(import_from_qiskit(qiskit_circuit))

    # Error budget is used to define what should be the failure rate of running
    # the whole calculation. It also allows to set relative weights for different
    # parts of the calculation, such as gate synthesis or circuit generation.
    error_budget = ErrorBudget.from_even_split(total_failure_tolerance=1e-3)

    # algorithm implementation encapsulates the how the algorithm is implemented
    # including the program, the number of times the program must be repeated,
    # and the error budget which will be used in the circuit.
    algorithm_implementation = AlgorithmImplementation(quantum_program, error_budget, 1)

    # Architecture model is used to define the hardware model.
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL

    print("Running resource estimation for Ruby Slippers...")
    try:
        run_custom_resource_estimation_pipeline(
            algorithm_implementation,
            estimator=GraphResourceEstimator(architecture_model),
            transformers=[
                transpile_to_native_gates,
                create_big_graph_from_subcircuits(
                    graph_production_method=get_ruby_slippers_compiler()
                ),
            ],
        )
    except:
        pass

    # print("Running resource estimation for Graph Sim mini...")
    # try:
    #     run_custom_resource_estimation_pipeline(
    #         algorithm_implementation,
    #         estimator=GraphResourceEstimator(architecture_model),
    #         transformers=[
    #             transpile_to_native_gates,
    #             create_big_graph_from_subcircuits(
    #                 graph_production_method=get_algorithmic_graph_from_graphsim_mini
    #             ),
    #         ],
    #     )
    # except:
    #     pass

    # print("Running resource estimation for Jabalizer...")
    # try:
    #     run_custom_resource_estimation_pipeline(
    #         algorithm_implementation,
    #         estimator=GraphResourceEstimator(architecture_model),
    #         transformers=[
    #             transpile_to_native_gates,
    #             create_big_graph_from_subcircuits(
    #                 graph_production_method=get_algorithmic_graph_from_Jabalizer
    #             ),
    #         ],
    #     )
    # except:
    #     pass


# Some notes:
# 1. These reset operations make graph sim mini about 10x faster than measured here.
# 2. The isolated nodes are from qubits which are used in the preparation and measurement
#    they are not used in the block encoding


if __name__ == "__main__":
    main("qasm_circuits/ising_circuit_10_for_100.qasm")
