import dataclasses
import warnings
from dataclasses import replace
from decimal import Decimal, getcontext
from math import ceil
from typing import Callable, Iterable, Optional

import networkx as nx
from graph_state_generation.optimizers import (
    fast_maximal_independent_set_stabilizer_reduction,
    greedy_stabilizer_measurement_scheduler,
)
from graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler

from ...data_structures import (
    AlgorithmImplementation,
    BasicArchitectureModel,
    DecoderInfo,
    DecoderModel,
    GraphData,
    GraphDataResourceInfo,
    GraphPartition,
    GraphResourceInfo,
)
from ..magic_state_distillation import Widget, default_widget_list

INITIAL_SYNTHESIS_ACCURACY = 0.0001


def substrate_scheduler(graph: nx.Graph, preset: str) -> TwoRowSubstrateScheduler:
    """A simple interface for running the substrate scheduler. Can be run quickly or
    optimized for smaller runtime.

    Args:
        graph (nx.Graph): Graph to create substrate schedule for.
        preset (str): Can optimize for speed ("fast") or for smaller number of
            measurement steps ("optimized").

    Returns:
        TwoRowSubstrateScheduler: A substrate scheduler object with the schedule
            already created.
    """
    connected_graph = graph.copy()
    connected_graph.remove_nodes_from(list(nx.isolates(graph)))  # remove isolated nodes
    connected_graph = nx.convert_node_labels_to_integers(connected_graph)
    if preset == "fast":
        compiler = TwoRowSubstrateScheduler(
            connected_graph,
            stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
        )
    if preset == "optimized":
        compiler = TwoRowSubstrateScheduler(
            graph,
            pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
            stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
        )
    compiler.run()
    return compiler


class GraphResourceEstimator:
    """Estimates resources needed to run an algorithm using graph state compilation.

    ATTRIBUTES:
        hw_model (BasicArchitectureModel): The hardware model to use for the estimate.
            typically, one would choose between the BASIC_SC_ARCHITECTURE_MODEL and
            BASIC_ION_TRAP_ARCHITECTURE_MODEL.
        decoder_model (Optional[DecoderModel]): The decoder model used to estimate.
            If None, no estimates on the number of decoder are provided.
        distillation_widget (str): The distillation widget to use for the estimate.
            The widget is specified as a string of the form "(15-to-1)_7,3,3", where
            the first part specifies the distillation ratio and the second part
            specifies the size of the widget.
        optimization (str): The optimization to use for the estimate. Either estimate
            the resources needed to run the algorithm in the shortest time possible
            ("time") or the resources needed to run the algorithm with the smallest
            number of physical qubits ("space").
        substrate_scheduler_preset (str): Optimize for speed ("fast") so that it can
            be run on larger graphs or for lower resource estimates ("optimized"). For
            graphs of sizes in the thousands of nodes or higher, "fast" is recommended.
        widgets (Optional[Iterable[Widget]]: Widgets to be used during estimation. If
            not provided (or passed None) default_widget_list will select widgets based
            on hw_model parameter.
    """

    def __init__(
        self,
        hw_model: BasicArchitectureModel,
        decoder_model: Optional[DecoderModel] = None,
        optimization: str = "space",
        substrate_scheduler_preset: str = "fast",
        widgets: Optional[Iterable[Widget]] = None,
    ):
        self.hw_model = hw_model
        self.decoder_model = decoder_model
        self.optimization = optimization
        self.substrate_scheduler_preset = substrate_scheduler_preset
        getcontext().prec = 100  # need some extra precision for this calculation
        self.widgets = widgets or default_widget_list(hw_model)

    # Assumes gridsynth scaling
    SYNTHESIS_SCALING = 4

    def _get_n_measurement_steps(self, graph) -> int:
        compiler = substrate_scheduler(graph, self.substrate_scheduler_preset)
        n_steps = len(compiler.measurement_steps)
        return n_steps

    def _get_graph_data_for_single_graph(self, problem: GraphPartition) -> GraphData:
        graph = problem.subgraphs[0]
        max_graph_degree = max(deg for _, deg in graph.degree())
        n_measurement_steps = self._get_n_measurement_steps(graph)
        return GraphData(
            max_graph_degree=max_graph_degree,
            n_nodes=problem.n_nodes,
            n_t_gates=problem.n_t_gates,
            n_rotation_gates=problem.n_rotation_gates,
            n_measurement_steps=n_measurement_steps,
        )

    def _minimize_code_distance(
        self,
        n_total_t_gates: int,
        graph_data: GraphData,
        hardware_failure_tolerance: float,
        widget: Widget,
        min_d: int = 4,
        max_d: int = 200,
    ) -> int:
        for code_distance in range(min_d, max_d):
            ec_error_rate_at_this_distance = self._get_total_logical_failure_rate(
                code_distance, n_total_t_gates, graph_data, widget
            )

            if ec_error_rate_at_this_distance < hardware_failure_tolerance:
                return code_distance

        raise RuntimeError(f"Required distance is greater than {max_d}.")

    def _get_total_logical_failure_rate(
        self, code_distance: int, n_total_t_gates: int, graph_data: GraphData, widget
    ) -> float:
        precise_logical_failure_rate = Decimal(
            self._logical_cell_error_rate(code_distance)
        )
        precise_logical_st_volume = Decimal(
            self.get_logical_st_volume(
                n_total_t_gates, graph_data, code_distance, widget
            )
        )
        return float(
            1 - (1 - precise_logical_failure_rate) ** precise_logical_st_volume
        )

    def _logical_cell_error_rate(self, distance: int) -> float:
        precise_physical_qubit_error_rate = Decimal(
            self.hw_model.physical_qubit_error_rate
        )
        precise_distance = Decimal(distance)
        precise_coefficent = Decimal(0.3)
        return float(
            1
            - (
                1
                - precise_coefficent
                * (70 * precise_physical_qubit_error_rate)
                ** ((precise_distance + 1) / 2)
            )
            ** precise_distance
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
        widget: Widget,
    ):
        if self.optimization == "space":
            V_measure = (
                2
                * graph_data.max_graph_degree
                * n_total_t_gates
                * (widget.time_in_tocks + code_distance)
            )
        elif self.optimization == "time":
            V_measure = (
                n_total_t_gates
                * widget.space[1]
                * (widget.time_in_tocks + code_distance)
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
        widget: Widget,
    ):
        return self._get_v_graph(graph_data, code_distance) + self._get_v_measure(
            n_total_t_gates, graph_data, code_distance, widget
        )

    def find_max_decodable_distance(self, min_d=4, max_d=100):
        max_distance = 0
        for distance in range(min_d, max_d):
            time_for_logical_operation = (
                6 * self.hw_model.surface_code_cycle_time_in_seconds * distance
            )
            if self.decoder_model.delay(distance) < time_for_logical_operation:
                max_distance = distance

        return max_distance

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
        widget: Widget,
    ) -> float:
        if self.optimization == "time":
            return (
                6
                * self.hw_model.physical_qubit_error_rate
                * (
                    graph_data.n_measurement_steps * code_distance
                    + widget.time_in_tocks
                    + code_distance
                )
            )
        elif self.optimization == "space":
            return (
                6
                * self.hw_model.physical_qubit_error_rate
                * (
                    graph_data.n_measurement_steps * code_distance
                    + (widget.time_in_tocks + code_distance) * n_total_t_gates
                )
            )
        else:
            raise NotImplementedError(
                "Must use either time or space optimal estimator."
            )

    def _get_n_physical_qubits(
        self, graph_data: GraphData, code_distance: int, widget: Widget
    ) -> int:
        patch_size = 2 * code_distance**2
        if self.optimization == "time":
            return ceil(
                graph_data.max_graph_degree * patch_size
                + 2 ** (0.5) * graph_data.n_measurement_steps * widget.space[0]
                + widget.qubits * graph_data.n_measurement_steps
            )
        elif self.optimization == "space":
            return 2 * graph_data.max_graph_degree * patch_size + widget.qubits
        else:
            raise NotImplementedError(
                "Must use either time or space optimal estimator."
            )

    def estimate_resources_from_graph_data(
        self,
        graph_data: GraphData,
        algorithm_implementation: AlgorithmImplementation,
    ) -> GraphResourceInfo:
        transpilation_failure_tolerance = 10 * (
            algorithm_implementation.error_budget.transpilation_failure_tolerance
        )

        widget_iterator = iter(self.widgets)

        for this_transpilation_failure_tolerance in [
            transpilation_failure_tolerance * (0.1**i) for i in range(10)
        ]:
            widget_found = False
            for widget in widget_iterator:
                tmp_graph_data = replace(
                    graph_data,
                    n_nodes=ceil(
                        graph_data.n_nodes / widget.n_t_gates_produced_per_cycle
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
                    widget,
                )
                _logical_cell_error_rate = self._logical_cell_error_rate(code_distance)

                if widget.distilled_magic_state_error_rate < _logical_cell_error_rate:
                    widget_found = True
                    break
            if not widget_found:
                raise ValueError("No viable widget found!")
            if this_transpilation_failure_tolerance < _logical_cell_error_rate:
                if graph_data.n_t_gates != 0:
                    # re-run estimates with new synthesis failure tolerance
                    raise RuntimeError(
                        "Run estimate again with lower synthesis failure tolerance."
                    )
            else:
                break

        # get error rate after correction
        space_time_volume = self.get_logical_st_volume(
            n_total_t_gates, graph_data, code_distance, widget
        )

        graph_measure_ratio = (
            self._get_v_graph(graph_data, code_distance) / space_time_volume
        )

        total_logical_error_rate = self._get_total_logical_failure_rate(
            code_distance, n_total_t_gates, graph_data, widget
        )

        # get number of physical qubits needed for the computation
        n_physical_qubits = self._get_n_physical_qubits(
            graph_data, code_distance, widget
        )

        # get total time to run algorithm
        time_per_circuit_in_seconds = self._get_time_per_circuit_in_seconds(
            graph_data, code_distance, n_total_t_gates, widget
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
            time_per_circuit_in_seconds * algorithm_implementation.n_calls
        )

        # get decoder requirements
        if self.decoder_model and self.decoder_model.distance_cap >= code_distance:
            decoder_total_energy_consumption = (
                space_time_volume
                * self.decoder_model.power(code_distance)
                * self.decoder_model.delay(code_distance)
            )
            decoder_power = (
                2
                * graph_data.max_graph_degree
                * self.decoder_model.power(code_distance)
            )
            decoder_area = graph_data.max_graph_degree * self.decoder_model.area(
                code_distance
            )
            max_decodable_distance = self.find_max_decodable_distance()
            decoder_info = DecoderInfo(
                total_energy_consumption=decoder_total_energy_consumption,
                power=decoder_power,
                area=decoder_area,
                max_decodable_distance=max_decodable_distance,
            )
        else:
            if self.decoder_model and self.decoder_model.distance_cap < code_distance:
                warnings.warn("Code distance is too high to be decoded.")
            decoder_info = None

        graph_data_resource_info = GraphDataResourceInfo(
            **dataclasses.asdict(graph_data), graph_measure_ratio=graph_measure_ratio
        )

        return GraphResourceInfo(
            code_distance=code_distance,
            logical_error_rate=total_logical_error_rate,
            # estimate the number of logical qubits using max node degree
            n_logical_qubits=graph_data.max_graph_degree,
            total_time_in_seconds=total_time_in_seconds,
            n_physical_qubits=n_physical_qubits,
            widget_name=widget.name,
            decoder_info=decoder_info,
            extra=graph_data_resource_info,
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
            return resource_info
        else:
            raise NotImplementedError(
                "Resource estimation without combining subgraphs is not yet "
                "supported."
            )
