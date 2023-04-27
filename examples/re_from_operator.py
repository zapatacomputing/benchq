################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
from pprint import pprint

from benchq import BasicSCArchitectureModel
from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.data_structures import ErrorBudget
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_custom_resource_estimation_pipeline,
    simplify_rotations,
    synthesize_clifford_t,
)
from benchq.timing import measure_time


def main():

    k = 2.0
    alpha = 0.6
    nu = 0.0
    evolution_time = 5

    error_budget = ErrorBudget(ultimate_failure_tolerance=1e-3)

    architecture_model = BasicSCArchitectureModel

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
        algorithm = qsp_time_evolution_algorithm(
            operator, evolution_time, error_budget.circuit_generation_weight
        )

    print("Circuit generation time:", t_info.total)
    # TA 2 part: model hardware resources

    with measure_time() as t_info:
        gsc_resource_estimates = run_custom_resource_estimation_pipeline(
            algorithm.program,
            error_budget,
            estimator=GraphResourceEstimator(architecture_model),
            transformers=[
                simplify_rotations,
                create_big_graph_from_subcircuits(delayed_gate_synthesis=True),
            ],
        )

    print("Resource estimation time without synthesis:", t_info.total)
    pprint(gsc_resource_estimates)

    with measure_time() as t_info:
        gsc_resource_estimates = run_custom_resource_estimation_pipeline(
            algorithm.program,
            error_budget,
            estimator=GraphResourceEstimator(architecture_model),
            transformers=[
                synthesize_clifford_t(error_budget),
                create_big_graph_from_subcircuits(delayed_gate_synthesis=False),
            ],
        )

    print("Resource estimation time with synthesis:", t_info.total)
    pprint(gsc_resource_estimates)


if __name__ == "__main__":
    main()
