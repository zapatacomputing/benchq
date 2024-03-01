from dataclasses import dataclass

from ...conversions import SUPPORTED_CIRCUITS, import_circuit
from ...problem_embeddings import QuantumProgram
from .error_budget import ErrorBudget


@dataclass
class AlgorithmImplementation:
    program: QuantumProgram
    error_budget: ErrorBudget
    n_shots: int

    def from_circuit(
        circuit: SUPPORTED_CIRCUITS, error_budget: ErrorBudget, n_shots: int = 1
    ):
        program = QuantumProgram.from_circuit(import_circuit(circuit))
        return AlgorithmImplementation(program, error_budget, n_shots)

    def transpile_to_clifford_t(self):
        return AlgorithmImplementation(
            self.program.transpile_to_clifford_t(self.error_budget), self.error_budget
        )
