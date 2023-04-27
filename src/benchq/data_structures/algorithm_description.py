from dataclasses import dataclass
from typing import Union

from ..resource_estimation.graph.structs import GraphPartition
from .error_budget import ErrorBudget
from .quantum_program import QuantumProgram


@dataclass
class AlgorithmDescription:
    program: Union[QuantumProgram, GraphPartition]
    n_calls: int
    error_budget: ErrorBudget
