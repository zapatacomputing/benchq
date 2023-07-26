import copy
from benchq.data_structures import SubroutineModel

from benchq.algorithms.ld_gsee import (
    get_ff_ld_gsee_max_evolution_time,
    get_ff_ld_gsee_num_circuit_repetitions,
    LD_GSEE,
)
from benchq.algorithms.gsee import (
    PhaseEstimationGSEE,
    StandardQuantumPhaseEstimation,
)
from benchq.algorithms.time_evolution import (
    QSPTimeEvolution,
)

from benchq.algorithms.time_evolution import _get_subnormalization
from benchq.resource_estimation.openfermion_re import (
    get_double_factorized_be_toffoli_and_qubit_cost,
    get_double_factorized_be_subnormalization,
    SFHamiltonianBlockEncoding,
    DFHamiltonianBlockEncoding,
    QubitizedQuantumPhaseEstimation,
)
from benchq.resource_estimation.magic_state_distillation import AutoCCZDistillation

from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)

import matplotlib.pyplot as plt


class SuperconductingHardwareArchitecture(SubroutineModel):
    def __init__(
        self,
        task_name="hardware_architecture_model",
        requirements=None,
    ):
        super().__init__(
            task_name,
            requirements,
        )

    def set_requirements(self, failure_tolerance):
        args = locals()
        # Clean up the args dictionary before setting requirements
        args.pop("self")
        args = {k: v for k, v in args.items() if not k.startswith("__")}
        super().set_requirements(**args)

    def populate_requirements_for_subroutines(self):
        pass

    def get_physical_error_rate(self):
        return 1e-3

    def get_cycle_time(self):
        return 1e-6


def get_hamiltonian_instance(number_of_hydrogens):
    instance = generate_hydrogen_chain_instance(number_of_hydrogens=number_of_hydrogens)
    instance.avas_atomic_orbitals = ["H 1s", "H 2s"]
    instance.avas_minao = "sto-3g"
    return instance


def generate_counts_for_hydrogen_list(hydrogen_list):
    counts_list = []

    for number_of_hydrogens in hydrogen_list:
        hydrogen_chain_instance = get_hamiltonian_instance(number_of_hydrogens)

        sc_arch = SuperconductingHardwareArchitecture()
        ccz_distillation = AutoCCZDistillation(hardware_architecture_model=sc_arch)

        # Create an instance of DFHamiltonianBlockEncoding
        df_ham_be = DFHamiltonianBlockEncoding(toffoli_gate=ccz_distillation)
        sf_ham_be = SFHamiltonianBlockEncoding()

        # Create an instance of QSPTimeEvolution
        qsp_te = QSPTimeEvolution(hamiltonian_block_encoding=df_ham_be)

        # # Create an instance of LD_GSEE with QSPTimeEvolution as a task
        ld_gsee = LD_GSEE(c_time_evolution=qsp_te)

        # Set the requirements for LD_GSEE
        ld_gsee.set_requirements(
            alpha=0.5,
            energy_gap=0.3,
            square_overlap=0.8,
            precision=0.001,
            failure_tolerance=0.1,
            hamiltonian=hydrogen_chain_instance,
        )

        # Run the profile
        ld_gsee.run_profile()

        # Print the profile
        ld_gsee.print_profile()

        # Count the subroutines
        counts_list += [ld_gsee.count_subroutines()]
        # print(ld_gsee.count_subroutines())
        # print(qsp_te.count_subroutines())
    print(counts_list)


def plot_hydrogen_resource_estimates(hydrogen_list):
    results = {}
    gsee_results = {}

    for number_of_hydrogens in hydrogen_list:
        hydrogen_chain_instance = get_hamiltonian_instance(number_of_hydrogens)

        for be_name, ham_be in [
            ("SF", SFHamiltonianBlockEncoding()),
            ("DF", DFHamiltonianBlockEncoding()),
        ]:
            ham_be2 = copy.deepcopy(ham_be)
            # Create an instance of QSPTimeEvolution with the current HamiltonianBlockEncoding
            # qubitized_qpe = QubitizedQuantumPhaseEstimation(
            #     hamiltonian_block_encoding=ham_be
            # )
            qsp_te = QSPTimeEvolution(hamiltonian_block_encoding=ham_be)
            standard_qpe = StandardQuantumPhaseEstimation(c_time_evolution=qsp_te)

            # Create an instance of GSEE with QSPTimeEvolution as a task
            gsee = PhaseEstimationGSEE(phase_estimation=standard_qpe)

            # Set the requirements for GSEE
            gsee.set_requirements(
                square_overlap=0.8,
                precision=0.001,
                failure_tolerance=0.1,
                hamiltonian=hydrogen_chain_instance,
            )

            # Create an instance of QSPTimeEvolution with the current HamiltonianBlockEncoding
            qsp_te2 = QSPTimeEvolution(hamiltonian_block_encoding=ham_be2)

            # Create an instance of LD_GSEE with QSPTimeEvolution as a task
            ld_gsee = LD_GSEE(c_time_evolution=qsp_te2)

            # Set the requirements for LD_GSEE
            ld_gsee.set_requirements(
                alpha=0,
                energy_gap=0.3,
                square_overlap=0.8,
                precision=0.001,
                failure_tolerance=0.1,
                hamiltonian=hydrogen_chain_instance,
            )

            # Run the profiles
            ld_gsee.run_profile()
            gsee.run_profile()

            # Count the subroutines
            # ld_subroutines_count = qsp_te2.count_subroutines()
            # print(ld_subroutines_count)
            # gsee_subroutines_count = qsp_te.count_subroutines()
            # print(gsee_subroutines_count)
            # # Count the subroutines
            ld_subroutines_count = ld_gsee.count_subroutines()
            gsee_subroutines_count = gsee.count_subroutines()

            # Add the number of 'toffoli_gate' operations to the results
            results[(number_of_hydrogens, be_name)] = ld_subroutines_count.get(
                "toffoli_gate", 0
            )
            gsee_results[(number_of_hydrogens, be_name)] = gsee_subroutines_count.get(
                "toffoli_gate", 0
            )

    # Prepare data for plot
    hydrogens = sorted(set(h for h, _ in results.keys()))
    sf_counts = [results[(h, "SF")] for h in hydrogens]
    df_counts = [results[(h, "DF")] for h in hydrogens]
    gsee_sf_counts = [gsee_results[(h, "SF")] for h in hydrogens]
    gsee_df_counts = [gsee_results[(h, "DF")] for h in hydrogens]

    # Create plot
    plt.scatter(
        hydrogens, sf_counts, label="LD_GSEE SFHamiltonianBlockEncoding", color="blue"
    )
    plt.scatter(
        hydrogens, df_counts, label="LD_GSEE DFHamiltonianBlockEncoding", color="red"
    )
    plt.scatter(
        hydrogens,
        gsee_sf_counts,
        label="GSEE SFHamiltonianBlockEncoding",
        color="blue",
        marker="x",
    )
    plt.scatter(
        hydrogens,
        gsee_df_counts,
        label="GSEE DFHamiltonianBlockEncoding",
        color="red",
        marker="x",
    )

    plt.xlabel("Number of Hydrogen Atoms")
    plt.ylabel("Toffoli Gate Count")
    plt.yscale("log")
    plt.legend()
    plt.title("Toffoli Gate Count vs. Number of Hydrogen Atoms")
    plt.show()


hydrogen_list = [
    7,
    8,
]
# plot_hydrogen_resource_estimates(hydrogen_list)
generate_counts_for_hydrogen_list(hydrogen_list)
