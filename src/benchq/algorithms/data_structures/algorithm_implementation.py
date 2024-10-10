from dataclasses import dataclass

from ...conversions import SUPPORTED_CIRCUITS, import_circuit
from ...problem_embeddings import QuantumProgram
from .error_budget import ErrorBudget


@dataclass
class AlgorithmImplementation:
    program: QuantumProgram
    error_budget: ErrorBudget
    n_shots: int

    @classmethod
    def from_circuit(
        cls, circuit: SUPPORTED_CIRCUITS, error_budget: ErrorBudget, n_shots: int = 1
    ):
        program = QuantumProgram.from_circuit(import_circuit(circuit))
        return AlgorithmImplementation(program, error_budget, n_shots)

    def transpile_to_clifford_t(self):
        return AlgorithmImplementation(
            self.program.transpile_to_clifford_t(
                self.error_budget.transpilation_failure_tolerance
            ),
            self.error_budget,
            self.n_shots,
        )

    @property
    def n_t_gates_after_transpilation(self):
        return self.program.get_n_t_gates_after_synthesis(
            self.error_budget.transpilation_failure_tolerance
        )

    def compile_to_native_gates(self, verbose: bool = False):
        return AlgorithmImplementation(
            self.program.compile_to_native_gates(verbose),
            self.error_budget,
            self.n_shots,
        )
