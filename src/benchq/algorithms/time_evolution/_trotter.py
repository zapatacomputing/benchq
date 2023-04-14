#####################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
import math

from orquestra.quantum.evolution import time_evolution
from orquestra.quantum.operators._pauli_operators import PauliRepresentation

from ...data_structures import QuantumProgram


# TODO: This method of calculating number of steps is not exact.
# It doesn't take into account the prefactor coming from the Hamiltonian.
def _get_n_trotter_steps(evolution_time, total_trotter_error) -> int:
    return math.ceil(evolution_time / total_trotter_error)


def get_trotter_circuit(hamiltonian, evolution_time, total_trotter_error):
    number_of_steps = _get_n_trotter_steps(evolution_time, total_trotter_error)
    return time_evolution(
        hamiltonian, time=evolution_time, trotter_order=number_of_steps
    )


def get_trotter_program(
    hamiltonian: PauliRepresentation, evolution_time: float, total_trotter_error: float
):
    number_of_steps = _get_n_trotter_steps(evolution_time, total_trotter_error)
    time_per_step = evolution_time / number_of_steps
    # NOTE:
    # `trotter_order` is named badly in `time_evolution`.
    # It actually is number of trotter steps
    circuit = time_evolution(hamiltonian, time=time_per_step, trotter_order=1)

    def subrountines_for_trotter(steps):
        return [0] * steps

    return QuantumProgram(
        subroutines=[circuit],
        steps=number_of_steps,
        calculate_subroutine_sequence=subrountines_for_trotter,
    )
