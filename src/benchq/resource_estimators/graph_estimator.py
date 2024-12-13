from pathlib import Path

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

from ..logical_architecture_modeling.graph_based_logical_architectures import (
    GraphBasedLogicalArchitectureModel,
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
    AbstractLogicalResourceInfo,
    GraphExtra,
    GraphResourceInfo,
    ResourceInfo,
    MagicStateFactoryInfo,
)


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
        magic_state_factory_iterator (Optional[Iterable[MagicStateFactoryInfo]]:
            iterator over all magic_state_factories.
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

    def estimate_resources_from_compiled_implementation(
        self,
        compiled_implementation: CompiledAlgorithmImplementation,
        logical_architecture_model: GraphBasedLogicalArchitectureModel,
        hw_model: BasicArchitectureModel,
        decoder_model: Optional[DecoderModel] = None,
        magic_state_factory_iterator: Optional[Iterable[MagicStateFactoryInfo]] = None,
    ) -> GraphResourceInfo:

        # Set magic state factory to listinski factory iterator if not provided
        magic_state_factory_iterator = iter(
            magic_state_factory_iterator or iter_litinski_factories(hw_model)
        )

        # Budget failure tolerance
        total_rotation_failure_tolerance = (
            compiled_implementation.error_budget.transpilation_failure_tolerance
        )

        # Evenly split the hardware failure tolerance between the t gate and
        # qec error rates
        total_t_gate_failure_tolerance = (
            compiled_implementation.error_budget.hardware_failure_tolerance / 2
        )
        total_qec_failure_tolerance = (
            compiled_implementation.error_budget.hardware_failure_tolerance / 2
        )

        # Find optimal magic state factory if needed:
        distillation_is_not_needed = (
            compiled_implementation.program.n_t_gates == 0
        ) and (compiled_implementation.program.n_rotation_gates == 0)
        if distillation_is_not_needed:
            # If there are no T gates or rotation gates, then there is
            # no need for a magic state factory
            n_t_gates_per_rotation = 0
            per_rotation_failure_tolerance = 0
            per_t_gate_failure_tolerance = 0
            magic_state_factory = None
            n_t_states = 0
        else:
            if compiled_implementation.program.n_rotation_gates == 0:
                # If there are no rotation gates, then no T gates for
                # rotations are needed
                n_t_gates_per_rotation = 0
                per_rotation_failure_tolerance = 0
                n_t_states = compiled_implementation.program.n_t_gates
            else:
                per_rotation_failure_tolerance = Decimal(
                    total_rotation_failure_tolerance
                ) * Decimal(1 / compiled_implementation.program.n_rotation_gates)
                n_t_gates_per_rotation = get_num_t_gates_per_rotation(
                    per_rotation_failure_tolerance
                )
                n_t_states = (
                    compiled_implementation.program.n_t_gates
                    + compiled_implementation.program.n_rotation_gates
                    * n_t_gates_per_rotation
                )
            per_t_gate_failure_tolerance = total_t_gate_failure_tolerance / n_t_states

            # Find minimal space or time factory satisfying error rate
            magic_state_factory = find_optimal_factory(
                per_t_gate_failure_tolerance,
                magic_state_factory_iterator,
                self.optimization,
            )

        # Find optimal layout by minimizing code distance
        log_arch_info = (
            logical_architecture_model.generate_minimal_code_distance_resources(
                compiled_implementation.program,
                self.optimization,
                n_t_gates_per_rotation,
                total_qec_failure_tolerance,
                magic_state_factory,
                hw_model,
            )
        )

        # Populate resource info

        # Compute runtime to execute a single circuit
        time_per_circuit_in_seconds = (
            log_arch_info.qec_cycle_allocation.total  # type: ignore
            * hw_model.surface_code_cycle_time_in_seconds
        )

        # Compute runtime to execute all circuits
        total_time_in_seconds = (
            time_per_circuit_in_seconds * compiled_implementation.n_shots
        )

        # Compute total number of physical qubits
        n_physical_qubits = (
            logical_architecture_model.get_total_number_of_physical_qubits(
                log_arch_info
            )
        )

        # Populate remaining logical failure rates

        # Rotations
        log_arch_info.logical_failure_rate_info.per_rotation_failure_rate = (  # type: ignore
            per_rotation_failure_tolerance
        )
        log_arch_info.logical_failure_rate_info.total_rotation_failure_rate = (  # type: ignore
            per_rotation_failure_tolerance
            * compiled_implementation.program.n_rotation_gates
        )

        # Distillation
        if magic_state_factory is None:
            log_arch_info.logical_failure_rate_info.per_t_gate_failure_rate = 0.0  # type: ignore
            log_arch_info.logical_failure_rate_info.total_distillation_failure_rate = (  # type: ignore
                0.0
            )
        else:
            log_arch_info.logical_failure_rate_info.per_t_gate_failure_rate = (  # type: ignore
                magic_state_factory.distilled_magic_state_error_rate
            )
            log_arch_info.logical_failure_rate_info.total_distillation_failure_rate = (  # type: ignore
                magic_state_factory.distilled_magic_state_error_rate * n_t_states
            )

        # Populate decoder resource info
        decoder_info = get_decoder_info(
            hw_model,
            decoder_model,
            log_arch_info.data_and_bus_code_distance,
            log_arch_info.spacetime_volume_in_logical_qubit_tocks,
            log_arch_info.num_logical_qubits,
        )

        # Extract nested attribute into a local variable
        logical_failure_info = log_arch_info.logical_failure_rate_info
        total_circuit_failure_rate = (
            logical_failure_info.total_circuit_failure_rate
            if logical_failure_info is not None
            else None
        )
        resource_info = ResourceInfo(
            n_physical_qubits=n_physical_qubits,
            total_time_in_seconds=total_time_in_seconds,
            total_circuit_failure_rate=total_circuit_failure_rate,
            logical_architecture_resource_info=log_arch_info,
            decoder_info=decoder_info,
            optimization=self.optimization,
            extra=GraphExtra(
                compiled_implementation,
            ),
        )

        # Allocate hardware resources according to logical architecture requirements
        resource_info.hardware_resource_info = (
            hw_model.get_hardware_resource_estimates(log_arch_info)
            if isinstance(hw_model, DetailedArchitectureModel)
            else None
        )

        return resource_info

    def compile_and_estimate(
        self,
        algorithm_implementation: AlgorithmImplementation,
        algorithm_implementation_compiler,
        logical_architecture_model: GraphBasedLogicalArchitectureModel,
        hw_model: BasicArchitectureModel,
        decoder_model: Optional[DecoderModel] = None,
        magic_state_factory_iterator: Optional[Iterable[MagicStateFactoryInfo]] = None,
    ):

        logical_architecture_model_name = logical_architecture_model.name

        # Compile the algorithm implementation
        compiled_implementation = algorithm_implementation_compiler(
            algorithm_implementation,
            logical_architecture_model_name,
            self.optimization,
            self.verbose,
        )

        # Estimate resources from compiled implementation
        resource_info = self.estimate_resources_from_compiled_implementation(
            compiled_implementation,
            logical_architecture_model,
            hw_model,
            decoder_model,
            magic_state_factory_iterator,
        )

        # Get abstract logical resource info
        abstract_logical_resource_info = AbstractLogicalResourceInfo(
            n_abstract_logical_qubits=algorithm_implementation.program.num_data_qubits,
            n_t_gates=algorithm_implementation.program.n_t_gates,
        )

        # Add abstract logical resource info to resource info
        resource_info.abstract_logical_resource_info = abstract_logical_resource_info
        resource_info.n_abstract_logical_qubits = (
            abstract_logical_resource_info.n_abstract_logical_qubits
        )
        resource_info.n_t_gates = abstract_logical_resource_info.n_t_gates

        return resource_info
