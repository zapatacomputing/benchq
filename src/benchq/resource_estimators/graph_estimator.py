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

        # distillation_error_rate = 1 - (
        #     1 - Decimal(magic_state_factory.distilled_magic_state_error_rate)
        # ) ** Decimal(
        #     compiled_program.get_n_t_gates_after_transpilation(
        #         transpilation_failure_tolerance
        #     )
        # )

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
                magic_state_factory,
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

        # Qubit resource breakdowns are given by the following layouts
        # for data qubits |D|, bus qubits |B|, and magic state factories |M|.
        # The ion trap architecture is designed for each ELU to connect to at most
        # three other ELUs.

        # The space optimal bus architecture is layed out as follows:
        #     |D| |D| |D| |D| |D|
        #      |   |   |   |   |
        # |B|-|B|-|B|-|B|-|B|-|B|
        #  |
        # |M|

        # The time optimal bus architecture is layed out as follows:
        # |D|                 |D|                 |D|
        #  |                   |                   |
        # |B|-|B|-|B|-|B|-|B|-|B|-|B|-|B|-|B|-|B|-|B|-|B|-|B|-|B|-|B|
        #      |   |   |   |       |   |   |   |       |   |   |   |
        #     |M| |M| |M| |M|     |M| |M| |M| |M|     |M| |M| |M| |M|
        # with the spacing between data qubits determined by the number of
        # teleportations that can happen per distillation according to the
        # "choral round" method.

        if self.optimization == "Space":
            num_logical_data_qubits = compiled_program.num_logical_qubits
            num_magic_state_factories = 1
            num_logical_bus_qubits = num_magic_state_factories + num_logical_data_qubits

            return BusArchitectureResourceInfo(
                num_logical_data_qubits=num_logical_data_qubits,
                num_logical_bus_qubits=num_logical_bus_qubits,
                data_and_bus_code_distance=data_and_bus_code_distance,
                num_magic_state_factories=num_magic_state_factories,
                magic_state_factory=magic_state_factory,
            )

        if self.optimization == "Time":

            num_logical_data_qubits = compiled_program.num_logical_qubits
            num_factories_per_data_qubit, _ = (
                self.model_bus_architecture_time_optimal_distillation_resources(
                    magic_state_factory,
                    compiled_program.n_rotation_gates,
                    data_and_bus_code_distance,
                )
            )
            num_magic_state_factories = (
                num_logical_data_qubits * num_factories_per_data_qubit
            )

            num_logical_bus_qubits = (
                self.model_bus_architecture_time_optimal_logical_bus_qubits(
                    num_logical_data_qubits,
                    num_factories_per_data_qubit,
                )
            )

        return BusArchitectureResourceInfo(
            num_logical_data_qubits=num_logical_data_qubits,
            num_logical_bus_qubits=num_logical_bus_qubits,
            data_and_bus_code_distance=data_and_bus_code_distance,
            num_magic_state_factories=num_magic_state_factories,
            magic_state_factory=magic_state_factory,
        )

    def model_bus_architecture_time_optimal_distillation_resources(
        self,
        magic_state_factory,
        n_rotation_gates,
        data_and_bus_code_distance,
    ):

        if n_rotation_gates == 0:
            # If there are no rotation gates, we can use a single factory
            # for each logical qubit.
            num_factories_per_data_qubit = 1
            tocks_for_enacting_cliffords_due_to_rotations = 0
        else:
            # Assume that at each layer we need to distill as many T gates
            # as can be consumed sequentially within a full distillation round
            # considering the "choral round" method.

            num_tocks_per_distillation = ceil(
                magic_state_factory.distillation_time_in_cycles
                / data_and_bus_code_distance
            )

            num_factories_per_data_qubit = num_tocks_per_distillation
            tocks_for_enacting_cliffords_due_to_rotations = 2

        # Can implement multiple T states per factory in general
        num_factories_per_data_qubit = ceil(
            num_factories_per_data_qubit / magic_state_factory.t_gates_per_distillation
        )
        return (
            num_factories_per_data_qubit,
            tocks_for_enacting_cliffords_due_to_rotations,
        )

    def model_bus_architecture_time_optimal_logical_bus_qubits(
        self,
        num_data_qubits,
        num_factories_per_data_qubit,
    ):
        # Ensure that there is a bus qubit to link to each magic state factory and each data qubit.
        num_data_linked_bus_qubits = num_data_qubits
        num_distillation_linked_bus_qubits = (
            num_data_qubits * num_factories_per_data_qubit
        )
        return num_data_linked_bus_qubits + num_distillation_linked_bus_qubits

    def compute_factory_width_in_logical_qubit_side_lengths(
        self, magic_state_factory, code_distance
    ):
        factory_width = magic_state_factory.space[1]
        # extra factor of 2 for the width of the logical qubit
        # comes from needing to expose rough an smooth boundaries.
        logical_qubit_side_length = 2 * 2 ** (1 / 2) * code_distance
        factory_width_in_logical_qubit_side_lengths = int(
            ceil(factory_width / logical_qubit_side_length)
        )
        return factory_width_in_logical_qubit_side_lengths

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
        magic_state_factory: MagicStateFactory,
        n_t_gates_per_rotation: int,
        data_and_bus_code_distance: int,
    ) -> CycleAllocation:
        time_allocation_for_each_subroutine = [
            CycleAllocation() for _ in range(len(compiled_program.subroutines))
        ]

        # First, generate data for cycle allocation
        if self.optimization == "Space":

            for i, subroutine in enumerate(compiled_program.subroutines):
                for layer in range(subroutine.num_layers):
                    num_t_states_in_this_layer = (
                        n_t_gates_per_rotation * subroutine.rotations_per_layer[layer]
                        + subroutine.t_states_per_layer[layer]
                    )
                    num_distillations_in_this_layer = (
                        num_t_states_in_this_layer
                        / magic_state_factory.t_gates_per_distillation
                    )

                    # Parallelize the first distillation and graph state preparation
                    cycles_for_graph_creation = (
                        subroutine.graph_creation_tocks_per_layer[layer]
                        * data_and_bus_code_distance
                    )
                    time_allocation_for_each_subroutine[i].log_parallelized(
                        (
                            magic_state_factory.distillation_time_in_cycles,
                            cycles_for_graph_creation,
                        ),
                        ("distillation", "entanglement"),
                    )

                    if magic_state_factory.t_gates_per_distillation == 1:
                        time_allocation_for_each_subroutine[i].log(
                            max(num_distillations_in_this_layer - 1, 0)
                            * magic_state_factory.distillation_time_in_cycles,
                            "distillation",
                        )
                        # 1 tock in needed to inject a T state. See the Fig. 2 in the
                        # paper magic state distillation: not as costly as you think.
                        time_allocation_for_each_subroutine[i].log(
                            num_distillations_in_this_layer
                            * data_and_bus_code_distance,
                            "Tstate-to-Tgate",
                        )
                    else:
                        # inject each T state into bus to hold them
                        time_allocation_for_each_subroutine[i].log(
                            num_distillations_in_this_layer
                            * data_and_bus_code_distance,
                            "Tstate-to-Tgate",
                        )
                        # injection from bus can be parallelized with distillation
                        time_allocation_for_each_subroutine[i].log_parallelized(
                            (
                                max(num_distillations_in_this_layer - 1, 0)
                                * magic_state_factory.distillation_time_in_cycles,
                                max(num_distillations_in_this_layer - 1, 0)
                                * magic_state_factory.t_gates_per_distillation
                                * data_and_bus_code_distance,
                            ),
                            ("distillation", "Tstate-to-Tgate"),
                        )
                        # inject gates from the last distillation
                        time_allocation_for_each_subroutine[i].log(
                            magic_state_factory.t_gates_per_distillation
                            * data_and_bus_code_distance,
                            "Tstate-to-Tgate",
                        )
        elif self.optimization == "Time":
            # Temporal accounting for the rate-limiting T gate related process of rotation synthesis:

            # Tocks |Tock1|Tock2|Tock3|Tock4|Tock5|Tock6|Tock7|Tock8|Tock9|Toc10|Toc11|Toc12|Toc13|
            # Dat1: |Graph state------------->|CoDT1----->|CoDT2----->|CoDT3----->|CoDT4----->|
            #                                     ^              ^           ^          ^
            # Bus1: |Graph state------------->|CoDT1----->|CoDT2----->|CoDT3----->|CoDT4----->|
            # Bus2: |Graph state------------->|CoDT1----->|     ^           ^           ^
            # Bus3: |Graph state------------->|  ^        |CoDT2----->|     ^           ^
            # Bus4: |Graph state------------->|  ^              ^     |CoDT3----->|     ^
            #                                 ^              ^           ^           ^
            # MSF1:     |Distill------------->|CoDT1----->| |Dis^ill--------^---->|CoDT4----->|
            # MSF2:                 |Distill------------->|CoDT2----->|     ^
            # MSF3:                             |Distill------------->|CoDT3----->|

            for i, subroutine in enumerate(compiled_program.subroutines):
                # print(f"{i}th subroutine number of layers", subroutine.num_layers)
                for layer_num, layer in enumerate(range(subroutine.num_layers)):
                    # print(f"{i}th subroutine {layer_num}th layer")
                    # print(f"number of qubits: {subroutine.num_logical_qubits}")
                    # print(
                    #     f"rotations_per_layer: {subroutine.rotations_per_layer[layer_num]}"
                    # )
                    # print(
                    #     f"graph creation tocks per layer: {subroutine.graph_creation_tocks_per_layer[layer_num]}"
                    # )
                    # print(
                    #     "Cycles per distillation",
                    #     magic_state_factory.distillation_time_in_cycles,
                    # )
                    cycles_per_tock = data_and_bus_code_distance
                    # Distill T states and prepare graph state in parallel.
                    time_allocation_for_each_subroutine[i].log_parallelized(
                        (
                            magic_state_factory.distillation_time_in_cycles,
                            subroutine.graph_creation_tocks_per_layer[layer]
                            * cycles_per_tock,
                        ),
                        ("distillation", "entanglement"),
                    )

                    cycles_per_t_consumption = 2 * cycles_per_tock

                    if subroutine.rotations_per_layer[layer] > 0:
                        time_allocation_for_each_subroutine[i].log_parallelized(
                            (
                                (n_t_gates_per_rotation - 1) * cycles_per_t_consumption,
                                (n_t_gates_per_rotation - 1) * cycles_per_t_consumption,
                            ),
                            ("distillation", "Tstate-to-Tgate"),
                        )

                    time_allocation_for_each_subroutine[i].log(
                        cycles_per_t_consumption,
                        "Tstate-to-Tgate",
                    )

        else:
            raise ValueError(
                f"Unknown optimization: {self.optimization}. "
                "Should be either 'Time' or 'Space'."
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

        logical_architecture_resource_info = (
            self.get_bus_architecture_resource_breakdown(
                compiled_implementation.program,
                data_and_bus_code_distance,
                magic_state_factory,
                n_t_gates_per_rotation,
            )
        )

        # get error rate after correction
        time_allocation = self.get_cycle_allocation(
            compiled_implementation.program,
            magic_state_factory,
            n_t_gates_per_rotation,
            data_and_bus_code_distance,
        )
        logical_architecture_resource_info.cycle_allocation = time_allocation

        num_logical_qubits = (
            logical_architecture_resource_info.num_logical_data_qubits
            + logical_architecture_resource_info.num_logical_bus_qubits
        )

        num_cycles = time_allocation.total

        st_volume_in_logical_qubit_tocks = (
            num_logical_qubits * num_cycles / data_and_bus_code_distance
        )

        total_logical_error_rate = get_total_logical_failure_rate(
            hw_model,
            st_volume_in_logical_qubit_tocks,
            data_and_bus_code_distance,
        )

        distillation_error_rate = float(
            1
            - (1 - Decimal(magic_state_factory.distilled_magic_state_error_rate))
            ** Decimal(
                compiled_implementation.program.get_n_t_gates_after_transpilation(
                    this_transpilation_failure_tolerance
                )
            )
        )

        this_hardware_failure_rate = float(
            distillation_error_rate
            + total_logical_error_rate
            + distillation_error_rate * total_logical_error_rate
        )

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
            # estimate the number of logical qubits using max node degree
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
