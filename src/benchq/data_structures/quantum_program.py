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
        calculate_multiplicities: Callable[[int], Sequence[int]],
    ) -> None:
        self.subroutines = subroutines
        self.steps = steps
        self.calculate_multiplicities = calculate_multiplicities

    @property
    def multiplicities(self) -> Sequence[int]:
        return self.calculate_multiplicities(self.steps)


"""
    circuit[0]
    for i in range(steps):
        circuit[1]
        circuit[2]
    for j in range(steps_2):
        circuit[3]
    circuit[1]
    circuit[0]
"""
