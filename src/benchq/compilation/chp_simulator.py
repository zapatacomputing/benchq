from typing import List, Tuple

import networkx as nx
import numpy as np
from numba import njit
from orquestra.quantum.circuits import Circuit

from .stim_simulator import get_icm, tableau_to_graph_adjacency_list


def get_algorithmic_graph_from_chp(circuit: Circuit) -> nx.Graph:
    """Get the algorithmic graph using a CHP simulator.

    Args:
        circuit (Circuit): the circuit to get the algorithmic graph from
    """
    print("starting ICM")
    circuit = get_icm(circuit)
    print("starting numba conversion")
    formatted_circuit, n_qubits = to_numba_circuit(circuit)
    print("start getting tableau")
    tableau = get_tableau_from_chp(formatted_circuit, n_qubits)
    print("finished tableau")
    A, _ = tableau_to_graph_adjacency_list(tableau)
    print("finished adjacency list")
    return nx.Graph(A, nodetype=bool)


def to_numba_circuit(circuit):
    new_circuit = []

    for op in reversed(circuit.operations):
        new_gate = (op.gate.name, [*op.qubit_indices])
        new_circuit.append(new_gate)

    return new_circuit, circuit.n_qubits


@njit
def get_tableau_from_chp(circuit: List[Tuple[str, List[int]]], n):
    table = np.eye(2 * n, dtype=np.bool_)

    print("actually Starting now")

    for op in circuit:
        if op[0] in ["I", "X", "Y", "Z"]:
            pass
        elif op[0] == "CNOT":
            table[op[1][1]] = np.logical_xor(table[op[1][1]], table[op[1][0]])
            table[op[1][0] + n] = np.logical_xor(
                table[op[1][0] + n], table[op[1][1] + n]
            )
        elif op[0] == "S" or op[0] == "S_Dagger":
            table[op[1][0]] = np.logical_xor(table[op[1][0]], table[op[1][0] + n])
        elif op[0] == "H":
            table[op[1][0] + n] = np.logical_xor(table[op[1][0] + n], table[op[1][0]])
            table[op[1][0]] = np.logical_xor(table[op[1][0]], table[op[1][0] + n])
            table[op[1][0] + n] = np.logical_xor(table[op[1][0] + n], table[op[1][0]])
        elif op[0] == "CZ":
            table[op[1][0] + n] = np.logical_xor(table[op[1][0] + n], table[op[1][1]])
            table[op[1][1] + n] = np.logical_xor(table[op[1][1] + n], table[op[1][0]])
        else:
            print("Unknown gate encountered: ", op[0])

    return np.transpose(table[:, n:])
