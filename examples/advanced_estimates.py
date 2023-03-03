################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import time

from benchq import BasicArchitectureModel
from benchq.algorithms import get_qsp_program
from benchq.problem_ingestion import (
    generate_hydrogen_chain_instance,
    generate_jw_qubit_hamiltonian_from_mol_data,
)
from benchq.resource_estimation import get_qpe_resource_estimates_from_mean_field_object

try:
    from benchq.resource_estimation.microsoft import (
        get_resource_estimations_for_program as msft_re_for_program,
    )
except Exception as e:
    print("Microsoft not configured, omitting importing related libraries")

from benchq.resource_estimation.graph_compilation import (
    get_resource_estimations_for_program,
)


def print_re(resource_estimates, label):
    print("*#*" * 15)
    print(f"{label} RESOURCE ESTIMATE")
    print(resource_estimates)
    print("n qubits (millions):", resource_estimates["physical_qubit_count"] / 1e6)
    print("time (seconds):", resource_estimates["total_time"])
    print("time (hours):", resource_estimates["total_time"] / 3600)
    print("*#*" * 15)


def get_of_resource_estimates(n_hydrogens):
    mean_field_object = generate_hydrogen_chain_instance(
        n_hydrogens
    ).get_avas_meanfield_object()

    # Running resource estimation with OpenFermion tools

    # Set number of bits of precision in ancilla state preparation
    bits_precision_state_prep = 4 * (n_hydrogens - 2) - n_hydrogens
    chemical_accuracy = 1e-3
    of_resource_estimates = get_qpe_resource_estimates_from_mean_field_object(
        mean_field_object,
        target_accuracy=chemical_accuracy,
        bits_precision_state_prep=bits_precision_state_prep,
    )

    print_re(of_resource_estimates, "OF")
    return of_resource_estimates


def main():
    dt = 0.5  # Integration timestep
    tmax = 5  # Maximal timestep
    sclf = 1

    for n_hydrogens in [2, 3]:
        print("!!*#*!!" * 15)
        print(f"N HYDROGENS: {n_hydrogens}")
        print("!!*#*!!" * 15)

        # TA 1 part: specify the core computational capability
        start = time.time()
        # Generate instance
        mol_data = generate_hydrogen_chain_instance(n_hydrogens).get_molecular_data()

        # Convert instance to core computational problem instance
        operator = generate_jw_qubit_hamiltonian_from_mol_data(mol_data)
        end = time.time()
        print("Operator generation time:", end - start)

        ### OPENFERMION ESTIMATES
        start = time.time()
        of_resource_estimates = get_of_resource_estimates(n_hydrogens)
        print(of_resource_estimates)
        end = time.time()
        print("OF resource estimation took:", end - start, "seconds")
        ### END OPENFERMION ESTIMATES

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

            try:
                start = time.time()
                msft_resource_estimates = msft_re_for_program(
                    quantum_program, remaining_error_budget, architecture_model
                )
                end = time.time()
                print("Microsoft estimation time:", end - start)
                print("Microsoft estimates:")
                print(msft_resource_estimates)
            except Exception as e:
                print(
                    "Microsoft estimation tools is not configured, aborting estimation. "
                    "Expect better documentation on how to get the access in the future."
                )
                # print("Original exception message", e)

            start = time.time()
            gsc_resource_estimates = get_resource_estimations_for_program(
                quantum_program,
                remaining_error_budget,
                architecture_model,
                plot=True,
            )
            end = time.time()
            print("Graph State Compilation estimation time:", end - start)
            print("Microsoft estimates:")
            print(gsc_resource_estimates)

            #### END OF STUFF FOR SUBCIRCUITS


if __name__ == "__main__":
    main()
