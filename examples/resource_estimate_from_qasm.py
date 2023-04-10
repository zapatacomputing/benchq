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
from benchq.data_structures import get_program_from_circuit
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_resource_estimation_pipeline,
    simplify_rotations,
    synthesize_clifford_t,
)
from benchq.timing import measure_time


def main(file_name):
    # Uncomment to see Jabalizer output
    logging.getLogger().setLevel(logging.INFO)

    qiskit_circuit = QuantumCircuit.from_qasm_file(file_name)
    quantum_program = get_program_from_circuit(import_from_qiskit(qiskit_circuit))

    error_budget = {
        "total_error": 1e-2,
        "trotter_required_precision": 1e-3,  
        "tolerable_circuit_error_rate": 1e-3,
        "remaining_error_budget": (5e-3),
        "synthesis_error_rate": 1e-3,
        "ec_error_rate": 1e-3,
    }

    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )

    with measure_time() as t_info:
        ### TODO: error budget is needed both for transforming AND
        ### in the estimation
        ### Hence, I suggest passing it once to run_resource_estimation_pipeline
        ### And then propagating it through transformer and estimator
        gsc_resource_estimates = run_resource_estimation_pipeline(
            quantum_program,
            error_budget,
            estimator=GraphResourceEstimator(architecture_model),
            transformers=[
                simplify_rotations,
                synthesize_clifford_t(error_budget),
                create_big_graph_from_subcircuits(synthesized=True),
            ],
        )
    print(gsc_resource_estimates)


if __name__ == "__main__":
    main("circuits/h_chain_circuit.qasm")
