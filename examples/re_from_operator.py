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
from pprint import pprint

from benchq import BasicArchitectureModel
from benchq.algorithms import get_qsp_program
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    run_resource_estimation_pipeline,
    synthesize_clifford_t,
    create_big_graph_from_subcircuits,
)
from benchq.problem_ingestion.hamiltonian_generation import (
    fast_load_qubit_op,
    generate_1d_heisenberg_hamiltonian,
)
from benchq.timing import measure_time


def main():
    # Uncomment to see Jabalizer output
    # logging.getLogger().setLevel(logging.INFO)

    k = 2.0
    alpha = 0.6
    nu = 0.0

    dt = 0.1  # Integration timestep
    tmax = 5  # Maximal timestep
    sclf = 1

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

    # TA 1 part: specify the core computational capability
    with measure_time() as t_info:
        N = 2
        operator = get_vlasov_hamiltonian(k, alpha, nu, N)
        
        # Alternative operator: 1D Heisenberg model
        # N = 100
        # operator = generate_1d_heisenberg_hamiltonian(N)

        # Alternative operator: Small molecules
        # Warning: they take ~1h-5h to run, depending on the case
        # hamiltonian_name = "C2H2-8-canonical_qubitop"
        # hamiltonian_name = "CH4-8-NOs_qubitop"
        # hamiltonian_name = "C2H4-12-NOs_qubitop"
        # file = "small_molecules/" + hamiltonian_name + ".json"
        # operator = fast_load_qubit_op(file)

    print("Operator generation time:", t_info.total)

    # TA 1.5 part: model algorithmic circuit
    with measure_time() as t_info:
        program = get_qsp_program(
            operator, qsp_required_precision, dt, tmax, sclf, mode="time_evolution"
        )

    print("Circuit generation time:", t_info.total)
    # TA 2 part: model hardware resources

    with measure_time() as t_info:
        gsc_resource_estimates = run_resource_estimation_pipeline(
            program,
            error_budget,
            estimator=GraphResourceEstimator(architecture_model),
            transformers=[
                synthesize_clifford_t(error_budget),
                create_big_graph_from_subcircuits(synthesized=False),
            ],
        )

    print("Resource estimation time without synthesis:", t_info.total)
    pprint(gsc_resource_estimates)

    with measure_time() as t_info:
        gsc_resource_estimates = run_resource_estimation_pipeline(
            program,
            error_budget,
            estimator=GraphResourceEstimator(architecture_model),
            transformers=[
                synthesize_clifford_t(error_budget),
                create_big_graph_from_subcircuits(synthesized=True),
            ],
        )

    print("Resource estimation time with synthesis:", t_info.total)
    pprint(gsc_resource_estimates)


if __name__ == "__main__":
    main()
