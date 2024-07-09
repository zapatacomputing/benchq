import warnings
from decimal import Decimal, getcontext
from math import ceil
from typing import Iterable, Optional, Tuple

from benchq.decoder_modeling.decoder_resource_estimator import get_decoder_info

from ..algorithms.data_structures import AlgorithmImplementation
from ..compilation.circuits.pyliqtr_transpilation import get_num_t_gates_per_rotation
from ..compilation.graph_states.compiled_data_structures import (
    CompiledAlgorithmImplementation,
    CompiledQuantumProgram,
)
from ..decoder_modeling import DecoderModel
from ..magic_state_distillation import MagicStateFactory, iter_litinski_factories
from ..quantum_hardware_modeling import (
    BasicArchitectureModel,
    DetailedArchitectureModel,
)

from ..quantum_hardware_modeling.devitt_surface_code import (
    get_total_logical_failure_rate,
    logical_cell_error_rate,
    physical_qubits_per_logical_qubit,
)
from ..visualization_tools.resource_allocation import CycleAllocation
from .resource_info import GraphExtra, GraphResourceInfo, BusArchitectureResourceInfo

INITIAL_SYNTHESIS_ACCURACY = 0.0001


class GraphResourceEstimator:
    """Estimates resources needed to run an algorithm using graph state compilation.

    ATTRIBUTES:
        hw_model (BasicArchitectureModel): The hardware model to use for the estimate.
            typically, one would choose between the BASIC_SC_ARCHITECTURE_MODEL and
            BASIC_ION_TRAP_ARCHITECTURE_MODEL.
        decoder_model (Optional[DecoderModel]): The decoder model used to estimate.
            If None, no estimates on the number of decoder are provided.
        optimization (str): The optimization to use for the estimate. Either estimate
            the resources needed to run the algorithm in the shortest time possible
            ("Time") or the resources needed to run the algorithm with the smallest
            number of physical qubits ("Space").
        magic_state_factory_iterator (Optional[Iterable[MagicStateFactory]]: iterator
            over all magic_state_factories.
            to be used during estimation. If not provided (or passed None)
            litinski_factory_iterator will select magic_state_factory based
            on hw_model parameter.
    """

    def __init__(
        self,
        optimization: str = "Space",
        verbose: bool = False,
    ):
        self.optimization = optimization
        self.verbose = verbose
        getcontext().prec = 100  # need some extra precision for this calculation

    def _minimize_code_distance(
        self,
        compiled_program: CompiledQuantumProgram,
        hardware_failure_tolerance: float,
        transpilation_failure_tolerance: float,
        magic_state_factory: MagicStateFactory,
        n_t_gates_per_rotation: int,
        hw_model: BasicArchitectureModel,
        min_d: int = 3,
        max_d: int = 200,
    ) -> int:

        distillation_error_rate = Decimal(
            magic_state_factory.distilled_magic_state_error_rate
        ) * Decimal(
            compiled_program.get_n_t_gates_after_transpilation(
                transpilation_failure_tolerance
            )
        )

        if distillation_error_rate > hardware_failure_tolerance:
            return -1

        for data_and_bus_code_distance in range(min_d, max_d, 2):

            logical_architecture_resource_info = (
                self.get_bus_architecture_resource_breakdown(
                    compiled_program,
                    data_and_bus_code_distance,
                    magic_state_factory,
                    n_t_gates_per_rotation,
                )
            )

            time_allocation = self.get_cycle_allocation(
                compiled_program,
                magic_state_factory.distillation_time_in_cycles,
                n_t_gates_per_rotation,
                data_and_bus_code_distance,
            )
            num_logical_qubits = (
                logical_architecture_resource_info.num_logical_data_qubits
                + logical_architecture_resource_info.num_logical_bus_qubits
            )
            num_cycles = time_allocation.total
            st_volume_in_logical_qubit_tocks = (
                num_logical_qubits * num_cycles / data_and_bus_code_distance
            )

            ec_error_rate_at_this_distance = Decimal(
                get_total_logical_failure_rate(
                    hw_model,
                    st_volume_in_logical_qubit_tocks,
                    data_and_bus_code_distance,
                )
            )

            this_hardware_failure_rate = float(
                distillation_error_rate
                + ec_error_rate_at_this_distance
                + distillation_error_rate * ec_error_rate_at_this_distance
            )

            if this_hardware_failure_rate < hardware_failure_tolerance:
                return data_and_bus_code_distance

        return -1

    def get_bus_architecture_resource_breakdown(
        self,
        compiled_program: CompiledQuantumProgram,
        data_and_bus_code_distance: int,
        magic_state_factory: MagicStateFactory,
        n_t_gates_per_rotation: int,
    ):

        num_logical_data_qubits = (
            self.get_max_number_of_data_qubits_from_compiled_program(compiled_program)
        )

        # Qubit resource breakdowns are given by the following layouts
        # for data qubits |D|, bus qubits |B|, and magic state factories |M|.
        # The ion trap architecture is designed for each ELU to connect to at most
        # three other ELUs.

        # The two-row bus architecture with degree-three connectivity is layed out as follows:
        # |D|     |D|     ...     |D| |D| ... |D|
        #  |       |               |   |       |
        # |B|-|B|-|B|-|B|-...-|B|-|B|-|B|-...-|B|
        #      |       |       |
        #     |M|     |M|     |M|
        # there is a bus qubit for each data qubit and each magic state factory.
        # The space optimal compilation uses just one factory, while the time optimal
        # compilation uses a number of factories determined by the maximum warranted
        # parallelization of distillation.
        if self.optimization == "Space":
            num_magic_state_factories = 1
        elif self.optimization == "Time":
            num_magic_state_factories = self.get_max_parallel_distillations(
                compiled_program
            )

        # The ion trap architecture 3-neighbor constraint requires each data qubit and each magic state factory
        # to be connected to a unique bus qubit. The bus qubits are connected to each other in a chain.
        num_logical_bus_qubits = num_logical_data_qubits + num_magic_state_factories

        return BusArchitectureResourceInfo(
            num_logical_data_qubits=num_logical_data_qubits,
            num_logical_bus_qubits=num_logical_bus_qubits,
            data_and_bus_code_distance=data_and_bus_code_distance,
            num_magic_state_factories=num_magic_state_factories,
            magic_state_factory=magic_state_factory,
        )

    def get_max_parallel_distillations(self, compiled_program):
        max_parallel_distillations = 0
        for subroutine in compiled_program.subroutines:
            t_states_per_layer = subroutine.t_states_per_layer
            rotations_per_layer = subroutine.rotations_per_layer
            parallel_distillations_per_layer = [
                t_states + rotations
                for t_states, rotations in zip(t_states_per_layer, rotations_per_layer)
            ]
            max_parallel_distillations_in_subroutine = max(
                parallel_distillations_per_layer
            )
            max_parallel_distillations = max(
                max_parallel_distillations, max_parallel_distillations_in_subroutine
            )
        return max_parallel_distillations

    def get_max_number_of_data_qubits_from_compiled_program(self, compiled_program):
        max_data_qubits = 0
        for subroutine in compiled_program.subroutines:
            max_data_qubits = max(max_data_qubits, subroutine.num_logical_qubits)
        return max_data_qubits

    def get_total_number_of_physical_qubits(self, logical_architecture_resource_info):
        num_data_and_bus_physical_qubits = physical_qubits_per_logical_qubit(
            logical_architecture_resource_info.data_and_bus_code_distance
        ) * (
            logical_architecture_resource_info.num_logical_data_qubits
            + logical_architecture_resource_info.num_logical_bus_qubits
        )
        num_distillation_physical_qubits = (
            logical_architecture_resource_info.magic_state_factory.qubits
            * logical_architecture_resource_info.num_magic_state_factories
        )

        return num_data_and_bus_physical_qubits + num_distillation_physical_qubits

    def get_cycle_allocation(
        self,
        compiled_program: CompiledQuantumProgram,
        distillation_time_in_cycles: int,
        n_t_gates_per_rotation: int,
        data_and_bus_code_distance: int,
    ) -> CycleAllocation:
        time_allocation_for_each_subroutine = [
            CycleAllocation() for _ in range(len(compiled_program.subroutines))
        ]

        # Legend:
        # |Graph state->| = "Entanglement" process of graph state creation
        # |CoDTX------->| = "T measurement" process of consuming the Xth T state as a T basis measurements
        # |Distill----->| = "Distillation" process of preparing a T state on a magic state factory

        # Tocks |Tock1|Tock2|Tock3|Tock4|Tock5|Tock6|Tock7|Tock8|Tock9|Toc10|Toc11|Toc12|Toc13|
        # Stages:[1: Graph creation      ] [2: Meas1 ] [3: Distill then Meas2          ] ... [N: Distill then MeasN-1]
        # Dat1: |Graph state------------->|CoDT1----->|                     |CoDT3----->|...
        # Dat2: |Graph state------------->|CoDT2----->|                     |CoDT4----->|...
        #                                       ^                                 ^
        # Bus1: |Graph state------------->|CoDT1----->|                     |CoDT3----->|...
        # Bus2: |Graph state------------->|CoDT1----->|                     |CoDT3----->|...
        # Bus3: |Graph state------------->|CoDT2----->|                     |CoDT4----->|...
        # Bus4: |Graph state------------->|CoDT2----->|                     |CoDT4----->|...
        #                                       ^                                 ^
        # MSF1:     |Distill------------->|CoDT1----->|Distill------------->|CoDT3----->|...
        # MSF2:     |Distill------------->|CoDT2----->|Distill------------->|CoDT4----->|...

        # For space optimal, a single factory is used and distillation is done serially.
        # For time optimal, multiple factories are used and distillation is done in parallel.

        for i, subroutine in enumerate(compiled_program.subroutines):
            for layer_num, layer in enumerate(range(subroutine.num_layers)):

                cycles_per_tock = data_and_bus_code_distance

                # Check if the number of T gates and number of rotations per layer is zero
                if (
                    subroutine.t_states_per_layer[layer] == 0
                    and subroutine.rotations_per_layer[layer] == 0
                ):
                    # In this case, the layer only requires graph state preparation
                    # Log Stage 1: Graph state creation
                    time_allocation_for_each_subroutine[i].log(
                        subroutine.graph_creation_tocks_per_layer[layer]
                        * cycles_per_tock,
                        "graph state prep",
                    )

                else:
                    # If there are T gates in the layer, then the layer requires graph state preparation,
                    # distillation, and T state measurement
                    # Log Stage 1: Graph state creation
                    time_allocation_for_each_subroutine[i].log_parallelized(
                        (
                            distillation_time_in_cycles,
                            subroutine.graph_creation_tocks_per_layer[layer]
                            * cycles_per_tock,
                        ),
                        ("distillation", "graph state prep"),
                    )

                    # Log Stage 2: First T measurement
                    cycles_per_t_measurement = 2 * cycles_per_tock

                    time_allocation_for_each_subroutine[i].log(
                        cycles_per_t_measurement,
                        "T measurement",
                    )

                    # Log Stage 3: Space optimal entails serially distilling T states
                    # and a T measurement is made after each distillation, while time optimal
                    # entails distilling T states in parallel and making a T measurement after,
                    # though T gates used to synthesize a rotation are still implemented serially.

                    # Calculate the number of remaining T rounds
                    if self.optimization == "Space":
                        number_of_remaining_t_rounds = (
                            subroutine.t_states_per_layer[layer]
                            + n_t_gates_per_rotation
                            * subroutine.rotations_per_layer[layer]
                        ) - 1
                    elif self.optimization == "Time":
                        number_of_remaining_t_rounds = (
                            n_t_gates_per_rotation
                            * subroutine.rotations_per_layer[layer]
                        ) - 1
                    else:
                        raise ValueError(
                            f"Unknown optimization: {self.optimization}. "
                            "Should be either 'Time' or 'Space'."
                        )

                    # Loop over remaining T rounds
                    for _ in range(number_of_remaining_t_rounds):
                        time_allocation_for_each_subroutine[i].log(
                            distillation_time_in_cycles,
                            "distillation",
                        )
                        time_allocation_for_each_subroutine[i].log(
                            cycles_per_t_measurement,
                            "T measurement",
                        )

        # Then initialize cycle allocation object and populate with data
        cycle_allocation = CycleAllocation()
        for subroutine_index in compiled_program.subroutine_sequence:
            cycle_allocation += time_allocation_for_each_subroutine[subroutine_index]
        return cycle_allocation

    def estimate_resources_from_compiled_implementation(
        self,
        compiled_implementation: CompiledAlgorithmImplementation,
        hw_model: BasicArchitectureModel,
        decoder_model: Optional[DecoderModel] = None,
        magic_state_factory_iterator: Optional[Iterable[MagicStateFactory]] = None,
    ) -> GraphResourceInfo:
        magic_state_factory_iterator = iter(
            magic_state_factory_iterator or iter_litinski_factories(hw_model)
        )
        n_rotation_gates = compiled_implementation.program.n_rotation_gates

        this_transpilation_failure_tolerance = (
            compiled_implementation.error_budget.transpilation_failure_tolerance
        )

        # Search minimize the distance, magic state factories, and synthesis accuracy
        # by looping over each until the smallest combination is found
        while True:
            magic_state_factory_found = False
            for magic_state_factory in magic_state_factory_iterator:
                if n_rotation_gates > 0:
                    per_gate_synthesis_accuracy = 1 - (
                        1 - Decimal(this_transpilation_failure_tolerance)
                    ) ** Decimal(1 / n_rotation_gates)
                    n_t_gates_per_rotation = get_num_t_gates_per_rotation(
                        per_gate_synthesis_accuracy
                    )
                else:
                    n_t_gates_per_rotation = 0  # no gates to synthesize

                data_and_bus_code_distance = self._minimize_code_distance(
                    compiled_implementation.program,
                    compiled_implementation.error_budget.hardware_failure_tolerance,
                    this_transpilation_failure_tolerance,
                    magic_state_factory,
                    n_t_gates_per_rotation,
                    hw_model,
                )

                this_logical_cell_error_rate = logical_cell_error_rate(
                    hw_model.physical_qubit_error_rate, data_and_bus_code_distance
                )

                if data_and_bus_code_distance == -1:
                    continue
                else:
                    magic_state_factory_found = True
                    break

            if not magic_state_factory_found:
                warnings.warn(
                    "No viable magic_state_factory found! Returning null results.",
                    RuntimeWarning,
                )
                return GraphResourceInfo(
                    total_time_in_seconds=0.0,
                    n_physical_qubits=-1,
                    optimization=self.optimization,
                    code_distance=-1,
                    logical_error_rate=1.0,
                    n_logical_qubits=-1,
                    magic_state_factory_name="No MagicStateFactory Found",
                    decoder_info=None,
                    extra=GraphExtra(
                        compiled_implementation,
                        None,
                        None,
                    ),
                )
            if this_transpilation_failure_tolerance < this_logical_cell_error_rate:
                # if the t gates typically do not come from rotation gates, then
                # then you will have to restart the calculation from scratch.
                if (
                    compiled_implementation.program.n_t_gates
                    < 0.01 * compiled_implementation.program.n_rotation_gates
                ):
                    raise RuntimeError(
                        "Run estimate again with lower synthesis failure tolerance."
                    )
                if this_transpilation_failure_tolerance < 1e-25:
                    warnings.warn(
                        "Synthesis tolerance low. Smaller problem size recommended.",
                        RuntimeWarning,
                    )
                this_transpilation_failure_tolerance /= 10
            else:
                break

        # Get logical architecture resource info
        # Generate spatial layout of data, bus, and magic state factories
        logical_architecture_resource_info = (
            self.get_bus_architecture_resource_breakdown(
                compiled_implementation.program,
                data_and_bus_code_distance,
                magic_state_factory,
                n_t_gates_per_rotation,
            )
        )

        # Generate temporal resource accounting
        time_allocation = self.get_cycle_allocation(
            compiled_implementation.program,
            magic_state_factory.distillation_time_in_cycles,
            n_t_gates_per_rotation,
            data_and_bus_code_distance,
        )
        logical_architecture_resource_info.cycle_allocation = time_allocation

        # Compute total failure rate
        num_logical_qubits = (
            logical_architecture_resource_info.num_logical_data_qubits
            + logical_architecture_resource_info.num_logical_bus_qubits
        )

        num_cycles = logical_architecture_resource_info.cycle_allocation.total

        st_volume_in_logical_qubit_tocks = (
            num_logical_qubits * num_cycles / data_and_bus_code_distance
        )

        total_logical_error_rate = get_total_logical_failure_rate(
            hw_model,
            st_volume_in_logical_qubit_tocks,
            data_and_bus_code_distance,
        )

        distillation_error_rate = (
            magic_state_factory.distilled_magic_state_error_rate
            * compiled_implementation.program.get_n_t_gates_after_transpilation(
                this_transpilation_failure_tolerance
            )
        )

        this_hardware_failure_rate = distillation_error_rate + total_logical_error_rate

        # get time to get a single shot
        time_per_circuit_in_seconds = (
            6 * num_cycles * hw_model.surface_code_cycle_time_in_seconds
        )

        total_time_in_seconds = (
            time_per_circuit_in_seconds * compiled_implementation.n_shots
        )

        decoder_info = get_decoder_info(
            hw_model,
            decoder_model,
            data_and_bus_code_distance,
            st_volume_in_logical_qubit_tocks,
            num_logical_qubits,
        )

        n_physical_qubits = self.get_total_number_of_physical_qubits(
            logical_architecture_resource_info
        )

        resource_info = GraphResourceInfo(
            total_time_in_seconds=total_time_in_seconds,
            n_physical_qubits=n_physical_qubits,
            optimization=self.optimization,
            code_distance=data_and_bus_code_distance,
            logical_error_rate=this_hardware_failure_rate,
            n_logical_qubits=num_logical_qubits,
            magic_state_factory_name=magic_state_factory.name,
            decoder_info=decoder_info,
            logical_architecture_resource_info=logical_architecture_resource_info,
            extra=GraphExtra(
                compiled_implementation,
            ),
        )

        # Allocate hardware resources according to logical architecture requirements
        resource_info.hardware_resource_info = (
            hw_model.get_hardware_resource_estimates(logical_architecture_resource_info)
            if isinstance(hw_model, DetailedArchitectureModel)
            else None
        )

        return resource_info

    def compile_and_estimate(
        self,
        algorithm_implementation: AlgorithmImplementation,
        algorithm_implementation_compiler,
        hw_model: BasicArchitectureModel,
        decoder_model: Optional[DecoderModel] = None,
        magic_state_factory_iterator: Optional[Iterable[MagicStateFactory]] = None,
    ):
        compiled_implementation = algorithm_implementation_compiler(
            algorithm_implementation,
            self.optimization,
            self.verbose,
        )

        return self.estimate_resources_from_compiled_implementation(
            compiled_implementation,
            hw_model,
            decoder_model,
            magic_state_factory_iterator,
        )
