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

from benchq import BASIC_SC_ARCHITECTURE_MODEL
from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.compilation import get_algorithmic_graph_from_Jabalizer
from benchq.compilation.chp_simulator import get_algorithmic_graph_from_chp
from benchq.compilation.stim_simulator import get_algorithmic_graph_from_stim
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.problem_ingestion.hamiltonian_generation import (
    generate_1d_heisenberg_hamiltonian,
)
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_custom_resource_estimation_pipeline,
    simplify_rotations,
    synthesize_clifford_t,
)
from benchq.timing import measure_time


def main():
    evolution_time = 5

    architecture_model = BASIC_SC_ARCHITECTURE_MODEL

    for N in range(2, 30):
        print(f"Length of Hydrogen Chain: {N}")

        # Generating Hamiltonian for a given set of parameters, which
        # defines the problem we try to solve.
        # measure_time is a utility tool which measures the execution time of
        # the code inside the with statement.
        operator = generate_1d_heisenberg_hamiltonian(N)

        # Here we generate the AlgorithmImplementation structure, which contains
        # information such as what subroutine needs to be executed and how many times.
        # In this example we perform time evolution using the QSP algorithm.
        algorithm = qsp_time_evolution_algorithm(operator, evolution_time, 1e-3)

        # Perform resource estimation using Jabalizer and caputure the timing output
        with measure_time() as t_info:
            algorithm.program = simplify_rotations(algorithm.program)
            big_circuit = algorithm.program.full_circuit
            get_algorithmic_graph_from_Jabalizer(big_circuit)

        print("total time: ", t_info.total, "\n")


if __name__ == "__main__":
    main()
