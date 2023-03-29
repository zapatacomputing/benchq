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
import pyLIQTR.sim_methods.quantum_ops as qops
from orquestra.integrations.cirq.conversions import from_openfermion

# At this stage of development we are aware that there are some issues with methods
# 2 and 3 and they do not necessarily yield correct results.
from pyLIQTR.QSP.Hamiltonian import Hamiltonian as pyH

from benchq import BasicArchitectureModel
from benchq.algorithms import get_qsp_circuit
from benchq.compilation import pyliqtr_transpile_to_clifford_t
from benchq.compilation.gate_stitching import get_algorithmic_graph_from_gate_stitching
from benchq.conversions import pyliqtr_to_openfermion
from benchq.resource_estimation.graph_compilation import (
    get_resource_estimations_for_graph,
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


def generate_hamiltonian(N):

    # Setting J/h's
    # Adjusting these from zero to nonzero may also increase the circuit depth, since additional terms in the Hamiltonian
    # are introduced.
    J_z = 1.0
    J_x = 1.1 * J_z
    J_y = J_x
    h_x = -1.0 * J_z
    h_y = 0.0 * J_z
    h_z = 0.0 * J_z

    tuples, types, coeffs = qops.params_heisenberg_1d(
        N,
        J_x=J_x,
        J_y=J_y,
        J_z=J_z,
        h_x=h_x,
        h_y=h_y,
        h_z=h_z,
        periodic=False,
    )

    sclf = np.sum(np.abs(coeffs))

    ham_strings = qops.ps_text_full_set(tuples, types, N, Coeffs=coeffs / sclf)
    qsp_H = pyH(ham_strings)
    pauli_sum = from_openfermion(pyliqtr_to_openfermion(qsp_H))
    for term in pauli_sum.terms:
        term.coefficient = term.coefficient.real
    return pauli_sum


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
        operator = generate_hamiltonian(N)
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
