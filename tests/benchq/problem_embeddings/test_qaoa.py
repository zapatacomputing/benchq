################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################

from orquestra.quantum.circuits import Circuit
from orquestra.quantum.operators import PauliSum, PauliTerm

from benchq.problem_embeddings.qaoa._qaoa import get_qaoa_circuit


def test_get_qaoa_circuit_produces_correct_output_for_small_coefficeints():
    term_1 = PauliTerm("I0", -0.125)
    term_2 = PauliTerm("Z0", -0.375)
    term_3 = PauliTerm("Z1", 0.625)
    term_4 = PauliTerm("Z0 * Z1", -0.125)
    hamiltonian = PauliSum([term_1, term_2, term_3, term_4]).simplify()

    for n_layers in range(1, 4):
        circuit = get_qaoa_circuit(hamiltonian, n_layers=n_layers)

        assert isinstance(circuit, Circuit)
        assert circuit.n_qubits == 2
        assert len(circuit.operations) == 2 + 11 * n_layers

        assert circuit.operations[0].gate.name == "H"
        assert circuit.operations[0].qubit_indices == (0,)

        assert circuit.operations[1].gate.name == "H"
        assert circuit.operations[1].qubit_indices == (1,)

        for i in range(n_layers):
            assert circuit.operations[i * 11 + 2].gate.name == "RZ"
            assert circuit.operations[i * 11 + 2].qubit_indices == (0,)

            assert circuit.operations[i * 11 + 3].gate.name == "RZ"
            assert circuit.operations[i * 11 + 3].qubit_indices == (1,)

            assert circuit.operations[i * 11 + 4].gate.name == "CNOT"
            assert circuit.operations[i * 11 + 4].qubit_indices == (0, 1)

            assert circuit.operations[i * 11 + 5].gate.name == "RZ"
            assert circuit.operations[i * 11 + 5].qubit_indices == (1,)

            assert circuit.operations[i * 11 + 6].gate.name == "CNOT"
            assert circuit.operations[i * 11 + 6].qubit_indices == (0, 1)

            assert circuit.operations[i * 11 + 7].gate.name == "H"
            assert circuit.operations[i * 11 + 7].qubit_indices == (0,)

            assert circuit.operations[i * 11 + 8].gate.name == "RZ"
            assert circuit.operations[i * 11 + 8].qubit_indices == (0,)

            assert circuit.operations[i * 11 + 9].gate.name == "H"
            assert circuit.operations[i * 11 + 9].qubit_indices == (0,)

            assert circuit.operations[i * 11 + 10].gate.name == "H"
            assert circuit.operations[i * 11 + 10].qubit_indices == (1,)

            assert circuit.operations[i * 11 + 11].gate.name == "RZ"
            assert circuit.operations[i * 11 + 11].qubit_indices == (1,)

            assert circuit.operations[i * 11 + 12].gate.name == "H"
            assert circuit.operations[i * 11 + 12].qubit_indices == (1,)


def test_get_qaoa_circuit_produces_correct_output_for_medium_coefficeints():
    term_1 = PauliTerm("I0", 1.0)
    term_2 = PauliTerm("Z1", -0.5)
    term_3 = PauliTerm("Z0 * Z1", -0.5)
    hamiltonian = PauliSum([term_1, term_2, term_3]).simplify()

    for n_layers in range(1, 4):
        circuit = get_qaoa_circuit(hamiltonian, n_layers=n_layers)

        assert isinstance(circuit, Circuit)
        assert circuit.n_qubits == 2
        assert len(circuit.operations) == 2 + 10 * n_layers

        assert circuit.operations[0].gate.name == "H"
        assert circuit.operations[0].qubit_indices == (0,)

        assert circuit.operations[1].gate.name == "H"
        assert circuit.operations[1].qubit_indices == (1,)

        for i in range(n_layers):
            assert circuit.operations[i * 10 + 2].gate.name == "RZ"
            assert circuit.operations[i * 10 + 2].qubit_indices == (1,)

            assert circuit.operations[i * 10 + 3].gate.name == "CNOT"
            assert circuit.operations[i * 10 + 3].qubit_indices == (0, 1)

            assert circuit.operations[i * 10 + 4].gate.name == "RZ"
            assert circuit.operations[i * 10 + 4].qubit_indices == (1,)

            assert circuit.operations[i * 10 + 5].gate.name == "CNOT"
            assert circuit.operations[i * 10 + 5].qubit_indices == (0, 1)

            assert circuit.operations[i * 10 + 6].gate.name == "H"
            assert circuit.operations[i * 10 + 6].qubit_indices == (0,)

            assert circuit.operations[i * 10 + 7].gate.name == "RZ"
            assert circuit.operations[i * 10 + 7].qubit_indices == (0,)

            assert circuit.operations[i * 10 + 8].gate.name == "H"
            assert circuit.operations[i * 10 + 8].qubit_indices == (0,)

            assert circuit.operations[i * 10 + 9].gate.name == "H"
            assert circuit.operations[i * 10 + 9].qubit_indices == (1,)

            assert circuit.operations[i * 10 + 10].gate.name == "RZ"
            assert circuit.operations[i * 10 + 10].qubit_indices == (1,)

            assert circuit.operations[i * 10 + 11].gate.name == "H"
            assert circuit.operations[i * 10 + 11].qubit_indices == (1,)


def test_get_qaoa_circuit_produces_correct_output_for_large_coefficeints():
    term_1 = PauliTerm("I0", 1.5)
    term_2 = PauliTerm("Z0", -0.5)
    term_3 = PauliTerm("Z1", -1.0)
    hamiltonian = PauliSum([term_1, term_2, term_3]).simplify()

    for n_layers in range(1, 4):
        circuit = get_qaoa_circuit(hamiltonian, n_layers=n_layers)

        assert isinstance(circuit, Circuit)
        assert circuit.n_qubits == 2
        assert len(circuit.operations) == 2 + 8 * n_layers

        assert circuit.operations[0].gate.name == "H"
        assert circuit.operations[0].qubit_indices == (0,)

        assert circuit.operations[1].gate.name == "H"
        assert circuit.operations[1].qubit_indices == (1,)

        for i in range(n_layers):
            assert circuit.operations[i * 8 + 2].gate.name == "RZ"
            assert circuit.operations[i * 8 + 2].qubit_indices == (0,)

            assert circuit.operations[i * 8 + 3].gate.name == "RZ"
            assert circuit.operations[i * 8 + 3].qubit_indices == (1,)

            assert circuit.operations[i * 8 + 4].gate.name == "H"
            assert circuit.operations[i * 8 + 4].qubit_indices == (0,)

            assert circuit.operations[i * 8 + 5].gate.name == "RZ"
            assert circuit.operations[i * 8 + 5].qubit_indices == (0,)

            assert circuit.operations[i * 8 + 6].gate.name == "H"
            assert circuit.operations[i * 8 + 6].qubit_indices == (0,)

            assert circuit.operations[i * 8 + 7].gate.name == "H"
            assert circuit.operations[i * 8 + 7].qubit_indices == (1,)

            assert circuit.operations[i * 8 + 8].gate.name == "RZ"
            assert circuit.operations[i * 8 + 8].qubit_indices == (1,)

            assert circuit.operations[i * 8 + 9].gate.name == "H"
            assert circuit.operations[i * 8 + 9].qubit_indices == (1,)
