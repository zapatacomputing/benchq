from dataclasses import dataclass
from typing import Generic, TypeVar

from ...conversions import SUPPORTED_CIRCUITS, import_circuit
from ...problem_embeddings import QuantumProgram, get_program_from_circuit
from .error_budget import ErrorBudget
from .graph_partition import GraphPartition

T = TypeVar("T", QuantumProgram, GraphPartition)


@dataclass
class AlgorithmImplementation(Generic[T]):
    program: T
    error_budget: ErrorBudget
    n_shots: int

    @classmethod
    def from_circuit(
        cls, circuit: SUPPORTED_CIRCUITS, error_budget: ErrorBudget, n_shots: int = 1
    ):
        program = get_program_from_circuit(import_circuit(circuit))
        return AlgorithmImplementation(program, error_budget, n_shots)
