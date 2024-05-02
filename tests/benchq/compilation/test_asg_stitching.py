import os

import numpy as np
import pytest
import test_rbs_with_pauli_tracking  # type: ignore
from orquestra.quantum.circuits import CNOT, CZ, RZ, Circuit, H, I, S, T, X, Y, Z

from benchq.compilation.graph_states import jl
from benchq.visualization_tools.plot_graph_state import plot_graph_state

SKIP_SLOW = pytest.mark.skipif(
    os.getenv("SLOW_BENCHMARKS") is None,
    reason="Slow benchmarks can only run if SLOW_BENCHMARKS env variable is defined",
)


def check_correctness_for_stitched_circuits(
    circuit,
    asg,
    pauli_tracker,
    init,
    show_graph=False,
    show_circuit=False,
):
    if show_graph:
        plot_graph_state(asg, pauli_tracker)

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

    all_bitstrings = [
        format(i, f"0{circuit._n_qubits}b") for i in range(2**circuit._n_qubits)
    ]

    for i in range(n):
        binary_distribution[all_bitstrings[i]] = pdf[i]
    reversed_prob_density = {}
    for binary_str, probability in binary_distribution.items():
        reversed_binary_str = binary_str[::-1]  # Reverse the binary string
        reversed_prob_density[reversed_binary_str] = probability

    correct_pdf = {
        bitstring: 1.0 if bitstring == "0" * circuit._n_qubits else 0.0
        for bitstring in all_bitstrings
    }
    if reversed_prob_density != correct_pdf:
        raise Exception("Incorrect Result Detected!")


def get_graph(circuit, hyperparams, connection_type, optimization, max_num_qubits=3):
    if connection_type == "input":
        asg, pauli_tracker, _ = jl.get_rbs_graph_state_data(
            circuit,
            verbose=False,
            takes_graph_input=True,
            gives_graph_output=False,
            manually_stitchable=True,
            optimization=optimization,
            max_num_qubits=max_num_qubits,
            hyperparams=hyperparams,
            max_time=1e8,
        )
    elif connection_type == "output":
        asg, pauli_tracker, _ = jl.get_rbs_graph_state_data(
            circuit,
            verbose=False,
            takes_graph_input=False,
            gives_graph_output=True,
            manually_stitchable=True,
            optimization=optimization,
            max_num_qubits=max_num_qubits,
            hyperparams=hyperparams,
            max_time=1e8,
        )
    elif connection_type == "both":
        asg, pauli_tracker, _ = jl.get_rbs_graph_state_data(
            circuit,
            verbose=False,
            takes_graph_input=True,
            gives_graph_output=True,
            manually_stitchable=True,
            optimization=optimization,
            max_num_qubits=max_num_qubits,
            hyperparams=hyperparams,
            max_time=1e8,
        )
    elif connection_type == "neither":
        asg, pauli_tracker, _ = jl.get_rbs_graph_state_data(
            circuit,
            verbose=False,
            takes_graph_input=False,
            gives_graph_output=False,
            manually_stitchable=True,
            optimization=optimization,
            max_num_qubits=max_num_qubits,
            hyperparams=hyperparams,
            max_time=1e8,
        )
    else:
        raise ValueError(f"connection_type {connection_type} not supported.")

    return asg, pauli_tracker


def to_python(asg, pauli_tracker):
    return jl.python_asg(asg), jl.python_pauli_tracker(pauli_tracker)


ghz_circuit = Circuit([H(0), CNOT(0, 1), CNOT(0, 2)])


@SKIP_SLOW
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
    "circuit_1, circuit_2, circuit_3",
    [
        (ghz_circuit, ghz_circuit, ghz_circuit),
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
        (
            # test T gates work as expected
            Circuit(
                [
                    T.dagger(2),
                    T(2),
                    T(2),
                    X(1),
                    Z(1),
                ]
            ),
            Circuit(
                [
                    Z(1),
                    T(2),
                    CZ(1, 2),
                    Z(1),
                    Y(2),
                ]
            ),
            Circuit(
                [
                    H(1),
                    S(1),
                    S(1),
                    Z(2),
                    CZ(0, 1),
                ]
            ),
        ),
    ],
)
def test_triple_stitched_circuit_produces_correct_result(
    optimization, init, circuit_1, circuit_2, circuit_3
):
    hyperparams = jl.RbSHyperparams(3, 2, 6, 1e5, 0)

    asg_1, pauli_tracker_1 = get_graph(
        init + circuit_1, hyperparams, "output", optimization
    )
    # plot_graph_state(*to_python(asg_1, pauli_tracker_1))
    asg_2, pauli_tracker_2 = get_graph(circuit_2, hyperparams, "both", optimization)
    # plot_graph_state(*to_python(asg_2, pauli_tracker_2))
    asg_3, pauli_tracker_3 = get_graph(circuit_3, hyperparams, "input", optimization)
    # plot_graph_state(*to_python(asg_3, pauli_tracker_3))

    # combine graphs
    asg_12, pauli_tracker_12 = jl.stitch_graphs(
        asg_1, pauli_tracker_1, asg_2, pauli_tracker_2
    )
    # plot_graph_state(*to_python(asg_12, pauli_tracker_12))
    asg_123, pauli_tracker_123 = jl.stitch_graphs(
        asg_12, pauli_tracker_12, asg_3, pauli_tracker_3
    )
    # plot_graph_state(*to_python(asg_123, pauli_tracker_123))

    asg, pauli_tracker = to_python(asg_123, pauli_tracker_123)
    check_correctness_for_stitched_circuits(
        circuit_1 + circuit_2 + circuit_3,
        asg,
        pauli_tracker,
        init,
        show_graph=False,
        show_circuit=True,
    )


@pytest.mark.parametrize("optimization", ["Space", "Time", "Variable"])
@pytest.mark.parametrize(
    "circuit_1, circuit_2",
    [
        (ghz_circuit, ghz_circuit),
        (
            # test rotations work as expected
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
        ),
        (
            # test T gates work as expected
            Circuit(
                [
                    T.dagger(2),
                    T(2),
                    T(2),
                    X(1),
                    Z(1),
                ]
            ),
            Circuit(
                [
                    Z(1),
                    T(2),
                    CZ(1, 2),
                    Z(1),
                    Y(2),
                ]
            ),
        ),
    ],
)
def test_double_stitched_circuit_produces_correct_result(
    optimization, circuit_1, circuit_2
):
    hyperparams = jl.RbSHyperparams(3, 2, 6, 1e5, 0)
    init = Circuit([H(0), H(1), H(2)])

    asg_1, pauli_tracker_1 = get_graph(
        init + circuit_1, hyperparams, "output", optimization
    )
    # plot_graph_state(*to_python(asg_1, pauli_tracker_1))
    asg_2, pauli_tracker_2 = get_graph(circuit_2, hyperparams, "input", optimization)
    # plot_graph_state(*to_python(asg_2, pauli_tracker_2))

    # combine graphs
    asg_12, pauli_tracker_12 = jl.stitch_graphs(
        asg_1, pauli_tracker_1, asg_2, pauli_tracker_2
    )
    # plot_graph_state(*to_python(asg_12, pauli_tracker_12))

    asg, pauli_tracker = to_python(asg_12, pauli_tracker_12)
    check_correctness_for_stitched_circuits(
        circuit_1 + circuit_2,
        asg,
        pauli_tracker,
        init,
        show_graph=False,
        show_circuit=True,
    )


# If you run this test, it will take a long time to complete. Make sure to
# run it with the -s option so that you can see the circuits being printed
# as well as the progress of the test.
@SKIP_SLOW
def test_1000_large_random_circuits():
    for n_circuits_checked in range(1000):
        # randomize hyperparams
        teleportation_threshold = np.random.randint(1, 10)
        teleportation_depth = np.random.randint(1, 3) * 2
        min_neighbor_degree = np.random.randint(5, 20)
        hyperparams = jl.RbSHyperparams(
            teleportation_threshold, teleportation_depth, min_neighbor_degree, 1e5, 0
        )

        init = Circuit([H(0), H(1), H(2)])

        optimization = np.random.choice(["Space", "Time", "Variable"])

        n_qubits = 4
        depth = 10
        circuit_1 = test_rbs_with_pauli_tracking.generate_random_circuit(
            n_qubits, depth
        )
        circuit_2 = test_rbs_with_pauli_tracking.generate_random_circuit(
            n_qubits, depth
        )
        asg_1, pauli_tracker_1 = get_graph(
            init + circuit_1, hyperparams, "output", optimization
        )
        # plot_graph_state(*to_python(asg_1, pauli_tracker_1))
        asg_2, pauli_tracker_2 = get_graph(
            circuit_2, hyperparams, "input", optimization
        )
        # plot_graph_state(*to_python(asg_2, pauli_tracker_2))

        # combine graphs
        asg_12, pauli_tracker_12 = jl.stitch_graphs(
            asg_1, pauli_tracker_1, asg_2, pauli_tracker_2
        )
        # plot_graph_state(*to_python(asg_12, pauli_tracker_12))

        asg, pauli_tracker = to_python(asg_12, pauli_tracker_12)
        check_correctness_for_stitched_circuits(
            circuit_1 + circuit_2,
            asg,
            pauli_tracker,
            init,
            show_graph=False,
            show_circuit=True,
        )

        print(
            "\033[92m"
            + f"{n_circuits_checked} circuits checked successfully!"
            + "\033[0m"
        )
        n_circuits_checked += 1


# if __name__ == "__main__":
#     test_double_stitched_circuit_produces_correct_result(
#         "Time",
#         Circuit([H(0), CNOT(0, 1), CNOT(0, 2), CNOT(0, 3)]),
#         Circuit([H(0), CNOT(0, 1), CNOT(0, 2), CNOT(0, 3)]),
#     )
