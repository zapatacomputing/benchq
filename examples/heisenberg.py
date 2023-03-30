################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
Objectives:

1. Use the heisenberg model as a stress test for our new graph compilation method
    - We should be able to get a resource estimate for this circuit for n = 1000
    in about a day or n = 100 in about 5 minutes.
"""
import logging
import time

from benchq import BasicArchitectureModel
from benchq.algorithms import get_qsp_circuit
from benchq.compilation import pyliqtr_transpile_to_clifford_t
from benchq.compilation.gate_stitching import get_algorithmic_graph_from_gate_stitching
from benchq.problem_ingestion.hamiltonian_generation import (
    generate_heisenberg_hamiltonian,
)
from benchq.resource_estimation.graph_compilation import (
    get_resource_estimations_for_graph,
)


def main():
    # Uncomment to see Jabalizer output
    logging.getLogger().setLevel(logging.INFO)

    dt = 0.05  # Integration timestep
    tmax = 5  # Maximal timestep
    sclf = 1

    tolerable_logical_error_rate = 1e-3
    qsp_required_precision = 1e-2
    gate_synthesis_error_budget = (tolerable_logical_error_rate) / 2
    error_correction_error_budget = (tolerable_logical_error_rate) / 2

    for N in [100]:
        # TA 1 part: specify the core computational capability
        print(f"Generating operator for N ={N}")
        start = time.time()
        # operator = get_vlasov_hamiltonian(k, alpha, nu, N)
        operator = generate_heisenberg_hamiltonian(N)
        end = time.time()
        print("Operator generation time:", end - start)

        ### METHOD 1: Full graph creation
        # TA 1.5 part: model algorithmic circuit
        print("Starting circuit generation")
        start = time.time()
        circuit = get_qsp_circuit(
            operator, qsp_required_precision, dt, tmax, sclf, use_random_angles=True
        )
        end = time.time()
        print("Circuit generation time:", end - start)

        # TA 2 part: FTQC compilation
        print("Starting transpilation")
        start = time.time()
        clifford_t_circuit = pyliqtr_transpile_to_clifford_t(
            circuit, gate_synthesis_error_budget
        )
        end = time.time()
        print("Transpilation time:", end - start)

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
    main()
