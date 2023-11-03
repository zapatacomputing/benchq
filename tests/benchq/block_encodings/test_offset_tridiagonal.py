import numpy as np
import pytest

from benchq.problem_ingestion.block_encodings.offset_tridiagonal import (
    get_offset_tridagonal_block_encoding,
)


@pytest.mark.parametrize("n", [1, 5, 10])
def test_circuit_is_correct_size(n):
    circuit = get_offset_tridagonal_block_encoding(n, 0.15, 0.1, 0.1)
    assert circuit.n_qubits >= n


@pytest.mark.parametrize("n", [3, 4])
@pytest.mark.parametrize("a, b, c", [(0.5, 0.25, 0.25), (0, 0, 0), (0.24, 0.1, 0.15)])
def test_correct_matrix_is_produced(n, a, b, c):
    circuit = get_offset_tridagonal_block_encoding(n, a, b, c)
    a_matrix = np.diag(a * np.ones(2**n))
    b_matrix = np.diag(b * np.ones(2**n - 2), k=-2)
    c_matrix = np.diag(c * np.ones(2**n - 2), k=2)

    target_unitary = a_matrix + b_matrix + c_matrix
    test_unitary = circuit.to_unitary()

    assert np.allclose(test_unitary[: 2**n, : 2**n], target_unitary)
