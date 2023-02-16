################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
import pytest
from openfermion import QubitOperator

from benchq.conversions import openfermion_to_pyliqtr, pyliqtr_to_openfermion


@pytest.mark.parametrize(
    "qubit_operator",
    [
        QubitOperator("2[Z0 Z1] - 2[X1 X2] + [Z0 X1 Y2]"),
        2j * QubitOperator("2[Z0 Z1] - 2[X1 X2]"),
        QubitOperator("[Z2 Y3]") + 2j * QubitOperator("2[Z1] - 2[X1 X2]"),
    ],
)
def test_openfermion_pyliqtr_conversion(qubit_operator):
    new_qubit_operator = pyliqtr_to_openfermion(openfermion_to_pyliqtr(qubit_operator))
    assert qubit_operator == new_qubit_operator
