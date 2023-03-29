import time
from typing import List, Set, Tuple

import networkx as nx
from orquestra.quantum.circuits import CNOT, Circuit

from .graph_sim_mini import get_vertices


def get_algorithmic_graph_from_gate_stitching(circuit: Circuit) -> nx.Graph:
    """Get the graph corresponding to the state generated by the circuit.

    Args:
        circuit (Circuit): the circuit to convert to a graph

    Returns:
        nx.Graph: graph corresponding to the state generated by the circuit
    """
    print("converting circuit to icm form")
    start = time.time()
    icm_circuit = get_icm(circuit)
    end = time.time()
    print(f"Converting to icm took {end - start} seconds")

    print("getting graph vertices")
    start = time.time()
    vertices = get_vertices(icm_circuit)
    end = time.time()
    print(f"getting graph vertices took {end - start} seconds")

    print("Convert vertices to networkx graph")
    start = time.time()
    algorithmic_graph = get_networkx(vertices)
    end = time.time()
    print(f"Converting vertices to networkx graph took {end - start} seconds")

    return algorithmic_graph


def get_icm(circuit: Circuit, gates_to_decompose=["T", "T_Dagger"]) -> Circuit:
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
            for (original_qubit, compiled_qubit) in zip(
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


def get_networkx(vertices: List[Tuple[int, Set[int]]]) -> nx.Graph:
    """Convert the vertices of the graph to a networkx graph.

    Args:
        vertices (list): list of tuples of the form
            (local clifford operation, adjacency list) corresponding to each node
            in the graph

        Returns:
            nx.Graph: the networkx graph with those vertices
    """
    G = nx.empty_graph(len(vertices))
    for vertex_id, vertex in enumerate(vertices):
        for neighbor in vertex[1]:
            G.add_edge(vertex_id, neighbor)
    return G
