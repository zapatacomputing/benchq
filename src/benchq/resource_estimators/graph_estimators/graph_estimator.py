import warnings
from dataclasses import replace
from decimal import Decimal, getcontext
from math import ceil
from typing import Iterable, Optional, Callable

from benchq.decoder_modeling.decoder_resource_estimator import get_decoder_info

from ...algorithms.data_structures import AlgorithmImplementation
from ...algorithms.data_structures.graph_partition import GraphPartition
from ...decoder_modeling import DecoderModel
from ...magic_state_distillation import MagicStateFactory, iter_litinski_factories
from ...quantum_hardware_modeling import (
    BasicArchitectureModel,
    DetailedArchitectureModel,
)
from ...quantum_hardware_modeling.devitt_surface_code import (
    get_total_logical_failure_rate,
    logical_cell_error_rate,
    physical_qubits_per_logical_qubit,
)
from ..resource_info import GraphData, GraphResourceInfo
from ...problem_embeddings.quantum_program import QuantumProgram
from ...compilation.graph_states.compiled_data_structures import (
    CompiledAlgorithmImplementation,
    CompiledQuantumProgram,
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

    # Assumes gridsynth scaling
    SYNTHESIS_SCALING = 4

    def __init__(
        self,
        optimization: str = "Space",
        verbose: bool = False,
    ):
        self.optimization = optimization
        getcontext().prec = 100  # need some extra precision for this calculation

    def _minimize_code_distance(
        self,
        compiled_program: CompiledQuantumProgram,
        hardware_failure_tolerance: float,
        magic_state_factory: MagicStateFactory,
        n_t_gates_per_rotation: float,
        hw_model: BasicArchitectureModel,
        min_d: int = 4,
        max_d: int = 200,
    ) -> int:

        for code_distance in range(min_d, max_d):
            num_logical_qubits, total_cycles = self.get_logical_qubits_and_num_cycles(
                compiled_program,
                magic_state_factory,
                n_t_gates_per_rotation,
                code_distance,
            )
            st_volume_in_logical_qubit_cycles = num_logical_qubits * total_cycles

            ec_error_rate_at_this_distance = get_total_logical_failure_rate(
                hw_model,
                st_volume_in_logical_qubit_cycles,
                code_distance,
            )

            if ec_error_rate_at_this_distance < hardware_failure_tolerance:
                return code_distance

        raise RuntimeError(
            f"Required distance is greater than maximum allowable distance: {max_d}."
        )

    def get_logical_qubits_and_num_cycles(
        self,
        compiled_program: CompiledQuantumProgram,
        magic_state_factory: MagicStateFactory,
        n_t_gates_per_rotation: float,
        code_distance: int,
    ):
        cycles_per_subroutine = [0 for _ in len(compiled_program.subroutines)]

        if self.optimization == "Space":
            # use a single factory
            num_logical_qubits = 2 * compiled_program.num_logical_qubits
            for i, subroutine in enumerate(compiled_program.subroutines):
                for layer in range(subroutine.num_layers):
                    num_t_states_in_this_layer = (
                        n_t_gates_per_rotation * subroutine.rotations_per_layer[layer]
                        + subroutine.t_states_per_layer[layer]
                    )
                    num_distillations_in_this_layer = (
                        num_t_states_in_this_layer
                        / magic_state_factory.n_t_gates_produced_per_distillation
                    )
                    graph_preparation_cycles_in_this_layer = (
                        subroutine.graph_creation_tocks_per_layer[layer] * code_distance
                    )
                    cycles_per_subroutine[i] += (
                        # prepare graph state, then distill and deliver T states
                        graph_preparation_cycles_in_this_layer
                        + num_distillations_in_this_layer
                        * (
                            magic_state_factory.distillation_time_in_cycles
                            + code_distance  # 1 tock to deliver T state
                        )
                    )
        elif self.optimization == "Time":
            if compiled_program.n_rotation_gates == 0:
                # If there are no rotation gates, we can use a single factory
                num_factories_per_logical_qubit = 1
            else:
                # Use n_t_gates_per_rotation factories for each logical qubit
                num_factories_per_logical_qubit = n_t_gates_per_rotation

            num_factories_per_logical_qubit /= (
                magic_state_factory.n_t_gates_produced_per_distillation
            )

            factory_width = magic_state_factory.space[1]
            factory_width_in_logical_qubit_side_lengths = factory_width / (
                2 ** (1 / 2) * code_distance  # logical qubit side length
            )
            # for each logical qubit, add enough factories to cover a single
            # node which can represent a distillation or a rotation
            num_logical_qubits = (
                num_factories_per_logical_qubit * compiled_program.num_logical_qubits
                # bus qubits which span factory sides
                * factory_width_in_logical_qubit_side_lengths
                + compiled_program.num_logical_qubits  # logical qubits for computation
            )
            for i, subroutine in enumerate(compiled_program.subroutines):
                for layer in range(subroutine.num_layers):
                    cycles_per_subroutine[i] += (
                        # Distill T states and prepare graph state in parallel so if the
                        # cycles needed to prepare the graph state are less than the
                        # cycles needed to distill the T states, then we can ignore the
                        # graph state preparation time.
                        max(
                            subroutine.graph_creation_tocks_per_layer[layer]
                            * code_distance,
                            magic_state_factory.distillation_time_in_cycles,
                        )
                        # cycles to deliver T states to the logical qubits
                        # here we are rate limited by access to the logical qubit
                        + code_distance * num_factories_per_logical_qubit
                        # assume that each T state from a given distillation is
                        # delivered in a different tock (pessimistic assumption)
                        * magic_state_factory.n_t_gates_produced_per_distillation
                    )
        else:
            raise ValueError(
                f"Unknown optimization: {self.optimization}. "
                "Should be either 'Time' or 'Space'."
            )

        total_cycles = 0
        for subroutine in compiled_program.subroutine_sequence:
            total_cycles += cycles_per_subroutine[subroutine]

        return num_logical_qubits, total_cycles

    def _get_time_per_circuit_in_seconds(
        self,
        graph_data: GraphData,
        code_distance: int,
        n_total_t_gates: float,
        magic_state_factory: MagicStateFactory,
    ) -> float:
        if self.optimization == "Space":
            return (
                6
                * self.hw_model.surface_code_cycle_time_in_seconds
                * (
                    graph_data.n_measurement_steps * code_distance
                    + (magic_state_factory.distillation_time_in_cycles + code_distance)
                    * n_total_t_gates
                )
            )
        elif self.optimization == "Time":
            return (
                6
                * self.hw_model.surface_code_cycle_time_in_seconds
                * (
                    graph_data.n_measurement_steps * code_distance
                    + magic_state_factory.distillation_time_in_cycles
                    + code_distance
                )
            )
        else:
            raise NotImplementedError(
                "Must use either Time or Space optimal estimator."
            )

    def _get_n_physical_qubits(
        self,
        graph_data: GraphData,
        code_distance: int,
        magic_state_factory: MagicStateFactory,
    ) -> int:
        patch_size =
        if self.optimization == "Space":
            return (
                2 * graph_data.num_logical_qubits * patch_size
                + magic_state_factory.qubits
            )
        elif self.optimization == "Time":
            return ceil(
                graph_data.num_logical_qubits * patch_size
                + 2 ** (0.5)
                * graph_data.n_measurement_steps
                * magic_state_factory.space[0]
                + magic_state_factory.qubits * graph_data.n_measurement_steps
            )
        else:
            raise NotImplementedError(
                "Must use either Time or Space optimal estimator."
            )

    def estimate_resources_from_compiled_implementation(
        self,
        compiled_algorithm_implementation,
        hw_model: BasicArchitectureModel,
        decoder_model: Optional[DecoderModel] = None,
        magic_state_factory_iterator: Optional[Iterable[MagicStateFactory]] = None,
    ) -> GraphResourceInfo:
        magic_state_factory_iterator = iter(
            magic_state_factory_iterator or iter_litinski_factories(hw_model)
        )
        n_rotation_gates = compiled_algorithm_implementation.n_rotation_gates

        this_transpilation_failure_tolerance = (
            compiled_algorithm_implementation.error_budget.transpilation_failure_tolerance
        )
        hardware_failure_tolerance = (
            compiled_algorithm_implementation.error_budget.hardware_failure_tolerance
        )
        while True:
            magic_state_factory_found = False
            for magic_state_factory in magic_state_factory_iterator:
                per_gate_synthesis_accuracy = 1 - (
                    1 - Decimal(this_transpilation_failure_tolerance)
                ) ** Decimal(1 / n_rotation_gates)
                n_t_gates_per_rotation = self.SYNTHESIS_SCALING * int(
                    (1 / per_gate_synthesis_accuracy).log10() / Decimal(2).log10()
                )

                code_distance = self._minimize_code_distance(
                    compiled_algorithm_implementation.program,
                    hardware_failure_tolerance,
                    magic_state_factory,
                    n_t_gates_per_rotation,
                    hw_model,
                )
                this_logical_cell_error_rate = logical_cell_error_rate(
                    self.hw_model.physical_qubit_error_rate, code_distance
                )

                # Ensure we can ignore errors from magic state distillation.
                if (
                    magic_state_factory.distilled_magic_state_error_rate
                    < this_logical_cell_error_rate
                ):
                    magic_state_factory_found = True
                    break
            if not magic_state_factory_found:
                warnings.warn(
                    "No viable magic_state_factory found! Returning null results.",
                    RuntimeWarning,
                )
                return GraphResourceInfo(
                    code_distance=-1,
                    logical_error_rate=1.0,
                    # estimate the number of logical qubits using max node degree
                    n_logical_qubits=compiled_algorithm_implementation.program.num_logical_qubits,
                    total_time_in_seconds=0.0,
                    n_physical_qubits=0,
                    magic_state_factory_name="No MagicStateFactory Found",
                    decoder_info=None,
                    routing_to_measurement_volume_ratio=0.0,
                    extra=compiled_algorithm_implementation.program,
                )
            if this_transpilation_failure_tolerance < this_logical_cell_error_rate:
                # if the t gates typically do not come from rotation gates, then
                # then you will have to restart the calculation from scratch.
                if (
                    compiled_algorithm_implementation.program.n_t_gates
                    < 0.01 * compiled_algorithm_implementation.program.n_rotation_gates
                ):
                    raise RuntimeError(
                        "Run estimate again with lower synthesis failure tolerance."
                    )
                if this_transpilation_failure_tolerance < 1e-10:
                    warnings.warn(
                        "Synthesis tolerance low. Smaller problem size recommended.",
                        RuntimeWarning,
                    )
                this_transpilation_failure_tolerance /= 10
            else:
                break

        # get error rate after correction
        num_logical_qubits, num_cycles = self.get_logical_qubits_and_num_cycles(
            compiled_algorithm_implementation.program,
            magic_state_factory,
            n_t_gates_per_rotation,
            code_distance,
        )

        st_volume_in_logical_qubit_cycles = num_logical_qubits * num_cycles

        total_logical_error_rate = get_total_logical_failure_rate(
            hw_model,
            st_volume_in_logical_qubit_cycles,
            code_distance,
        )

        # get number of physical qubits needed for the computation
        n_physical_qubits = physical_qubits_per_logical_qubit(code_distance) * num_logical_qubits

        # get total time to run algorithm
        time_per_circuit_in_seconds = 6 * num_cycles * hw_model.surface_code_cycle_time_in_seconds

        total_time_in_seconds = time_per_circuit_in_seconds * compiled_algorithm_implementation.n_shots

        decoder_info = get_decoder_info(
            hw_model,
            decoder_model,
            code_distance,
            st_volume_in_logical_qubit_cycles,
            num_logical_qubits,
        )

        resource_info = GraphResourceInfo(
            code_distance=code_distance,
            logical_error_rate=total_logical_error_rate,
            # estimate the number of logical qubits using max node degree
            n_logical_qubits=num_logical_qubits,
            total_time_in_seconds=total_time_in_seconds,
            n_physical_qubits=n_physical_qubits,
            magic_state_factory_name=magic_state_factory.name,
            decoder_info=decoder_info,
            routing_to_measurement_volume_ratio=None,
            extra=None,
        )

        resource_info.hardware_resource_info = (
            hw_model.get_hardware_resource_estimates(resource_info)
            if isinstance(hw_model, DetailedArchitectureModel)
            else None
        )

        return resource_info


def prepare_program_for_compilation(implementation: QuantumProgram) -> QuantumProgram:
    implementation.program = compile_to_native_gates(implementation.program)
    if transpile_to_clifford_t:
        transpile_to_clifford_t(implementation)
