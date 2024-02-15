from functools import singledispatch
from typing import Union
import warnings


with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    # Numpy throws deprecation warnings due to the scipy import
    from openfermion import QubitOperator, IsingOperator

from pyLIQTR.QSP.Hamiltonian import Hamiltonian

from ..conversions import openfermion_to_pyliqtr
from orquestra.integrations.cirq.conversions import to_openfermion
from orquestra.quantum.operators import PauliTerm, PauliSum

SUPPORTED_OPERATORS = Union[
    PauliTerm, PauliSum, QubitOperator, IsingOperator, Hamiltonian
]


@singledispatch
def operator_to_pyliqtr(hamiltonian):
    raise NotImplementedError(f"Operator of type {type(hamiltonian)} not supported")


@operator_to_pyliqtr.register
def _(hamiltonian: Union[PauliTerm, PauliSum]) -> Hamiltonian:
    return openfermion_to_pyliqtr(to_openfermion(hamiltonian))


@operator_to_pyliqtr.register
def _(hamiltonian: Union[QubitOperator, IsingOperator]) -> Hamiltonian:
    return openfermion_to_pyliqtr(hamiltonian)


@operator_to_pyliqtr.register
def _(hamiltonian: Hamiltonian) -> Hamiltonian:
    return hamiltonian
