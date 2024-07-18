import numpy as np
from orquestra.quantum.operators import PauliRepresentation
from pyLIQTR.phase_factors.fourier_response.fourier_response import (
    get_steps_from_logeps,
    getlogepsilon,
)
from pyLIQTR.utils.Hamiltonian import Hamiltonian


from ..algorithms.data_structures import AlgorithmImplementation, ErrorBudget
from ..conversions import SUPPORTED_OPERATORS, get_pyliqtr_operator
from ..problem_embeddings.qsp import get_qsp_program
from ..problem_embeddings.trotter import get_trotter_program


# TODO: This logic is copied from pyLIQTR, perhaps we want to change it to our own?
def _get_steps(tau, req_prec):
    # have tau and epsilon, backtrack in order to get steps
    steps, close_val = get_steps_from_logeps(np.log(req_prec), tau, 1)
    # print(':------------------------------------------')
    # print(f': Steps = {steps}')
    while getlogepsilon(tau, steps) > np.log(req_prec):
        steps += 4
    return steps


def _n_block_encodings_for_time_evolution(
    hamiltonian: Hamiltonian, time: float, failure_tolerance: float
):
    tau = time * hamiltonian.alpha
    steps = _get_steps(tau, failure_tolerance)

    # number of steps needs to be odd for QSP
    if not (steps % 2):
        steps += 1

    return int((steps - 3) // 2)


def qsp_time_evolution_algorithm(
    hamiltonian: SUPPORTED_OPERATORS, time: float, failure_tolerance: float
) -> AlgorithmImplementation:
    """Returns a program that implements time evolution using QSP.

    Args:
        hamiltonian: Hamiltonian defining the problem
        time: time of the evolution
        failure_tolerance: how often the algorithm can fail
    """
    pyliqtr_hamiltonian = get_pyliqtr_operator(hamiltonian)
    n_block_encodings = _n_block_encodings_for_time_evolution(
        pyliqtr_hamiltonian, time, failure_tolerance
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
