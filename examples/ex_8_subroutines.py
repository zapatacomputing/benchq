from benchq.data_structures import SubroutineModel

from benchq.algorithms.ld_gsee import (
    get_ff_ld_gsee_max_evolution_time,
    get_ff_ld_gsee_num_circuit_repetitions,
)


class LD_GSEE(SubroutineModel):
    def __init__(
        self,
        name="ff_gsee",
        requirements=None,
        c_time_evolution_hadamard_test=SubroutineModel(
            "c_time_evolution_hadamard_test"
        ),
    ):
        super().__init__(
            name,
            requirements,
            c_time_evolution_hadamard_test=c_time_evolution_hadamard_test,
        )

    def set_requirements(
        self,
        alpha,
        energy_gap,
        square_overlap,
        precision,
        failure_probability,
        hamiltonian,
    ):
        args = locals()
        args.pop("self")
        super().set_requirements(**args)

    def populate_subroutine_profile(self):
        for i, (subroutine, count) in enumerate(self.subroutine_profile):
            if subroutine.name == "c_time_evolution_hadamard_test":
                # Compute number of samples
                n_samples = get_ff_ld_gsee_num_circuit_repetitions(
                    self.requirements["alpha"],
                    self.requirements["energy_gap"],
                    self.requirements["square_overlap"],
                    self.requirements["precision"],
                    self.requirements["failure_probability"],
                )
                self.subroutine_profile[i] = (subroutine, n_samples)

                # Set controlled time evolution hadamard test requirements
                hadamard_failure_rate = (
                    self.requirements["failure_probability"] / n_samples
                )
                evolution_time = get_ff_ld_gsee_max_evolution_time(
                    self.requirements["alpha"],
                    self.requirements["energy_gap"],
                    self.requirements["square_overlap"],
                    self.requirements["precision"],
                )
                subroutine.set_requirements(
                    evolution_time=evolution_time,
                    hamiltonian=self.requirements["hamiltonian"],
                    failure_rate=hadamard_failure_rate,
                )


class CTimeEvolutionHadamardTest(SubroutineModel):
    def __init__(
        self,
        name="c_time_evolution_hadamard_test",
        requirements=None,
        hamiltonian_block_encoding=SubroutineModel("hamiltonian_block_encoding"),
    ):
        super().__init__(
            name,
            requirements,
            hamiltonian_block_encoding=hamiltonian_block_encoding,
        )

    def set_requirements(
        self,
        evolution_time,
        hamiltonian,
        failure_rate,
    ):
        args = locals()
        args.pop("self")
        super().set_requirements(**args)

    def populate_subroutine_profile(self):
        for i, (subroutine, count) in enumerate(self.subroutine_profile):
            if subroutine.name == "hamiltonian_block_encoding":
                # Compute number of samples
                n_block_encodings = 1 / self.requirements["failure_rate"]
                self.subroutine_profile[i] = (subroutine, n_block_encodings)
                n_block_encodings
                be_failure_rate = self.requirements["failure_rate"] / n_block_encodings
                subroutine.set_requirements(
                    failure_rate=be_failure_rate,
                )


# # cliff = Subroutine("clifford_gate")
# # BE = DFBlockEncoding()


# # # Create a specific HadamardTest subroutine
my_hadamard_test = CTimeEvolutionHadamardTest(
    hamiltonian_block_encoding=SubroutineModel("hamiltonian_block_encoding"),
)


# Pass this specific HadamardTest to LD_GSEE
my_ff_gsee = LD_GSEE(c_time_evolution_hadamard_test=my_hadamard_test)
my_ff_gsee.set_requirements(
    alpha=0.5,
    energy_gap=0.2,
    square_overlap=0.1,
    precision=0.01,
    failure_probability=0.1,
    hamiltonian=None,
)
my_ff_gsee.run_profile()
my_ff_gsee.print_profile()
print(my_ff_gsee.count_subroutines())
