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
)

from openfermion.resource_estimates.molecule import pyscf_to_cas
from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)


def get_test_hamiltonian():
    instance = generate_hydrogen_chain_instance(8)
    instance.avas_atomic_orbitals = ["H 1s", "H 2s"]
    instance.avas_minao = "sto-3g"
    mean_field_object = instance.get_active_space_meanfield_object()
    h1, eri_full, _, _, _ = pyscf_to_cas(mean_field_object)
    return h1, eri_full


class DFHamiltonianBlockEncoding(SubroutineModel):
    def __init__(
        self,
        task_name="hamiltonian_block_encoding",
        requirements=None,
        toffoli_gate=SubroutineModel("toffoli_gate"),
    ):
        super().__init__(task_name, requirements, toffoli_gate=toffoli_gate)

    def set_requirements(self, hamiltonian, failure_tolerance):
        args = locals()
        # Clean up the args dictionary before setting requirements
        args.pop("self")
        args = {k: v for k, v in args.items() if not k.startswith("__")}
        super().set_requirements(**args)

    def populate_requirements_for_subroutines(self):
        # self.requirements["hamiltonian"]
        h1, eri_full = get_test_hamiltonian()
        toffoli_gate_cost, _ = get_double_factorized_be_toffoli_and_qubit_cost(
            h1, eri_full, 1e-6
        )
        self.toffoli_gate.number_of_times_called = toffoli_gate_cost
        self.toffoli_gate.set_requirements(
            failure_tolerance=self.requirements["failure_tolerance"] / toffoli_gate_cost
        )

    def get_subnormalization(self):
        h1, eri_full = get_test_hamiltonian()
        return get_double_factorized_be_subnormalization(h1, eri_full, 1e-6)


# Create an instance of DFHamiltonianBlockEncoding
df_ham_be = DFHamiltonianBlockEncoding()

# Create an instance of QSPTimeEvolution
qsp_te = QSPTimeEvolution(hamiltonian_block_encoding=df_ham_be)

# Create an instance of LD_GSEE with QSPTimeEvolution as a task
ld_gsee = LD_GSEE(c_time_evolution=qsp_te)

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
