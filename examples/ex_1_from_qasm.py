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

from timeout_decorator import timeout


class TimeoutException(Exception):
    pass


timeout_seconds = 6000


def main():
    # Uncomment to see extra debug output
    # logging.getLogger().setLevel(logging.INFO)

    # store functions to run compilers as well as whether they timed out
    compiler_data = [
        [get_ruby_slippers_compiler(), False, "Ruby Slippers"],
        [get_algorithmic_graph_from_graphsim_mini, False, "GraphSim Mini"],
        [get_algorithmic_graph_from_Jabalizer, False, "Jabalizer"],
    ]

    for N in range(2, 11):
        print(f"loading circuit for N={N}...")
        file_name = "qasm_circuits/ising_circuit_" + str(N) + "_for_100.qasm"
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
        algorithm_implementation = AlgorithmImplementation(
            quantum_program, error_budget, 1
        )

        # Architecture model is used to define the hardware model.
        architecture_model = BASIC_SC_ARCHITECTURE_MODEL

        for data in compiler_data:
            if not data[1]:
                try:
                    test_compiler(
                        algorithm_implementation,
                        architecture_model,
                        data[0],
                        data[2],
                    )
                except Exception as e:
                    if isinstance(e, TimeoutException):
                        print(data[2] + " timed out!")
                        data[1] = True

        del algorithm_implementation


@timeout(
    timeout_seconds,
    timeout_exception=TimeoutException,
)
def test_compiler(
    algorithm_implementation,
    architecture_model,
    compiler,
    compiler_name,
):
    print("Running resource estimation for " + compiler_name + "...")
    run_custom_resource_estimation_pipeline(
        algorithm_implementation,
        estimator=GraphResourceEstimator(architecture_model),
        transformers=[
            transpile_to_native_gates,
            create_big_graph_from_subcircuits(graph_production_method=compiler),
        ],
    )


# Some notes:
# 1. These reset operations make graph sim mini about 10x faster than measured here.
# 2. The isolated nodes are from qubits which are used in the preparation and measurement
#    they are not used in the block encoding


if __name__ == "__main__":
    main()
