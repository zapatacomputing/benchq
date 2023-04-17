import itertools
from pathlib import Path
import pytest
from orquestra.integrations.qiskit.conversions import import_from_qiskit
from orquestra.quantum.circuits import CNOT, RX, Circuit, H, S, X, Z
from qiskit import QuantumCircuit

from benchq.compilation import jl, pyliqtr_transpile_to_clifford_t


H_CHAIN_CIRCUIT_PATH = (
    Path(__file__).parent / "../examples/circuits/h_chain_circuit.qasm"
)

@pytest.mark.parametrize(
    "circuit",
    [
        pytest.param(
            Circuit([gate(i) for i in range(1000) for gate in [H, X, Z, S, H] * 10]),
            id="many single qubit gates"
        ),
        # ghz state
        pytest.param(
            Circuit([H(0)] + [CNOT(0, i) for i in range(100)]),
            id="GHZ state"
        ),
        # fully connected state
        pytest.param(
            Circuit(
                [H(0)] + [CNOT(i, j) for i, j in itertools.combinations(range(100), 2)]
            ),
            id="Fully connected state"
        ),
        # cnot chain
        pytest.param(
            Circuit([H(0)] + [CNOT(i, i + 1) for i in range(100)]),
            id="CNOT chain"
        ),
        # rotation chain
        pytest.param(
            pyliqtr_transpile_to_clifford_t(Circuit([RX(0.237482734682374687)(0)]), 1e-10),
            id="rotation chain"
        ),
        # h_chain_from_qasm circuit
        pytest.param(
            pyliqtr_transpile_to_clifford_t(
            import_from_qiskit(QuantumCircuit.from_qasm_file(str(H_CHAIN_CIRCUIT_PATH))),
            1e-10,
            ),
            id="h_chain_from_qasm"
        ),
    ],
)
def test_graph_sim_mini(benchmark, circuit):
    benchmark(jl.run_graph_sim_mini, circuit)
