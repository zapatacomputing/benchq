################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
Objectives:

1. Have a "benchq" script, which takes in a circuit and outputs a resource estimate
    - Prototype, but needs to make sense in principle.
    - Well defined I/Os


2. Have a "darpa-1.5" script, which creates a circuit from an application instance.
    - This is mostly for completeness and illustratory purposes
    - Software can be quite crappy
"""
import logging
import time

import numpy as np

from benchq import BasicArchitectureModel
from benchq.algorithms import get_qsp_circuit, get_qsp_program
from benchq.compilation import get_algorithmic_graph, pyliqtr_transpile_to_clifford_t
from benchq.compilation.gate_stitching import get_algorithmic_graph_from_gate_stitching
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.resource_estimation.graph_compilation import (
    get_resource_estimations_for_graph,
    get_resource_estimations_for_program,
)

# This examples shows three ways of performing resource estimation:
# 1. Generating the whole circuit, creating a graph out of it and performing
#   estimation on it
# 2. Using Quantum Program, performing estimation on the subcircuits
#   and then combining them together
# 3. Using Quantum Program, recreating the full graph from it, and then
#   performing resource estimation on it
#
# The first method is a reference, as it does not involve any simplification,
# it represents the exact result. However, given the size of the target circuits
# it's not scalable.
#
# The second method does not explicitly create the whole circuit, but uses the quantum
# program and subcircuits. For each subcircuit it creats a graph and then joins all
# the graphs together to recreate the graph of the full circuit. Ideally,
# the recreated graph should exactly match the ful graph from the previous
# example (up to local clifford transformations). However, at this point the method
# for recreating graph is imperfect, so it might introduce some approximations.

# The third method creates only the subgraphs for each subroutine in a quantum program,
# and the creates resource estimation based on them, without explicitly recreating
# the full graph. It is the least accurate from all threee, as it introduces
# certain assumptions, so should be treated as an upper bound on the resources needed.
# However, it is also the fastest and the least resource intensive.

# At this stage of development we are aware that there are some issues with methods
# 2 and 3 and they do not necessarily yield correct results.


def main():
    # Uncomment to see Jabalizer output
    # logging.getLogger().setLevel(logging.INFO)

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

    gate_synthesis_error_budget = (
        tolerable_logical_error_rate - qsp_required_precision
    ) / 3
    error_correction_error_budget = (
        tolerable_logical_error_rate - qsp_required_precision
    ) / 3

    for N in [2]:
        # TA 1 part: specify the core computational capability
        start = time.time()
        operator = get_vlasov_hamiltonian(k, alpha, nu, N)
        end = time.time()
        print("Operator generation time:", end - start)

        ### METHOD 1: Full graph creation
        # TA 1.5 part: model algorithmic circuit
        start = time.time()
        circuit = get_qsp_circuit(
            operator, qsp_required_precision, dt, tmax, sclf, use_random_angles=True
        )
        end = time.time()
        print("Circuit generation time:", end - start)
        # TA 2 part: FTQC compilation
        clifford_t_circuit = pyliqtr_transpile_to_clifford_t(
            circuit, gate_synthesis_error_budget
        )
        graph = get_algorithmic_graph_from_gate_stitching(clifford_t_circuit)

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

        ### METHOD 2: Estimation from quantum program, without recreating full graph
        # TA 1.5 part: model algorithmic circuit
        start = time.time()
        program = get_qsp_program(
            operator, qsp_required_precision, dt, tmax, sclf, mode="time_evolution"
        )

        end = time.time()
        print("Circuit generation time:", end - start)
        # TA 2 part: model hardware resources
        start = time.time()
        resource_estimates = get_resource_estimations_for_program(
            program,
            gate_synthesis_error_budget + error_correction_error_budget,
            architecture_model,
            use_full_program_graph=False,
        )
        end = time.time()
        print("Resource estimation time:", end - start)
        print(resource_estimates)

        ### METHOD 3: Estimation from quantum program, with recreating the full graph
        start = time.time()
        resource_estimates = get_resource_estimations_for_program(
            program,
            gate_synthesis_error_budget + error_correction_error_budget,
            architecture_model,
            use_full_program_graph=True,
            plot=False,
        )
        end = time.time()
        print("Resource estimation time:", end - start)
        print(resource_estimates)


if __name__ == "__main__":
    main()
