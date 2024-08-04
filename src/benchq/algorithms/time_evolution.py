import numpy as np
from orquestra.quantum.operators import PauliRepresentation

from pyLIQTR.phase_factors.fourier_response.fourier_response import (
    get_steps_from_logeps,
    getlogepsilon,
)
from pyLIQTR.utils.Hamiltonian import Hamiltonian


from ..algorithms.data_structures import AlgorithmImplementation, ErrorBudget

from ..problem_embeddings.qsp import (
    get_qsp_program_from_block_encoding,
)
from ..problem_embeddings.trotter import get_trotter_program

from pyLIQTR.BlockEncodings.BlockEncoding import BlockEncoding


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


def qsp_time_evolution_algorithm_from_block_encoding(
    block_encoding: BlockEncoding, evolution_time: float, failure_tolerance: float
) -> AlgorithmImplementation:
    """Returns a program that implements time evolution using QSP.

    Args:
        block_encoding: pyLIQTR block encoding defining the encoding of the Hamiltonian
        time: time of the evolution
        failure_tolerance: how often the algorithm can fail
    """

    # Allocate failure tolerance to QSP
    qsp_failure_tolerance = failure_tolerance / 2
    remaining_failure_tolerance = failure_tolerance - qsp_failure_tolerance

    program = get_qsp_program_from_block_encoding(
        block_encoding, evolution_time, qsp_failure_tolerance
    )

    return AlgorithmImplementation(
        program, ErrorBudget.from_even_split(remaining_failure_tolerance), 1
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
