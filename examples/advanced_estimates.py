################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import time
import logging
from benchq import BasicArchitectureModel
from benchq.algorithms.time_evolution import get_qsp_time_evolution_program
from benchq.problem_ingestion import generate_jw_qubit_hamiltonian_from_mol_data
from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)
from benchq.resource_estimation import get_qpe_resource_estimates_from_mean_field_object
from benchq.timing import measure_time

try:
    from benchq.resource_estimation.azure import (
        get_resource_estimations_for_program as azure_re_for_program,
    )
except Exception as e:
    print("Azure QRE not configured, omitting importing related libraries")

from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_resource_estimation_pipeline,
    simplify_rotations,
    synthesize_clifford_t,
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
    instance = generate_hydrogen_chain_instance(n_hydrogens)
    instance.avas_atomic_orbitals = ["H 1s", "H 2s"]
    instance.avas_minao = "STO-3G"
    mean_field_object = instance.get_active_space_meanfield_object()

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
    # Uncomment to see Jabalizer output
    logging.getLogger().setLevel(logging.INFO)
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

        ### OPENFERMION ESTIMATES
        start = time.time()
        of_resource_estimates = get_of_resource_estimates(n_hydrogens)
        print(of_resource_estimates)
        end = time.time()
        print("OF resource estimation took:", end - start, "seconds")
        ### END OPENFERMION ESTIMATES

        error_budget = {
            "total_error": 1e-2,
            "qsp_required_precision": 1e-3,
            "tolerable_circuit_error_rate": 1e-3,
            "synthesis_error_rate": 1e-3,
            "ec_error_rate": 1e-3,
        }

        architecture_model = BasicArchitectureModel(
            physical_gate_error_rate=1e-3,
            physical_gate_time_in_seconds=1e-6,
        )

        ##### STUFF FOR SUBCIRCUITS
        # TA 1.5 part: model algorithmic circuit

        print("!!*#*!!" * 15)
        print(f"n hydrogens: {n_hydrogens}")
        print("!!*#*!!" * 15)
        start = time.time()
        quantum_program = get_qsp_time_evolution_program(
            operator,
            error_budget["qsp_required_precision"],
            dt,
            tmax,
            sclf,
        )
        end = time.time()
        print("Circuit generation time:", end - start)

        try:
            start = time.time()
            azure_resource_estimates = azure_re_for_program(
                quantum_program,
                error_budget["synthesis_error_rate"] + error_budget["ec_error_rate "],
                architecture_model,
            )
            end = time.time()
            print("Azure QRE estimation time:", end - start)
            print("Azure QRE estimates:")
            print(azure_resource_estimates)
        except Exception as e:
            print(
                "Azure QRE is not configured, aborting estimation. "
                "Expect better documentation on how to get the access in the future."
            )
            # print("Original exception message", e)]

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
                    create_big_graph_from_subcircuits(synthesized=False),
                ],
            )
        print(gsc_resource_estimates)


if __name__ == "__main__":
    main()
