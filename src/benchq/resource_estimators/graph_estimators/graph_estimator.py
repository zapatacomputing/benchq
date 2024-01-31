import time
import warnings
from dataclasses import replace
from decimal import Decimal, getcontext
from math import ceil
from typing import Iterable, Optional

import networkx as nx
from graph_state_generation.optimizers import (
    fast_maximal_independent_set_stabilizer_reduction,
    greedy_stabilizer_measurement_scheduler,
)
from graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler

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
from .transformers import remove_isolated_nodes_from_graph

INITIAL_SYNTHESIS_ACCURACY = 0.0001


def substrate_scheduler(graph: nx.Graph, preset: str) -> TwoRowSubstrateScheduler:
    """A simple interface for running the substrate scheduler. Can be run quickly or
    optimized for smaller runtime. Using the "optimized" preset can halve the number
    of measurement steps, but takes about 100x longer to run. It's probably only
    suitable for graphs with less than 10^5 nodes.

    Args:
        graph (nx.Graph): Graph to create substrate schedule for.
        preset (str): Can optimize for speed ("fast") or for smaller number of
            measurement steps ("optimized").

    Returns:
        TwoRowSubstrateScheduler: A substrate scheduler object with the schedule
            already created.
    """
    cleaned_graph = remove_isolated_nodes_from_graph(graph)[1]

    print("starting substrate scheduler")
    start = time.time()
    if preset == "fast":
        compiler = TwoRowSubstrateScheduler(
            cleaned_graph,
            stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
        )
    elif preset == "optimized":
        compiler = TwoRowSubstrateScheduler(
            cleaned_graph,
            pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
            stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
        )
    else:
        raise ValueError(
            f"Unknown preset: {preset}. Should be either 'fast' or 'optimized'."
        )
    compiler.run()
    end = time.time()
    print("substrate scheduler took", end - start, "seconds")
    return compiler


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
            ("time") or the resources needed to run the algorithm with the smallest
            number of physical qubits ("space").
        substrate_scheduler_preset (str): Optimize for speed ("fast") so that it can
            be run on larger graphs or for lower resource estimates ("optimized"). For
            graphs of sizes in the thousands of nodes or higher, "fast" is recommended.
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
        hw_model: BasicArchitectureModel,
        decoder_model: Optional[DecoderModel] = None,
        optimization: str = "space",
        substrate_scheduler_preset: str = "fast",
        magic_state_factory_iterator: Optional[Iterable[MagicStateFactory]] = None,
    ):
        self.hw_model = hw_model
        self.decoder_model = decoder_model
        self.optimization = optimization
        self.substrate_scheduler_preset = substrate_scheduler_preset
        getcontext().prec = 100  # need some extra precision for this calculation
        self.magic_state_factory_iterator = (
            magic_state_factory_iterator or iter_litinski_factories(hw_model)
        )

    def _get_n_measurement_steps(self, graph) -> int:
        compiler = substrate_scheduler(graph, self.substrate_scheduler_preset)
        n_measurement_steps = len(compiler.measurement_steps)
        return n_measurement_steps

    def _get_graph_data_for_single_graph(self, problem: GraphPartition) -> GraphData:
        graph = problem.subgraphs[0]
        print("getting max graph degree")
        max_graph_degree = max(deg for _, deg in graph.degree())
        n_measurement_steps = self._get_n_measurement_steps(graph)
        return GraphData(
            max_graph_degree=max_graph_degree,
            n_nodes=graph.number_of_nodes(),
            n_t_gates=problem.n_t_gates,
            n_rotation_gates=problem.n_rotation_gates,
            n_measurement_steps=n_measurement_steps,
        )

    def _minimize_code_distance(
        self,
        n_total_t_gates: int,
        graph_data: GraphData,
        hardware_failure_tolerance: float,
        magic_state_factory: MagicStateFactory,
        min_d: int = 4,
        max_d: int = 200,
    ) -> int:
        for code_distance in range(min_d, max_d):
            logical_st_volume = self.get_logical_st_volume(
                n_total_t_gates, graph_data, code_distance, magic_state_factory
            )
            ec_error_rate_at_this_distance = get_total_logical_failure_rate(
                self.hw_model,
                logical_st_volume,
                code_distance,
            )

            if ec_error_rate_at_this_distance < hardware_failure_tolerance:
                return code_distance

        raise RuntimeError(
            f"Required distance is greater than maximum allowable distance: {max_d}."
        )

    def _get_v_graph(
        self,
        graph_data: GraphData,
        code_distance: int,
    ):
        if self.optimization == "space":
            V_graph = (
                2
                * graph_data.max_graph_degree
                * graph_data.n_measurement_steps
                * code_distance
            )
        elif self.optimization == "time":
            V_graph = (
                2 * graph_data.n_nodes * graph_data.n_measurement_steps * code_distance
            )
        else:
            raise ValueError(
                f"Unknown optimization: {self.optimization}. "
                "Should be either 'time' or 'space'."
            )
        return V_graph

    def _get_v_measure(
        self,
        n_total_t_gates: int,
        graph_data: GraphData,
        code_distance: int,
        magic_state_factory: MagicStateFactory,
    ):
        if self.optimization == "space":
            V_measure = (
                2
                * graph_data.max_graph_degree
                * n_total_t_gates
                * (magic_state_factory.distillation_time_in_cycles + code_distance)
            )
        elif self.optimization == "time":
            V_measure = (
                n_total_t_gates
                * magic_state_factory.space[1]
                * (magic_state_factory.distillation_time_in_cycles + code_distance)
                / (2 ** (1 / 2) * code_distance + 1)
            )
        else:
            raise ValueError(
                f"Unknown optimization: {self.optimization}. "
                "Should be either 'time' or 'space'."
            )
        return V_measure

    def get_logical_st_volume(
        self,
        n_total_t_gates: int,
        graph_data: GraphData,
        code_distance: int,
        magic_state_factory: MagicStateFactory,
    ):
        return self._get_v_graph(graph_data, code_distance) + self._get_v_measure(
            n_total_t_gates, graph_data, code_distance, magic_state_factory
        )

    def get_n_total_t_gates(
        self,
        n_t_gates: int,
        n_rotation_gates: int,
        transpilation_failure_tolerance: float,
    ) -> int:
        if n_rotation_gates != 0:
            per_gate_synthesis_accuracy = 1 - (
                1 - Decimal(transpilation_failure_tolerance)
            ) ** Decimal(1 / n_rotation_gates)

            n_t_gates_used_at_measurement = (
                n_rotation_gates
                * self.SYNTHESIS_SCALING
                * int((1 / per_gate_synthesis_accuracy).log10() / Decimal(2).log10())
            )
        else:
            n_t_gates_used_at_measurement = 0

        return n_t_gates + n_t_gates_used_at_measurement

    def _get_time_per_circuit_in_seconds(
        self,
        graph_data: GraphData,
        code_distance: int,
        n_total_t_gates: float,
        magic_state_factory: MagicStateFactory,
    ) -> float:
        if self.optimization == "space":
            return (
                6
                * self.hw_model.surface_code_cycle_time_in_seconds
                * (
                    graph_data.n_measurement_steps * code_distance
                    + (magic_state_factory.distillation_time_in_cycles + code_distance)
                    * n_total_t_gates
                )
            )
        elif self.optimization == "time":
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
                "Must use either time or space optimal estimator."
            )

    def _get_n_physical_qubits(
        self,
        graph_data: GraphData,
        code_distance: int,
        magic_state_factory: MagicStateFactory,
    ) -> int:
        patch_size = physical_qubits_per_logical_qubit(code_distance)
        if self.optimization == "space":
            return (
                2 * graph_data.max_graph_degree * patch_size
                + magic_state_factory.qubits
            )
        elif self.optimization == "time":
            return ceil(
                graph_data.max_graph_degree * patch_size
                + 2 ** (0.5)
                * graph_data.n_measurement_steps
                * magic_state_factory.space[0]
                + magic_state_factory.qubits * graph_data.n_measurement_steps
            )
        else:
            raise NotImplementedError(
                "Must use either time or space optimal estimator."
            )

    def estimate_resources_from_graph_data(
        self,
        graph_data: GraphData,
        algorithm_implementation: AlgorithmImplementation,
    ) -> GraphResourceInfo:
        this_transpilation_failure_tolerance = (
            algorithm_implementation.error_budget.transpilation_failure_tolerance
        )

        magic_state_factory_iterator = iter(self.magic_state_factory_iterator)

        # Approximate the number of logical qubits for the bus architecture
        # TODO: Update to accommodate the space vs time optimal compilation
        # once we have the substrate scheduler properly implemented.
        n_logical_qubits = 2 * graph_data.max_graph_degree

        while True:
            magic_state_factory_found = False
            for magic_state_factory in magic_state_factory_iterator:
                tmp_graph_data = replace(
                    graph_data,
                    n_nodes=ceil(
                        graph_data.n_nodes
                        / magic_state_factory.n_t_gates_produced_per_distillation
                    ),
                    n_t_gates=ceil(
                        graph_data.n_t_gates
                        / magic_state_factory.n_t_gates_produced_per_distillation
                    ),
                )

                n_total_t_gates = self.get_n_total_t_gates(
                    tmp_graph_data.n_t_gates,
                    tmp_graph_data.n_rotation_gates,
                    this_transpilation_failure_tolerance,
                )
                code_distance = self._minimize_code_distance(
                    n_total_t_gates,
                    tmp_graph_data,
                    algorithm_implementation.error_budget.hardware_failure_tolerance,
                    magic_state_factory,
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
                    n_logical_qubits=n_logical_qubits,
                    total_time_in_seconds=0.0,
                    n_physical_qubits=0,
                    magic_state_factory_name="No MagicStateFactory Found",
                    decoder_info=None,
                    routing_to_measurement_volume_ratio=0.0,
                    extra=graph_data,
                )
            if this_transpilation_failure_tolerance < this_logical_cell_error_rate:
                # if the t gates typically do not come from rotation gates, then
                # then you will have to restart the calculation from scratch.
                if graph_data.n_t_gates < 0.01 * graph_data.n_nodes:
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
                graph_data = tmp_graph_data
                break

        # get error rate after correction
        space_time_volume = self.get_logical_st_volume(
            n_total_t_gates, graph_data, code_distance, magic_state_factory
        )

        graph_measure_ratio = (
            self._get_v_graph(graph_data, code_distance) / space_time_volume
        )

        logical_st_volume = self.get_logical_st_volume(
            n_total_t_gates, graph_data, code_distance, magic_state_factory
        )

        total_logical_error_rate = get_total_logical_failure_rate(
            self.hw_model,
            logical_st_volume,
            code_distance,
        )

        # get number of physical qubits needed for the computation
        n_physical_qubits = self._get_n_physical_qubits(
            graph_data, code_distance, magic_state_factory
        )

        # get total time to run algorithm
        time_per_circuit_in_seconds = self._get_time_per_circuit_in_seconds(
            graph_data, code_distance, n_total_t_gates, magic_state_factory
        )

        # The total space time volume, prior to measurements is,
        # V_{graph}= 2\Delta S (where we measure each of the steps,
        # S in terms of tocks, corresponding to d cycle times.
        # d will be solved for later).  For each distilled T-state,
        # C-cycles are needed to prepare the state and 1-Tock is required
        # to interact the state with the graph node and measure it in
        # the X or Z-basis.  Hence for each node measurement (assuming
        # T-basis measurements), the volume increases to,
        # V = 2*Delta*S*d+ 2*Delta*(C+d).

        total_time_in_seconds = (
            time_per_circuit_in_seconds * algorithm_implementation.n_shots
        )

        decoder_info = get_decoder_info(
            self.hw_model,
            self.decoder_model,
            code_distance,
            space_time_volume,
            n_logical_qubits,
        )

        return GraphResourceInfo(
            code_distance=code_distance,
            logical_error_rate=total_logical_error_rate,
            n_logical_qubits=n_logical_qubits,
            total_time_in_seconds=total_time_in_seconds,
            n_physical_qubits=n_physical_qubits,
            magic_state_factory_name=magic_state_factory.name,
            decoder_info=decoder_info,
            routing_to_measurement_volume_ratio=graph_measure_ratio,
            extra=graph_data,
        )

    def estimate(
        self, algorithm_implementation: AlgorithmImplementation
    ) -> GraphResourceInfo:
        assert isinstance(algorithm_implementation.program, GraphPartition)
        if len(algorithm_implementation.program.subgraphs) == 1:
            graph_data = self._get_graph_data_for_single_graph(
                algorithm_implementation.program
            )
            resource_info = self.estimate_resources_from_graph_data(
                graph_data, algorithm_implementation
            )
            if isinstance(self.hw_model, DetailedArchitectureModel):
                resource_info.hardware_resource_info = (
                    self.hw_model.get_hardware_resource_estimates(resource_info)
                )
            return resource_info
        else:
            raise NotImplementedError(
                "Resource estimation without combining subgraphs is not yet "
                "supported."
            )
