from dataclasses import dataclass
from typing import Union

from .error_budget import ErrorBudget
from .graph_partition import GraphPartition
from .quantum_program import QuantumProgram, get_program_from_circuit


@dataclass
class AlgorithmDescription:
    program: Union[QuantumProgram, GraphPartition]
    error_budget: ErrorBudget
    n_calls: int


def get_algorithm_description_from_circuit(circuit, error_budget, n_calls=1):
    quantum_program = get_program_from_circuit(circuit)
    return AlgorithmDescription(quantum_program, error_budget, n_calls)
