#!/usr/bin/env python
import os
import random

import numpy as np
import pytest
import qiskit
from orquestra.quantum.circuits import CNOT, CZ, RZ, Circuit, H, I, S, T, X, Y, Z
from qiskit import Aer, ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.transpiler.passes import RemoveBarriers

from benchq.compilation.graph_states import jl
from benchq.conversions import export_circuit
from benchq.visualization_tools.plot_graph_state import plot_graph_state

np.random.seed(0)

SKIP_SLOW = pytest.mark.skipif(
    os.getenv("SLOW_BENCHMARKS") is None,
    reason="Slow benchmarks can only run if SLOW_BENCHMARKS env variable is defined",
)


def verify_random_circuit(n_qubits, depth, hyperparams, optimization, verbose):
    # test that a single random circuit works for |0> initialization

    circuit = generate_random_circuit(n_qubits, depth)

    check_correctness_for_single_init(
        circuit,
        # Initialize in all possible single qubit stabiilzer states
        Circuit([H(0), H(1), H(2), H(3), H(4), H(5), S(3), S(4), S(5)]),
        hyperparams,
        show_circuit=True,
        throw_error_on_incorrect_result=True,
        optimization=optimization,
        verbose=verbose,
    )


def generate_random_circuit(n_qubits, depth):
    # Generate a random circuit, but make sure
    ops = [I, X, Y, Z, H, S, RZ, T, T.dagger, CNOT, CZ]

    circuit = Circuit([])
    for gate in random.choices(ops, k=depth):
        if gate in [CNOT, CZ]:
            qubit_1, qubit_2 = random.sample(range(n_qubits), 2)
            circuit += gate(qubit_1, qubit_2)
        else:
            qubit = random.choice(list(range(n_qubits)))
            if gate == RZ:
                circuit += gate(random.uniform(0, 2 * np.pi))(qubit)
            else:
                circuit += gate(qubit)

    return circuit


def check_correctness_for_single_init(
    circuit,
    init,
    hyperparams,
    show_circuit=False,
    show_graph_state=False,
    throw_error_on_incorrect_result=True,
    optimization="Time",
    max_num_qubits=3,
    verbose=False,
):
    full_circuit = init + circuit

    asg, pauli_tracker, _ = jl.get_rbs_graph_state_data(
        full_circuit,
        verbose=verbose,
        takes_graph_input=False,
        gives_graph_output=False,
        optimization=str(optimization),
        max_num_qubits=max_num_qubits,
        hyperparams=hyperparams,
    )

    print("Returned to Python!")

    asg, pauli_tracker = jl.python_asg(asg), jl.python_pauli_tracker(pauli_tracker)

    print("Converted to Python!")

    pdf = simulate(circuit, init, asg, pauli_tracker, show_circuit=show_circuit)

    print("Finished Simulation!")

    if show_graph_state:
        plot_graph_state(asg, pauli_tracker)

    # Format the pdf for printing
    binary_distribution = {}
    n = len(pdf)

    all_bitstrings = [
        format(i, f"0{full_circuit.n_qubits}b")
        for i in range(2**full_circuit.n_qubits)
    ]

    for i in range(n):
        binary_distribution[all_bitstrings[i]] = pdf[i]
    reversed_prob_density = {}
    for binary_str, probability in binary_distribution.items():
        reversed_binary_str = binary_str[::-1]  # Reverse the binary string
        reversed_prob_density[reversed_binary_str] = probability

    correct_pdf = {
        bitstring: 1.0 if bitstring == "0" * full_circuit.n_qubits else 0.0
        for bitstring in all_bitstrings
    }
    if reversed_prob_density != correct_pdf:
        print("\033[91m" + "Incorrect Result Detected!" + "\033[0m")
        # remove trivial parts of pdf so it's easier to read
        reversed_prob_density = {
            k: v for k, v in reversed_prob_density.items() if v != 0
        }
        print(f"circuit: {circuit},\ninit: {init} \npdf: {reversed_prob_density}")
        if throw_error_on_incorrect_result:
            raise Exception("Incorrect Result Detected!")
        return circuit, init, reversed_prob_density
    else:
        print("\033[92m" + "Correct Result!" + "\033[0m")
        return None


def simulate(circuit, init, asg, pauli_tracker, show_circuit=True):
    creg = ClassicalRegister(asg["n_nodes"])
    reg = QuantumRegister(asg["n_nodes"])
    c = QuantumCircuit(reg, creg)
    for i in range(asg["n_nodes"]):
        c.h(reg[i])

    c.barrier(label="graph")
    for node, neighborhood in enumerate(asg["edge_data"]):
        for neighbor in neighborhood:
            if node < neighbor:  # avoid duplicate edges
                c.cz(reg[node], reg[neighbor])

    c.barrier(label="SQC")
    enact_sqc_layer(asg, c, reg)

    control_values = [True] * asg["n_nodes"]
    node_measured = [False] * asg["n_nodes"]

    remaining_dag = [[[], []] for _ in range(asg["n_nodes"])]
    # only include paulis which have an affect
    for target, controls in enumerate(pauli_tracker["cond_paulis"]):
        x_controls, z_controls = controls
        for control in x_controls:
            if (
                pauli_tracker["measurements"][target][0] != jl.I_code
                or target in asg["data_nodes"]
            ):
                remaining_dag[target][0].append(control)
        for control in z_controls:
            if (
                pauli_tracker["measurements"][target][0] != jl.H_code
                or target in asg["data_nodes"]
            ):
                remaining_dag[target][1].append(control)

    sorted_nodes = topological_sort(
        list(range(asg["n_nodes"])), pauli_tracker["cond_paulis"]
    )

    print("Creating layering in simulation!")

    for layer_label, layer in enumerate(pauli_tracker["layering"]):
        c.barrier(label=f"Layer:{layer_label}")
        for node in layer:
            # the last frame always contains the data nodes, so we can skip them here
            if node in asg["data_nodes"]:
                continue

            measure_node(node, pauli_tracker, c, creg)
            node_measured[node] = True

        c.barrier(label=f"Paulis:{layer_label}")
        # repeat many times to ensure that all possible paulis are enacted
        for _ in range(100):
            for control in sorted_nodes:
                # enact paulis which are controlled by that measurement
                for target, controls in enumerate(remaining_dag):
                    x_controls, z_controls = controls
                    if node_measured[control]:
                        control_basis = int(pauli_tracker["measurements"][control][0])
                        target_basis = int(pauli_tracker["measurements"][target][0])

                        # In the control is blocked by a non-clifford measurement,
                        # we can't enact the Pauli yet.
                        if (
                            remaining_dag[control][0] == []
                            and control_basis in jl.non_clifford_gate_codes
                        ) or control_basis != jl.non_clifford_gate_codes:
                            enact_controlled_paulis(
                                x_controls,
                                z_controls,
                                remaining_dag,
                                control,
                                target,
                                control_values,
                                asg,
                                c,
                                creg,
                                node_measured,
                                target_basis,
                            )

    c.barrier(label="inv circ")
    c &= get_reversed_qiskit_circuit(circuit, asg["data_nodes"])

    c.barrier(label="inv init")
    c &= get_reversed_qiskit_circuit(init, asg["data_nodes"])

    c.barrier(label="output")
    for node in asg["data_nodes"]:
        c.measure(reg[node], creg[node])

    if show_circuit:
        print(c)

    print("Starting simulation!")
    simulator = Aer.get_backend("aer_simulator_matrix_product_state")
    cc = qiskit.transpile(RemoveBarriers()(c), backend=simulator, optimization_level=3)
    result = simulator.run(cc, shots=1000).result().get_counts()

    return counts_to_pdf(asg["data_nodes"], result)


def reverse_dag(dag):
    reversed_dag = [[[], []] for _ in range(len(dag))]
    for node, controls in enumerate(dag):
        x_controls, z_controls = controls
        for control in x_controls:
            reversed_dag[control][0].append(node)
        for control in z_controls:
            reversed_dag[control][1].append(node)
    return reversed_dag


def enact_sqc_layer(asg, c, reg):
    for node, sqs in enumerate(asg["sqs"]):
        if sqs == jl.I_code:
            pass
        elif sqs == jl.S_code:
            c.s(reg[node])
        elif sqs == jl.H_code:
            c.h(reg[node])
        elif sqs == jl.HSH_code:
            c.h(reg[node])
            c.s(reg[node])
            c.h(reg[node])
        elif sqs == jl.SH_code:
            c.h(reg[node])
            c.s(reg[node])
        elif sqs == jl.HS_code:
            c.s(reg[node])
            c.h(reg[node])
        else:
            raise Exception(f"other sqs: {sqs}")

    for node, pauli in enumerate(asg["sqp"]):
        if pauli == jl.I_code:
            pass
        elif pauli == jl.X_code_internal:
            c.x(reg[node])
        elif pauli == jl.Y_code_internal:
            c.y(reg[node])
        elif pauli == jl.Z_code_internal:
            c.z(reg[node])
        else:
            raise Exception(f"other pauli: {pauli}")


def measure_node(node, pauli_tracker, c, creg):
    if pauli_tracker["measurements"][node][0] == jl.I_code:
        pass
    elif pauli_tracker["measurements"][node][0] == jl.H_code:
        c.h(node)
    elif pauli_tracker["measurements"][node][0] == jl.T_code:
        c.t(node)
    elif pauli_tracker["measurements"][node][0] == jl.T_Dagger_code:
        c.tdg(node)
    elif pauli_tracker["measurements"][node][0] == jl.RZ_code:
        c.rz(pauli_tracker["measurements"][node][1], node)
    else:
        measurement = pauli_tracker["measurements"][node][0]
        raise Exception(f"Unknown measurement type: {measurement}")

    c.h(node)
    c.measure(node, creg[node])


def enact_controlled_paulis(
    x_controls,
    z_controls,
    remaining_dag,
    control,
    target,
    control_values,
    asg,
    c,
    creg,
    node_measured,
    target_basis,
):
    if control in x_controls:
        remaining_dag[target][0].remove(control)
        if target in asg["data_nodes"]:
            c.x(target).c_if(control, control_values[control])
        else:
            if target_basis in jl.non_clifford_gate_codes:
                c.x(target).c_if(control, control_values[control])
            if target_basis == jl.H_code:
                if node_measured[target]:
                    c.x(target).c_if(control, control_values[control])
                    c.measure(target, creg[target])
                else:
                    c.x(target).c_if(control, control_values[control])
    if control in z_controls:
        remaining_dag[target][1].remove(control)
        if (
            target_basis == jl.I_code
            or target_basis in jl.non_clifford_gate_codes
            or target in asg["data_nodes"]
        ):
            if node_measured[target]:
                c.x(target).c_if(control, control_values[control])
                c.measure(target, creg[target])
            else:
                c.z(target).c_if(control, control_values[control])


def get_reversed_qiskit_circuit(circuit, data_qubits):
    shifted_orquestra_circuit = Circuit([])
    for op in circuit.inverse()._operations:
        shifted_qubits = (data_qubits[index] for index in op.qubit_indices)
        shifted_orquestra_circuit += op.gate(*shifted_qubits)

    return export_circuit(QuantumCircuit, shifted_orquestra_circuit)


# transformed the counts from the qiskit simulation into a real pdf; some really ugly
# bit shifting (and similar) is necessary here
def counts_to_pdf(bits, counts):
    num_bits = len(bits)
    pdf = np.zeros(2**num_bits, dtype=np.int_)
    masks = []
    for i, _ in enumerate(pdf):
        bit = 0
        for j, b in enumerate(bits):
            bit += (i & 2**j) << (b - j)
        masks.append(bit)
    masks.reverse()
    for e in counts:
        found = False
        for i, mask in enumerate(masks):
            if (int(e, 2) & mask) == mask:
                pdf[2**num_bits - 1 - i] += counts[e]
                found = True
                break
        if not found:
            raise Exception(f"no mask found for {e}")
    pdf = pdf / float(np.sum(pdf))
    return pdf


def topological_sort(layer, cond_paulis):
    visited = set()
    result = []

    def dfs(node):
        visited.add(node)
        for neighbor in cond_paulis[node][0] + cond_paulis[node][1]:
            if neighbor not in visited and neighbor in layer:
                dfs(neighbor)
        result.append(node)

    for node in layer:
        if node not in visited:
            dfs(node)

    return result


@pytest.mark.parametrize("optimization", ["Space", "Time", "Variable"])
@pytest.mark.parametrize(
    "init",
    [
        # All start in Z basis
        Circuit([]),
        # Some start in X basis, one in Z basis
        Circuit([H(0), H(1)]),
        # All start in X basis
        Circuit([H(0), H(1), H(2)]),
        # all start in Y basis
        Circuit([H(0), S(0), H(1), S(1), H(2), S(2)]),
    ],
)
@pytest.mark.parametrize(
    "circuit",
    [
        # T gates work alone
        Circuit([T(0), T(0)]),
        # rotations work alone
        Circuit([RZ(2.44)(0), RZ(5.71)(0)]),
        # rotations work in circuit
        Circuit([Z(0), Y(0), RZ(1.07)(2), X(1)]),
        # Standard single qubit gates
        Circuit([X(0)]),
        Circuit([H(0)]),
        Circuit([S(0)]),
        Circuit([H(0), S(0), H(0)]),
        Circuit([H(0), S(0)]),
        Circuit([S(0), H(0)]),
        Circuit([H(2)]),
        Circuit([H(0), CNOT(0, 1)]),
        Circuit([CZ(0, 1), H(2)]),
        Circuit([H(0), S(0), CNOT(0, 1), H(2)]),
        Circuit([CNOT(0, 1), CNOT(1, 2)]),
        Circuit([H(0), RZ(0.034023)(0)]),
        # Test pauli tracker layering
        Circuit(
            [
                H(0),
                S(0),
                H(1),
                CZ(0, 1),
                H(2),
                CZ(1, 2),
            ]
        ),
        Circuit(
            [
                H(0),
                H(1),
                H(3),
                CZ(0, 3),
                CZ(1, 4),
                H(3),
                H(4),
                CZ(3, 4),
            ]
        ),
        Circuit(
            [
                H(0),
                H(1),
                H(4),
                T(1),
                CZ(0, 4),
                CNOT(1, 0),
                H(1),
                CNOT(3, 1),
                T(1),
                CNOT(4, 1),
                T(4),
                H(4),
                T(4),
            ]
        ),
        Circuit(
            [
                H(3),
                CZ(0, 2),
                T(1),
                H(1),
                T(1),
                T(1),
                CNOT(0, 1),
                CZ(1, 2),
                CNOT(2, 1),
                T(1),
            ],
        ),
        # test layering with non-clifford dependencies
        Circuit(
            [
                T(0),
                H(0),
                T(0),
                T(0),
                H(0),
                T(0),
            ]
        ),
    ],
)
def test_particular_circuits_give_correct_results(circuit, init, optimization):
    hyperparams = jl.RbSHyperparams(3, 2, 6, 1e5, 0)
    check_correctness_for_single_init(
        circuit,
        init,
        hyperparams,
        show_circuit=True,
        throw_error_on_incorrect_result=True,
        optimization=optimization,
        max_num_qubits=3,
    )


# If you run this test, it will take a long time to complete. Make sure to
# run it with the -s option so that you can see the circuits being printed
# as well as the progress of the test.
# @SKIP_SLOW
def test_1000_large_random_circuits():
    for n_circuits_checked in range(1000):
        # randomize hyperparams
        teleportation_threshold = np.random.randint(1, 10)
        teleportation_depth = np.random.randint(1, 3) * 2
        min_neighbor_degree = np.random.randint(5, 20)
        hyperparams = jl.RbSHyperparams(
            teleportation_threshold, teleportation_depth, min_neighbor_degree, 1e5, 0
        )

        optimization = np.random.choice(["Space", "Time", "Variable"])

        print(
            "\033[92m"
            + f"{n_circuits_checked} circuits checked successfully!"
            + "\033[0m"
        )
        verify_random_circuit(
            n_qubits=10,
            depth=30,
            hyperparams=hyperparams,
            optimization=optimization,
            verbose=True,
        )
        n_circuits_checked += 1


# leaving this here because it is useful for quickly debugging a circuit
# if __name__ == "__main__":
# # Eliminate unneeded gates quickly from examples
# ops = []
# for _ in range(1000):
#     to_remove = np.random.randint(0, len(ops))
#     new_ops = ops[:to_remove] + ops[to_remove + 1 :]
#     try:
#         check_correctness_for_single_init(
#             Circuit(ops),
#             Circuit([]),
#             jl.RbSHyperparams(6, 4, 15, 1e5, 0),
#             show_circuit=False,
#             show_graph_state=False,
#             throw_error_on_incorrect_result=True,
#             optimization="Time",
#             max_num_qubits=3,
#         )
#     except Exception:
#         ops = new_ops

# print(Circuit(ops))

# # For more meticulous debugging, use this
# check_correctness_for_single_init(
#     Circuit(
#         [],
#     ),
#     Circuit([]),
#     jl.RbSHyperparams(60, 4, 15, 1e5, 0),
#     show_circuit=True,
#     show_graph_state=False,
#     throw_error_on_incorrect_result=True,
#     optimization="Time",
#     max_num_qubits=3,
# )
# # stops evaluation on a correct result so you dont have to run it twice
# breakpoint()
