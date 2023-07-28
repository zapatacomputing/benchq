import numpy as np
from orquestra.integrations.cirq.conversions import to_openfermion
from orquestra.quantum.operators import PauliRepresentation
from pyLIQTR.QSP import gen_qsp

from ..conversions import openfermion_to_pyliqtr
from ..data_structures import AlgorithmImplementation, ErrorBudget
from ..problem_embeddings import get_qsp_program, get_trotter_program
from ..data_structures import SubroutineModel


# TODO: This logic is copied from pyLIQTR, perhaps we want to change it to our own?
def _get_steps(tau, req_prec):
    # have tau and epsilon, backtrack in order to get steps
    steps, closeval = gen_qsp.get_steps_from_logeps(np.log(req_prec), tau, 1)
    # print(':------------------------------------------')
    # print(f': Steps = {steps}')
    while gen_qsp.getlogepsilon(tau, steps) > np.log(req_prec):
        steps += 4
    return steps


def _n_block_encodings_for_time_evolution(
    hamiltonian, evolution_time, failure_tolerance
):
    subnormalization = _get_subnormalization(hamiltonian)
    return _n_block_encodings_for_time_evolution_from_subnormalization(
        subnormalization, evolution_time, failure_tolerance
    )


def _get_subnormalization(hamiltonian):
    pyliqtr_operator = openfermion_to_pyliqtr(to_openfermion(hamiltonian))
    subnormalization = pyliqtr_operator.alpha
    return subnormalization


def _n_block_encodings_for_time_evolution_from_subnormalization(
    subnormalization, evolution_time, failure_tolerance
):
    tau = evolution_time * subnormalization
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
    program = get_qsp_program(hamiltonian, n_block_encodings)
    return AlgorithmImplementation(
        program, ErrorBudget.from_even_split(failure_tolerance), 1
    )


class QSPTimeEvolution(SubroutineModel):
    def __init__(
        self,
        task_name="c_time_evolution",
        requirements=None,
        hamiltonian_block_encoding=None,
    ):
        super().__init__(
            task_name,
            requirements,
            hamiltonian_block_encoding=hamiltonian_block_encoding
            if hamiltonian_block_encoding is not None
            else SubroutineModel("hamiltonian_block_encoding"),
        )

    def set_requirements(
        self,
        evolution_time,
        hamiltonian,
        failure_tolerance,
    ):
        args = locals()
        # Clean up the args dictionary before setting requirements
        args.pop("self")
        args = {k: v for k, v in args.items() if not k.startswith("__")}
        super().set_requirements(**args)

    def populate_requirements_for_subroutines(self):
        # Allocate failure tolerance
        allocation = 0.5
        consumed_failure_tolerance = allocation * self.requirements["failure_tolerance"]
        remaining_failure_tolerance = (
            self.requirements["failure_tolerance"] - consumed_failure_tolerance
        )

        # Compute subnormalization of block encoding if the get_subnormalization method is available
        if hasattr(self.hamiltonian_block_encoding, "get_subnormalization"):
            subnormalization = self.hamiltonian_block_encoding.get_subnormalization(
                self.requirements["hamiltonian"]
            )
            n_block_encodings = (
                _n_block_encodings_for_time_evolution_from_subnormalization(
                    subnormalization,
                    self.requirements["evolution_time"],
                    consumed_failure_tolerance,
                )
            )
        else:
            n_block_encodings = None
            print(
                "Warning: No subroutine for the Hamiltonian block encoding task has been provided that has a get_subnormalization method."
            )

        self.hamiltonian_block_encoding.number_of_times_called = n_block_encodings

        if n_block_encodings:
            be_failure_tolerance = remaining_failure_tolerance / n_block_encodings
        else:
            be_failure_tolerance = None
        self.hamiltonian_block_encoding.set_requirements(
            hamiltonian=self.requirements["hamiltonian"],
            failure_tolerance=be_failure_tolerance,
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
