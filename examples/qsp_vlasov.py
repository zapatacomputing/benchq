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
from pyLIQTR.QSP import gen_qsp as qspFuncs

from benchq import BasicArchitectureModel
from benchq.algorithms import get_qsp_circuit
from benchq.compilation import get_algorithmic_graph, pyliqtr_transpile_to_clifford_t
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.resource_estimation.graph_compilation import (
    get_resource_estimations_for_graph,
)


def main():
    # Uncomment to see Jabalizer output
    # logging.getLogger().setLevel(logging.INFO)

    k = 2.0
    alpha = 0.6
    nu = 0.0

    required_precision = 1e-2

    dt = 0.1  # Integration timestep
    tmax = 5  # Maximal timestep
    sclf = 1

    for N in [2]:
        # TA 1 part: specify the core computational capability
        start = time.time()
        operator = get_vlasov_hamiltonian(k, alpha, nu, N)
        end = time.time()
        print("Operator generation time:", end - start)

        # TA 1.5 part: model algorithmic circuit
        start = time.time()
        circuit = get_qsp_circuit(operator, required_precision, dt, tmax, sclf)
        end = time.time()
        print("Circuit generation time:", end - start)

        # TA 2 part: FTQC compilation
        synthesis_accuracy = 1e-10
        clifford_t_circuit = pyliqtr_transpile_to_clifford_t(
            circuit, synthesis_accuracy
        )
        graph = get_algorithmic_graph(clifford_t_circuit)

        # TA 2 part: model hardware resources
        architecture_model = BasicArchitectureModel(
            physical_gate_error_rate=1e-3,
            physical_gate_time_in_seconds=1e-6,
        )
        synthesis_accuracy = 1e-3
        start = time.time()
        resource_estimates = get_resource_estimations_for_graph(
            graph, architecture_model, synthesis_accuracy
        )
        end = time.time()
        print("Resource estimation time:", end - start)
        print(resource_estimates)


if __name__ == "__main__":
    main()
