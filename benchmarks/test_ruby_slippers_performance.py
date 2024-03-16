import itertools

import pytest
from orquestra.quantum.circuits import CNOT, RX, Circuit, H, S, X, Z

from benchq.compilation.circuits import pyliqtr_transpile_to_clifford_t
from benchq.compilation.graph_states import jl


@pytest.mark.parametrize(
    "circuit",
    [
        pytest.param(
            Circuit([gate(i) for i in range(1000) for gate in [H, X, Z, S, H] * 10]),
            id="many single qubit gates",
        ),
        # ghz state
        pytest.param(
            Circuit([H(0)] + [CNOT(0, i) for i in range(100)]), id="GHZ state"
        ),
        # fully connected state
        pytest.param(
            Circuit(
                [H(0)] + [CNOT(i, j) for i, j in itertools.combinations(range(100), 2)]
            ),
            id="Fully connected state",
        ),
        # cnot chain
        pytest.param(
            Circuit([H(0)] + [CNOT(i, i + 1) for i in range(100)]), id="CNOT chain"
        ),
        # rotation chain
        pytest.param(
            pyliqtr_transpile_to_clifford_t(
                Circuit([RX(0.237482734682374687)(0)]), 1e-10
            ),
            id="rotation chain",
        ),
    ],
)
def test_ruby_slippers(benchmark, circuit):
    benchmark(jl.run_ruby_slippers, circuit)
