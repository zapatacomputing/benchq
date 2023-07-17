from benchq.data_structures import SubroutineModel

from benchq.algorithms.ld_gsee import (
    get_ff_ld_gsee_max_evolution_time,
    get_ff_ld_gsee_num_circuit_repetitions,
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
        # Compute number of samples
        n_samples = get_ff_ld_gsee_num_circuit_repetitions(
            self.requirements["alpha"],
            self.requirements["energy_gap"],
            self.requirements["square_overlap"],
            self.requirements["precision"],
            self.requirements["failure_tolerance"],
        )
        self.c_time_evolution.number_of_times_called = n_samples

        # Set controlled time evolution hadamard test requirements
        hadamard_failure_rate = self.requirements["failure_tolerance"] / n_samples
        evolution_time = get_ff_ld_gsee_max_evolution_time(
            self.requirements["alpha"],
            self.requirements["energy_gap"],
            self.requirements["square_overlap"],
            self.requirements["precision"],
        )
        self.c_time_evolution.set_requirements(
            evolution_time=evolution_time,
            hamiltonian=self.requirements["hamiltonian"],
            failure_rate=hadamard_failure_rate,
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
        failure_rate,
    ):
        args = locals()
        # Clean up the args dictionary before setting requirements
        args.pop("self")
        args = {k: v for k, v in args.items() if not k.startswith("__")}
        super().set_requirements(**args)

    def populate_requirements_for_subroutines(self):
        # Compute number of samples
        n_block_encodings = 1 / self.requirements["failure_rate"]
        self.hamiltonian_block_encoding.number_of_times_called = n_block_encodings

        be_failure_rate = self.requirements["failure_rate"] / n_block_encodings
        self.hamiltonian_block_encoding.set_requirements(
            failure_rate=be_failure_rate,
        )


# Create an instance of QSPTimeEvolution
c_time_evolution = QSPTimeEvolution()

# Create an instance of LD_GSEE with QSPTimeEvolution as a task
ld_gsee = LD_GSEE(c_time_evolution=c_time_evolution)

# Set the requirements for LD_GSEE
ld_gsee.set_requirements(
    alpha=0.5,
    energy_gap=0.3,
    square_overlap=0.8,
    precision=0.001,
    failure_tolerance=0.1,
    hamiltonian="H",
)

# Run the profile
ld_gsee.run_profile()

# Print the profile
ld_gsee.print_profile()

# Count the subroutines
print(ld_gsee.count_subroutines())
