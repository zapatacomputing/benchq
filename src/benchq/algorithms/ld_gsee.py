################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
"""Tools for the Fourier-Filtered Low-Depth Ground State Energy Estimation (FF-LD-GSEE)
algorithm (arXiv:2209.06811v2)."""

import numpy as np

from ..data_structures import SubroutineModel


def _get_sigma(
    alpha: float, energy_gap: float, square_overlap: float, precision: float
) -> float:
    """Get the standard deviation of the Gaussian convolution function (Eq. 15 of
    arXiv:2209.06811v2).

    See get_ldgsee_num_iterations for argument descriptions.

    Returns: The standard deviation of the Gaussian convolution function.
    """
    delta = precision**alpha * energy_gap ** (1 - alpha)
    return min(
        0.9
        * delta
        / (np.sqrt(2 * np.log(9 * delta * precision ** (-1) * square_overlap ** (-1)))),
        0.2 * delta,
    )


def _get_epsilon_1(precision: float, square_overlap: float, sigma: float) -> float:
    """Get the error with respect to the convolution function (Eq. 28 of
        arXiv:2209.06811v2).

    See get_ldgsee_num_iterations for argument descriptions.

    Returns: The error with respect to the convolution function.
    """

    return 0.1 * precision * square_overlap / (np.sqrt(2 * np.pi) * sigma**3)


def get_ff_ld_gsee_max_evolution_time(
    alpha: float, energy_gap: float, square_overlap: float, precision: float
) -> float:
    """Get the maximum evolution time for the FF-LD-GSEE algorithm (Eq. 34 of
    arXiv:2209.06811v2).

    Args:
        alpha: The parameter alpha controlling the tradeoff between circuit repetitions
            and circuit depth. Zero corresponds to the minimum circuit depth, while one
            corresponds to the minimum number of circuit repetitions.
        energy_gap: The energy gap of the Hamiltonian, corresponds to Delta_true in the
            paper. Should use the same units as precision.
        square_overlap: The square overlap of the initial state with the ground state.
            Corresponds to eta in the paper.
        precision: The desired ground state energy precision. Corresponds to epsilon in
            the paper. Should use the same units as energy_gap.

    Returns: The estimated number of iterations required by the FF-LD-GSEE algorithm.
    """
    sigma = _get_sigma(alpha, energy_gap, square_overlap, precision)
    epsilon_1 = _get_epsilon_1(precision, square_overlap, sigma)
    return (
        np.pi ** (-1)
        * sigma ** (-1)
        * np.sqrt(2 * np.log(8 * np.pi ** (-1) * epsilon_1 ** (-1) * sigma ** (-2)))
    )


def get_ff_ld_gsee_num_circuit_repetitions(
    alpha: float,
    energy_gap: float,
    square_overlap: float,
    precision: float,
    failure_probability: float,
) -> float:
    """Get the number of circuit repetitions for the FF-LD-GSEE algorithm (Eqs. 52 and
    62 of arXiv:2209.06811v2).

    Args:
        alpha: The parameter alpha controlling the tradeoff between circuit repetitions
            and circuit depth. Zero corresponds to the minimum circuit depth, while one
            corresponds to the minimum number of circuit repetitions.
        energy_gap: The energy gap of the Hamiltonian, corresponds to Delta_true in the
            paper. Should use the same units as precision.
        square_overlap: The square overlap of the initial state with the ground state.
            Corresponds to eta in the paper.
        precision: The desired ground state energy precision. Corresponds to epsilon in
            the paper. Should use the same units as energy_gap.
        failure_probability: The tolerable probability of the algorithm failing due to
            sampling. Corresponds to delta in the paper. Note that this failure
            probability does not include failure due to other sources such as gate
            synthesis, quantum error correction, or distillation.

    Returns: The estimated number of circuit repetitions required by the FF-LD-GSEE
        algorithm.
    """

    sigma = _get_sigma(alpha, energy_gap, square_overlap, precision)
    epsilon_1 = _get_epsilon_1(precision, square_overlap, sigma)

    # number of grid points along the x-axis
    M = np.ceil(sigma / precision) + 1

    return (
        (16 / np.pi**2)
        * np.log(4 * M / failure_probability)
        / (sigma**4 * epsilon_1**2)
    )


class LD_GSEE(SubroutineModel):
    def __init__(
        self,
        task_name="ground_state_energy_estimation",
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
        alpha,
        energy_gap,
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
        n_samples = get_ff_ld_gsee_num_circuit_repetitions(
            self.requirements["alpha"],
            self.requirements["energy_gap"],
            self.requirements["square_overlap"],
            self.requirements["precision"],
            consumed_failure_tolerance,
        )
        self.c_time_evolution.number_of_times_called = n_samples

        # Set controlled time evolution hadamard test requirements
        # TODO: properly set this with a correct error budgeting: depends on robustness of algorithm
        hadamard_failure_tolerance = remaining_failure_tolerance
        evolution_time = get_ff_ld_gsee_max_evolution_time(
            self.requirements["alpha"],
            self.requirements["energy_gap"],
            self.requirements["square_overlap"],
            self.requirements["precision"],
        )
        self.c_time_evolution.set_requirements(
            evolution_time=evolution_time,
            hamiltonian=self.requirements["hamiltonian"],
            failure_tolerance=hadamard_failure_tolerance,
        )
