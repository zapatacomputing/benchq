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
from time import time

from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm

# Requires jabalizer install. See README.
# from benchq.compilation.graph_states import get_jabalizer_circuit_compiler
from benchq.compilation.graph_states import get_ruby_slippers_circuit_compiler
from benchq.compilation.graph_states.implementation_compiler import (
    get_implementation_compiler,
)
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.problem_ingestion.solid_state_hamiltonians.heisenberg import (
    generate_1d_heisenberg_hamiltonian,
)
from benchq.quantum_hardware_modeling import BASIC_SC_ARCHITECTURE_MODEL
from benchq.resource_estimators.graph_estimator import GraphResourceEstimator, TwoRowBusArchitectureModel, ActiveVolumeArchitectureModel
from benchq.timing import measure_time


def main():
    evolution_time = 4

    start_time = time()
    # Generating Hamiltonian for a given set of parameters, which
    # defines the problem we try to solve.
    # measure_time is a utility tool which measures the execution time of
    # the code inside the with statement.
    with measure_time() as t_info:
        N = 6  # Problem size

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

    # Transpile the circuit to a Clifford+T circuit
    # cliff_t_algorithm = algorithm.transpile_to_clifford_t()
    cliff_t_algorithm = algorithm
    print("Circuit generation time:", t_info.total)
    print("n qubits in circuit:", cliff_t_algorithm.program.subroutines[0].n_qubits)

    # Allows for parallelized compilation. Uses ruby slippers compiler by default.
    # The single-thread setting is simplest to use. You can parallelize on a local
    # machine by setting the destination to "local" and running `orq up` in the
    # terminal. Additional settings as well as using a remote cluster can be
    # configured by using other settings available in the get_implementation_compiler
    implementation_compiler = get_implementation_compiler(
        circuit_compiler=get_ruby_slippers_circuit_compiler(),
        destination="single-thread",
    )

    two_row_architecture = TwoRowBusArchitectureModel()
    active_volume_architecture = ActiveVolumeArchitectureModel()

    graph_estimator = GraphResourceEstimator(optimization="Time", verbose=True)
    # active_volume_estimator = GraphResourceEstimator(optimization="Time", verbose=True)

    with measure_time() as t_info:
        two_row_resource_estimate = graph_estimator.compile_and_estimate(
            cliff_t_algorithm,
            implementation_compiler,
            two_row_architecture,
            BASIC_SC_ARCHITECTURE_MODEL,
        )
        active_volume_resource_estimate = graph_estimator.compile_and_estimate(
            cliff_t_algorithm,
            implementation_compiler,
            active_volume_architecture,
            BASIC_SC_ARCHITECTURE_MODEL,
        )

    # print("Resource estimation time without synthesis:", t_info.total)
    # pprint(two_row_resource_estimate.total_time_in_seconds)

    print("Two row resource estimate", two_row_resource_estimate)
    print("Active volume resource estimate", active_volume_resource_estimate)
    # pprint("Runtime", active_volume_resource_estimate.total_time_in_seconds)
    # print("Total error rate", active_volume_resource_estimate.logical_error_rate)
    print("Two row graph state cycles", two_row_resource_estimate.logical_architecture_resource_info.qec_cycle_allocation.inclusive("graph state prep"))
    print("Active volume graph state cycles", active_volume_resource_estimate.logical_architecture_resource_info.qec_cycle_allocation.inclusive("graph state prep"))
    print("Two row total cycles", two_row_resource_estimate.logical_architecture_resource_info.qec_cycle_allocation.total)
    print("Active volume total cycles", active_volume_resource_estimate.logical_architecture_resource_info.qec_cycle_allocation.total)

    print("Total time to estimate resources:", time() - start_time)

if __name__ == "__main__":
    main()
