################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
from typing import Callable, Sequence

from orquestra.quantum.circuits import Circuit, GateOperation, ResetOperation


class QuantumProgram:
    """A quantum circuit represented as a sequence of subroutine invocations."""

    def __init__(
        self,
        subroutines: Sequence[Circuit],
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
        if not all(
            subroutine.n_qubits == subroutines[0].n_qubits for subroutine in subroutines
        ):
            raise ValueError("All subroutines must have the same number of qubits")
        self.num_data_qubits = subroutines[0].n_qubits
        self.subroutines = subroutines
        self.steps = steps
        self.calculate_subroutine_sequence = calculate_subroutine_sequence

    @property
    def multiplicities(self) -> Sequence[int]:
        mult_list = [0] * (max(self.subroutine_sequence) + 1)
        for i in self.subroutine_sequence:
            mult_list[i] += 1
        return mult_list

    @property
    def subroutine_sequence(self) -> Sequence[int]:
        return self.calculate_subroutine_sequence(self.steps)

    @property
    def full_circuit(self) -> Circuit:
        recreated_circuit = Circuit()
        for i in self.subroutine_sequence:
            recreated_circuit += self.subroutines[i]
        return recreated_circuit

    @property
    def n_rotation_gates(self) -> int:
        return self.count_operations_in_program(["RX", "RY", "RZ"])

    @property
    def n_c_gates(self) -> int:
        return self.count_operations_in_program(["CZ", "CNOT"])

    @property
    def n_t_gates(self) -> int:
        return self.count_operations_in_program(["T", "Tdag"])

    @property
    def min_n_nodes(self) -> int:
        return self.n_t_gates + self.n_rotation_gates + self.subroutines[0].n_qubits

    def count_operations_in_subroutine(self, step: int, gates: Sequence[str]) -> int:
        n_gates = 0
        for op in self.subroutines[step].operations:
            if isinstance(op, GateOperation) and op.gate.name in gates:
                n_gates += 1
            if isinstance(op, ResetOperation) and "ResetOperation" in gates:
                n_gates += 1
        return n_gates

    def count_operations_in_program(self, gates: Sequence[str]) -> int:
        n_gates_per_subroutine = [
            self.count_operations_in_subroutine(subroutine, gates)
            for subroutine in range(len(self.subroutines))
        ]

        total_gates = 0
        for step in self.calculate_subroutine_sequence(self.steps):
            total_gates += n_gates_per_subroutine[step]

        return total_gates

    def replace_circuits(self, new_circuits: Sequence[Circuit]) -> "QuantumProgram":
        return QuantumProgram(
            subroutines=new_circuits,
            steps=self.steps,
            calculate_subroutine_sequence=self.calculate_subroutine_sequence,
        )

    @staticmethod
    def from_circuit(circuit: Circuit) -> "QuantumProgram":
        return QuantumProgram(
            [circuit], steps=1, calculate_subroutine_sequence=lambda x: [0]
        )


def get_program_from_circuit(circuit: Circuit):
    return QuantumProgram(
        [circuit], steps=1, calculate_subroutine_sequence=lambda x: [0]
    )
