################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import numpy as np
import pytest
import stim
from orquestra.integrations.qiskit.conversions import import_from_qiskit
from orquestra.quantum.circuits import CNOT, CZ, Circuit, H, I, S
from qiskit import QuantumCircuit

from benchq.compilation import pyliqtr_transpile_to_clifford_t
from benchq.compilation.gate_stitching import get_icm
from benchq.compilation.graph_sim_mini import get_vertices


@pytest.mark.parametrize(
    "circuit",
    [
        Circuit([I(0)]),
        Circuit([H(0)]),
        Circuit([S(0)]),
        Circuit([H(0), S(0), H(0)]),
        Circuit([H(0), S(0)]),
        Circuit([S(0), H(0)]),
        Circuit([S.dagger(0)]),
        Circuit([H(2)]),
        Circuit([CZ(0, 1), H(2)]),
        Circuit([H(0), S(0), CNOT(0, 1), H(2)]),
        Circuit([CNOT(0, 1), CNOT(1, 2)]),
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
    ],
)
def test_stabilizer_states_are_the_same_for_simple_circuits(circuit):

    target_tableau = get_target_tableau(circuit)
    vertices = get_vertices(circuit)
    graph_tableau = get_stabilizer_tableau_from_vertices(vertices)

    assert tableaus_correspond_to_same_state(graph_tableau, target_tableau)


@pytest.mark.parametrize(
    "filename",
    [
        "single_rotation.qasm",
        "h_chain_circuit.qasm",
    ],
)
def test_stabilizer_states_are_the_same_for_larger_circuits(filename):
    # we want to repeat the experiment here since pyliqtr_transpile_to_clifford_t
    # is a random process.
    try:
        qiskit_circuit = import_from_qiskit(QuantumCircuit.from_qasm_file(filename))
    except FileNotFoundError:
        qiskit_circuit = import_from_qiskit(
            QuantumCircuit.from_qasm_file("examples/circuits/" + filename)
        )

    for i in range(1, 10):
        clifford_t = pyliqtr_transpile_to_clifford_t(qiskit_circuit, 10**-2)
        test_circuit = get_icm(clifford_t)

        target_tableau = get_target_tableau(test_circuit)
        vertices = get_vertices(test_circuit)
        graph_tableau = get_stabilizer_tableau_from_vertices(vertices)

        assert tableaus_correspond_to_same_state(graph_tableau, target_tableau)


def get_target_tableau(circuit):
    sim = stim.TableauSimulator()
    for op in circuit.operations:
        if op.gate.name == "I":
            pass
        elif op.gate.name == "CNOT":
            sim.cx(*op.qubit_indices)
        elif op.gate.name == "S_Dagger":
            sim.s_dag(*op.qubit_indices)
        else:
            getattr(sim, op.gate.name.lower())(*op.qubit_indices)
    return get_tableau_from_stim_simulator(sim)


def get_stabilizer_tableau_from_vertices(vertices):
    n_qubits = len(vertices)

    all_xs = np.identity(n_qubits, dtype=bool)
    all_zs = np.zeros((n_qubits, n_qubits), dtype=bool)

    for vertex_id, vertex in enumerate(vertices):
        for neighbor in vertex[1]:
            all_zs[neighbor, vertex_id] = True
            all_zs[vertex_id, neighbor] = True

    paulis = []
    for xs, zs in zip(all_xs, all_zs):
        paulis = paulis + [stim.PauliString.from_numpy(xs=xs, zs=zs)]

    sim = stim.TableauSimulator()
    tableau = stim.Tableau.from_stabilizers(paulis)
    sim.set_inverse_tableau(tableau.inverse())

    cliffords = []
    for vertex in vertices:
        # perform the vertex operation on the tableau
        pauli_perm_class = divmod(vertex[0], 4)[0]
        if pauli_perm_class == 0:
            cliffords += [[]]
        if pauli_perm_class == 1:
            cliffords += [["s"]]
        if pauli_perm_class == 2:
            cliffords += [["h"]]
        if pauli_perm_class == 3:
            cliffords += [["h", "s", "h"]]
        if pauli_perm_class == 4:
            cliffords += [["s", "h"]]
        if pauli_perm_class == 5:
            cliffords += [["h", "s"]]

    # perform the vertices operations on the tableau
    for i in range(n_qubits):
        for clifford in cliffords[i]:
            getattr(sim, clifford)(i)

    return get_tableau_from_stim_simulator(sim)


def get_tableau_from_stim_simulator(sim):
    return np.column_stack(sim.current_inverse_tableau().inverse().to_numpy()[2:4])


def tableaus_correspond_to_same_state(state_1, state_2):
    for stab_1 in state_1:
        for stab_2 in state_2:
            if not commutes(stab_1, stab_2):
                return False
    return True


def commutes(stab_1, stab_2):
    """Returns true if self commutes with other, otherwise false.

    Args:
        other (SymplecticPauli): SymplecticPauli for commutation

    Returns:
        bool: true if self and other commute, false otherwise.
    """
    n_qubits = len(stab_1) // 2
    comm1 = _bool_dot(stab_1[:n_qubits], stab_2[n_qubits:])
    comm2 = _bool_dot(stab_1[n_qubits:], stab_2[:n_qubits])
    return not (comm1 ^ comm2)


# numpy doesn't use the boolean binary ring when performing dot products
# https://github.com/numpy/numpy/issues/1456.
# So we define our own dot product which uses "xor" instead of "or" for addition.
def _bool_dot(x, y):
    return np.logical_xor.reduce(np.logical_and(x, y))
