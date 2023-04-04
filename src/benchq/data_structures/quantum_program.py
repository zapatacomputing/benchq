################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
from typing import Callable, List, Sequence

from orquestra.quantum.circuits import Circuit


class QuantumProgram:
    """Simple structure describing a quantum program consisting of multiple circuits

    Params:
        circuits: a sequence of circuits, each representing
        steps: number of steps in the circuit.

    """

    def __init__(
        self,
        subroutines: Sequence[Circuit],
        steps: int,
        calculate_subroutine_sequence: Callable[[int], Sequence[int]],
    ) -> None:
        """An object which abbreviates repeated subcircuits within a quantum circuit.
        Each one of these subcircuits is called a subroutine and the subroutine_sequence
        is a list of indices which specify the order in which the subroutines.

        Args:
            subroutines (Sequence[Circuit]): a list of integers labeled 0 through the
                number of subroutines showing how the subroutines are ordered.
            subroutine_sequence (Sequence[int]): _description_
            steps (int): _description_
            calculate_multiplicities (Callable[[int], Sequence[int]]): _description_
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

    def replace_circuits(self, new_circuits: Sequence[Circuit]) -> "QuantumProgram":
        return QuantumProgram(
            subroutines=new_circuits,
            steps=self.steps,
            calculate_subroutine_sequence=self.calculate_subroutine_sequence
        )

def get_program_from_circuit(circuit):
    return QuantumProgram(
        [circuit], steps=1, calculate_subroutine_sequence=lambda x: [0]
    )
