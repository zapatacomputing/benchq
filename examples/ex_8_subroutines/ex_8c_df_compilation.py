import numpy as np

from benchq.data_structures import SubroutineModel

from benchq.algorithms.ld_gsee import (
    get_ff_ld_gsee_max_evolution_time,
    get_ff_ld_gsee_num_circuit_repetitions,
    LD_GSEE,
)

from benchq.algorithms.time_evolution import (
    QSPTimeEvolution,
)

from benchq.algorithms.time_evolution import _get_subnormalization
from benchq.resource_estimation.openfermion_re import (
    get_double_factorized_be_toffoli_and_qubit_cost,
    get_double_factorized_be_subnormalization,
    get_integrals_from_hamiltonian_instance,
    choose_threshold_for_df,
    _validate_eri,
)

from openfermion.resource_estimates.molecule import pyscf_to_cas
from openfermion.resource_estimates import df, sf
from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)

from scipy.optimize import minimize


class DoubleFactorizedHamiltonianBlockEncoding:
    def __init__(
        self,
        task_name="hamiltonian_block_encoding",
        requirements=None,
        linearly_combine_block_encodings=SubroutineModel(
            "linearly_combine_block_encodings"
        ),
        one_body_fermionic_block_encoding=SubroutineModel(
            "one_body_fermionic_block_encoding"
        ),
        two_body_fermionic_be=SubroutineModel("two_body_fermionic_be"),
    ):
        super().__init__(
            task_name,
            requirements,
            linearly_combine_block_encodings=linearly_combine_block_encodings,
            one_body_fermionic_block_encoding=one_body_fermionic_block_encoding,
            two_body_fermionic_be=two_body_fermionic_be,
        )

    def set_requirements(
        self,
        number_of_data_entries,
        number_of_bits,
        max_dirty_qubits,
        failure_tolerance,
    ):
        args = locals()
        # Clean up the args dictionary before setting requirements
        args.pop("self")
        args = {k: v for k, v in args.items() if not k.startswith("__")}
        super().set_requirements(**args)

    def populate_requirements_for_subroutines(self):
        # Convert Hamiltonian into integrals
        h1, eri_full = get_integrals_from_hamiltonian_instance(
            self.requirements["hamiltonian"]
        )

        # Populate one-body block encoding requirements
        # Gather one body terms
        one_body_tensor = (
            h1 - 0.5 * np.einsum("illj->ij", eri_full) + np.einsum("llij->ij", eri_full)
        )
        self.one_body_fermionic_block_encoding.requirements[
            "one_body_tensor"
        ] = one_body_tensor

        # Compute double factorization
        eri_rr, df_factors, rank, Lxi = df.factorize(eri_full, threshold)

        # linearly_combine_be.requirements["BEs"] = [one_particle, two_particle]
        two_body_fermionic_be.requirements["hamiltonian"] = self.requirements[
            "hamiltonian"
        ]


class OneElectronBlockEncoding(SubroutineModel):
    def __init__(
        self,
        task_name="one_body_fermionic_block_encoding",
        requirements=None,
        toffoli_gate=SubroutineModel("toffoli_gate"),
        multiplexed_phase_rotation=SubroutineModel("multiplexed_phase_rotation"),
        state_preparation=SubroutineModel("state_preparation"),
    ):
        super().__init__(task_name, requirements, toffoli_gate=toffoli_gate)
        self.multiplexed_phase_rotation = multiplexed_phase_rotation
        self.state_preparation = state_preparation

    def set_requirements(
        self,
        one_body_tensor,
        failure_tolerance,
    ):
        args = locals()
        args.pop("self")
        args = {k: v for k, v in args.items() if not k.startswith("__")}
        super().set_requirements(**args)

    def populate_requirements_for_subroutines(self):
        # Allocate failure tolerance
        allocation = 0.5
        consumed_failure_tolerance = allocation * self.requirements["failure_tolerance"]
        consumed_error_budget_allocation = [0.5, 0.5]
        remaining_failure_tolerance = (
            self.requirements["failure_tolerance"] - consumed_failure_tolerance
        )

        # Set subroutine error budget allocation (TODO: un-hardcode this)
        subroutine_error_budget_allocation = [0.5, 0.5]

        # Get info needed for one electron block encoding compilation
        number_of_orbitals = self.one_body_tensor.shape[0]

        # Set number of phase rotations
        eigenvalues, _ = np.linalg.eigh(self.requirements["one_body_tensor"])
        number_of_eigenvectors = len(eigenvalues)

        # Calculate bits of precision for angles
        multiplex_angle_precision_error = (
            consumed_error_budget_allocation[0] * consumed_failure_tolerance
        )
        bits_of_precision_for_angles = np.ceil(
            5.152
            + np.log2(np.pi * number_of_orbitals / (multiplex_angle_precision_error))
        )

        self.multiplexed_phase_rotation.set_requirements(
            number_of_multiplexed_phase_rotations=number_of_orbitals,
            number_of_used_phase_rotations=number_of_eigenvectors,
            bits_of_precision_for_angles=bits_of_precision_for_angles,
            failure_tolerance=subroutine_error_budget_allocation[0]
            * consumed_failure_tolerance,
        )
        self.multiplexed_phase_rotation.number_of_times_called = 1

        # State preparation
        # Calculate bits of precision for state preparation coefficients
        state_prep_precision_error = (
            consumed_error_budget_allocation[1] * consumed_failure_tolerance
        )
        state_prep_coefficients_bits_of_precision = np.ceil(
            2.5 * np.log2(1 / state_prep_precision_error)
        )

        number_of_data_entries = number_of_used_phase_rotations
        # Use optimal value suggested in paper
        max_dirty_qubits = np.sqrt(
            number_of_used_phase_rotations
            / ((number_of_multiplexed_phase_rotations / 4) * number_of_bits)
        )

        # Set number of data entries for state preparation
        max_state_prep_dirty_qubits = (
            max_multiplex_dirty_qubits
            + num_orbitals * (2 + multiplex_bits_of_precision),
        )
        self.state_preparation.set_requirements(
            number_of_coefficients=number_of_eigenvectors,
            # Come back to this:
            bits_of_precision=state_prep_coefficients_bits_of_precision,
            max_dirty_qubits=max_state_prep_dirty_qubits,
            failure_tolerance=subroutine_error_budget_allocation[1]
            * remaining_failure_tolerance,
        )
        self.state_preparation.number_of_times_called = 2


def compute_eigendecomposition_of_one_body_tensor(h1, eri_full):
    """Compute eigendecomposition of one body tensor for Hamiltonian
    according to DF method of von Burg, et al.

    Args:
        h1: Matrix elements of the one-body operator that includes kinetic
            energy operator and electorn-nuclear Coulomb operator.
        eri: Four-dimensional array containing electron-repulsion
            integrals.

    Returns:
        eigenvalues: eigenvalues for the one body tensor
    """
    one_body_tensor = (
        h1 - 0.5 * np.einsum("illj->ij", eri_full) + np.einsum("llij->ij", eri_full)
    )
    eigenvalues, _ = np.linalg.eigh(one_body_tensor)
    return eigenvalues


class MultiplexedPhaseRotations(SubroutineModel):
    def __init__(
        self,
        task_name="multiplexed_phase_rotations",
        requirements=None,
        data_lookup=SubroutineModel("data_lookup"),
        data_lookup_uncompute=SubroutineModel("data_lookup_uncompute"),
        arbitrary_rotation_gate=SubroutineModel("arbitrary_rotation_gate"),
        controlled_swap=SubroutineModel("controlled_swap"),
    ):
        super().__init__(
            task_name,
            requirements,
            data_lookup=data_lookup,
            data_lookup_uncompute=data_lookup_uncompute,
            arbitrary_rotation_gate=arbitrary_rotation_gate,
            controlled_swap=controlled_swap,
        )

    def set_requirements(
        self,
        number_of_multiplexed_phase_rotations,
        number_of_used_phase_rotations,
        bits_of_precision_for_angles,
        failure_tolerance,
    ):
        args = locals()
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

        # Set subroutine error budget allocation (TODO: un-hardcode this)
        subroutine_error_budget_allocation = [0.8, 0.1, 0.1]

        number_of_multiplexed_phase_rotations = self.requirements[
            "number_of_multiplexed_phase_rotations"
        ]
        number_of_used_phase_rotations = self.requirements[
            "number_of_used_phase_rotations"
        ]
        bits_of_precision_for_angles = self.requirements["bits_of_precision_for_angles"]

        # Set requirements and number of times called for each subroutine

        # Data lookup
        data_lookup_failure_tolerance = (
            subroutine_error_budget_allocation[0] * remaining_failure_tolerance
        )
        # Data lookup compute
        # Use optimal values suggested in paper
        max_compute_dirty_qubits = np.sqrt(
            number_of_used_phase_rotations
            / (
                (number_of_multiplexed_phase_rotations / 4)
                * bits_of_precision_for_angles
            )
        )

        data_lookup_compute_failure_tolerance = 0.5 * data_lookup_failure_tolerance

        self.data_lookup.set_requirements(
            number_of_data_entries=number_of_used_phase_rotations,
            number_of_bits=bits_of_precision_for_angles,
            max_compute_dirty_qubits=max_compute_dirty_qubits,
            failure_tolerance=data_lookup_compute_failure_tolerance,
        )
        self.data_lookup.number_of_times_called = 1

        # Data lookup uncompute

        max_uncompute_dirty_qubits = (
            max_compute_dirty_qubits
            * (number_of_multiplexed_phase_rotations / 4)
            * bits_of_precision_for_angles
        )
        data_lookup_uncompute_failure_tolerance = (
            data_lookup_failure_tolerance - data_lookup_compute_failure_tolerance
        )

        self.data_lookup_uncompute.set_requirements(
            number_of_data_entries=number_of_used_phase_rotations,
            number_of_bits=bits_of_precision_for_angles,
            max_uncompute_dirty_qubits=max_uncompute_dirty_qubits,
            failure_tolerance=data_lookup_uncompute_failure_tolerance,
        )
        self.data_lookup_uncompute.number_of_times_called = 1

        # Rotation gate
        self.arbitrary_rotation_gate.set_requirements(
            failure_tolerance=subroutine_error_budget_allocation[1]
            * remaining_failure_tolerance
        )
        self.arbitrary_rotation_gate.number_of_times_called = (
            number_of_multiplexed_phase_rotations * bits_of_precision_for_angles
        )

        # Controlled swap
        self.controlled_swap.set_requirements(
            failure_tolerance=subroutine_error_budget_allocation[2]
            * remaining_failure_tolerance
        )
        self.controlled_swap.number_of_times_called = (
            number_of_multiplexed_phase_rotations / 2
        )


class DataLookup(SubroutineModel):
    def __init__(
        self,
        task_name="data_lookup",
        requirements=None,
        toffoli_gate=SubroutineModel("toffoli_gate"),
        rotation_gate=SubroutineModel("rotation_gate"),
        clifford_gate=SubroutineModel("clifford_gate"),
    ):
        super().__init__(
            task_name,
            requirements,
            toffoli_gate=toffoli_gate,
            rotation_gate=rotation_gate,
            clifford_gate=clifford_gate,
        )

    def set_requirements(
        self,
        number_of_data_entries,
        number_of_bits,
        max_dirty_qubits,
        failure_tolerance,
    ):
        args = locals()
        # Clean up the args dictionary before setting requirements
        args.pop("self")
        args = {k: v for k, v in args.items() if not k.startswith("__")}
        super().set_requirements(**args)

    def populate_requirements_for_subroutines(self):
        # Compute the cost of the data lookup
        optimal_toffoli_count = self.minimize_toffoli_count(
            self.requirements["number_of_data_entries"],
            self.requirements["number_of_bits"],
            self.requirements["max_dirty_qubits"],
        )
        toffoli_cost = optimal_toffoli_count
        rotation_cost = 1  # As mentioned in the lemma
        clifford_cost = (
            self.requirements["number_of_data_entries"]
            * self.requirements["number_of_bits"]
        )

        # Fill number of times called
        self.toffoli_gate.number_of_times_called = toffoli_cost
        self.rotation_gate.number_of_times_called = rotation_cost
        self.clifford_gate.number_of_times_called = clifford_cost

        # Fill other requirements
        self.toffoli_gate.requirements["failure_tolerance"] = (
            self.requirements["failure_tolerance"] / toffoli_cost
        )
        self.rotation_gate.requirements["failure_tolerance"] = (
            self.requirements["failure_tolerance"] / rotation_cost
        )
        self.clifford_gate.requirements["failure_tolerance"] = (
            self.requirements["failure_tolerance"] / clifford_cost
        )

    @staticmethod
    def toffoli_cost(lambda_prime, number_of_data_entries, number_of_bits):
        # Compute the cost of Toffoli gates for the given lambda_prime
        return (
            number_of_data_entries / (1 + lambda_prime) + number_of_bits * lambda_prime
        )

    def minimize_toffoli_count(
        self, number_of_data_entries, number_of_bits, max_dirty_qubits
    ):
        # Define the bounds for lambda_prime
        bounds = [(0, max_dirty_qubits)]
        # Initial guess for lambda_prime
        initial_guess = [max_dirty_qubits / 2]

        # Use scipy's minimize function to find the lambda_prime that minimizes toffoli_cost
        result = minimize(
            self.toffoli_cost,
            initial_guess,
            args=(number_of_data_entries, number_of_bits),
            bounds=bounds,
        )
        # Return the optimal number of Toffoli gates
        return result.fun


class DataLookupUncompute(SubroutineModel):
    def __init__(
        self,
        task_name="data_lookup",
        requirements=None,
        toffoli_gate=SubroutineModel("toffoli_gate"),
        rotation_gate=SubroutineModel("rotation_gate"),
        clifford_gate=SubroutineModel("clifford_gate"),
    ):
        super().__init__(
            task_name,
            requirements,
            toffoli_gate=toffoli_gate,
            rotation_gate=rotation_gate,
            clifford_gate=clifford_gate,
        )

    def set_requirements(
        self,
        number_of_data_entries,
        number_of_bits,
        max_dirty_qubits,
        failure_tolerance,
    ):
        args = locals()
        # Clean up the args dictionary before setting requirements
        args.pop("self")
        args = {k: v for k, v in args.items() if not k.startswith("__")}
        super().set_requirements(**args)

    def populate_requirements_for_subroutines(self):
        # Compute the cost of the data lookup
        optimal_toffoli_count = self.minimize_toffoli_count(
            self.requirements["number_of_data_entries"],
            self.requirements["number_of_bits"],
            self.requirements["max_dirty_qubits"],
        )
        toffoli_cost = optimal_toffoli_count
        rotation_cost = 1  # As mentioned in the lemma
        clifford_cost = (
            self.requirements["number_of_data_entries"]
            * self.requirements["number_of_bits"]
        )

        # Fill number of times called
        self.toffoli_gate.number_of_times_called = toffoli_cost
        self.rotation_gate.number_of_times_called = rotation_cost
        self.clifford_gate.number_of_times_called = clifford_cost

        # Fill other requirements
        self.toffoli_gate.requirements["failure_tolerance"] = (
            self.requirements["failure_tolerance"] / toffoli_cost
        )
        self.rotation_gate.requirements["failure_tolerance"] = (
            self.requirements["failure_tolerance"] / rotation_cost
        )
        self.clifford_gate.requirements["failure_tolerance"] = (
            self.requirements["failure_tolerance"] / clifford_cost
        )

    @staticmethod
    def toffoli_cost(lambda_prime, number_of_data_entries, number_of_bits):
        # Compute the cost of Toffoli gates for the given lambda_prime
        # Note: the Toffoli cost of uncompute differs from the cost of compute
        return number_of_data_entries / (1 + lambda_prime) + lambda_prime

    def minimize_toffoli_count(
        self, number_of_data_entries, number_of_bits, max_dirty_qubits
    ):
        # Define the bounds for lambda_prime
        bounds = [(0, max_dirty_qubits)]
        # Initial guess for lambda_prime
        initial_guess = [max_dirty_qubits / 2]

        # Use scipy's minimize function to find the lambda_prime that minimizes toffoli_cost
        result = minimize(
            self.toffoli_cost,
            initial_guess,
            args=(number_of_data_entries, number_of_bits),
            bounds=bounds,
        )
        # Return the optimal number of Toffoli gates
        return result.fun


class GridSynth(SubroutineModel):
    def __init__(
        self,
        task_name="arbitrary_rotation_gate",
        requirements=None,
        t_gate=SubroutineModel("t_gate"),
        clifford_gate=SubroutineModel("clifford_gate"),
    ):
        super().__init__(
            task_name, requirements, t_gate=t_gate, clifford_gate=clifford_gate
        )

    def set_requirements(self, failure_tolerance):
        args = locals()
        args.pop("self")
        args = {k: v for k, v in args.items() if not k.startswith("__")}
        super().set_requirements(**args)

    def populate_requirements_for_subroutines(self):
        failure_tolerance = self.requirements["failure_tolerance"]

        # From https://arxiv.org/abs/1403.2975 and Euler decomposition
        number_of_euler_angles = 3
        t_gate_cost_of_z_rotation = 3 * np.log2(1 / failure_tolerance)
        t_gate_cost_estimate = number_of_euler_angles * t_gate_cost_of_z_rotation

        # Set requirements for subroutines
        # TODO: proper error budgeting
        self.t_gate.set_requirements(failure_tolerance=failure_tolerance)
        self.clifford_gate.set_requirements(failure_tolerance=failure_tolerance)

        # Estimate the number of times T gates are called
        self.t_gate.number_of_times_called = t_gate_cost_estimate

        # Using a rough empirically checked guess from example here: https://www.mathstat.dal.ca/~selinger/newsynth/
        self.clifford_gate.number_of_times_called = 1.5 * t_gate_cost_estimate


class ControlledSwap(SubroutineModel):
    def __init__(
        self,
        task_name="controlled_swap",
        requirements=None,
        toffoli_gate=SubroutineModel("toffoli_gate"),
        clifford_gate=SubroutineModel("clifford_gate"),
    ):
        super().__init__(
            task_name,
            requirements,
            toffoli_gate=toffoli_gate,
            clifford_gate=clifford_gate,
        )

    def set_requirements(self, failure_tolerance):
        args = locals()
        args.pop("self")
        args = {k: v for k, v in args.items() if not k.startswith("__")}
        super().set_requirements(**args)

    def populate_requirements_for_subroutines(self):
        toffoli_gate_cost = 1
        clifford_gate_cost = 2

        self.toffoli_gate.number_of_times_called = toffoli_gate_cost
        self.clifford_gate.number_of_times_called = clifford_gate_cost

        self.toffoli_gate.set_requirements(
            failure_tolerance=self.requirements["failure_tolerance"] / toffoli_gate_cost
        )
        self.clifford_gate.set_requirements(
            failure_tolerance=self.requirements["failure_tolerance"]
            / clifford_gate_cost
        )


class StatePreparationWithGarbage(SubroutineModel):
    def __init__(
        self,
        task_name="state_preparation",
        requirements=None,
        data_lookup=SubroutineModel("data_lookup"),
        toffoli_gate=SubroutineModel("toffoli_gate"),
        arbitrary_rotation_gate=SubroutineModel("arbitrary_rotation_gate"),
        clifford_gate=SubroutineModel("clifford_gate"),
    ):
        super().__init__(
            task_name,
            requirements,
            data_lookup=data_lookup,
            toffoli_gate=toffoli_gate,
            arbitrary_rotation_gate=arbitrary_rotation_gate,
            clifford_gate=clifford_gate,
        )

    def set_requirements(
        self,
        number_of_coefficients,
        bits_of_precision,
        max_dirty_qubits,
        failure_tolerance,
    ):
        args = locals()
        args.pop("self")
        args = {k: v for k, v in args.items() if not k.startswith("__")}
        super().set_requirements(**args)

    def populate_requirements_for_subroutines(self):
        # Allocate failure tolerance: state preparation itself consumes no error budget
        allocation = 0.0
        consumed_failure_tolerance = allocation * self.requirements["failure_tolerance"]
        remaining_failure_tolerance = (
            self.requirements["failure_tolerance"] - consumed_failure_tolerance
        )

        subroutine_error_budget_allocation = [0.6, 0.2, 0.1, 0.1]

        number_of_coefficients = self.requirements["number_of_coefficients"]
        bits_of_precision = self.requirements["bits_of_precision"]
        max_dirty_qubits = self.requirements["max_dirty_qubits"]

        # Data lookup
        self.data_lookup.number_of_times_called = 1
        self.data_lookup.set_requirements(
            number_of_data_entries=number_of_coefficients,
            number_of_bits=np.ceil(np.log2(number_of_coefficients)) + bits_of_precision,
            max_dirty_qubits=max_dirty_qubits,
            failure_tolerance=subroutine_error_budget_allocation[0]
            * remaining_failure_tolerance,
        )

        # Toffoli gates
        number_of_toffoli_gates = bits_of_precision + np.ceil(
            np.log2(number_of_coefficients)
        )
        self.toffoli_gate.number_of_times_called = number_of_toffoli_gates
        self.toffoli_gate.set_requirements(
            failure_tolerance=subroutine_error_budget_allocation[1]
            * remaining_failure_tolerance
            / number_of_toffoli_gates
        )

        # Arbitrary single-qubit rotations
        self.arbitrary_rotation_gate.number_of_times_called = 1
        self.arbitrary_rotation_gate.set_requirements(
            failure_tolerance=subroutine_error_budget_allocation[2]
            * remaining_failure_tolerance
        )

        # Clifford gates
        clifford_count = number_of_coefficients * bits_of_precision
        self.clifford_gate.number_of_times_called = clifford_count
        self.clifford_gate.set_requirements(
            failure_tolerance=subroutine_error_budget_allocation[3]
            * remaining_failure_tolerance
            / clifford_count
        )


# # Create an instance of DataLookup
# one_electron_be = OneElectronBlockEncoding()

# # Set the requirements for the data lookup
# one_electron_be.set_requirements(
#     number_of_orbitals=10, number_of_eigenvectors=8, epsilon=0.01, lambda_value=20
# )

# # Populate the requirements for the subroutines
# one_electron_be.run_profile()

# one_electron_be.print_profile()

# gs = GridSynth()
# dl = DataLookup(rotation_gate=gs)
# dlu = DataLookupUncompute(rotation_gate=gs)
# cs = ControlledSwap()
# mpr = MultiplexedPhaseRotations(
#     data_lookup=dl,
#     data_lookup_uncompute=dlu,
#     arbitrary_rotation_gate=gs,
#     controlled_swap=cs,
# )
# mpr.set_requirements(
#     number_of_multiplexed_phase_rotations=10,
#     number_of_used_phase_rotations=8,
#     failure_tolerance=0.001,
# )
# mpr.run_profile()
# mpr.print_profile()
# print(mpr.count_subroutines())

sp = StatePreparationWithGarbage()
sp.set_requirements(
    number_of_coefficients=10,
    bits_of_precision=5,
    max_dirty_qubits=3,
    failure_tolerance=0.001,
)
sp.run_profile()
sp.print_profile()
