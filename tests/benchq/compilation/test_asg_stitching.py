from juliacall import Main as jl
import test_rbs_with_pauli_tracking
import os
import pathlib
from benchq.visualization_tools.plot_graph_state import plot_graph_state
import pytest
from benchq.compilation import icmop_to_circuit
from orquestra.quantum.circuits import Y, X, CNOT, RZ, CZ, H, Circuit, T


jl.include(
    os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        "../../../src/benchq/compilation/ruby_slippers/ruby_slippers.jl",
    ),
)


def check_correctness_for_stiched_circuits(
    circuit,
    asg,
    pauli_tracker,
    init,
    show_graph=False,
    show_circuit=False,
):
    n_qubits = 0
    for code, qubit_1, qubit_2, angle in init + circuit:
        n_qubits = max(n_qubits, qubit_1 + 1, qubit_2 + 1)

    if show_graph:
        plot_graph_state.plot_graph_state(asg, pauli_tracker)

    pdf = test_rbs_with_pauli_tracking.simulate(
        circuit,
        init,
        asg,
        pauli_tracker,
        show_circuit=show_circuit,
    )

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
        raise Exception("Incorrect Result Detected!")


def get_graph(circuit, hyperparams, connection_type, optimization):
    # # TODO: get qubit count from orq circuit
    # for code, qubit_1, qubit_2, angle in circuit:
    #     n_qubits = max(n_qubits, qubit_1 + 1, qubit_2 + 1)
    n_qubits = circuit._n_qubits

    # TODO: delete
    # jabalized_circuit = [
    #     jl.ICMOp(code, qubit_1 + 1, qubit_2 + 1, angle)
    #     for code, qubit_1, qubit_2, angle in circuit
    # ]

    if connection_type == "input":
        asg, pauli_tracker = jl.get_graph_state_data(
            circuit,
            n_qubits,
            True,
            False,
            False,
            500,
            1e8,
            optimization,
            hyperparams,
        )
    elif connection_type == "output":
        asg, pauli_tracker = jl.get_graph_state_data(
            circuit,
            n_qubits,
            False,
            True,
            False,
            500,
            1e8,
            optimization,
            hyperparams,
        )
    elif connection_type == "both":
        asg, pauli_tracker = jl.get_graph_state_data(
            circuit,
            n_qubits,
            True,
            True,
            False,
            500,
            1e8,
            optimization,
            hyperparams,
        )
    elif connection_type == "neither":
        asg, pauli_tracker = jl.get_graph_state_data(
            circuit,
            n_qubits,
            False,
            False,
            False,
            500,
            1e8,
            optimization,
            hyperparams,
        )
    else:
        raise ValueError(f"connection_type {connection_type} not supported.")

    return asg, pauli_tracker


def get_stiched_graphs(circuit_1, circuit_2, hyperparams, optimization):
    asg_1, pauli_tracker_1 = get_graph(circuit_1, hyperparams, "output", optimization)
    # plot_graph_state.plot_graph_state(*to_python(asg_1, pauli_tracker_1))

    asg_2, pauli_tracker_2 = get_graph(circuit_2, hyperparams, "both", optimization)
    # plot_graph_state.plot_graph_state(*to_python(asg_2, pauli_tracker_2))

    asg, pauli_tracker = jl.stitch_graphs(
        asg_1, pauli_tracker_1, asg_2, pauli_tracker_2
    )
    # plot_graph_state.plot_graph_state(*to_python(asg, pauli_tracker))

    asg_3, pauli_tracker_3 = get_graph(circuit_3, hyperparams, "input", optimization)
    # plot_graph_state.plot_graph_state(*to_python(asg_3, pauli_tracker_3))

    # combine graphs
    asg, pauli_tracker = jl.stitch_graphs(asg, pauli_tracker, asg_3, pauli_tracker_3)

    # plot_graph_state.plot_graph_state(*to_python(asg, pauli_tracker))

    return asg, pauli_tracker


def to_python(asg, pauli_tracker):
    return jl.python_asg(asg), jl.python_pauli_tracker(pauli_tracker)


@pytest.mark.parametrize("optimization", ["ST-Volume", "Space", "Time"])
@pytest.mark.parametrize(
    "circuit_1, circuit_2, circuit_3",
    [
        (
            Circuit(
                [
                    Y(2),
                    Y(2),
                    CNOT(1, 0),
                    X(1),
                    RZ(1.3856216182779741)(2),
                ]
            ),
            Circuit(
                [
                    RZ(3.9206180253660037)(1),
                    CZ(2, 0),
                    X(1),
                    CNOT(0, 1),
                    H(2),
                ]
            ),
            Circuit(
                [
                    X(1),
                    H(2),
                    T(1),
                    RZ(1.8024498348644822)(1),
                    X(2),
                ]
            ),
        ),
        # (
        #     # test T gates work as expected
        #     icmop_to_circuit(
        #         [
        #             (13, 2, -1, 0),
        #             (12, 2, -1, 0),
        #             (12, 2, -1, 0),
        #             (7, 1, -1, 0),
        #             (9, 1, -1, 0),
        #         ]
        #     ),
        #     icmop_to_circuit(
        #         [
        #             (9, 1, -1, 0),
        #             (12, 2, -1, 0),
        #             (11, 1, 2, 0),
        #             (9, 1, -1, 0),
        #             (8, 2, -1, 0),
        #         ]
        #     ),
        #     icmop_to_circuit(
        #         [
        #             (3, 1, -1, 0),
        #             (2, 1, -1, 0),
        #             (2, 1, -1, 0),
        #             (9, 1, -1, 0),
        #             (11, 0, 1, 0),
        #         ]
        #     ),
        # ),
    ],
)
def test_triple_stitched_circuit_produces_correct_result(
    optimization, circuit_1, circuit_2, circuit_3
):
    hyperparams = jl.RubySlippersHyperparams(3, 2, 6, 1e5, 0)

    asg_1, pauli_tracker_1 = get_graph(circuit_1, hyperparams, "output", optimization)
    # plot_graph_state.plot_graph_state(*to_python(asg_1, pauli_tracker_1))
    asg_2, pauli_tracker_2 = get_graph(circuit_2, hyperparams, "both", optimization)
    # plot_graph_state.plot_graph_state(*to_python(asg_2, pauli_tracker_2))
    asg_3, pauli_tracker_3 = get_graph(circuit_3, hyperparams, "input", optimization)
    # plot_graph_state.plot_graph_state(*to_python(asg_3, pauli_tracker_3))

    # combine graphs
    asg_12, pauli_tracker_12 = jl.stitch_graphs(
        asg_1, pauli_tracker_1, asg_2, pauli_tracker_2
    )
    # plot_graph_state.plot_graph_state(*to_python(asg, pauli_tracker))
    asg, pauli_tracker = jl.stitch_graphs(
        asg_12, pauli_tracker_12, asg_3, pauli_tracker_3
    )
    # plot_graph_state.plot_graph_state(*to_python(asg, pauli_tracker))

    asg, pauli_tracker = to_python(asg, pauli_tracker)

    check_correctness_for_stiched_circuits(
        circuit_1,
        circuit_2,
        circuit_3,
        asg,
        pauli_tracker,
        [
            (3, 0, -1, 0),
            (3, 1, -1, 0),
            (3, 2, -1, 0),
        ],
        hyperparams,
        optimization,
        show_graph=False,
        show_circuit=True,
        throw_error_on_incorrect_result=True,
    )


# @pytest.mark.parametrize("optimization", ["ST-Volume", "Space", "Time", "Variable"])
# @pytest.mark.parametrize(
#     "circuit_1, circuit_2",
#     [
#         (
#             # test rotations work as expected
#             [
#                 (8, 2, -1, 0),
#                 (8, 2, -1, 0),
#                 (11, 1, 0, 0),
#                 (7, 1, -1, 0),
#                 (14, 2, -1, 1.3856216182779741),
#             ],
#             [
#                 (14, 1, -1, 3.9206180253660037),
#                 (10, 2, 0, 0),
#                 (8, 1, -1, 0),
#                 (11, 0, 1, 0),
#                 (3, 2, -1, 0),
#             ],
#         ),
#         (
#             # test T gates work as expected
#             [
#                 (13, 2, -1, 0),
#                 (12, 2, -1, 0),
#                 (12, 2, -1, 0),
#                 (7, 1, -1, 0),
#                 (9, 1, -1, 0),
#             ],
#             [
#                 (9, 1, -1, 0),
#                 (12, 2, -1, 0),
#                 (11, 1, 2, 0),
#                 (9, 1, -1, 0),
#                 (8, 2, -1, 0),
#             ],
#         ),
#     ],
# )
# def test_double_stitched_circuit_produces_correct_result(
#     optimization, circuit_1, circuit_2
# ):
#     hyperparams = jl.RubySlippersHyperparams(3, 2, 6, 1e5, 0)

#     asg_1, pauli_tracker_1 = get_graph(circuit_1, hyperparams, "output", optimization)
#     # plot_graph_state.plot_graph_state(*to_python(asg_1, pauli_tracker_1))
#     asg_2, pauli_tracker_2 = get_graph(circuit_2, hyperparams, "both", optimization)
#     # plot_graph_state.plot_graph_state(*to_python(asg_2, pauli_tracker_2))

#     # combine graphs
#     asg, pauli_tracker = jl.stitch_graphs(
#         asg_1, pauli_tracker_1, asg_2, pauli_tracker_2
#     )
#     # plot_graph_state.plot_graph_state(*to_python(asg, pauli_tracker))

#     asg, pauli_tracker = to_python(asg, pauli_tracker)

#     check_correctness_for_stiched_circuits(
#         circuit_1,
#         circuit_2,
#         circuit_3,
#         [
#             (3, 0, -1, 0),
#             (3, 1, -1, 0),
#             (3, 2, -1, 0),
#         ],
#         hyperparams,
#         optimization,
#         show_graph=False,
#         show_circuit=True,
#         throw_error_on_incorrect_result=True,
#     )
