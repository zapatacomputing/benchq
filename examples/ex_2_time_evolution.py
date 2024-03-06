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

WARNING: This example requires the pyscf extra as well as the sdk extra.
run `pip install benchq[pyscf]` then `pip install benchq[sdk]` from the
main to install the extras. Then run `orq start` to start local ray.
"""
from pprint import pprint

from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.problem_ingestion.solid_state_hamiltonians.heisenberg import (
    generate_1d_heisenberg_hamiltonian,
)
from benchq.quantum_hardware_modeling import BASIC_SC_ARCHITECTURE_MODEL
from benchq.timing import measure_time
from benchq.compilation.graph_states.implementation_compiler import (
    get_implementation_compiler,
)
from benchq.resource_estimators.graph_estimator import GraphResourceEstimator

from time import time


def main():
    evolution_time = 5

    start_time = time()
    # Generating Hamiltonian for a given set of parameters, which
    # defines the problem we try to solve.
    # measure_time is a utility tool which measures the execution time of
    # the code inside the with statement.
    with measure_time() as t_info:
        N = 200  # Problem size

        # Get a Vlasov Hamiltonian for simulation
        operator = get_vlasov_hamiltonian(N=N, k=2.0, alpha=0.6, nu=0)
        # Alternative operator: 1D Heisenberg model
        # operator = generate_1d_heisenberg_hamiltonian(N)

    print("Operator generation time:", t_info.total)

    # Here we generate the AlgorithmImplementation structure, which contains
    # information such as what subroutine needs to be executed and how many times.
    # In this example we perform time evolution using the QSP algorithm.
    with measure_time() as t_info:
        algorithm = qsp_time_evolution_algorithm(operator, evolution_time, 1e-3)

    print("Circuit generation time:", t_info.total)
    print("n qubits in circuit:", algorithm.program.subroutines[0].n_qubits)

    # allows for parallelization of the compilation
    # uses ruby slippers compiler by default
    # set destination to "local" to parallelize compilation on your machine
    # if you have set up orquestra, you can use the "remote" option to
    # parallelize the compilation on the cloud.
    implementation_compiler = get_implementation_compiler(destination="single-thread")
    estimator = GraphResourceEstimator(optimization="Time", verbose=True)

    with measure_time() as t_info:
        resource_estimate = estimator.compile_and_estimate(
            algorithm,
            implementation_compiler,
            BASIC_SC_ARCHITECTURE_MODEL,
        )

    print("Resource estimation time without synthesis:", t_info.total)
    pprint(resource_estimate)

    print("Total time:", time() - start_time)


if __name__ == "__main__":
    main()
