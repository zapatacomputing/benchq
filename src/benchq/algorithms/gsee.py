import warnings

import numpy as np
from orquestra.integrations.cirq.conversions import to_openfermion

from ..conversions import openfermion_to_pyliqtr
from ..data_structures import AlgorithmImplementation, ErrorBudget, SubroutineModel
from ..problem_embeddings import get_qsp_program


def _n_block_encodings(hamiltonian, precision):
    pyliqtr_operator = openfermion_to_pyliqtr(to_openfermion(hamiltonian))

    return int(np.ceil(np.pi * (pyliqtr_operator.alpha) / (precision)))


def qpe_gsee_algorithm(hamiltonian, precision, failure_tolerance):
    warnings.warn("This is experimental implementation, use at your own risk.")
    n_block_encodings = _n_block_encodings(hamiltonian, precision)
    program = get_qsp_program(hamiltonian, n_block_encodings)
    error_budget = ErrorBudget.from_even_split(failure_tolerance)
    n_calls = np.ceil(np.log(1 / error_budget.algorithm_failure_tolerance))
    return AlgorithmImplementation(program, error_budget, n_calls)


class PhaseEstimationGSEE(SubroutineModel):
    def __init__(
        self,
        task_name="ground_state_energy_estimation",
        requirements=None,
        phase_estimation=None,
    ):
        super().__init__(
            task_name,
            requirements,
            phase_estimation=phase_estimation
            if phase_estimation is not None
            else SubroutineModel("phase_estimation"),
        )

    def set_requirements(
        self,
        square_overlap,
        precision,
        failure_tolerance,
        hamiltonian,
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

        # Compute number of samples
        n_samples = (1 / self.requirements["square_overlap"]) * np.ceil(
            np.log(1 / consumed_failure_tolerance)
        )

        self.phase_estimation.number_of_times_called = n_samples

        # Set phase estimation requirements

        self.phase_estimation.set_requirements(
            precision=self.requirements["precision"],
            failure_tolerance=remaining_failure_tolerance,
            hamiltonian=self.requirements["hamiltonian"],
        )


class StandardQuantumPhaseEstimation(SubroutineModel):
    def __init__(
        self,
        task_name="phase_estimation",
        requirements=None,
        c_time_evolution=None,
    ):
        super().__init__(
            task_name,
            requirements,
            c_time_evolution=c_time_evolution
            if c_time_evolution is not None
            else SubroutineModel("c_time_evolution"),
        )

    def set_requirements(
        self,
        precision,
        failure_tolerance,
        hamiltonian,
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

        self.c_time_evolution.number_of_times_called = 1

        # Set controlled time evolution hadamard test requirements
        # TODO: properly set this with a correct error budgeting
        evolution_time = np.ceil(
            (1 + 1 / consumed_failure_tolerance) / (self.requirements["precision"] * 2)
        )
        self.c_time_evolution.set_requirements(
            evolution_time=evolution_time,
            hamiltonian=self.requirements["hamiltonian"],
            failure_tolerance=remaining_failure_tolerance,
        )
