################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
Example showing how to estimate the resources required to run a time evolution 
algorithm. It shows two different ways of estimating the resources: one with gate 
synthesis performed at the circuit level, while the other one does it during the
measurement phase. The first is more accurate and leads to lower resources, 
but is also more expensive in terms of runtime and memory usage.

Most of the objects has been described in the `1_from_qasm.py` examples, here
we only explain new concepts.
"""
from pprint import pprint

from benchq import BasicArchitectureModel
from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.data_structures import ErrorBudget
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_resource_estimation_pipeline,
    simplify_rotations,
    synthesize_clifford_t,
)
from benchq.timing import measure_time


def main():

    evolution_time = 5
    error_budget = ErrorBudget(ultimate_failure_tolerance=1e-3)

    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )

    # Generating Hamiltonian for a given set of parameters, which
    # defines the problem we try to solve.
    # measure_time is a utility tool which measures the execution time of
    # the code inside the with statement.
    with measure_time() as t_info:
        N = 2  # Problem size
        operator = get_vlasov_hamiltonian(N=N, k=2.0, alpha=0.6, nu=0)

        ## Alternative operator: 1D Heisenberg model
        # N = 100
        # operator = generate_1d_heisenberg_hamiltonian(N)

    print("Operator generation time:", t_info.total)

    # Here we generate the AlgorithmDescription structure, which contains
    # information such as what subroutine needs to be executed and how many times.
    # In this example we perform time evolution using the QSP algorithm.
    with measure_time() as t_info:
        algorithm = qsp_time_evolution_algorithm(
            operator, evolution_time, error_budget.circuit_generation_weight
        )
    print("Circuit generation time:", t_info.total)

    # First we perform resource estimation with gate synthesis at the circuit level.
    # It's more accurate and leads to lower estimates, but also more expensive
    # in terms of runtime and memory usage.
    # Then we perform resource estimation with gate synthesis during the measurement,
    # which we call "delayed gate synthesis".
    with measure_time() as t_info:
        gsc_resource_estimates = run_resource_estimation_pipeline(
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

    with measure_time() as t_info:
        gsc_resource_estimates = run_resource_estimation_pipeline(
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


if __name__ == "__main__":
    main()
