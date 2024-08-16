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
from ..magic_state_distillation import iter_litinski_factories, find_optimal_factory
from ..quantum_hardware_modeling import (
    BasicArchitectureModel,
    DetailedArchitectureModel,
)
from ..quantum_hardware_modeling.devitt_surface_code import (
    get_total_logical_failure_rate,
    logical_cell_error_rate,
    physical_qubits_per_logical_qubit,
)
from ..visualization_tools.resource_allocation import QECCycleAllocation
from .resource_info import (
    LogicalArchitectureResourceInfo,
    GraphExtra,
    GraphResourceInfo,
    MagicStateFactoryInfo,
)

INITIAL_SYNTHESIS_ACCURACY = 0.0001


class GraphResourceEstimator:
    """Estimates resources needed to run an algorithm using graph state compilation.

    ATTRIBUTES:
        hw_model (BasicArchitectureModel): The hardware model to use for the estimate.
            typically, one would choose between the BASIC_SC_ARCHITECTURE_MODEL and
            BASIC_ION_TRAP_ARCHITECTURE_MODEL.
        decoder_model (Optional[DecoderModel]): The decoder model used to estimate.
            If None, no estimates on the number of decoder are provided.
        # TODO: delete logical_architecture
        logical_architecture (str): The logical architecture name that determines 
            the compilation strategy.
        optimization (str): The optimization to use for the estimate. Either estimate
            the resources needed to run the algorithm in the shortest time possible
            ("Time") or the resources needed to run the algorithm with the smallest
            number of physical qubits ("Space").
        magic_state_factory_iterator (Optional[Iterable[MagicStateFactoryInfo]]:
            iterator over all magic_state_factories.
            to be used during estimation. If not provided (or passed None)
            litinski_factory_iterator will select magic_state_factory based
            on hw_model parameter.
    """

    def __init__(
        self,
        # logical_architecture: str = "two_row_bus",
        optimization: str = "Space",
        verbose: bool = False,
    ):
        # self.logical_architecture = logical_architecture
        self.optimization = optimization
        self.verbose = verbose
        getcontext().prec = 100  # need some extra precision for this calculation

    def estimate_resources_from_compiled_implementation(
        self,
        compiled_implementation: CompiledAlgorithmImplementation,
        # TODO: add LogicalArchitectureModel type hint
        logical_architecture_model,
        hw_model: BasicArchitectureModel,
        decoder_model: Optional[DecoderModel] = None,
        magic_state_factory_iterator: Optional[Iterable[MagicStateFactoryInfo]] = None,
    ) -> GraphResourceInfo:
        
        # Set magic state factory to listinski factory iterator if not provided
        magic_state_factory_iterator = iter(magic_state_factory_iterator or iter_litinski_factories(hw_model))

        # Budget failure tolerance
        total_synthesis_failure_tolerance = (
            compiled_implementation.error_budget.transpilation_failure_tolerance
        )
        
        # Evenly split the hardware failure tolerance between the t gate and qec error rates
        total_t_gate_failure_tolerance = compiled_implementation.error_budget.hardware_failure_tolerance/2
        total_qec_failure_tolerance = compiled_implementation.error_budget.hardware_failure_tolerance/2

        # Find optimal magic state factory if needed:
        distillation_is_not_needed = (compiled_implementation.program.n_t_gates ==0) and (compiled_implementation.program.n_rotation_gates == 0)
        if distillation_is_not_needed:
            # If there are no T gates or rotation gates, then there is no need for a magic state factory
            n_t_gates_per_rotation = 0
            per_t_gate_failure_tolerance = 0
            magic_state_factory = None
            n_t_states = 0
        else:
            if compiled_implementation.program.n_rotation_gates == 0:
                # If there are no rotation gates, then no T gates for rotations are needed
                n_t_gates_per_rotation = 0
                per_gate_synthesis_failure_tolerance = 0
                n_t_states = compiled_implementation.program.n_t_gates
            else:
                per_gate_synthesis_failure_tolerance = Decimal(total_synthesis_failure_tolerance) * Decimal(1 / compiled_implementation.program.n_rotation_gates)
                n_t_gates_per_rotation = get_num_t_gates_per_rotation(
                    per_gate_synthesis_failure_tolerance
                )
                n_t_states = compiled_implementation.program.n_t_gates + compiled_implementation.program.n_rotation_gates * n_t_gates_per_rotation
            per_t_gate_failure_tolerance = total_t_gate_failure_tolerance/n_t_states
            # Find minimal space or time factory satisfying error rate
            magic_state_factory = find_optimal_factory(per_t_gate_failure_tolerance,magic_state_factory_iterator, self.optimization)



        # Find optimal layout by minimizing code distance
        logical_architecture_resource_info = logical_architecture_model.generate_resource_info_with_minimal_code_distance(
            compiled_implementation.program,
            self.optimization,
            n_t_gates_per_rotation,
            total_qec_failure_tolerance,
            magic_state_factory,
            hw_model,
        )

        # Populate resource info

        # Compute runtime to execute a single circuit
        time_per_circuit_in_seconds = (
            logical_architecture_resource_info.qec_cycle_allocation.total * hw_model.surface_code_cycle_time_in_seconds
        )

        # Compute runtime to execute all circuits
        total_time_in_seconds = (
            time_per_circuit_in_seconds * compiled_implementation.n_shots
        )

        # TODO: add this into the logical architecture resource info
        # Compute total number of physical qubits
        n_physical_qubits = logical_architecture_model.get_total_number_of_physical_qubits(
            logical_architecture_resource_info
        )

        # TODO: add this into the logical architecture resource info
        # Compute total failure rate
        total_logical_error_rate = get_total_logical_failure_rate(
            hw_model,
            logical_architecture_resource_info.spacetime_volume_in_logical_qubit_tocks,
            logical_architecture_resource_info.data_and_bus_code_distance,
        )
        
        if distillation_is_not_needed:
            distillation_failure_rate = 0
        else:
            distillation_failure_rate = (
                logical_architecture_resource_info.magic_state_factory.distilled_magic_state_error_rate
                * n_t_states
            )
        total_synthesis_failure_rate=total_synthesis_failure_tolerance
        total_circuit_error_rate = distillation_failure_rate + total_logical_error_rate + total_synthesis_failure_rate

        # Populate decoder resource info
        decoder_info = get_decoder_info(
            hw_model,
            decoder_model,
            logical_architecture_resource_info.data_and_bus_code_distance,
            logical_architecture_resource_info.spacetime_volume_in_logical_qubit_tocks,
            logical_architecture_resource_info.num_logical_qubits,
        )

        # TODO: create a default empty factory rather than using the if statements
        if distillation_is_not_needed:
            magic_state_factory_name = None
        else:
            magic_state_factory_name = magic_state_factory.name

        resource_info = GraphResourceInfo(
            total_time_in_seconds=total_time_in_seconds,
            n_physical_qubits=n_physical_qubits,
            optimization=self.optimization,
            code_distance=logical_architecture_resource_info.data_and_bus_code_distance,
            logical_error_rate=total_circuit_error_rate,
            n_logical_qubits=logical_architecture_resource_info.num_logical_qubits,
            magic_state_factory_name=magic_state_factory_name,
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
        # TODO: add LogicalArchitectureModel type hint
        logical_architecture_model,
        hw_model: BasicArchitectureModel,
        decoder_model: Optional[DecoderModel] = None,
        magic_state_factory_iterator: Optional[Iterable[MagicStateFactoryInfo]] = None,
    ):
        compiled_implementation = algorithm_implementation_compiler(
            algorithm_implementation,
            logical_architecture_model.name,
            self.optimization,
            self.verbose,
        )

        return self.estimate_resources_from_compiled_implementation(
            compiled_implementation,
            logical_architecture_model,
            hw_model,
            decoder_model,
            magic_state_factory_iterator,
        )

# TODO: move to somewhere more general
class LogicalArchitectureModel:
    def __init__(self):
        self._name = None

    @property
    def name(self):
        return self._name

class GraphBasedLogicalArchitectureModel(LogicalArchitectureModel):
    def __init__(self):
        self._name = None

    @property
    def name(self):
        return self._name
    
    def generate_resource_info_with_minimal_code_distance(
        self,
        compiled_program: CompiledQuantumProgram,
        optimization: str,
        n_t_gates_per_rotation: int,
        total_qec_failure_tolerance: float,
        magic_state_factory: MagicStateFactoryInfo,
        hw_model: BasicArchitectureModel,
        min_d: int = 3,
        max_d: int = 200,
    ) -> LogicalArchitectureResourceInfo:                
        
        lay_out_found = False

        # Initialize with fixed spatial layout
        logical_architecture_resource_info = (
            self.get_bus_architecture_resource_breakdown(
                compiled_program,
                optimization,
                min_d,
                magic_state_factory,
            )
        )

        for data_and_bus_code_distance in range(min_d, max_d, 2):

            # Get time allocation for each subroutine
            time_allocation = self.get_qec_cycle_allocation(
                compiled_program,
                optimization,
                logical_architecture_resource_info,
                n_t_gates_per_rotation,
            )
            
            # Get spatial allocation
            num_logical_qubits = (
                logical_architecture_resource_info.num_logical_data_qubits
                + logical_architecture_resource_info.num_logical_bus_qubits
            )

            # Compute total spacetime volume
            num_cycles = time_allocation.total
            st_volume_in_logical_qubit_tocks = (
                num_logical_qubits * num_cycles / data_and_bus_code_distance
            )

            # Compute total qec failure rate
            total_qec_error_rate_at_this_distance = Decimal(
                get_total_logical_failure_rate(
                    hw_model,
                    st_volume_in_logical_qubit_tocks,
                    data_and_bus_code_distance,
                )
            )

            # Check if the total qec error rate is below the total qec failure tolerance
            # and if so, set the layout found flag to True, update the relevant fields, 
            # and return the logical architecture resource info
            if total_qec_error_rate_at_this_distance < total_qec_failure_tolerance:
                lay_out_found = True

                logical_architecture_resource_info.data_and_bus_code_distance = data_and_bus_code_distance
                logical_architecture_resource_info.qec_cycle_allocation = time_allocation
                return logical_architecture_resource_info            

        if not lay_out_found:
            warnings.warn(
                "No viable layout found! Returning null results.",
                RuntimeWarning,
            )
            logical_architecture_resource_info.data_and_bus_code_distance = None
            logical_architecture_resource_info.qec_cycle_allocation = None
            return logical_architecture_resource_info 
    
    def get_bus_architecture_resource_breakdown(self):
        raise NotImplementedError
    
    def get_qec_cycle_allocation(self):
        raise NotImplementedError
    
    def get_max_parallel_t_states(self, compiled_program):
        max_parallel_t_states = 0
        for subroutine in compiled_program.subroutines:
            t_states_per_layer = subroutine.t_states_per_layer
            rotations_per_layer = subroutine.rotations_per_layer
            parallel_t_measurements_per_layer = [
                t_states + rotations
                for t_states, rotations in zip(t_states_per_layer, rotations_per_layer)
            ]
            max_parallel_t_measurements_in_subroutine = max(
                parallel_t_measurements_per_layer
            )
            max_parallel_t_states = max(
                max_parallel_t_states, max_parallel_t_measurements_in_subroutine
            )
        return max_parallel_t_states

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
        if logical_architecture_resource_info.num_magic_state_factories == 0:
            num_distillation_physical_qubits = 0
        else:
            num_distillation_physical_qubits = (
                logical_architecture_resource_info.magic_state_factory.qubits
                * logical_architecture_resource_info.num_magic_state_factories
            )

        return num_data_and_bus_physical_qubits + num_distillation_physical_qubits
    


class ActiveVolumeArchitectureModel(GraphBasedLogicalArchitectureModel):
    def __init__(self):
        super().__init__()
        self._name = "active_volume"
    def get_bus_architecture_resource_breakdown(
        self,
        compiled_program: CompiledQuantumProgram,
        optimization: str,
        data_and_bus_code_distance: int,
        magic_state_factory: MagicStateFactoryInfo,
    ) -> LogicalArchitectureResourceInfo:

        num_logical_data_qubits = (
            self.get_max_number_of_data_qubits_from_compiled_program(compiled_program)
        )

        # Qubit resource breakdowns are given by the following layouts
        # for data qubits |D|, bus qubits |B|, and magic state factories |M|.

        # Active volume architecture has all-to-all connectivity
        # TODO: redo this diagram
        # |D|     |D|     ...     |D| |D| ... |D|
        #  |       |               |   |       |
        #   ---*---*---*---*---*---*---*---*---*---
        #  |       |       |
        # |M|     |M|     |M|
        # The space optimal compilation uses just one factory, while the time optimal
        # compilation uses a number of factories determined by the maximum warranted
        # parallelization of distillation.
        if compiled_program.n_t_gates == 0 and compiled_program.n_rotation_gates==0:
            num_magic_state_factories = 0
            magic_state_factory = None
        else:
            if optimization == "Space":
                # For space optimal, a single factory is used
                num_magic_state_factories = 1
            elif optimization == "Time":
                # For time optimal, we use as many factories as would be needed by any layer
                # Note that if the factory is outputting multiple T states per distillation,
                # then the factories may produce more T states than the number of T states
                # needed by any layer.
                num_magic_state_factories = ceil(self.get_max_parallel_t_states(
                    compiled_program
                )/magic_state_factory.t_gates_per_distillation)
            else:
                raise ValueError(
                    f"Unknown optimization: {optimization}. "
                    "Should be either 'Time' or 'Space'."
                )            

        # The ion trap architecture 3-neighbor constraint requires each data qubit
        # and each magic state factory to be connected to a unique bus qubit.
        # The bus qubits are connected to each other in a chain.
        num_logical_bus_qubits = 0

        return LogicalArchitectureResourceInfo(
            num_logical_data_qubits=num_logical_data_qubits,
            num_logical_bus_qubits=num_logical_bus_qubits,
            data_and_bus_code_distance=data_and_bus_code_distance,
            num_magic_state_factories=num_magic_state_factories,
            magic_state_factory=magic_state_factory,
        )

    def get_qec_cycle_allocation(
        self,
        compiled_program: CompiledQuantumProgram,
        optimization: str,
        logical_architecture_resource_info: LogicalArchitectureResourceInfo,
        n_t_gates_per_rotation: int,
    ) -> QECCycleAllocation:

        time_allocation_for_each_subroutine = [
            QECCycleAllocation() for _ in range(len(compiled_program.subroutines))
        ]
        data_and_bus_code_distance=logical_architecture_resource_info.data_and_bus_code_distance

        # Legend:
        # |Graph state->| = "Entanglement" process of graph state creation
        # |CoDTX------->| = "T measurement" process of consuming the Xth T state
        # as a T basis measurements
        # |Distill----->| = "Distillation" process of preparing a T state
        # on a magic state factory

        # TODO: redo this to match active volume picture
        # Stages:[1: Graph creation ] [2: Meas1 ] [3: Distill then Meas2     ] ...
        # Dat1: |Graph state-------->|CoDT1----->|                |CoDT3----->|...
        # Dat2: |Graph state-------->|CoDT2----->|                |CoDT4----->|...
        #                                  ^                            ^
        # Bus1: |Graph state-------->|CoDT1----->|                |CoDT3----->|...
        # Bus2: |Graph state-------->|CoDT1----->|                |CoDT3----->|...
        # Bus3: |Graph state-------->|CoDT2----->|                |CoDT4----->|...
        # Bus4: |Graph state-------->|CoDT2----->|                |CoDT4----->|...
        #                                  ^                            ^
        # MSF1:     |Distill-------->|CoDT1----->|Distill-------->|CoDT3----->|...
        # MSF2:     |Distill-------->|CoDT2----->|Distill-------->|CoDT4----->|...

        # For space optimal, a single factory is used and distillation
        # is done serially.
        # For time optimal, multiple factories are used and distillation
        # is done in parallel.

        for i, subroutine in enumerate(compiled_program.subroutines):
            for layer_num, layer in enumerate(range(subroutine.num_layers)):

                cycles_per_tock = data_and_bus_code_distance

                # Check if the number of T gates and number of rotations
                # per layer is zero
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
                    distillation_time_in_cycles=logical_architecture_resource_info.magic_state_factory.distillation_time_in_cycles
                    t_gates_per_distillation=logical_architecture_resource_info.magic_state_factory.t_gates_per_distillation

                    # Set number of parallel T measurements according to optimization strategy
                    if optimization == "Space":
                        # Space optimal entails using just a single factory that outputs 
                        # t_gates_per_distillation T states per distillation
                        number_of_parallel_t_measurements = t_gates_per_distillation

                    elif optimization == "Time":
                        # Time optimal entails using as many factories as would be needed 
                        # by any layer in the subroutine to distill T states in parallel
                        number_of_parallel_t_measurements = subroutine.t_states_per_layer[layer] + subroutine.rotations_per_layer[layer]
                    else:
                        raise ValueError(
                            f"Unknown optimization: {optimization}. "
                            "Should be either 'Time' or 'Space'."
                        )
                    # Construct a vector of remaining number of T measurements for each node that needs a T measurement
                    remaining_t_measurements_per_node = [n_t_gates_per_rotation]*subroutine.rotations_per_layer[layer]+[1]*subroutine.t_states_per_layer[layer]

                    # If there are T gates in the layer, then the layer requires
                    # graph state preparation, distillation, and T state measurement
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
                    # TODO: write unit tests for this function and place it in an appropriate correct module
                    def consume_t_measurements(remaining_t_measurements_per_node, number_of_parallel_t_measurements):
                        """This function helps with accounting for the scheduling of T state measurements
                        given a specified number of T measurements that can be made in parallel. 
                        The funtion decrements the number of remaining T measurements needed for each node 
                        according to which nodes still need a T measurement and the number of T measurements
                        that can be made in parallel.

                        Args:
                            remaining_t_measurements_per_node (List[int]): A list of the number of T measurements
                                still needed for each node that needs a T measurement.
                            number_of_parallel_t_measurements (int): The number of T measurements that can be made in parallel.
                        """
                        # Note: because the rotation nodes are listed first, this function consumes
                        # all available T measurements for rotations before consuming T measurements
                        # for T states. This is because, in general, rotations require more T measurements
                        # and so we ensure that we deplete the T measurements of these rate-limiting
                        # operations first.
                        n_remaining_measurements_in_moment = number_of_parallel_t_measurements

                        for non_clifford_node_index in range(len(remaining_t_measurements_per_node)):
                            # Subract 1 from each node that still needs a T measurement
                            # until the n_remaining_measurements_in_moment is 0
                            if remaining_t_measurements_per_node[non_clifford_node_index] > 0:
                                remaining_t_measurements_per_node[non_clifford_node_index] -= 1
                                n_remaining_measurements_in_moment -= 1
                            else:
                                # If there are no more T measurements to be made, break
                                break
                        return remaining_t_measurements_per_node                        

                    remaining_t_measurements_per_node = consume_t_measurements(remaining_t_measurements_per_node, number_of_parallel_t_measurements)

                    # Log Stage 3: Space optimal entails serially distilling T states
                    # and a T measurement is made after each distillation, while time
                    # optimal entails distilling T states in parallel and making a
                    # T measurement after, though T gates used to synthesize a
                    # rotation are still implemented serially.

                    # Loop over remaining T rounds
                    while sum(remaining_t_measurements_per_node) > 0:
                        # Log distillation time
                        time_allocation_for_each_subroutine[i].log(
                            distillation_time_in_cycles,
                            "distillation",
                        )

                        # Log T measurement time
                        time_allocation_for_each_subroutine[i].log(
                            cycles_per_t_measurement,
                            "T measurement",
                        )

                        # Update remaining T measurements
                        remaining_t_measurements_per_node = consume_t_measurements(remaining_t_measurements_per_node, number_of_parallel_t_measurements)


        # Then initialize cycle allocation object and populate with data
        qec_cycle_allocation = QECCycleAllocation()
        for subroutine_index in compiled_program.subroutine_sequence:
            qec_cycle_allocation += time_allocation_for_each_subroutine[subroutine_index]
        return qec_cycle_allocation            


class TwoRowBusArchitectureModel(GraphBasedLogicalArchitectureModel):
    def __init__(self):
        super().__init__()
        self._name = "two_row_bus"

    def get_bus_architecture_resource_breakdown(
        self,
        compiled_program: CompiledQuantumProgram,
        optimization: str,
        data_and_bus_code_distance: int,
        magic_state_factory: MagicStateFactoryInfo,
    ) -> LogicalArchitectureResourceInfo:

        num_logical_data_qubits = (
            self.get_max_number_of_data_qubits_from_compiled_program(compiled_program)
        )

        # Qubit resource breakdowns are given by the following layouts
        # for data qubits |D|, bus qubits |B|, and magic state factories |M|.
        # The ion trap architecture is designed for each ELU to connect to at most
        # three other ELUs.

        # The two-row bus architecture with degree-three connectivity
        # is layed out as follows:
        # |D|     |D|     ...     |D| |D| ... |D|
        #  |       |               |   |       |
        # |B|-|B|-|B|-|B|-...-|B|-|B|-|B|-...-|B|
        #      |       |       |
        #     |M|     |M|     |M|
        # there is a bus qubit for each data qubit and each magic state factory.
        # The space optimal compilation uses just one factory, while the time optimal
        # compilation uses a number of factories determined by the maximum warranted
        # parallelization of distillation.
        if compiled_program.n_t_gates == 0 and compiled_program.n_rotation_gates==0:
            num_magic_state_factories = 0
            magic_state_factory = None
        else:
            if optimization == "Space":
                # For space optimal, a single factory is used
                num_magic_state_factories = 1
            elif optimization == "Time":
                # For time optimal, we use as many factories as would be needed by any layer
                # Note that if the factory is outputting multiple T states per distillation,
                # then the factories may produce more T states than the number of T states
                # needed by any layer.
                num_magic_state_factories = ceil(self.get_max_parallel_t_states(
                    compiled_program
                )/magic_state_factory.t_gates_per_distillation)
            else:
                raise ValueError(
                    f"Unknown optimization: {optimization}. "
                    "Should be either 'Time' or 'Space'."
                )            

        # The ion trap architecture 3-neighbor constraint requires each data qubit
        # and each magic state factory to be connected to a unique bus qubit.
        # The bus qubits are connected to each other in a chain.
        num_logical_bus_qubits = num_logical_data_qubits + num_magic_state_factories

        return LogicalArchitectureResourceInfo(
            num_logical_data_qubits=num_logical_data_qubits,
            num_logical_bus_qubits=num_logical_bus_qubits,
            data_and_bus_code_distance=data_and_bus_code_distance,
            num_magic_state_factories=num_magic_state_factories,
            magic_state_factory=magic_state_factory,
        )

    def get_qec_cycle_allocation(
        self,
        compiled_program: CompiledQuantumProgram,
        optimization: str,
        logical_architecture_resource_info: LogicalArchitectureResourceInfo,
        n_t_gates_per_rotation: int,
    ) -> QECCycleAllocation:

        time_allocation_for_each_subroutine = [
            QECCycleAllocation() for _ in range(len(compiled_program.subroutines))
        ]
        data_and_bus_code_distance=logical_architecture_resource_info.data_and_bus_code_distance

        # Legend:
        # |Graph state->| = "Entanglement" process of graph state creation
        # |CoDTX------->| = "T measurement" process of consuming the Xth T state
        # as a T basis measurements
        # |Distill----->| = "Distillation" process of preparing a T state
        # on a magic state factory

        # Stages:[1: Graph creation ] [2: Meas1 ] [3: Distill then Meas2     ] ...
        # Dat1: |Graph state-------->|CoDT1----->|                |CoDT3----->|...
        # Dat2: |Graph state-------->|CoDT2----->|                |CoDT4----->|...
        #                                  ^                            ^
        # Bus1: |Graph state-------->|CoDT1----->|                |CoDT3----->|...
        # Bus2: |Graph state-------->|CoDT1----->|                |CoDT3----->|...
        # Bus3: |Graph state-------->|CoDT2----->|                |CoDT4----->|...
        # Bus4: |Graph state-------->|CoDT2----->|                |CoDT4----->|...
        #                                  ^                            ^
        # MSF1:     |Distill-------->|CoDT1----->|Distill-------->|CoDT3----->|...
        # MSF2:     |Distill-------->|CoDT2----->|Distill-------->|CoDT4----->|...

        # For space optimal, a single factory is used and distillation
        # is done serially.
        # For time optimal, multiple factories are used and distillation
        # is done in parallel.

        for i, subroutine in enumerate(compiled_program.subroutines):
            for layer_num, layer in enumerate(range(subroutine.num_layers)):

                cycles_per_tock = data_and_bus_code_distance

                # Check if the number of T gates and number of rotations
                # per layer is zero
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
                    distillation_time_in_cycles=logical_architecture_resource_info.magic_state_factory.distillation_time_in_cycles
                    t_gates_per_distillation=logical_architecture_resource_info.magic_state_factory.t_gates_per_distillation

                    # Set number of parallel T measurements according to optimization strategy
                    if optimization == "Space":
                        # Space optimal entails using just a single factory that outputs 
                        # t_gates_per_distillation T states per distillation
                        number_of_parallel_t_measurements = t_gates_per_distillation

                    elif optimization == "Time":
                        # Time optimal entails using as many factories as would be needed 
                        # by any layer in the subroutine to distill T states in parallel
                        number_of_parallel_t_measurements = subroutine.t_states_per_layer[layer] + subroutine.rotations_per_layer[layer]
                    else:
                        raise ValueError(
                            f"Unknown optimization: {optimization}. "
                            "Should be either 'Time' or 'Space'."
                        )
                    # Construct a vector of remaining number of T measurements for each node that needs a T measurement
                    remaining_t_measurements_per_node = [n_t_gates_per_rotation]*subroutine.rotations_per_layer[layer]+[1]*subroutine.t_states_per_layer[layer]

                    # If there are T gates in the layer, then the layer requires
                    # graph state preparation, distillation, and T state measurement
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
                    # TODO: write unit tests for this function and place it in an appropriate correct module
                    def consume_t_measurements(remaining_t_measurements_per_node, number_of_parallel_t_measurements):
                        """This function helps with accounting for the scheduling of T state measurements
                        given a specified number of T measurements that can be made in parallel. 
                        The funtion decrements the number of remaining T measurements needed for each node 
                        according to which nodes still need a T measurement and the number of T measurements
                        that can be made in parallel.

                        Args:
                            remaining_t_measurements_per_node (List[int]): A list of the number of T measurements
                                still needed for each node that needs a T measurement.
                            number_of_parallel_t_measurements (int): The number of T measurements that can be made in parallel.
                        """
                        # Note: because the rotation nodes are listed first, this function consumes
                        # all available T measurements for rotations before consuming T measurements
                        # for T states. This is because, in general, rotations require more T measurements
                        # and so we ensure that we deplete the T measurements of these rate-limiting
                        # operations first.
                        n_remaining_measurements_in_moment = number_of_parallel_t_measurements

                        for non_clifford_node_index in range(len(remaining_t_measurements_per_node)):
                            # Subract 1 from each node that still needs a T measurement
                            # until the n_remaining_measurements_in_moment is 0
                            if remaining_t_measurements_per_node[non_clifford_node_index] > 0:
                                remaining_t_measurements_per_node[non_clifford_node_index] -= 1
                                n_remaining_measurements_in_moment -= 1
                            else:
                                # If there are no more T measurements to be made, break
                                break
                        return remaining_t_measurements_per_node                        

                    remaining_t_measurements_per_node = consume_t_measurements(remaining_t_measurements_per_node, number_of_parallel_t_measurements)

                    # Log Stage 3: Space optimal entails serially distilling T states
                    # and a T measurement is made after each distillation, while time
                    # optimal entails distilling T states in parallel and making a
                    # T measurement after, though T gates used to synthesize a
                    # rotation are still implemented serially.

                    # Loop over remaining T rounds
                    while sum(remaining_t_measurements_per_node) > 0:
                        # Log distillation time
                        time_allocation_for_each_subroutine[i].log(
                            distillation_time_in_cycles,
                            "distillation",
                        )

                        # Log T measurement time
                        time_allocation_for_each_subroutine[i].log(
                            cycles_per_t_measurement,
                            "T measurement",
                        )

                        # Update remaining T measurements
                        remaining_t_measurements_per_node = consume_t_measurements(remaining_t_measurements_per_node, number_of_parallel_t_measurements)


        # Then initialize cycle allocation object and populate with data
        qec_cycle_allocation = QECCycleAllocation()
        for subroutine_index in compiled_program.subroutine_sequence:
            qec_cycle_allocation += time_allocation_for_each_subroutine[subroutine_index]
        return qec_cycle_allocation
    
       

