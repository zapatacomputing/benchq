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
from benchq.algorithms.time_evolution import get_trotter_program
from benchq.data_structures import ErrorBudget
from benchq.problem_ingestion import generate_jw_qubit_hamiltonian_from_mol_data
from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_resource_estimation_pipeline,
    simplify_rotations,
    synthesize_clifford_t,
)
from benchq.timing import measure_time


def main():
    for n_hydrogens in [2, 3]:
        print(f"Number of hydrogen atoms: {n_hydrogens}")

        with measure_time() as t_info:
            mol_data = generate_hydrogen_chain_instance(n_hydrogens)

        begtime = t_info.start_counter
        print(f"Generate instance: {t_info.total}")

        # Convert instance to core computational problem instance
        with measure_time() as t_info:
            operator = generate_jw_qubit_hamiltonian_from_mol_data(mol_data)
        print(f"Generate JW qubit hamiltonian {t_info.total}")
        print(f"Size of Hamiltonian: {operator.n_qubits}")

        # Resource estimation for partial circuits:
        tolerable_circuit_error_rate = 1e-3
        # Allocate half the error budget to QSP precision
        trotter_required_precision = tolerable_circuit_error_rate / 2

        architecture_model = BasicArchitectureModel(
            physical_gate_error_rate=1e-3,
            physical_gate_time_in_seconds=1e-6,
        )

        error_budget = ErrorBudget(ultimate_failure_tolerance=1e-3)

        # TA 1.5 part: model algorithmic circuit
        evolution_time = 1

        with measure_time() as t_info:
            # This could be replaced with QSP, please see `advanced_estimates`
            # as an example of how to do that.
            quantum_program = get_trotter_program(
                operator,
                evolution_time=evolution_time,
                total_trotter_error=trotter_required_precision,
            )

        print("Circuit generation time:", t_info.total)
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
                    create_big_graph_from_subcircuits(delayed_gate_synthesis=False),
                ],
            )

        print(f"Resource estimation time: {t_info.total}")
        print(gsc_resource_estimates)
        print(f"Total time for {n_hydrogens} {t_info.stop_counter - begtime}")  # type: ignore

        ### END OF STUFF FOR SUBCIRCUITS


if __name__ == "__main__":
    main()
