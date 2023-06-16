################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
"""Unit tests for benchq.problem_embeddings._qsp."""
from collections import Counter
from typing import Mapping

import numpy as np
import pytest
from orquestra.quantum import circuits
from orquestra.quantum.operators import PauliSum

from benchq.problem_embeddings import _qsp


def _make_real_pauli_sum(terms_str: str) -> PauliSum:
    operator = PauliSum(terms_str)
    # Mimicks the workaround used in pqb.problem_ingestion.get_vlasov_hamiltonian
    for term in operator.terms:
        term.coefficient = term.coefficient.real

    return operator


def _gate_op_counts(circuit: circuits.Circuit) -> Mapping[str, int]:
    """Counts gate operations per gate type in the circuit."""
    names = [op.gate.name for op in circuit.operations]
    return Counter(names)


class TestGetQSPCircuit:
    @staticmethod
    @pytest.mark.parametrize("use_random_angles", [False, True])
    def test_example_circuit(use_random_angles: bool):
        """Uses values inspired by running the "qsp_vlasov.py" example.py"""
        if not use_random_angles:
            pytest.skip(
                "Skipping case for use_random_angles=True, "
                "as it takes very long time to run"
            )
        # Given
        operator = _make_real_pauli_sum("0.75*X0*X1 + 0.75*Y0*Y1")
        required_precision = 0.01
        dt = 0.1
        tmax = 5
        sclf = 1

        # We're using 'np.random.random()' inside QSP.
        np.random.seed(42)

        # When
        circuit = _qsp.get_qsp_circuit(
            operator=operator,
            required_precision=required_precision,
            dt=dt,
            tmax=tmax,
            sclf=sclf,
            use_random_angles=use_random_angles,
        )

        # Then
        # We expect this many gates being applied in the circuit
        assert len(circuit.operations) == 375

        # We expect the following gate types being applied n times
        assert _gate_op_counts(circuit) == {
            "CZ": 84,
            "RX": 3,
            "RY": 190,
            "S": 8,
            "S_Dagger": 8,
            "T": 28,
            "T_Dagger": 28,
            "X": 26,
        }


@pytest.mark.parametrize("decompose_select_v", [True, False])
def test_example_program(decompose_select_v):
    # Given
    operator = _make_real_pauli_sum("0.75*X0*X1 + 0.75*Y0*Y1")

    # We're using 'np.random.random()' inside QSP.
    np.random.seed(42)

    # When
    qsp_program = _qsp.get_qsp_program(
        operator=operator, n_block_encodings=1, decompose_select_v=decompose_select_v
    )
    circuit_from_program = qsp_program.full_circuit

    # Then
    # We expect this many gates being applied in the circuit
    assert len(circuit_from_program.operations) == 373

    # We expect the following gate types being applied n times
    assert _gate_op_counts(circuit_from_program) == {
        "CZ": 84,
        "RX": 3,
        "RY": 190,
        "S": 8,
        "S_Dagger": 8,
        "T": 28,
        "T_Dagger": 28,
        "X": 24,
    }


@pytest.mark.parametrize("n_block_encodings", [1, 2, 3])
def test_gate_count_is_the_same_for_decomposed_and_not_decomposed_selectv(
    n_block_encodings: int,
):
    operator = _make_real_pauli_sum("0.75*X0*X1 + 0.75*Y0*Y1")

    np.random.seed(42)
    program_wo_decomposition = _qsp.get_qsp_program(
        operator=operator, n_block_encodings=n_block_encodings, decompose_select_v=False
    )

    np.random.seed(42)
    program_w_decomposition = _qsp.get_qsp_program(
        operator=operator, n_block_encodings=n_block_encodings, decompose_select_v=True
    )

    assert _gate_op_counts(program_wo_decomposition.full_circuit) == _gate_op_counts(
        program_w_decomposition.full_circuit
    )
