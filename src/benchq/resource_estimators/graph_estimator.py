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
from ..visualization_tools.resource_allocation import CycleAllocation, QubitAllocation
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

        distillation_error_rate = 1 - (
            1 - Decimal(magic_state_factory.distilled_magic_state_error_rate)
        ) ** Decimal(
            compiled_program.get_n_t_gates_after_transpilation(
                transpilation_failure_tolerance
            )
        )

        if distillation_error_rate > hardware_failure_tolerance:
            return -1

        for code_distance in range(min_d, max_d, 2):
            qubit_allocation, time_allocation = self.get_qubit_and_time_allocation(
                compiled_program,
                magic_state_factory,
                n_t_gates_per_rotation,
                code_distance,
            )
            num_logical_qubits = qubit_allocation.get_num_logical_qubits(
                2 * physical_qubits_per_logical_qubit(code_distance)
            )
            num_cycles = time_allocation.total
            st_volume_in_logical_qubit_tocks = (
                num_logical_qubits * num_cycles / code_distance
            )

            ec_error_rate_at_this_distance = Decimal(
                get_total_logical_failure_rate(
                    hw_model,
                    st_volume_in_logical_qubit_tocks,
                    code_distance,
                )
            )

            this_hardware_failure_rate = float(
                distillation_error_rate
                + ec_error_rate_at_this_distance
                + distillation_error_rate * ec_error_rate_at_this_distance
            )

            if this_hardware_failure_rate < hardware_failure_tolerance:
                return code_distance

        return -1

    def get_bus_architecture_resource_breakdown(
        self,
        compiled_program: CompiledQuantumProgram,
        magic_state_factory: MagicStateFactory,
        n_t_gates_per_rotation: int,
    ):
        if self.optimization == "Space":
            # Not implemented error
            raise NotImplementedError(
                "Bus architecture resource breakdown is not yet implemented for Space optimization."
            )
        if self.optimization == "Time":

            num_logical_data_qubits = compiled_program.num_logical_qubits
            num_factories_per_data_qubit, _ = (
                self.model_bus_architecture_time_optimal_distillation_resources(
                    n_t_gates_per_rotation,
                    compiled_program.n_rotation_gates,
                    magic_state_factory.t_gates_per_distillation,
                )
            )
            factory_width_in_logical_qubit_side_lengths = (
                self.compute_factory_width_in_logical_qubit_side_lengths(
                    magic_state_factory, compiled_program.code_distance
                )
            )
            num_logical_bus_qubits = (
                self.model_bus_architecture_time_optimal_logical_bus_qubits(
                    num_logical_data_qubits,
                    num_factories_per_data_qubit,
                    factory_width_in_logical_qubit_side_lengths,
                )
            )
            num_magic_state_factories = (
                num_logical_data_qubits * num_factories_per_data_qubit
            )

        return BusArchitectureResourceInfo(
            num_logical_data_qubits=num_logical_data_qubits,
            num_logical_bus_qubits=num_logical_bus_qubits,
            num_magic_state_factories=num_magic_state_factories,
        )

    def model_bus_architecture_time_optimal_distillation_resources(
        n_t_gates_per_rotation, n_rotation_gates, t_gates_per_distillation
    ):
        if n_rotation_gates == 0:
            # If there are no rotation gates, we can use a single factory
            # for each logical qubit.
            num_factories_per_data_qubit = 1
            tocks_for_enacting_cliffords_due_to_rotations = 0
        else:
            # Assume that at each layer we need to distill as many T gates
            # as are needed for performing rotations on each logical qubit.
            num_factories_per_data_qubit = n_t_gates_per_rotation
            tocks_for_enacting_cliffords_due_to_rotations = 2

        num_factories_per_data_qubit = ceil(
            num_factories_per_data_qubit / t_gates_per_distillation
        )
        return (
            num_factories_per_data_qubit,
            tocks_for_enacting_cliffords_due_to_rotations,
        )

    def model_bus_architecture_time_optimal_logical_bus_qubits(
        n_data_qubits,
        num_factories_per_data_qubit,
        factory_width_in_logical_qubit_side_lengths,
    ):
        return (
            n_data_qubits
            * num_factories_per_data_qubit
            * factory_width_in_logical_qubit_side_lengths
        )

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

    def get_qubit_and_time_allocation(
        self,
        compiled_program: CompiledQuantumProgram,
        magic_state_factory: MagicStateFactory,
        n_t_gates_per_rotation: int,
        code_distance: int,
    ) -> Tuple[QubitAllocation, CycleAllocation]:
        time_allocation_for_each_subroutine = [
            CycleAllocation() for _ in range(len(compiled_program.subroutines))
        ]
        qubit_allocation = QubitAllocation()

        if self.optimization == "Space":
            # Injection and entanglement use the same bus and data qubits
            qubit_allocation.log(
                2
                * compiled_program.num_logical_qubits
                * physical_qubits_per_logical_qubit(code_distance),
                "entanglement",
                "Tstate-to-Tgate",
            )
            # Use only 1 magic state factory
            qubit_allocation.log(magic_state_factory.qubits, "distillation")
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

                    # Paralellize the first distillation and graph state preparation
                    time_allocation_for_each_subroutine[i].log_parallelized(
                        (
                            magic_state_factory.distillation_time_in_cycles,
                            subroutine.graph_creation_tocks_per_layer[layer]
                            * code_distance,
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
                            num_distillations_in_this_layer * code_distance,
                            "Tstate-to-Tgate",
                        )
                    else:
                        # inject each T state into bus to hold them
                        time_allocation_for_each_subroutine[i].log(
                            num_distillations_in_this_layer * code_distance,
                            "Tstate-to-Tgate",
                        )
                        # injection from bus can be parallelized with distillation
                        time_allocation_for_each_subroutine[i].log_parallelized(
                            (
                                max(num_distillations_in_this_layer - 1, 0)
                                * magic_state_factory.distillation_time_in_cycles,
                                max(num_distillations_in_this_layer - 1, 0)
                                * magic_state_factory.t_gates_per_distillation
                                * code_distance,
                            ),
                            ("distillation", "Tstate-to-Tgate"),
                        )
                        # inject gates from the last distillation
                        time_allocation_for_each_subroutine[i].log(
                            magic_state_factory.t_gates_per_distillation
                            * code_distance,
                            "Tstate-to-Tgate",
                        )
        elif self.optimization == "Time":

            (
                num_factories_per_data_qubit,
                tocks_for_enacting_cliffords_due_to_rotations,
            ) = self.model_bus_architecture_time_optimal_distillation_resources(
                n_t_gates_per_rotation,
                compiled_program.n_rotation_gates,
                magic_state_factory.t_gates_per_distillation,
            )

            qubit_allocation.log(
                compiled_program.num_logical_qubits
                * num_factories_per_data_qubit
                * magic_state_factory.qubits,
                "distillation",
            )

            factory_width_in_logical_qubit_side_lengths = (
                self.compute_factory_width_in_logical_qubit_side_lengths(
                    magic_state_factory, code_distance
                )
            )
            # For each logical qubit, add enough factories to cover a single
            # node which can represent a distillation or a rotation.
            # Note that the logical qubits are twice as wide as they are tall
            # so that a rough and a smooth boundary can both face the bus.
            qubit_allocation.log(
                2 * physical_qubits_per_logical_qubit(code_distance)
                # bus qubits which span factory sides but are not
                # used to inject T states
                * compiled_program.num_logical_qubits
                * num_factories_per_data_qubit
                * (factory_width_in_logical_qubit_side_lengths - 1),
                "entanglement",
            )
            qubit_allocation.log(
                2 * physical_qubits_per_logical_qubit(code_distance)
                # bus qubits which span factory sides
                * (
                    compiled_program.num_logical_qubits * num_factories_per_data_qubit
                    # logical qubits for computation
                    + compiled_program.num_logical_qubits
                ),
                "entanglement",
                "Tstate-to-Tgate",
            )

            for i, subroutine in enumerate(compiled_program.subroutines):
                for layer_num, layer in enumerate(range(subroutine.num_layers)):

                    if layer_num > 0:
                        # we need to wait for the previous subroutine to finish
                        # measuring the qubits in the T basis before we continue
                        # with the next subroutine. However, we can distill T states
                        # and perform these measurements in parallel. We assume that
                        # it takes 1 cycle to measure these T states, which is a
                        # conservative assumption according to Fowler et al.'s
                        # seminal surface code paper: https://arxiv.org/abs/1208.0928
                        # which puts measurement times at about 1/2 cycle time (see
                        # the middle of page 2).
                        time_allocation_for_each_subroutine[i].log_parallelized(
                            (
                                num_factories_per_data_qubit,
                                num_factories_per_data_qubit,
                            ),
                            ("distillation", "Tstate-to-Tgate"),
                        )

                    if (
                        num_factories_per_data_qubit
                        > magic_state_factory.distillation_time_in_cycles
                        and layer_num > 0
                    ):
                        # cannot parallelize injection from previous layer
                        # and graph state preparation
                        time_allocation_for_each_subroutine[i].log(
                            num_factories_per_data_qubit
                            - magic_state_factory.distillation_time_in_cycles,
                            "Tstate-to-Tgate",
                        )
                        time_allocation_for_each_subroutine[i].log(
                            (
                                subroutine.graph_creation_tocks_per_layer[layer]
                                + tocks_for_enacting_cliffords_due_to_rotations
                            )
                            * code_distance,
                            "entanglement",
                        )
                    elif layer_num > 0:
                        # Distill T states and prepare graph state in parallel.
                        time_allocation_for_each_subroutine[i].log_parallelized(
                            (
                                magic_state_factory.distillation_time_in_cycles
                                - num_factories_per_data_qubit,
                                (
                                    subroutine.graph_creation_tocks_per_layer[layer]
                                    + tocks_for_enacting_cliffords_due_to_rotations
                                )
                                * code_distance,
                            ),
                            ("distillation", "entanglement"),
                        )

                    # 1 tock to deliver T states to the synthilation qubits.
                    time_allocation_for_each_subroutine[i].log(
                        code_distance, "Tstate-to-Tgate"
                    )

        else:
            raise ValueError(
                f"Unknown optimization: {self.optimization}. "
                "Should be either 'Time' or 'Space'."
            )

        total_time_allocation = CycleAllocation()
        for subroutine_index in compiled_program.subroutine_sequence:
            total_time_allocation += time_allocation_for_each_subroutine[
                subroutine_index
            ]

        return qubit_allocation, total_time_allocation

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

                code_distance = self._minimize_code_distance(
                    compiled_implementation.program,
                    compiled_implementation.error_budget.hardware_failure_tolerance,
                    this_transpilation_failure_tolerance,
                    magic_state_factory,
                    n_t_gates_per_rotation,
                    hw_model,
                )

                this_logical_cell_error_rate = logical_cell_error_rate(
                    hw_model.physical_qubit_error_rate, code_distance
                )

                if code_distance == -1:
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

        # get error rate after correction
        qubit_allocation, time_allocation = self.get_qubit_and_time_allocation(
            compiled_implementation.program,
            magic_state_factory,
            n_t_gates_per_rotation,
            code_distance,
        )
        num_logical_qubits = qubit_allocation.get_num_logical_qubits(
            2 * physical_qubits_per_logical_qubit(code_distance)
        )

        num_cycles = time_allocation.total

        st_volume_in_logical_qubit_tocks = (
            num_logical_qubits * num_cycles / code_distance
        )

        total_logical_error_rate = get_total_logical_failure_rate(
            hw_model,
            st_volume_in_logical_qubit_tocks,
            code_distance,
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
            code_distance,
            st_volume_in_logical_qubit_tocks,
            num_logical_qubits,
        )

        resource_info = GraphResourceInfo(
            total_time_in_seconds=total_time_in_seconds,
            n_physical_qubits=qubit_allocation.total,
            optimization=self.optimization,
            code_distance=code_distance,
            logical_error_rate=this_hardware_failure_rate,
            # estimate the number of logical qubits using max node degree
            n_logical_qubits=num_logical_qubits,
            magic_state_factory_name=magic_state_factory.name,
            decoder_info=decoder_info,
            extra=GraphExtra(
                compiled_implementation,
                time_allocation,
                qubit_allocation,
            ),
        )

        resource_info.logical_architecture_resource_info = (
            self.get_bus_architecture_resource_breakdown(compiled_implementation)
        )

        # Allocate hardware resources according to logical architecture requirements
        resource_info.hardware_resource_info = (
            hw_model.get_hardware_resource_estimates(
                resource_info.logical_architecture_resource_info
            )
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
