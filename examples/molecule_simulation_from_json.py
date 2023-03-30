################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
MAKE SURE TO UNZIP THE problem.zip FILE BEFORE RUNNING THIS SCRIPT!!!

There are 3 small molecules (smolecules) in the .zip file. These are:

C2H2-8-cannonical_qubitop - very small
CH4-8-NOs_qubitop         - medium small
C2H4-12-NOs_qubitop       - big small

Objectives:

    1. create a testing ground to see how close we are to handling the larger
    problem instances that jerome has been working on.
"""
import logging
import time

from benchq import BasicArchitectureModel
from benchq.algorithms import get_qsp_program
from benchq.compilation import (
    get_algorithmic_graph_from_gate_stitching,
    pyliqtr_transpile_to_clifford_t,
)
from benchq.problem_ingestion.hamiltonian_generation import fast_load_qubit_op
from benchq.resource_estimation.graph_compilation import (
    get_resource_estimations_for_graph,
)


def main(hamiltonian_name):
    # Uncomment to see Jabalizer output
    # logging.getLogger().setLevel(logging.INFO)

    dt = 0.05  # Integration timestep
    tmax = 5  # Maximal timestep
    sclf = 1

    tolerable_logical_error_rate = 1e-3
    qsp_required_precision = 1e-2
    gate_synthesis_error_budget = (tolerable_logical_error_rate) / 2
    error_correction_error_budget = (tolerable_logical_error_rate) / 2

    # TA 1 part: specify the core computational capability
    print("Generating hamiltonian for " + hamiltonian_name)
    start = time.time()
    file = "small_molecules/" + hamiltonian_name + ".json"
    # operator = get_vlasov_hamiltonian(k, alpha, nu, N)
    # # TA 1 part: specify the core computational capability
    operator = fast_load_qubit_op(file)
    end = time.time()
    print("Hamiltonian generation time: ", end - start)

    ### METHOD 1: Full graph creation
    # TA 1.5 part: model algorithmic circuit
    print("Starting circuit generation")
    start = time.time()
    program = get_qsp_program(operator, qsp_required_precision, dt, tmax, sclf)
    circuit = program.subroutines[1]
    end = time.time()
    print("Circuit generation time: ", end - start)

    # TA 2 part: FTQC compilation
    print("Starting transpilation")
    start = time.time()
    clifford_t_circuit = pyliqtr_transpile_to_clifford_t(
        circuit, gate_synthesis_error_budget
    )
    end = time.time()
    print("Transpilation time: ", end - start)

    print("Starting graph compilation")
    start = time.time()
    graph = get_algorithmic_graph_from_gate_stitching(clifford_t_circuit)
    end = time.time()
    print("Graph compilation time: ", end - start)

    print("Starting resource estimation")
    # TA 2 part: model hardware resources
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
    start = time.time()
    resource_estimates = get_resource_estimations_for_graph(
        graph, architecture_model, error_correction_error_budget
    )
    end = time.time()

    print("Resource estimation time:", end - start)
    print(resource_estimates)


if __name__ == "__main__":
    main("C2H2-8-canonical_qubitop")
