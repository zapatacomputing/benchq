################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
MAKE SURE TO UNZIP THE problem.zip FILE BEFORE RUNNING THIS SCRIPT!!!

Objectives:

    1. create a testing ground to see how close we are to handling the larger
    problem instances that jerome has been working on.
"""
import json
import logging
import time

import numpy as np
import pyLIQTR.sim_methods.quantum_ops as qops
from openfermion import QubitOperator
from orquestra.integrations.cirq.conversions import from_openfermion

# At this stage of development we are aware that there are some issues with methods
# 2 and 3 and they do not necessarily yield correct results.
from pyLIQTR.QSP.Hamiltonian import Hamiltonian as pyH

from benchq import BasicArchitectureModel
from benchq.algorithms import get_qsp_program
from benchq.compilation import pyliqtr_transpile_to_clifford_t
from benchq.compilation.jabalizer_utils import get_algorithmic_graph_from_python
from benchq.conversions import pyliqtr_to_openfermion
from benchq.resource_estimation.graph_compilation import (
    get_resource_estimations_for_graph,
)


def load_qubit_op(file):
    if isinstance(file, str):
        with open(file, "r") as f:
            data = json.load(f)
    else:
        data = json.load(file)

    full_operator = QubitOperator()
    for term_dict in data["terms"]:
        operator = []
        for pauli_op in term_dict["pauli_ops"]:
            operator.append((pauli_op["qubit"], pauli_op["op"]))
        coefficient = term_dict["coefficient"]["real"]
        if term_dict["coefficient"].get("imag"):
            coefficient += 1j * term_dict["coefficient"]["imag"]
        full_operator += QubitOperator(operator, coefficient)

    return from_openfermion(full_operator)


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
    file = "problems/" + hamiltonian_name + ".json"
    # operator = get_vlasov_hamiltonian(k, alpha, nu, N)
    # # TA 1 part: specify the core computational capability
    operator = load_qubit_op(file)
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
    graph = get_algorithmic_graph_from_python(clifford_t_circuit)
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
    main("CH4-8-NOs_qubitop")
