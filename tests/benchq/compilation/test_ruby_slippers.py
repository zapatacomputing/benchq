################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import os

import networkx as nx
import numpy as np
import pytest
import stim
from numba import njit
from orquestra.integrations.qiskit.conversions import import_from_qiskit
from orquestra.quantum.circuits import CNOT, CZ, Circuit, H, S, T, X
from qiskit import QuantumCircuit
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import matplotlib.patches as mpatches

from benchq.compilation import (
    jl,
    pyliqtr_transpile_to_clifford_t,
    transpile_to_native_gates,
)
from benchq.data_structures import QuantumProgram


@pytest.mark.parametrize(
    "circuit",
    [
        Circuit([X(0)]),
        Circuit([H(0)]),
        Circuit([S(0)]),
        Circuit([H(0), S(0), H(0)]),
        Circuit([H(0), S(0)]),
        Circuit([S(0), H(0)]),
        Circuit([S.dagger(0)]),
        Circuit([H(2)]),
        Circuit([H(0), CNOT(0, 1)]),
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
        # check simple teleportation circuits
        Circuit(
            [
                H(1),
                CNOT(1, 2),
                CNOT(0, 1),
                H(0),
            ]
        ),
        Circuit(
            [
                H(1),
                CNOT(1, 2),
                CNOT(0, 1),
                H(0),
                H(3),
                CNOT(3, 4),
                CNOT(2, 3),
                H(2),
            ]
        ),
        Circuit(
            [
                H(0),
                H(1),
                CNOT(1, 2),
                CNOT(0, 1),
                H(0),
                H(3),
                CNOT(3, 4),
                CNOT(2, 3),
                H(2),
            ]
        ),
    ],
)
def test_stabilizer_states_are_the_same_for_simple_circuits(circuit):
    target_tableau = get_target_tableau(circuit)

    lco, adj, _ = jl.run_ruby_slippers(circuit, False, 999)

    vertices = list(zip(lco, adj))

    graph_tableau = get_stabilizer_tableau_from_vertices(vertices)

    assert_tableaus_correspond_to_the_same_stabilizer_state(
        graph_tableau, target_tableau
    )


@pytest.mark.parametrize(
    "filename",
    [
        "example_circuit.qasm",
    ],
)
def test_stabilizer_states_are_the_same_for_circuits(filename):
    # we want to repeat the experiment here since pyliqtr_transpile_to_clifford_t
    # is a random process.
    try:
        qiskit_circuit = import_from_qiskit(QuantumCircuit.from_qasm_file(filename))
    except FileNotFoundError:
        qiskit_circuit = import_from_qiskit(
            QuantumCircuit.from_qasm_file(os.path.join("examples", "data", filename))
        )

    circuit = transpile_to_native_gates(qiskit_circuit)
    test_circuit = get_icm(circuit)

    target_tableau = get_target_tableau(test_circuit)

    lco, adj, _ = jl.run_ruby_slippers(test_circuit, False, 999)
    vertices = list(zip(lco, adj))
    graph_tableau = get_stabilizer_tableau_from_vertices(vertices)

    assert_tableaus_correspond_to_the_same_stabilizer_state(
        graph_tableau, target_tableau
    )


@pytest.mark.parametrize(
    "filename",
    [
        "single_rotation.qasm",
        "example_circuit.qasm",
    ],
)
def test_stabilizer_states_are_the_same_for_circuits_with_decomposed_rotations(
    filename,
):
    # we want to repeat the experiment here since pyliqtr_transpile_to_clifford_t
    # is a random process.
    try:
        qiskit_circuit = import_from_qiskit(QuantumCircuit.from_qasm_file(filename))
    except FileNotFoundError:
        qiskit_circuit = import_from_qiskit(
            QuantumCircuit.from_qasm_file(os.path.join("examples", "data", filename))
        )

    # pyliqtr_transpile_to_clifford_t is random and cannot be seeded
    # so multiple trials are needed
    for i in range(1, 10):
        clifford_t = pyliqtr_transpile_to_clifford_t(
            qiskit_circuit, circuit_precision=10**-2
        )
        test_circuit = get_icm(clifford_t)

        target_tableau = get_target_tableau(test_circuit)

        # ensure state does not teleport
        lco, adj, _ = jl.run_ruby_slippers(test_circuit, True, 9999, 9999)
        vertices = list(zip(lco, adj))

        graph_tableau = get_stabilizer_tableau_from_vertices(vertices)

        assert_tableaus_correspond_to_the_same_stabilizer_state(
            graph_tableau, target_tableau
        )


# big circuit
teleportation_buffers = [
    [
        # make bell pair 1
        H((i * 10 + i) + 1),
        CNOT((i * 10 + i) + 1, (i * 10 + i) + 2),
        # teleport 1
        CNOT((i * 10 + i) + 0, (i * 10 + i) + 1),
        H((i * 10 + i) + 0),
        # make bell pair 2
        H((i * 10 + i) + 3),
        CNOT((i * 10 + i) + 3, (i * 10 + i) + 4),
        # teleport 3
        CNOT((i * 10 + i) + 2, (i * 10 + i) + 3),
        H((i * 10 + i) + 2),
        # make bell pair 3
        H((i * 10 + i) + 5),
        CNOT((i * 10 + i) + 5, (i * 10 + i) + 6),
        # teleport 3
        CNOT((i * 10 + i) + 4, (i * 10 + i) + 5),
        H((i * 10 + i) + 4),
        # make bell pair 4
        H((i * 10 + i) + 7),
        CNOT((i * 10 + i) + 7, (i * 10 + i) + 8),
        # teleport 4
        CNOT((i * 10 + i) + 6, (i * 10 + i) + 7),
        H((i * 10 + i) + 6),
        # make bell pair 5
        H((i * 10 + i) + 9),
        CNOT((i * 10 + i) + 9, (i * 10 + i) + 10),
        # teleport 5
        CNOT((i * 10 + i) + 8, (i * 10 + i) + 9),
        H((i * 10 + i) + 8),
    ]
    for i in range(4)
]
manually_concatenated_circuit = [op for ops in teleportation_buffers for op in ops]

manually_concatenated_circuit += [
    H(10),
    CNOT(10, 21),
    CNOT(10, 32),
    CNOT(10, 43),
]

manually_concatenated_subcircuit = [
    [
        # make bell pair 1
        H((i * 10) + 45 + 1),
        CNOT((i * 10) + 45 + 1, (i * 10) + 45 + 2),
        H((i * 10) + 45 + 3),
        CNOT((i * 10) + 45 + 3, (i * 10) + 45 + 4),
        H((i * 10) + 45 + 5),
        CNOT((i * 10) + 45 + 5, (i * 10) + 45 + 6),
        H((i * 10) + 45 + 7),
        CNOT((i * 10) + 45 + 7, (i * 10) + 45 + 8),
        H((i * 10) + 45 + 9),
        CNOT((i * 10) + 45 + 9, (i * 10) + 45 + 10),
    ]
    for i in range(0, 4)
]

manually_concatenated_circuit += [
    op for ops in manually_concatenated_subcircuit for op in ops
]

manually_concatenated_circuit += [
    # teleport 1
    CNOT(10, 46),
    H(10),
    CNOT(47, 48),
    H(47),
    CNOT(49, 50),
    H(49),
    CNOT(51, 52),
    H(51),
    CNOT(53, 54),
    H(53),
    # teleport 2
    CNOT(21, 56),
    H(21),
    CNOT(57, 58),
    H(57),
    CNOT(59, 60),
    H(59),
    CNOT(61, 62),
    H(61),
    CNOT(63, 64),
    H(63),
    # teleport 3
    CNOT(32, 66),
    H(32),
    CNOT(67, 68),
    H(67),
    CNOT(69, 70),
    H(69),
    CNOT(71, 72),
    H(71),
    CNOT(73, 74),
    H(73),
    # teleport 4
    CNOT(43, 76),
    H(43),
    CNOT(77, 78),
    H(77),
    CNOT(79, 80),
    H(79),
    CNOT(81, 82),
    H(81),
    CNOT(83, 84),
    H(83),
]


manually_concatenated_circuit += [
    H(55),
    CNOT(55, 65),
    CNOT(55, 75),
    CNOT(55, 85),
]


manually_concatenated_subcircuit = [
    [
        # make bell pair 1
        H((i * 10) + 85 + 1),
        CNOT((i * 10) + 85 + 1, (i * 10) + 85 + 2),
        H((i * 10) + 85 + 3),
        CNOT((i * 10) + 85 + 3, (i * 10) + 85 + 4),
        H((i * 10) + 85 + 5),
        CNOT((i * 10) + 85 + 5, (i * 10) + 85 + 6),
        H((i * 10) + 85 + 7),
        CNOT((i * 10) + 85 + 7, (i * 10) + 85 + 8),
        H((i * 10) + 85 + 9),
        CNOT((i * 10) + 85 + 9, (i * 10) + 85 + 10),
    ]
    for i in range(0, 4)
]

manually_concatenated_circuit += [
    op for ops in manually_concatenated_subcircuit for op in ops
]

manually_concatenated_circuit += [
    # teleport 1
    CNOT(55, 86),
    H(55),
    CNOT(87, 88),
    H(87),
    CNOT(89, 90),
    H(89),
    CNOT(91, 92),
    H(91),
    CNOT(93, 94),
    H(93),
    # teleport 2
    CNOT(65, 96),
    H(65),
    CNOT(97, 98),
    H(97),
    CNOT(99, 100),
    H(99),
    CNOT(101, 102),
    H(101),
    CNOT(103, 104),
    H(103),
    # teleport 3
    CNOT(75, 106),
    H(75),
    CNOT(107, 108),
    H(107),
    CNOT(109, 110),
    H(109),
    CNOT(111, 112),
    H(111),
    CNOT(113, 114),
    H(113),
    # teleport 4
    CNOT(85, 116),
    H(85),
    CNOT(117, 118),
    H(117),
    CNOT(119, 120),
    H(119),
    CNOT(121, 122),
    H(121),
    CNOT(123, 124),
    H(123),
]


@pytest.mark.parametrize(
    "circuit, teleportation_threshold, teleportation_distance, num_teleportations",
    [
        # tests that a circuit with no teleportations does not teleport
        # (Circuit([H(0), *[CNOT(0, i) for i in range(1, 5)]]), 4, 4, 0),
        # # tests changing threshold
        # (Circuit([H(0), *[CNOT(0, i) for i in range(1, 5)]]), 3, 4, 1),
        # # test that teleportation_distance is respected
        # (Circuit([H(0), *[CNOT(0, i) for i in range(1, 6)]]), 4, 6, 1),
        # # creates a node of degree 4 which will be teleported. Requires 5 CNOTS
        # # 4 to make the node of degree 4 and 1 to activate the teleport
        # (Circuit([H(0), *[CNOT(0, i) for i in range(1, 6)]]), 4, 4, 1),
        # (Circuit([H(0), *[CNOT(0, i) for i in range(1, 8)]]), 4, 4, 1),
        # # test multiple teleportations:
        # (Circuit([H(0), *[CNOT(0, i) for i in range(1, 9)]]), 4, 4, 2),
        # (Circuit([H(0), *[CNOT(0, i) for i in range(1, 11)]]), 4, 4, 2),
        # (Circuit([H(0), *[CNOT(0, i) for i in range(1, 12)]]), 4, 4, 3),
        # (Circuit([H(0), *[CNOT(0, i) for i in range(1, 14)]]), 4, 4, 3),
        # (Circuit([H(0), *[CNOT(0, i) for i in range(1, 15)]]), 4, 4, 4),
        # # test gates that must be decomposed
        # (Circuit([H(0), *[T(0) for _ in range(1, 5)]]), 10, 4, 0),
        (
            Circuit(manually_concatenated_circuit),
            1000,
            4,
            0,
        ),
        # (
        #     Circuit([H(0), CNOT(0, 1), CNOT(0, 2), CNOT(0, 3)]),
        #     1000,
        #     4,
        #     0,
        # ),
        # (
        #     Circuit(
        #         [
        #             H(0),
        #             CNOT(0, 9),
        #             H(0),
        #             # make bell pairs
        #             H(1),
        #             CNOT(1, 2),
        #             H(3),
        #             CNOT(3, 4),
        #             H(5),
        #             CNOT(5, 6),
        #             H(7),
        #             CNOT(7, 8),
        #             # teleport
        #             CNOT(0, 1),
        #             H(0),
        #             CNOT(2, 3),
        #             H(2),
        #             CNOT(4, 5),
        #             H(4),
        #             CNOT(6, 7),
        #             H(6),
        #         ]
        #     ),
        #     10,
        #     4,
        #     0,
        # ),
        # (
        #     Circuit(
        #         [
        #             H(0),
        #             CNOT(0, 9),
        #             H(0),
        #             S(0),
        #             # make bell pairs
        #             H(1),
        #             CNOT(1, 2),
        #             H(3),
        #             CNOT(3, 4),
        #             H(5),
        #             CNOT(5, 6),
        #             H(7),
        #             CNOT(7, 8),
        #             # teleport
        #             CNOT(0, 1),
        #             H(0),
        #             CNOT(2, 3),
        #             H(2),
        #             CNOT(4, 5),
        #             H(4),
        #             CNOT(6, 7),
        #             H(6),
        #         ]
        #     ),
        #     10,
        #     4,
        #     0,
        # ),
        # (
        #     Circuit(
        #         [
        #             H(0),
        #             CNOT(0, 9),
        #             S(0),
        #             H(0),
        #             # make bell pairs
        #             H(1),
        #             CNOT(1, 2),
        #             H(3),
        #             CNOT(3, 4),
        #             H(5),
        #             CNOT(5, 6),
        #             H(7),
        #             CNOT(7, 8),
        #             # teleport
        #             CNOT(0, 1),
        #             H(0),
        #             CNOT(2, 3),
        #             H(2),
        #             CNOT(4, 5),
        #             H(4),
        #             CNOT(6, 7),
        #             H(6),
        #         ]
        #     ),
        #     10,
        #     4,
        #     0,
        # ),
        # (
        #     Circuit(
        #         [
        #             H(0),
        #             CNOT(0, 9),
        #             S(0),
        #             # make bell pairs
        #             H(1),
        #             CNOT(1, 2),
        #             H(3),
        #             CNOT(3, 4),
        #             H(5),
        #             CNOT(5, 6),
        #             H(7),
        #             CNOT(7, 8),
        #             # teleport
        #             CNOT(0, 1),
        #             H(0),
        #             CNOT(2, 3),
        #             H(2),
        #             CNOT(4, 5),
        #             H(4),
        #             CNOT(6, 7),
        #             H(6),
        #         ]
        #     ),
        #     10,
        #     4,
        #     0,
        # ),
        # (
        #     Circuit(
        #         [
        #             H(0),
        #             CNOT(0, 9),
        #             H(0),
        #             S(0),
        #             H(0),
        #             # make bell pairs
        #             H(1),
        #             CNOT(1, 2),
        #             H(3),
        #             CNOT(3, 4),
        #             H(5),
        #             CNOT(5, 6),
        #             H(7),
        #             CNOT(7, 8),
        #             # teleport
        #             CNOT(0, 1),
        #             H(0),
        #             CNOT(2, 3),
        #             H(2),
        #             CNOT(4, 5),
        #             H(4),
        #             CNOT(6, 7),
        #             H(6),
        #         ]
        #     ),
        #     10,
        #     4,
        #     0,
        # ),
        # # test single teleporatation
        # (Circuit([H(0), *[T(0) for _ in range(1, 6)]]), 4, 4, 1),
        # (Circuit([H(0), *[T(0) for _ in range(1, 8)]]), 4, 4, 1),
        # # test multiple teleportations:
        # (Circuit([H(0), *[T(0) for _ in range(1, 9)]]), 4, 4, 2),
        # (Circuit([H(0), *[T(0) for _ in range(1, 11)]]), 4, 4, 2),
        # (Circuit([H(0), *[T(0) for _ in range(1, 12)]]), 4, 4, 3),
        # (Circuit([H(0), *[T(0) for _ in range(1, 14)]]), 4, 4, 3),
        # (Circuit([H(0), *[T(0) for _ in range(1, 15)]]), 4, 4, 4),
    ],
)
def test_teleportation_produces_correct_number_of_nodes_for_small_circuits(
    circuit, teleportation_threshold, teleportation_distance, num_teleportations
):
    quantum_program = QuantumProgram.from_circuit(circuit)
    n_t_gates = quantum_program.n_t_gates
    n_rotations = quantum_program.n_rotation_gates

    lco, adj, input_nodes, output_nodes = jl.run_ruby_slippers(
        circuit,
        True,
        9999,
        teleportation_threshold,
        teleportation_distance,
        6,
        99999,
        1,
    )

    breakpoint()

    n_nodes = len(lco)

    assert (
        n_nodes
        == circuit.n_qubits
        + (n_t_gates + n_rotations)
        + teleportation_distance * num_teleportations
    )


@pytest.mark.parametrize(
    "filename",
    [
        "single_rotation.qasm",
        "example_circuit.qasm",
    ],
)
def test_teleportation_produces_correct_node_parity_for_large_circuits(
    filename,
):
    # we want to repeat the experiment here since pyliqtr_transpile_to_clifford_t
    # is a random process.
    try:
        qiskit_circuit = import_from_qiskit(QuantumCircuit.from_qasm_file(filename))
    except FileNotFoundError:
        qiskit_circuit = import_from_qiskit(
            QuantumCircuit.from_qasm_file(os.path.join("examples", "data", filename))
        )

    # pyliqtr_transpile_to_clifford_t is random and cannot be seeded
    # so multiple trials are needed
    for i in range(1, 10):
        clifford_t = pyliqtr_transpile_to_clifford_t(
            qiskit_circuit, circuit_precision=10**-2
        )

        quantum_program = QuantumProgram.from_circuit(clifford_t)
        n_t_gates = quantum_program.n_t_gates

        lco, adj, _ = jl.run_ruby_slippers(clifford_t, False, 9999)

        n_nodes = len(lco)

        assert n_nodes >= n_t_gates
        # teleportation only adds 2 nodes at a time.
        assert (n_nodes - n_t_gates) % 2 == 0


@pytest.mark.parametrize(
    "circuit, rbs_iteration_time, expected_prop_range",
    [
        (Circuit([H(0), CNOT(0, 1)]), 1.0, [0.9, 1.0]),
        (
            Circuit(
                [H(0), *[CNOT(j, i) for i in range(1, 300) for j in range(2, 300)]]
            ),
            0.1,
            [0.0, 0.5],
        ),
    ],
)
def test_rbs_gives_reasonable_prop(circuit, rbs_iteration_time, expected_prop_range):
    # when
    _, _, prop = jl.run_ruby_slippers(
        circuit, True, 9999, 40, 4, 6, 99999, 1, rbs_iteration_time
    )

    # then
    assert prop >= expected_prop_range[0] and prop <= expected_prop_range[1]


########################################################################################
# Everything below here is testing utils
########################################################################################


def get_icm(circuit: Circuit, gates_to_decompose=["T", "T_Dagger", "RZ"]) -> Circuit:
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
        elif op.gate.name == "RESET":
            for original_qubit, compiled_qubit in zip(
                op.qubit_indices, compiled_qubits
            ):
                icm_circuit_n_qubits += 1
                compiled_qubit_index[original_qubit] = icm_circuit_n_qubits
        else:
            icm_circuit += [
                op.gate(*[compiled_qubit_index[i] for i in op.qubit_indices])
            ]

    return Circuit(icm_circuit)


def get_target_tableau(circuit):
    sim = stim.TableauSimulator()
    for op in circuit.operations:
        if op.gate.name == "I":
            continue
        if op.gate.name == "X":
            sim.x(*op.qubit_indices)
        elif op.gate.name == "Y":
            sim.y(*op.qubit_indices)
        elif op.gate.name == "Z":
            sim.z(*op.qubit_indices)
        elif op.gate.name == "CNOT":
            sim.cx(*op.qubit_indices)
        elif op.gate.name == "S_Dagger":
            sim.s_dag(*op.qubit_indices)
        elif op.gate.name == "S":
            sim.s(*op.qubit_indices)
        elif op.gate.name == "SX":
            sim.sqrt_x(*op.qubit_indices)
        elif op.gate.name == "SX_Dagger":
            sim.sqrt_x_dag(*op.qubit_indices)
        elif op.gate.name == "H":
            sim.h(*op.qubit_indices)
        elif op.gate.name == "CZ":
            sim.cz(*op.qubit_indices)
        else:
            raise ValueError(f"Gate {op.gate.name} not supported.")
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
    tableau = stim.Tableau.from_stabilizers(paulis)  # performance bottleneck is here
    sim.set_inverse_tableau(tableau.inverse())

    cliffords = []
    for vertex in vertices:
        # get vertex operations for each node in the tableau
        pauli_perm_class = vertex[0] - 1
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
            if clifford == "s":
                sim.s(i)
            elif clifford == "h":
                sim.h(i)

    return get_tableau_from_stim_simulator(sim)


def get_tableau_from_stim_simulator(sim):
    return np.column_stack(sim.current_inverse_tableau().inverse().to_numpy()[2:4])


def assert_tableaus_correspond_to_the_same_stabilizer_state(tableau_1, tableau_2):
    assert tableau_1.shape == tableau_2.shape

    n_qubits = len(tableau_2)

    # ensure that the graph tableau and the target tableau are composed
    # of paulis belonging to the same stabilizer group
    assert check_tableau_entries_commute

    # ensure that the stabilizers in the tableaus are linearly independent
    assert np.linalg.matrix_rank(tableau_1) == n_qubits
    assert np.linalg.matrix_rank(tableau_2) == n_qubits


@njit
def check_tableau_entries_commute(tableau_1, tableau_2):
    """Checks that the entries of two tableaus commute with each other.

    Args:
        tableau (np.array): tableau to check

    Returns:
        bool: true if the entries commute, false otherwise.
    """
    n_qubits = len(tableau_1) // 2

    for i in range(n_qubits):
        for j in range(i, n_qubits):
            if not commutes(tableau_1[i], tableau_2[j]):
                return False
    return True


@njit
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
@njit
def _bool_dot(x, y):
    array_and = np.logical_and(x, y)
    ans = array_and[0]
    for i in array_and[1:]:
        ans = np.logical_xor(ans, i)
    return ans


def plot_graph_state(adj, lco, input_nodes, output_nodes):
    """Converts an adjacency list to an adjacency matrix.

    Args:
      adj: The adjacency list to convert.

    Returns:
      The adjacency matrix.
    """

    # Create the adjacency matrix.
    adjacency_matrix = [[0 for _ in range(len(adj))] for _ in range(len(adj))]

    # Iterate over the adjacency list and fill in the adjacency matrix.
    for node, neighbors in enumerate(adj):
        for neighbor in neighbors:
            adjacency_matrix[node][neighbor] = 1

    graph = nx.from_numpy_matrix(np.array(adjacency_matrix))

    # Remove isolated nodes
    isolated_nodes = [
        node for node, degree in dict(graph.degree()).items() if degree == 0
    ]
    graph.remove_nodes_from(isolated_nodes)

    # Plot a graph with lco labels
    color_map = []
    for node, lco in enumerate(lco):
        if lco == 1:
            color_map.append("grey")
        elif lco == 2:
            color_map.append("cyan")
        elif lco == 3:
            color_map.append("red")
        elif lco == 4:
            color_map.append("purple")
        elif lco == 5:
            color_map.append("orange")
        elif lco == 6:
            color_map.append("yellow")
        else:
            raise ValueError(f"lco {lco} not supported.")

    # Create a legend for node colors
    node_colors = {
        "I": "grey",
        "S": "cyan",
        "H": "red",
        "HSH": "purple",
        "HS": "orange",
        "SH": "yellow",
    }
    legend_patches = [
        mpatches.Patch(color=color, label=node) for node, color in node_colors.items()
    ]

    legend_patches += [
        Line2D(
            [0],
            [0],
            marker="s",
            color="black",
            label="Input",
            markerfacecolor="w",
            markersize=10,
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="black",
            label="Intermediate",
            markerfacecolor="w",
            markersize=10,
        ),
        Line2D(
            [0],
            [0],
            marker="d",
            color="black",
            label="Output",
            markerfacecolor="w",
            markersize=10,
        ),
    ]

    plt.legend(handles=legend_patches, loc="upper right")
    for node in graph.nodes:
        if node in input_nodes:
            graph.nodes[node]["shape"] = "s"
        elif node in output_nodes:
            graph.nodes[node]["shape"] = "d"
        else:
            graph.nodes[node]["shape"] = "o"

    # Drawing the graph
    # First obtain the node positions using one of the layouts
    nodePos = nx.layout.spring_layout(graph)

    # The rest of the code here attempts to automate the whole process by
    # first determining how many different node classes (according to
    # attribute 's') exist in the node set and then repeatedly calling
    # draw_networkx_node for each. Perhaps this part can be optimized further.

    # Get all distinct node classes according to the node shape attribute
    nodeShapes = set((aShape[1]["shape"] for aShape in graph.nodes(data=True)))

    # For each node class...
    for aShape in nodeShapes:
        # ...filter and draw the subset of nodes with the same symbol in the positions
        # that are now known through the use of the layout.
        nodes_with_this_shape = [
            sNode[0]
            for sNode in filter(
                lambda x: x[1]["shape"] == aShape, graph.nodes(data=True)
            )
        ]
        colors_for_nodes_with_this_shape = [
            color_map[i] for i in nodes_with_this_shape if 0 <= i < len(color_map)
        ]

        nx.draw_networkx_nodes(
            graph,
            nodePos,
            node_shape="o",
            nodelist=nodes_with_this_shape,
            node_color=colors_for_nodes_with_this_shape,
            node_size=60,
        )
    # nx.draw_networkx_labels(graph, nodePos)

    # Finally, draw the edges between the nodes
    nx.draw_networkx_edges(graph, nodePos)

    plt.show()

    return graph
