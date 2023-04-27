################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
from pprint import pprint

from benchq import BasicSCArchitectureModel
from benchq.algorithms.time_evolution import get_qsp_time_evolution_program
from benchq.data_structures import ErrorBudget, get_program_from_circuit
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.resource_estimation.azure import AzureResourceEstimator
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_custom_resource_estimation_pipeline,
    simplify_rotations,
)
from benchq.timing import measure_time


def main():

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

    error_budget = ErrorBudget(ultimate_failure_tolerance=1e-3)

    architecture_model = BasicSCArchitectureModel(
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

    print("Operator generation time:", t_info.total)

    # TA 1.5 part: model algorithmic circuit
    with measure_time() as t_info:
        program = get_qsp_time_evolution_program(
            operator, qsp_required_precision, dt, tmax, sclf
        )
        full_circuit = program.full_circuit
        program = get_program_from_circuit(full_circuit)

    print("Circuit generation time:", t_info.total)
    # TA 2 part: model hardware resources

    with measure_time() as t_info:
        gsc_resource_estimates = run_custom_resource_estimation_pipeline(
            program,
            error_budget,
            estimator=GraphResourceEstimator(architecture_model),
            transformers=[
                simplify_rotations,
                create_big_graph_from_subcircuits(delayed_gate_synthesis=False),
            ],
        )

    print("Resource estimation time with GSC:", t_info.total)
    pprint(gsc_resource_estimates)

    with measure_time() as t_info:
        azure_resource_estimates = run_custom_resource_estimation_pipeline(
            program,
            error_budget,
            estimator=AzureResourceEstimator(architecture_model),
            transformers=[],
        )

    print("Resource estimation time with Azure:", t_info.total)
    pprint(azure_resource_estimates)


if __name__ == "__main__":
    main()
