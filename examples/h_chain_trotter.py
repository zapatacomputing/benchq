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
import time

from benchq import BasicArchitectureModel
from benchq.algorithms import get_trotter_program
from benchq.problem_ingestion import (
    generate_jw_qubit_hamiltonian_from_mol_data,
    generate_hydrogen_chain_instance,
)
from benchq.resource_estimation.graph_compilation import (
    get_resource_estimations_for_program,
)


def main():
    for n_hydrogens in [2, 3, 5]:
        print("Number of hydrogen atoms:", n_hydrogens)

        begtime = time.time()
        start = begtime
        mol_data = generate_hydrogen_chain_instance(n_hydrogens)
        print("Generate instance:", time.time() - start)

        # Convert instance to core computational problem instance
        start = time.time()
        operator = generate_jw_qubit_hamiltonian_from_mol_data(mol_data)
        print("Generate JW qubit hamiltonian", time.time() - start)
        print("Size of Hamiltonian:", operator.n_qubits)

        # Resource estimation for partial circuits:
        tolerable_circuit_error_rate = 1e-3
        trotter_required_precision = (
            tolerable_circuit_error_rate / 2
        )  # Allocate half the error budget to QSP precision
        remaining_error_budget = (
            tolerable_circuit_error_rate - trotter_required_precision
        )

        architecture_model = BasicArchitectureModel(
            physical_gate_error_rate=1e-3,
            physical_gate_time_in_seconds=1e-6,
        )

        # TA 1.5 part: model algorithmic circuit
        evolution_time = 1

        start = time.time()
        # This could be replaced with QSP, please see `advanced_estimates`
        # as an example of how to do that.
        quantum_program = get_trotter_program(
            operator,
            evolution_time=evolution_time,
            total_trotter_error=trotter_required_precision,
        )
        end = time.time()
        print("Circuit generation time:", end - start)

        start = time.time()
        gsc_resource_estimates = get_resource_estimations_for_program(
            quantum_program, remaining_error_budget, architecture_model, plot=True
        )
        end = time.time()
        print("Resource estimation time:", end - start)
        print(gsc_resource_estimates)
        print("Total time for ", n_hydrogens, " ", end - begtime)

        ### END OF STUFF FOR SUBCIRCUITS


if __name__ == "__main__":
    main()
