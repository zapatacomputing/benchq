from benchq.data_structures import (
    SubroutineModel,
)

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
from openfermion.resource_estimates.surface_code_compilation.physical_costing import (
    _autoccz_factory_dimensions,
    _compute_autoccz_distillation_error,
    _physical_qubits_per_logical_qubit,
)
from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)
from benchq.resource_estimation.magic_state_distillation import AutoCCZDistillation


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


sc_arch = SuperconductingHardwareArchitecture()


test_distillation = AutoCCZDistillation(hardware_architecture_model=sc_arch)

test_distillation.set_requirements(failure_tolerance=1e-13)

test_distillation.run_profile()
test_distillation.print_profile()
