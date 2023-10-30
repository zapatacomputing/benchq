from dataclasses import dataclass
from typing import Generic, TypeVar

from orquestra.quantum.circuits import Circuit

from ..data_structures.error_budget import ErrorBudget
from ..resource_estimation.graph_estimators.graph_partition import GraphPartition
from ..data_structures.quantum_program import QuantumProgram, get_program_from_circuit

T = TypeVar("T", QuantumProgram, GraphPartition)


@dataclass
class AlgorithmImplementation(Generic[T]):
    program: T
    error_budget: ErrorBudget
    n_shots: int


def get_algorithm_implementation_from_circuit(
    circuit: Circuit, error_budget: ErrorBudget, n_calls: int = 1
):
    quantum_program = get_program_from_circuit(circuit)
    return AlgorithmImplementation(quantum_program, error_budget, n_calls)
