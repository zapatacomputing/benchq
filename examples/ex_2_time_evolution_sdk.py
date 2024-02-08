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

WARNING: This example requires the pyscf extra. run `pip install benchq[pyscf]`
to install the extra.
"""
from pprint import pprint

from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.problem_ingestion.solid_state_hamiltonians.heisenberg import (
    generate_1d_heisenberg_hamiltonian,
)
from benchq.quantum_hardware_modeling import BASIC_SC_ARCHITECTURE_MODEL
from benchq.resource_estimators.graph_estimators import (
    GraphResourceEstimator,
    create_graphs_for_subcircuits,
    get_custom_resource_estimation,
    synthesize_clifford_t,
    transpile_to_native_gates,
)
from benchq.timing import measure_time
from benchq.compilation.julia_utils import get_ruby_slippers_compiler
from benchq.problem_embeddings.quantum_program import (
    split_large_subroutines_into_smaller_subroutines,
)
from rigetti_application_instances import FHInstance


def main():
    evolution_time = 5

    architecture_model = BASIC_SC_ARCHITECTURE_MODEL

    # Generating Hamiltonian for a given set of parameters, which
    # defines the problem we try to solve.
    # measure_time is a utility tool which measures the execution time of
    # the code inside the with statement.
    with measure_time() as t_info:
        # N = 2  # Problem size
        # operator = get_vlasov_hamiltonian(N=N, k=2.0, alpha=0.6, nu=0)

        # Alternative operator: 1D Heisenberg model
        # N = 2
        # operator = generate_1d_heisenberg_hamiltonian(N)

        # Specify final time and limits on number of time steps and epsilon
        T = 10
        # MAX_STEPS = 1000
        # J value
        J = 1
        # J' next nearest neighbour
        J_nnn = -J / 3
        # U values
        # u_values = np.arange(1, 7) * J
        u_val = 1 * J
        # hz
        hz = 0
        # mu
        mu = 0
        N = 3

        instance = FHInstance(N=N, J=-J, U=u_val, hz=hz, mu=mu, J_nnn=J_nnn, end_time=T)
        operator, alpha = instance.make_hamiltonian_and_alpha()

    print("Operator generation time:", t_info.total)

    # Here we generate the AlgorithmImplementation structure, which contains
    # information such as what subroutine needs to be executed and how many times.
    # In this example we perform time evolution using the QSP algorithm.
    with measure_time() as t_info:
        algorithm = qsp_time_evolution_algorithm(operator, evolution_time, 1e-3)
    print("Circuit generation time:", t_info.total)

    algorithm.program = split_large_subroutines_into_smaller_subroutines(
        algorithm.program, 10000
    )

    # First we perform resource estimation with gate synthesis at the circuit level.
    # It's more accurate and leads to lower estimates, but also more expensive
    # in terms of runtime and memory usage.
    # Then we perform resource estimation with gate synthesis during the measurement,
    # which we call "delayed gate synthesis".
    compiler = get_ruby_slippers_compiler(
        layering_optimization="Space",
    )

    with measure_time() as t_info:
        gsc_resource_estimates = get_custom_resource_estimation(
            algorithm,
            estimator=GraphResourceEstimator(architecture_model),
            transformers=[
                transpile_to_native_gates,
                create_graphs_for_subcircuits(compiler, destination="debug"),
            ],
        )

    print("Resource estimation time without synthesis:", t_info.total)
    pprint(gsc_resource_estimates)


# def break_into_smaller_subroutines(circuit, chunk_size=1e7):
#     for subroutine in circuit.subroutines:
#         if len(subroutine._operations) > chunk_size:

#         subroutine._operations = break_into_chunks(subroutine._operations, chunk_size)
#     [lst[i:i + chunk_size] for i in range(0, len(circuit._operations), chunk_size)]


if __name__ == "__main__":
    main()
