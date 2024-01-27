import numpy as np
from orquestra.integrations.cirq.conversions import (
    to_openfermion,  # pyright: ignore[reportPrivateImportUsage]
)
from orquestra.quantum.operators import PauliRepresentation
from pyLIQTR.QSP import gen_qsp

from ..algorithms.data_structures import AlgorithmImplementation, ErrorBudget
from ..conversions import openfermion_to_pyliqtr
from ..problem_embeddings import get_qsp_program, get_trotter_program


# TODO: This logic is copied from pyLIQTR, perhaps we want to change it to our own?
def _get_steps(tau, req_prec):
    # have tau and epsilon, backtrack in order to get steps
    steps, closeval = gen_qsp.get_steps_from_logeps(np.log(req_prec), tau, 1)
    # print(':------------------------------------------')
    # print(f': Steps = {steps}')
    while gen_qsp.getlogepsilon(tau, steps) > np.log(req_prec):
        steps += 4
    return steps


def _n_block_encodings_for_time_evolution(hamiltonian, time, failure_tolerance):
    pyliqtr_operator = openfermion_to_pyliqtr(to_openfermion(hamiltonian))

    tau = time * pyliqtr_operator.alpha
    steps = _get_steps(tau, failure_tolerance)

    # number of steps needs to be odd for QSP
    if not (steps % 2):
        steps += 1

    return int((steps - 3) // 2)


def qsp_time_evolution_algorithm(
    hamiltonian: PauliRepresentation, time: float, failure_tolerance: float
) -> AlgorithmImplementation:
    """Returns a program that implements time evolution using QSP.

    Args:
        hamiltonian: Hamiltonian defining the problem
        time: time of the evolution
        failure_tolerance: how often the algorithm can fail
    """
    n_block_encodings = _n_block_encodings_for_time_evolution(
        hamiltonian, time, failure_tolerance
    )
    program = get_qsp_program(hamiltonian, n_block_encodings, decompose_select_v=False)
    return AlgorithmImplementation(
        program, ErrorBudget.from_even_split(failure_tolerance), 1
    )


# TODO: This method of calculating number of steps is not exact.
# It doesn't take into account the prefactor coming from the Hamiltonian.
def _n_trotter_steps(evolution_time, total_trotter_error) -> int:
    return np.ceil(evolution_time / total_trotter_error)


def trotter_time_evolution_algorithm(
    hamiltonian: PauliRepresentation, time: float, failure_tolerance: float
) -> AlgorithmImplementation:
    """Returns a program that implements time evolution using 1-st order
    trotterization.

    Args:
        hamiltonian: Hamiltonian defining the problem
        time: time of the evolution
        failure_tolerance: how often the algorithm can fail
    """

    n_trotter_steps = _n_trotter_steps(time, failure_tolerance)
    program = get_trotter_program(hamiltonian, time, n_trotter_steps)
    return AlgorithmImplementation(
        program, ErrorBudget.from_even_split(failure_tolerance), 1
    )
