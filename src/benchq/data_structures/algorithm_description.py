from dataclasses import dataclass

from .quantum_program import QuantumProgram


@dataclass
class AlgorithmDescription:
    program: QuantumProgram
    n_calls: int
    failure_tolerance: float
