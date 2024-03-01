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
from benchq.resource_estimators.graph_estimators import (
    GraphResourceEstimator,
    get_custom_resource_estimation,
    compile_to_native_gates,
)
from benchq.timing import measure_time
from benchq.compilation.graph_states.julia_utils import get_ruby_slippers_compiler
from benchq.compilation.graph_states.quantum_program_compiler import (
    get_quantum_program_compiler,
)
from benchq.compilation.graph_states.compiled_data_structures import (
    CompiledAlgorithmImplementation,
)
from benchq.problem_embeddings.quantum_program import (
    split_large_subroutines_into_smaller_subroutines,
)

from rigetti_application_instances import FHInstance
from time import time


def main():
    evolution_time = 5

    architecture_model = BASIC_SC_ARCHITECTURE_MODEL

    start_time = time()
    # Generating Hamiltonian for a given set of parameters, which
    # defines the problem we try to solve.
    # measure_time is a utility tool which measures the execution time of
    # the code inside the with statement.
    with measure_time() as t_info:
        # N = 2  # Problem size
        # operator = get_vlasov_hamiltonian(N=N, k=2.0, alpha=0.6, nu=0)

        # Alternative operator: 1D Heisenberg model
        N = 2
        operator = generate_1d_heisenberg_hamiltonian(N)

    print("Operator generation time:", t_info.total)

    # Here we generate the AlgorithmImplementation structure, which contains
    # information such as what subroutine needs to be executed and how many times.
    # In this example we perform time evolution using the QSP algorithm.
    with measure_time() as t_info:
        algorithm = qsp_time_evolution_algorithm(operator, evolution_time, 1e-3)

    print("Circuit generation time:", t_info.total)
    print("n qubits:", algorithm.program.subroutines[0].n_qubits)

    algorithm.program = split_large_subroutines_into_smaller_subroutines(
        algorithm.program, int(1e3)
    )

    # First we perform resource estimation with gate synthesis at the circuit level.
    # It's more accurate and leads to lower estimates, but also more expensive
    # in terms of runtime and memory usage.
    # Then we perform resource estimation with gate synthesis during the measurement,
    # which we call "delayed gate synthesis".
    compiler = get_ruby_slippers_compiler(
        teleportation_threshold=5,
        teleportation_distance=2,
        layering_optimization="Space",
    )

    with measure_time() as t_info:
        num_cores = len(algorithm.program.subroutines)
        compiler = get_ruby_slippers_compiler(
            teleportation_threshold=5,
            teleportation_distance=2,
            layering_optimization="Space",
            max_graph_size=1e7,
        )

        compiler = get_quantum_program_compiler(compiler)

        compiled_program = compiler(algorithm.program)

        compiled_algorithm = CompiledAlgorithmImplementation(
            compiled_program, algorithm
        )
        estimator = GraphResourceEstimator(optimization="Space", verbose=True)
        resource_estimate = estimator.estimate_resources_from_compiled_implementation(
            compiled_algorithm,
            BASIC_SC_ARCHITECTURE_MODEL,
        )

    print("Resource estimation time without synthesis:", t_info.total)
    pprint(resource_estimate)

    print("Total time:", time() - start_time)


# def break_into_smaller_subroutines(circuit, chunk_size=1e7):
#     for subroutine in circuit.subroutines:
#         if len(subroutine._operations) > chunk_size:

#         subroutine._operations = break_into_chunks(subroutine._operations, chunk_size)
#     [lst[i:i + chunk_size] for i in range(0, len(circuit._operations), chunk_size)]


if __name__ == "__main__":
    main()
