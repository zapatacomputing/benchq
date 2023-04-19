from .quantum_program import QuantumProgram
from dataclasses import dataclass


@dataclass
class AlgorithmDescription:
    program: QuantumProgram
    n_calls: int
    failure_tolerance: float
