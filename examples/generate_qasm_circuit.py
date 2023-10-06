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

from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.problem_ingestion.hamiltonian_generation import (
    generate_1d_heisenberg_hamiltonian,
    generate_cubic_hamiltonian,
)
from benchq.conversions import export_circuit
from qiskit import QuantumCircuit

from qiskit import QuantumCircuit

from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Optimize1qGates, Depth
from copy import deepcopy


# Here we give a qasm circuit for a single block encoding of a
# utility scale instance of the Ising problem. In order to get
# good estimates of the full circuit with all blocks, we would
# need to contatenate 10 of these together and then run the
# resource estimation.

# Our circuit generation has some randomness in it. So to ensure
# all compilation methods get the same circuit, we can compile
# everything to qasm here.


# Utility scale numbers:
# evolution_time = 100
# N = 10


evolution_time = 100
N = 2  # must be >= 2!

print("Generating circuit...")
operator = generate_cubic_hamiltonian(N)
algorithm = qsp_time_evolution_algorithm(operator, evolution_time, 1e-3)

print("Exporting circuit to qiskit...")
# get circuit for single bock encoding
algorithm.program.steps = 1
qiskit_circuit = export_circuit(QuantumCircuit, algorithm.program.full_circuit)


print("Optimizing circuit...")
# Define the set of allowed gates (X, Y, Z, H, S, RZ, T, and CZ)
allowed_gates = ["i", "x", "y", "z", "h", "s", "rz", "cz", "t", "tdg", "sdg"]

# I tried to optimize the circuit with qiskit, but it seems to add a bunch of
# isolated nodes to the graph. If Rigetti is getting isolated nodes, this might be why....
# I don't have time to look at this now, but maybe someone else will down the line? ¯\_(ツ)_/¯
# optimized_circuit = transpile(
#     qiskit_circuit,
#     basis_gates=allowed_gates,
#     optimization_level=1,
# )

# # combine adjacent RY gates manually in an attempt to make up for the fact that
# # transpile is not working.... Also remove RY gates with theta = 0
optimized_circuit = QuantumCircuit(qiskit_circuit.num_qubits)

prev_gate_name = None
prev_qubit = None
accumulated_theta = 0.0

for operation in qiskit_circuit.data:
    instruction = operation[0]
    qubits = operation[1]

    if instruction.name == "ry":
        theta = instruction.params[0]
        qubit = qubits[0]

        if prev_gate_name == "ry" and prev_qubit == qubit:
            # Combine consecutive RY gates
            accumulated_theta += theta
        else:
            # Add the RY gate as-is
            if prev_gate_name == "ry":
                optimized_circuit.ry(accumulated_theta, prev_qubit)
            accumulated_theta = theta
            # optimized_circuit.ry(theta, qubit)
            prev_gate_name = "ry"
            prev_qubit = qubit
    else:
        # Add non-RY gates as-is
        if prev_gate_name == "ry":
            optimized_circuit.ry(accumulated_theta, prev_qubit)
            prev_gate_name = None
            prev_qubit = None
        optimized_circuit.append(instruction, qubits)

old_optimized_circuit = deepcopy(optimized_circuit)


# Remove RY gates with theta = 0
optimized_circuit = QuantumCircuit(old_optimized_circuit.num_qubits)

for operation in old_optimized_circuit.data:
    instruction = operation[0]
    qubits = operation[1]

    if instruction.name in ["rx", "ry", "rz"]:
        theta = instruction.params[0]
        if theta != 0:
            optimized_circuit.append(instruction, qubits)
    elif instruction.name == "reset":
        # Remove reset operations because Jabalizer doesn't support them
        pass
    else:
        optimized_circuit.append(instruction, qubits)


# Get the QASM representation of the circuit
print("Writing circuit to qasm file...")
qasm_string = qiskit_circuit.qasm()
# Specify the file path where you want to write the QASM data
qasm_file_path = (
    "qasm_circuits/ising_circuit_"
    + str(N)
    + "_for_"
    + str(evolution_time)
    + "_amara_2.qasm"
)  # Replace with the desired file path
# Write the QASM data to a file
with open(qasm_file_path, "w") as qasm_file:
    qasm_file.write(qasm_string)
