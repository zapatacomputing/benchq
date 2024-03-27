import warnings
from functools import singledispatch
from typing import Union

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    # Numpy throws deprecation warnings due to the scipy import
    from openfermion import QubitOperator, IsingOperator, InteractionOperator

import openfermion
from orquestra.integrations.cirq.conversions._openfermion_conversions import (
    to_openfermion,
)
from orquestra.quantum.operators import PauliSum, PauliTerm
from pyLIQTR.QSP.Hamiltonian import Hamiltonian

from ._openfermion_pyliqtr import openfermion_to_pyliqtr

SUPPORTED_OPERATORS = Union[
    PauliTerm, PauliSum, QubitOperator, IsingOperator, Hamiltonian, InteractionOperator
]


@singledispatch
def get_pyliqtr_operator(hamiltonian):
    raise NotImplementedError(f"Operator of type {type(hamiltonian)} not supported")


@get_pyliqtr_operator.register
def _(hamiltonian: Union[PauliTerm, PauliSum]) -> Hamiltonian:
    return openfermion_to_pyliqtr(to_openfermion(hamiltonian))


@get_pyliqtr_operator.register
def _(hamiltonian: Union[QubitOperator, IsingOperator]) -> Hamiltonian:
    return openfermion_to_pyliqtr(hamiltonian)


@get_pyliqtr_operator.register
def _(hamiltonian: InteractionOperator) -> Hamiltonian:
    raise NotImplementedError(
        "Method for converting InteractionOperator to Hamiltonian is unspecified. "
        "Please convert using Jordan-Wigner or Bravyi-Kitaev transformations."
    )


@get_pyliqtr_operator.register
def _(hamiltonian: Hamiltonian) -> Hamiltonian:
    return hamiltonian
