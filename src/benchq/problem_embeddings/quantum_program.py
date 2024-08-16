################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import time
from copy import copy
from decimal import Decimal
from typing import Callable, List, Sequence

from orquestra.quantum.circuits import Circuit, GateOperation, I, ResetOperation

from ..compilation.circuits import (
    compile_to_native_gates,
    get_num_t_gates_per_rotation,
    pyliqtr_transpile_to_clifford_t,
)


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

    @staticmethod
    def from_circuit(circuit: Circuit) -> "QuantumProgram":
        return QuantumProgram(
            [circuit], steps=1, calculate_subroutine_sequence=lambda x: [0]
        )

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

    def count_operations_in_subroutine(
        self, subroutine: int, gates: Sequence[str]
    ) -> int:
        n_gates = 0
        for op in self.subroutines[subroutine].operations:
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

    def transpile_to_clifford_t(
        self,
        transpilation_failure_tolerance: float,
    ) -> "QuantumProgram":
        tolerances = _distribute_transpilation_failure_tolerance_over_program(
            self, transpilation_failure_tolerance
        )
        circuits = [
            pyliqtr_transpile_to_clifford_t(circuit, circuit_precision=tolerance)
            for circuit, tolerance in zip(self.subroutines, tolerances)
        ]
        return self.replace_circuits(circuits)

    def get_n_t_gates_after_synthesis(self, transpilation_failure_tolerance: float):
        if self.n_rotation_gates == 0:
            return self.n_t_gates
                
        per_gate_synthesis_failure_tolerance = Decimal(transpilation_failure_tolerance) * Decimal(1 / self.n_rotation_gates)

        n_t_gates_per_rotation = get_num_t_gates_per_rotation(
            per_gate_synthesis_failure_tolerance
        )

        return self.n_t_gates + self.n_rotation_gates * n_t_gates_per_rotation

    def compile_to_native_gates(self, verbose: bool = False) -> "QuantumProgram":
        if verbose:
            print("Compiling to native gates...")
        start = time.time()
        circuits = [compile_to_native_gates(circuit) for circuit in self.subroutines]
        if verbose:
            print(f"Compiled in {time.time() - start} seconds.")
        return self.replace_circuits(circuits)

    def combine_subroutines(self) -> "QuantumProgram":
        new_circuit = Circuit()
        for i in self.subroutine_sequence:
            new_circuit += self.subroutines[i]
        return QuantumProgram(
            [new_circuit],
            steps=1,
            calculate_subroutine_sequence=lambda x: [0],
        )

    def split_into_smaller_subroutines(self, max_size: int) -> "QuantumProgram":
        max_size = int(max_size)
        new_subroutines = []
        subroutine_splits: List[List[int]] = [[] for _ in range(len(self.subroutines))]
        num_new_subroutines = 0
        n_qubits = self.subroutines[0].n_qubits
        for i, sub in enumerate(self.subroutines):
            if len(sub.operations) > max_size:
                for j in range(0, len(sub.operations), max_size):
                    new_subroutines.append(
                        Circuit(sub._operations[j : j + max_size] + [I(n_qubits - 1)])
                    )
                    subroutine_splits[i].append(
                        len(self.subroutines) - 1 + num_new_subroutines
                    )
                    num_new_subroutines += 1
            else:
                new_subroutines.append(sub)
                subroutine_splits[i] = [i]

        old_calculate_subroutine_sequence = copy(self.calculate_subroutine_sequence)

        def calculate_split_subroutine_sequence(steps: int) -> Sequence[int]:
            new_sequence = []
            for i in old_calculate_subroutine_sequence(steps):
                for j in subroutine_splits[i]:
                    new_sequence.append(j)
            return new_sequence

        return QuantumProgram(
            new_subroutines,
            steps=self.steps,
            calculate_subroutine_sequence=calculate_split_subroutine_sequence,
        )


def _distribute_transpilation_failure_tolerance_over_program(
    program: QuantumProgram, total_transpilation_failure_tolerance: float
) -> Sequence[float]:
    n_rots_per_subroutine = [
        program.count_operations_in_subroutine(i, ["RX", "RY", "RZ"])
        for i in range(len(program.subroutines))
    ]

    return (
        [0 for _ in program.subroutines]
        if program.n_rotation_gates == 0
        else [
            total_transpilation_failure_tolerance * count / program.n_rotation_gates
            for count in n_rots_per_subroutine
        ]
    )
