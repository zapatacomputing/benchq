#####################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
from typing import List

from orquestra.quantum.evolution import time_evolution
from orquestra.quantum.operators._pauli_operators import PauliRepresentation

from .quantum_program import QuantumProgram


def get_trotter_circuit(hamiltonian, evolution_time, number_of_steps):
    return time_evolution(hamiltonian, time=evolution_time, n_steps=number_of_steps)


def get_trotter_program(
    hamiltonian: PauliRepresentation, evolution_time: float, number_of_steps: int
) -> QuantumProgram:
    time_per_step = evolution_time / number_of_steps
    # NOTE:
    # `trotter_order` is named badly in `time_evolution`.
    # It actually is number of trotter steps
    circuit = time_evolution(hamiltonian, time=time_per_step, n_steps=1)

    def subroutines_for_trotter(steps: int) -> List[int]:
        return [0] * steps

    return QuantumProgram(
        subroutines=[circuit],
        steps=number_of_steps,
        calculate_subroutine_sequence=subroutines_for_trotter,
    )
