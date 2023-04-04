################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import time

from benchq import BasicArchitectureModel
from benchq.algorithms import get_qsp_program
from benchq.problem_ingestion import (
    generate_jw_qubit_hamiltonian_from_mol_data,
)
from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)
from benchq.resource_estimation import get_qpe_resource_estimates_from_mean_field_object

from benchq.resource_estimation.microsoft import (
    get_resource_estimations_for_program as msft_re_for_program,
)


def main():
    dt = 0.5  # Integration timestep
    tmax = 5  # Maximal timestep
    sclf = 1

    for n_hydrogens in [2]:
        print("!!*#*!!" * 15)
        print(f"N HYDROGENS: {n_hydrogens}")
        print("!!*#*!!" * 15)

        # TA 1 part: specify the core computational capability
        start = time.time()
        # Generate instance
        mol_data = generate_hydrogen_chain_instance(n_hydrogens)

        # Convert instance to core computational problem instance
        operator = generate_jw_qubit_hamiltonian_from_mol_data(mol_data)
        end = time.time()
        print("Operator generation time:", end - start)

        ###### RE FOR PARTIAL CIRCUITS
        ### THIS CODE BELOW IS SUCH A MESS, BEWARE!
        # TODO: extract to a separate function
        tolerable_circuit_error_rate = 1e-3
        qsp_required_precision = (
            tolerable_circuit_error_rate / 2
        )  # Allocate half the error budget to QSP precision
        remaining_error_budget = tolerable_circuit_error_rate - qsp_required_precision
        ### THOUGH I THINK IT WORKS

        architecture_model = BasicArchitectureModel(
            physical_gate_error_rate=1e-3,
            physical_gate_time_in_seconds=1e-6,
        )

        ##### STUFF FOR SUBCIRCUITS
        # TA 1.5 part: model algorithmic circuit
        for mode in ["time_evolution", "gse"]:
            print("!!*#*!!" * 15)
            print(f"MODE: {mode}, n hydrogens: {n_hydrogens}")
            print("!!*#*!!" * 15)
            start = time.time()
            quantum_program = get_qsp_program(
                operator, qsp_required_precision, dt, tmax, sclf, mode=mode
            )
            end = time.time()
            print("Circuit generation time:", end - start)

            start = time.time()
            msft_resource_estimates = msft_re_for_program(
                quantum_program, remaining_error_budget, architecture_model
            )
            end = time.time()
            print("Microsoft estimation time:", end - start)
            print("Microsoft estimates:")
            print(msft_resource_estimates)

            #### END OF STUFF FOR SUBCIRCUITS


if __name__ == "__main__":
    main()
