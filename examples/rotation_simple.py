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
from pathlib import Path

from orquestra.integrations.qiskit.conversions import import_from_qiskit
from qiskit.circuit import QuantumCircuit
from pprint import pprint

from benchq import BasicArchitectureModel
<<<<<<< HEAD
from benchq.compilation import (
    get_algorithmic_graph_from_Jabalizer,
    pyliqtr_transpile_to_clifford_t,
    simplify_rotations,
=======
from benchq.algorithms import get_qsp_program
from benchq.timing import measure_time
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.resource_estimation.v2 import (
    GraphResourceEstimator,
    run_resource_estimation_pipeline,
>>>>>>> 14cc028710a1b70aa61d27e37ff00e91f45eccd8
)
from benchq.resource_estimation.v2 import (
    GraphResourceEstimator,
    run_resource_estimation_pipeline,
    simplify_only,
    synthesize_clifford_t,
)
from benchq.data_structures import get_program_from_circuit


# This demo shows how to get resource estimation for a circuit in two ways:
# First, with explicit transpilation of rotations into Clifford + T
# Second, without the transpilation, with passing rotations through Jabalizer.


def main():
    # Uncomment to see Jabalizer output
    # logging.getLogger().setLevel(logging.INFO)

    tolerable_logical_error_rate = 1e-3
    qsp_required_precision = (
        tolerable_logical_error_rate / 3
    )  # Allocate half the error budget to trotter precision

    error_budget = {
        "qsp_required_precision": qsp_required_precision,
        "tolerable_circuit_error_rate": tolerable_logical_error_rate,
        "total_error": 1e-2,
        "synthesis_error_rate": 0.5,
        "ec_error_rate": 0.5,
    }

    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
<<<<<<< HEAD
    qiskit_circuit = QuantumCircuit.from_qasm_file(file_name)
    # TA 2 part: FTQC compilation
    # synthesis_accuracy = 1e-1
    synthesis_accuracy = 1e-2
    # synthesis_accuracy = 0.01
    # breakpoint()
    clifford_t_circuit = pyliqtr_transpile_to_clifford_t(
        qiskit_circuit, synthesis_accuracy
    )
    graph = get_algorithmic_graph_from_Jabalizer(clifford_t_circuit)
=======
>>>>>>> 14cc028710a1b70aa61d27e37ff00e91f45eccd8

    file_name = Path(__file__).resolve().parent / "circuits/h_chain_circuit.qasm"
    ### METHOD 2: Estimation from quantum program, without recreating full graph
    # TA 1.5 part: model algorithmic circuit
    with measure_time() as t_info:
        qiskit_circuit = QuantumCircuit.from_qasm_file(file_name)
        program = get_program_from_circuit(import_from_qiskit(qiskit_circuit))

    print("Program generation time:", t_info.total)

<<<<<<< HEAD
    graph = get_algorithmic_graph_from_Jabalizer(circuit_with_rotations_2)
    start = time.time()
    resource_estimates = get_resource_estimations_for_graph_with_rotations(
        graph, architecture_model, logical_error_rate, plot=True
    )
    end = time.time()
    print("Resource estimation time ROTATIONS:", end - start)
    print(resource_estimates)
=======
    # TA 2 part: model hardware resources
    with measure_time() as t_info:
        gsc_resource_estimates = run_resource_estimation_pipeline(
            program,
            error_budget,
            estimator=GraphResourceEstimator(architecture_model),
            transformer=synthesize_clifford_t,
        )

    print("Gate Synthesis: On")
    print("Resource estimation time:", t_info.total)
    pprint(gsc_resource_estimates)

    with measure_time() as t_info:
        gsc_resource_estimates = run_resource_estimation_pipeline(
            program,
            error_budget,
            estimator=GraphResourceEstimator(architecture_model),
            transformer=simplify_only,
        )

    print("Gate Synthesis: Off")
    print("Resource estimation time:", t_info.total)
    pprint(gsc_resource_estimates)
>>>>>>> 14cc028710a1b70aa61d27e37ff00e91f45eccd8


if __name__ == "__main__":
    main()
