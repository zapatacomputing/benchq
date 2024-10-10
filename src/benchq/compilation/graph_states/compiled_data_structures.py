from dataclasses import dataclass
from decimal import Decimal
from typing import Callable, List, Sequence

from ...problem_embeddings.quantum_program import QuantumProgram
from ..circuits import get_num_t_gates_per_rotation


@dataclass
class GSCInfo:
    num_logical_qubits: int
    num_layers: int
    graph_creation_tocks_per_layer: List[int]
    t_states_per_layer: List[int]
    rotations_per_layer: List[int]

    @staticmethod
    def from_dict(data: dict) -> "GSCInfo":
        return GSCInfo(
            data["num_logical_qubits"],
            data["num_layers"],
            data["graph_creation_tocks_per_layer"],
            data["t_states_per_layer"],
            data["rotations_per_layer"],
        )


class CompiledQuantumProgram:
    """A quantum circuit represented as a sequence of subroutine invocations."""

    def __init__(
        self,
        subroutines: Sequence[GSCInfo],
        steps: int,
        calculate_subroutine_sequence: Callable[[int], Sequence[int]],
    ) -> None:
        """Initializer for the QuantumProgram class.

        Args:
            subroutines: The circuits which are used in the program. All subroutines
                must act on the same number of qubits.
            steps: The number of repetitions of the main repeated part of the circuit.
            calculate_subroutine_sequence: A function which takes the number of steps
                and returns a list containing the indices of the subroutines to be used.

        Raises:
            ValueError: If the subroutines do not all act on the same number of qubits.
        """
        self.num_logical_qubits = max(
            subroutine.num_logical_qubits for subroutine in subroutines
        )
        self.subroutines = subroutines
        self.steps = steps
        self.calculate_subroutine_sequence = calculate_subroutine_sequence

    @staticmethod
    def from_program(
        program: QuantumProgram, compiled_circuits: List[GSCInfo]
    ) -> "CompiledQuantumProgram":
        assert len(compiled_circuits) == len(program.subroutines)
        return CompiledQuantumProgram(
            compiled_circuits,
            steps=program.steps,
            calculate_subroutine_sequence=program.calculate_subroutine_sequence,
        )

    @property
    def subroutine_sequence(self) -> Sequence[int]:
        return self.calculate_subroutine_sequence(self.steps)

    @property
    def n_rotation_gates(self) -> int:
        n_rotation_gates_per_subroutine = [0] * len(self.subroutines)
        for i, compiled_circuit in enumerate(self.subroutines):
            n_rotation_gates_per_subroutine[i] = sum(
                compiled_circuit.rotations_per_layer
            )
        return sum(
            n_rotation_gates_per_subroutine[subroutine]
            for subroutine in self.subroutine_sequence
        )

    @property
    def n_t_gates(self) -> int:
        n_t_gates_per_subroutine = [0] * len(self.subroutines)
        for i, compiled_circuit in enumerate(self.subroutines):
            n_t_gates_per_subroutine[i] = sum(compiled_circuit.t_states_per_layer)
        return sum(
            n_t_gates_per_subroutine[subroutine]
            for subroutine in self.subroutine_sequence
        )

    @property
    def t_depth(self) -> int:
        """If the circuit is transpiled to a gate set containing T-gates, this
        function returns the depth of the circuit in terms of T-gates. If not,
        then it returns the depth in terms of non-clifford rotations.

        Returns:
            int: number of T-gates in the circuit.
        """
        return sum(
            self.subroutines[subroutine].num_layers
            for subroutine in self.subroutine_sequence
        )

    def get_n_t_gates_after_synthesis(self, transpilation_failure_tolerance: float):
        if self.n_rotation_gates == 0:
            return self.n_t_gates

        per_gate_synthesis_failure_tolerance = Decimal(
            transpilation_failure_tolerance
        ) * Decimal(1 / self.n_rotation_gates)

        n_t_gates_per_rotation = get_num_t_gates_per_rotation(
            per_gate_synthesis_failure_tolerance
        )

        return self.n_t_gates + self.n_rotation_gates * n_t_gates_per_rotation


class CompiledAlgorithmImplementation:
    def __init__(
        self, program: CompiledQuantumProgram, algorithm_implementation
    ) -> None:
        self.program = program
        self.n_shots = algorithm_implementation.n_shots
        self.error_budget = algorithm_implementation.error_budget
