################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
"""
Unit tests for benchq.algorithms._qsp.
"""
import typing as t
from collections import Counter

import numpy as np
import numpy.random
import pytest
from orquestra.quantum import circuits
from orquestra.quantum.operators import PauliSum

from benchq.algorithms import _qsp


def _make_real_pauli_sum(terms_str: str) -> PauliSum:
    operator = PauliSum(terms_str)
    # Mimicks the workaround used in pqb.problem_ingestion.get_vlasov_hamiltonian
    for term in operator.terms:
        term.coefficient = term.coefficient.real

    return operator


def _gate_op_counts(circuit: circuits.Circuit) -> t.Mapping[str, int]:
    """
    Counts gate operations per gate type in the circuit.
    """
    names = [op.gate.name for op in circuit.operations]
    return Counter(names)


class TestGetQSPCircuit:
    @staticmethod
    @pytest.mark.parametrize("use_random_angles", [False, True])
    def test_example_circuit(use_random_angles: bool):
        """
        Uses values inspired by running the "qsp_vlasov.py" example.py
        """
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
        assert len(circuit.operations) == 347

        # We expect the following gate types being applied n times
        assert _gate_op_counts(circuit) == {
            "CZ": 84,
            "RX": 3,
            "RY": 188,
            "S": 8,
            "S_Dagger": 8,
            "T": 28,
            "T_Dagger": 28,
        }
