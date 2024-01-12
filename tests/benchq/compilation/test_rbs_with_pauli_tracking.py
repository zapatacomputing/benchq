#!/usr/bin/env python
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, Aer
import qiskit
from qiskit_aer.aerprovider import AerSimulator
import numpy as np
import os
import pathlib
import random
from juliacall import Main as jl
from qiskit.transpiler.passes import RemoveBarriers
from benchq.visualization_tools.plot_graph_state import plot_graph_state


jl.include(
    os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        "../../../src/benchq/compilation/ruby_slippers/ruby_slippers.jl",
    ),
)


def test_random_circuit(n_qubits, depth, hyperparams):
    # test that a single random circuit works for |0> initialization

    circuit = generate_random_circuit(n_qubits, depth)

    check_correctness_for_single_init(
        circuit,
        [(3, 0, -1, 0), (3, 1, -1, 0), (3, 2, -1, 0)],
        hyperparams,
        show_circuit=False,
        throw_error_on_incorrect_result=True,
    )


def generate_random_circuit(n_qubits, depth):
    # Generate a random circuit, but make sure
    ops = [2, 3, 7, 8, 9, 10, 11, 12, 13, 14]

    circuit = []
    for op_code in random.choices(ops, k=depth):
        if op_code in [10, 11]:
            qubit_1, qubit_2 = random.sample(range(n_qubits), 2)
            circuit += [(op_code, qubit_1, qubit_2, 0)]
        else:
            qubit = random.choice(list(range(1, n_qubits)))
            if op_code == 14:
                circuit += [(op_code, qubit, -1, random.uniform(0, 2 * np.pi))]
            else:
                circuit += [(op_code, qubit, -1, 0)]

    return circuit


def check_correctness_for_single_init(
    circuit,
    init,
    hyperparams,
    show_circuit=False,
    show_graph_state=False,
    throw_error_on_incorrect_result=True,
):
    n_qubits = 0
    for op_code, qubit_1, qubit_2, angle in init + circuit:
        n_qubits = max(n_qubits, qubit_1 + 1, qubit_2 + 1)

    full_circuit = init + circuit

    # create the graph
    jabalized_circuit = [
        jl.ICMOp(code, qubit_1 + 1, qubit_2 + 1, angle)
        for code, qubit_1, qubit_2, angle in full_circuit
    ]

    asg, pauli_tracker = jl.get_graph_state_data(
        jabalized_circuit,
        n_qubits,
        False,
        False,
        False,
        200,
        1e8,
        "Space",
        hyperparams,
    )

    asg, pauli_tracker = jl.python_asg(asg), jl.python_pauli_tracker(pauli_tracker)

    pdf = simulate(circuit, init, asg, pauli_tracker, show_circuit=show_circuit)

    if show_graph_state:
        plot_graph_state(asg, pauli_tracker)

    # Format the pdf for printing
    binary_distribution = {}
    n = len(pdf)

    all_bitstrings = [format(i, f"0{n_qubits}b") for i in range(2**n_qubits)]

    for i in range(n):
        binary_distribution[all_bitstrings[i]] = pdf[i]
    reversed_prob_density = {}
    for binary_str, probability in binary_distribution.items():
        reversed_binary_str = binary_str[::-1]  # Reverse the binary string
        reversed_prob_density[reversed_binary_str] = probability

    correct_pdf = {
        bitstring: 1.0 if bitstring == "0" * n_qubits else 0.0
        for bitstring in all_bitstrings
    }
    if reversed_prob_density != correct_pdf:
        print("\033[91m" + "Incorrect Result Detected!" + "\033[0m")
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
    for layer_label, layer in enumerate(pauli_tracker["layering"]):
        # the last frame always contains the data nodes, so we can skip them here
        c.barrier(label=f"Layer:{layer_label}")
        for node in layer:
            if node in asg["data_nodes"]:
                continue

            # measure the nodes in the layer
            if pauli_tracker["measurements"][node][0] == jl.I_code:
                pass
            elif pauli_tracker["measurements"][node][0] == jl.H_code:
                c.h(node)
            elif pauli_tracker["measurements"][node][0] == jl.T_code:
                c.t(node)
            elif pauli_tracker["measurements"][node][0] == jl.T_Dagger_code:
                c.tdg(node)
            elif pauli_tracker["measurements"][node][0] == jl.RZ_code:
                c.rz(-pauli_tracker["measurements"][node][1], node)
            else:
                measurement = pauli_tracker["measurements"][node][0]
                raise Exception(f"Unknown measurement type: {measurement}")

            c.h(node)
            c.measure(node, creg[node])
            node_measured[node] = True

        c.barrier(label=f"Paulis:{layer_label}")
        for _ in range(100):
            for control in sorted_nodes:
                # enact paulis which are controlled by that measurement
                for target, controls in enumerate(remaining_dag):
                    x_controls, z_controls = controls
                    if node_measured[control]:
                        if remaining_dag[control] == [[], []]:
                            target_basis = int(pauli_tracker["measurements"][target][0])
                            if control in x_controls:
                                remaining_dag[target][0].remove(control)
                                if target in asg["data_nodes"]:
                                    c.x(target).c_if(control, control_values[control])
                                else:
                                    if target_basis in jl.non_clifford_gate_codes:
                                        c.x(target).c_if(
                                            control, control_values[control]
                                        )
                                    if target_basis == jl.H_code:
                                        if node_measured[target]:
                                            c.x(target).c_if(
                                                control, control_values[control]
                                            )
                                            c.measure(target, creg[target])
                                        else:
                                            c.x(target).c_if(
                                                control, control_values[control]
                                            )
                            if control in z_controls:
                                remaining_dag[target][1].remove(control)
                                if (
                                    target_basis == jl.I_code
                                    or target_basis in jl.non_clifford_gate_codes
                                    or target in asg["data_nodes"]
                                ):
                                    if node_measured[target]:
                                        c.x(target).c_if(
                                            control, control_values[control]
                                        )
                                        c.measure(target, creg[target])
                                    else:
                                        c.z(target).c_if(
                                            control, control_values[control]
                                        )

    c.barrier(label="inv circ")

    append_inverse_qiskit_circuit(circuit, c, asg["data_nodes"])

    c.barrier(label="inv init")

    append_inverse_qiskit_circuit(init, c, asg["data_nodes"])

    c.barrier(label="output")

    for node in asg["data_nodes"]:
        c.measure(reg[node], creg[node])

    if show_circuit:
        print(c)

    cc = qiskit.transpile(
        RemoveBarriers()(c), backend=AerSimulator(), optimization_level=3
    )
    # print(cc)
    simulator = Aer.get_backend("aer_simulator_matrix_product_state")
    result = simulator.run(cc, shots=10000).result().get_counts()

    return counts_to_pdf(asg["data_nodes"], result)


# create function which implements the reverse of the circuit in qiskit
def append_inverse_qiskit_circuit(circuit, c: QuantumCircuit, bits):
    for gate in reversed(circuit):
        if gate[0] == 1:
            continue
        elif gate[0] == 2:
            c.sdg(bits[gate[1]])
        elif gate[0] == 3:
            c.h(bits[gate[1]])
        elif gate[0] == 4:
            c.h(bits[gate[1]])
            c.sdg(bits[gate[1]])
            c.h(bits[gate[1]])
        elif gate[0] == 5:
            c.sdg(bits[gate[1]])
            c.h(bits[gate[1]])
        elif gate[0] == 6:
            c.h(bits[gate[1]])
            c.sdg(bits[gate[1]])
        elif gate[0] == 7:
            c.x(bits[gate[1]])
        elif gate[0] == 8:
            c.y(bits[gate[1]])
        elif gate[0] == 9:
            c.z(bits[gate[1]])
        elif gate[0] == 10:
            c.cz(bits[gate[1]], bits[gate[2]])
        elif gate[0] == 11:
            c.cx(bits[gate[1]], bits[gate[2]])
        elif gate[0] == 12:
            c.tdg(bits[gate[1]])
        elif gate[0] == 13:
            c.t(bits[gate[1]])
        elif gate[0] == 14:
            c.rz(gate[3], bits[gate[1]])
        else:
            raise Exception(f"Unrecognized gate: {gate}")


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


if __name__ == "__main__":
    hyperparams = jl.RubySlippersHyperparams(3, 2, 6, 1e5, 0)
    for n_circuits_checked in range(1000):
        print(
            "\033[92m"
            + f"{n_circuits_checked} circuits checked successfully!"
            + "\033[0m"
        )
        test_random_circuit(
            n_qubits=10,
            depth=50,
            hyperparams=hyperparams,
        )
        n_circuits_checked += 1

    # check_correctness_for_single_init(
    #     [
    #         (14, 1, -1, 2.448088786866598),
    #         (14, 1, -1, 5.711008414454667),
    #     ],
    #     [(3, 0, -1, 0), (3, 1, -1, 0), (3, 2, -1, 0)],
    #     hyperparams,
    #     show_circuit=True,
    #     show_graph_state=True,
    #     throw_error_on_incorrect_result=True,
    # )

    # check_correctness_for_single_init(
    #     [
    #         (3, 0, -1, 0),
    #         (3, 1, -1, 0),
    #         (3, 4, -1, 0),
    #         (12, 1, -1, 0),
    #         (10, 0, 4, 0),
    #         (11, 1, 0, 0),
    #         (3, 1, -1, 0),
    #         (11, 3, 0, 0),
    #         (12, 1, -1, 0),
    #         (11, 4, 1, 0),
    #         (12, 4, -1, 0),
    #         (3, 4, -1, 0),
    #         (12, 4, -1, 0),
    #     ],
    #     [],
    #     hyperparams,
    #     show_circuit=True,
    #     show_graph_state=True,
    #     throw_error_on_incorrect_result=True,
    # )

    # check_correctness_for_single_init(
    #     [
    #         (3, 0, -1, 0),
    #         (10, 0, 2, 0),
    #         (12, 1, -1, 0),
    #         (3, 1, -1, 0),
    #         (12, 1, -1, 0),
    #         (12, 1, -1, 0),
    #         (11, 0, 1, 0),
    #         (10, 1, 2, 0),
    #         (11, 2, 1, 0),
    #         (12, 1, -1, 0),
    #     ],
    #     [],
    #     hyperparams,
    #     show_circuit=True,
    #     show_graph_state=True,
    #     throw_error_on_incorrect_result=True,
    # )
