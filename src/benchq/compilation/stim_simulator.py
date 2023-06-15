import networkx as nx
import numpy as np
from numba import njit
from orquestra.quantum.circuits import CNOT, Circuit
from stim import TableauSimulator


def get_algorithmic_graph_from_stim(circuit: Circuit) -> nx.Graph:
    """Get the algorithmic graph from a stim circuit.

    Args:
        circuit (Circuit): the circuit to get the algorithmic graph from
    """
    print("starting ICM")
    circuit = get_icm(circuit)
    print("finished ICM")
    tableau = get_tableau_from_stim(circuit)
    print("finished tableau")
    A, _ = tableau_to_graph_adjacency_list(tableau)
    print("finished adjacency list")
    return nx.Graph(A, nodetype=bool)


def get_icm(
    circuit: Circuit, gates_to_decompose=["T", "T_Dagger", "RX", "RY", "RZ"]
) -> Circuit:
    """Convert a circuit to the ICM form.

    Args:
        circuit (Circuit): the circuit to convert to ICM form
        gates_to_decompose (list, optional): list of gates to decompose into CNOT
        and adding ancilla qubits. Defaults to ["T", "T_Dagger"].

    Returns:
        Circuit: the circuit in ICM form
    """
    compiled_qubit_index = {i: i for i in range(circuit.n_qubits)}
    icm_circuit = []
    icm_circuit_n_qubits = circuit.n_qubits - 1
    for op in circuit.operations:
        compiled_qubits = [
            compiled_qubit_index.get(qubit, qubit) for qubit in op.qubit_indices
        ]

        if op.gate.name in gates_to_decompose:
            for original_qubit, compiled_qubit in zip(
                op.qubit_indices, compiled_qubits
            ):
                icm_circuit_n_qubits += 1
                compiled_qubit_index[original_qubit] = icm_circuit_n_qubits
                icm_circuit += [CNOT(compiled_qubit, icm_circuit_n_qubits)]
        else:
            icm_circuit += [
                op.gate(*[compiled_qubit_index[i] for i in op.qubit_indices])
            ]

    return Circuit(icm_circuit)


@njit
def get_tableau_from_stim(circuit):
    sim = TableauSimulator()
    sim.set_num_qubits(circuit.n_qubits)
    for op in circuit.operations:
        if op.gate.name in ["I", "X", "Y", "Z"]:
            pass
        elif op.gate.name == "CNOT":
            sim.cx(*op.qubit_indices)
        elif op.gate.name == "S_Dagger":
            sim.s_dag(*op.qubit_indices)
        elif op.gate.name == "S":
            sim.s(*op.qubit_indices)
        elif op.gate.name == "H":
            sim.h(*op.qubit_indices)
        elif op.gate.name == "CZ":
            sim.cz(*op.qubit_indices)
        else:
            raise ValueError(f"Gate {op.gate.name} not supported.")
    full_tableau = np.linalg.inv(sim.current_inverse_tableau())
    return np.column_stack(full_tableau.to_numpy()[2:4])


@njit
def x_locs(tableau, qubits, bit, above=False):
    incr = -1 if above else 1
    stop = -1 if above else qubits

    locs = []
    for i in range(bit, stop, incr):
        if tableau[i][bit]:
            locs.append(i)
    return locs


def tableau_to_graph_adjacency_list(tableau):
    qubits = tableau.shape[0]
    op_seq = []

    print(qubits)
    for n in range(qubits):
        locs = x_locs(tableau, qubits, n)
        x_num = len(locs)
        print(n)
        print("number of 1s to delete", x_num)

        if x_num == 0:
            # swap columns n and n + qubits
            tableau[:, n + qubits] = np.logical_xor(
                tableau[:, n + qubits], tableau[:, n]
            )
            tableau[:, n] = np.logical_xor(tableau[:, n], tableau[:, n + qubits])
            tableau[:, n + qubits] = np.logical_xor(
                tableau[:, n + qubits], tableau[:, n]
            )
            op_seq.append(("H", n))
            locs = x_locs(tableau, qubits, n)
            x_num = len(locs)

        if locs[0] != n:
            # swap rows n and locs[0]
            tableau[n] = np.logical_xor(tableau[n], tableau[locs[0]])
            tableau[locs[0]] = np.logical_xor(tableau[locs[0]], tableau[n])
            tableau[n] = np.logical_xor(tableau[n], tableau[locs[0]])

        locs.pop(0)
        for r_idx in locs:
            tableau[r_idx] = np.logical_xor(tableau[r_idx], tableau[n])

    for n in range(qubits - 1, -1, -1):
        locs = x_locs(tableau, qubits, n, above=True)

        test_idx = locs.pop(0)
        if test_idx != n:
            raise ValueError(
                "No diagonal X in upper-triangular block - algorithm failure!"
            )

        for idx in locs:
            tableau[idx] = np.logical_xor(tableau[idx], tableau[n])

    for n in range(qubits):
        if tableau[n, n] == 1 and tableau[n, n + qubits] == 1:
            tableau[n, n + qubits] = 0
            op_seq.append(("Pdag", n))

    A = tableau[:, qubits:]

    for n in range(qubits):
        if A[n][n] != 0:
            print("Error: invalid graph conversion (non-zero trace).")

    if not np.array_equal(A, np.transpose(A)):
        print("Error: invalid graph conversion (non-symmetric).")

    return A, op_seq
