import itertools

import pytest
from orquestra.integrations.qiskit.conversions import import_from_qiskit
from orquestra.quantum.circuits import CNOT, RX, Circuit, H, S, X, Z
from qiskit import QuantumCircuit

from benchq.compilation import jl, pyliqtr_transpile_to_clifford_t


@pytest.mark.parametrize(
    "circuit",
    [  # many single qubit gates
        Circuit([gate(i) for i in range(1000) for gate in [H, X, Z, S, H] * 10]),
        # ghz state
        Circuit([H(0)] + [CNOT(0, i) for i in range(1000)]),
        # fully connected state
        Circuit(
            [H(0)] + [CNOT(i, j) for i, j in itertools.combinations(range(1000), 2)]
        ),
        # cnot chain
        Circuit([H(0)] + [CNOT(i, i + 1) for i in range(100)]),
        # rotation chain
        pyliqtr_transpile_to_clifford_t(Circuit([RX(0.237482734682374687)(0)]), 1e-10),
        # h_chain_from_qasm circuit
        pyliqtr_transpile_to_clifford_t(
            import_from_qiskit(QuantumCircuit.from_qasm_file("h_chain_circuit.qasm")),
            1e-10,
        ),
    ],
)
def test_graph_sim_mini(circuit):
    jl.run_graph_sim_mini(circuit, True)
