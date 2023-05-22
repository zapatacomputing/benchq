from decimal import Decimal, getcontext
from math import ceil
from typing import Optional

import networkx as nx
from graph_state_generation.optimizers import greedy_stabilizer_measurement_scheduler
from graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler

from ...data_structures import (
    AlgorithmImplementation,
    BasicArchitectureModel,
    DecoderInfo,
    DecoderModel,
    GraphData,
    GraphPartition,
    GraphResourceInfo,
)
from ..magic_state_distillation import Widget, WidgetIterator

INITIAL_SYNTHESIS_ACCURACY = 0.0001


def substrate_scheduler(graph: nx.Graph) -> TwoRowSubstrateScheduler:
    connected_graph = graph.copy()
    connected_graph.remove_nodes_from(list(nx.isolates(graph)))  # remove isolated nodes
    connected_graph = nx.convert_node_labels_to_integers(connected_graph)
    scheduler_only_compiler = TwoRowSubstrateScheduler(
        connected_graph, stabilizer_scheduler=greedy_stabilizer_measurement_scheduler
    )
    scheduler_only_compiler.run()
    return scheduler_only_compiler


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
    """

    def __init__(
        self,
        hw_model: BasicArchitectureModel,
        decoder_model: Optional[DecoderModel] = None,
        optimization: str = "space",
    ):
        self.hw_model = hw_model
        self.decoder_model = decoder_model
        self.optimization = optimization
        self.widget: Optional[Widget] = None

    # Assumes gridsynth scaling
    SYNTHESIS_SCALING = 4

    def _get_n_measurement_steps(self, graph) -> int:
        return len(substrate_scheduler(graph).measurement_steps)

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
        ec_failure_tolerance: float,
        min_d: int = 4,
        max_d: int = 100,
    ) -> int:
        for code_distance in range(min_d, max_d):
            ec_error_rate_at_this_distance = 1 - (
                1 - self._logical_cell_error_rate(code_distance)
            ) ** self.get_logical_st_volume(n_total_t_gates, graph_data, code_distance)

            if ec_error_rate_at_this_distance < ec_failure_tolerance:
                return code_distance

        raise RuntimeError(f"Not found good error rates under distance code: {max_d}.")

    def _logical_cell_error_rate(self, distance: int) -> float:
        return (
            1
            - (
                1
                - 0.3
                * (70 * self.hw_model.physical_gate_error_rate) ** ((distance + 1) / 2)
            )
            ** distance
        )

    def get_logical_st_volume(
        self, n_total_t_gates: int, graph_data: GraphData, code_distance: int
    ):
        assert isinstance(self.widget, Widget)

        # For example, check that we are properly including/excluding
        # the distillation spacetime volume
        if self.optimization == "space":
            V_graph = (
                2
                * graph_data.max_graph_degree
                * graph_data.n_measurement_steps
                * code_distance
            )
            V_measure = (
                2
                * graph_data.max_graph_degree
                * n_total_t_gates
                * (self.widget.time + code_distance)
            )
        elif self.optimization == "time":
            V_graph = (
                2 * graph_data.n_nodes * graph_data.n_measurement_steps * code_distance
            )
            V_measure = (
                n_total_t_gates
                * self.widget.space[1]
                * (self.widget.time + code_distance)
                / (2 ** (1 / 2) * code_distance + 1)
            )
        else:
            raise ValueError(
                f"Unknown optimization: {self.optimization}. "
                "Should be either 'time' or 'space'."
            )
        return V_graph + V_measure

    def find_max_decodable_distance(self, min_d=4, max_d=100):
        max_distance = 0
        for distance in range(min_d, max_d):
            time_for_logical_operation = (
                6 * self.hw_model.physical_gate_time_in_seconds * distance
            )
            if self.decoder_model.delay(distance) < time_for_logical_operation:
                max_distance = distance

        return max_distance

    def get_n_total_t_gates(
        self, n_t_gates: int, n_rotation_gates: int, synthesis_failure_tolerance: float
    ) -> int:
        getcontext().prec = 100
        if n_rotation_gates != 0:
            per_gate_synthesis_accuracy = 1 - (
                1 - Decimal(synthesis_failure_tolerance)
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
    ) -> float:
        assert isinstance(self.widget, Widget)

        if self.optimization == "time":
            return (
                6
                * self.hw_model.physical_gate_time_in_seconds
                * (
                    graph_data.n_measurement_steps * code_distance
                    + self.widget.time
                    + code_distance
                )
            )
        elif self.optimization == "space":
            return (
                6
                * self.hw_model.physical_gate_time_in_seconds
                * (
                    graph_data.n_measurement_steps * code_distance
                    + (self.widget.time + code_distance) * n_total_t_gates
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
    ) -> int:
        assert isinstance(self.widget, Widget)
        patch_size = 2 * code_distance**2
        if self.optimization == "time":
            return ceil(
                graph_data.max_graph_degree * patch_size
                + 2 ** (0.5) * graph_data.n_measurement_steps * self.widget.space[0]
                + self.widget.qubits * graph_data.n_measurement_steps
            )
        elif self.optimization == "space":
            return 2 * graph_data.max_graph_degree * patch_size + self.widget.qubits
        else:
            raise NotImplementedError(
                "Must use either time or space optimal estimator."
            )

    def estimate_resources_from_graph_data(
        self,
        graph_data: GraphData,
        algorithm_implementation: AlgorithmImplementation,
    ) -> GraphResourceInfo:
        synthesis_failure_tolerance = 10 * (
            algorithm_implementation.error_budget.synthesis_failure_tolerance
        )

        for this_synthesis_failure_tolerance in [
            synthesis_failure_tolerance * (0.1**i) for i in range(10)
        ]:
            for widget in WidgetIterator(self.hw_model):
                if "20-to-4" in widget.name:
                    graph_data.n_measurement_steps //= 4
                self.widget = widget
                n_total_t_gates = self.get_n_total_t_gates(
                    graph_data.n_t_gates,
                    graph_data.n_rotation_gates,
                    this_synthesis_failure_tolerance,
                )
                code_distance = self._minimize_code_distance(
                    n_total_t_gates,
                    graph_data,
                    this_synthesis_failure_tolerance,
                )
                _logical_cell_error_rate = self._logical_cell_error_rate(code_distance)

                if widget.p_out < _logical_cell_error_rate:
                    break
                elif "20-to-4" in widget.name:
                    graph_data.n_measurement_steps *= 4
            if this_synthesis_failure_tolerance < _logical_cell_error_rate:
                if graph_data.n_t_gates != 0:
                    # re-run estimates with new synthesis failure tolerance
                    raise RuntimeError(
                        "Run estimate again with lower synthesis failure tolerance."
                    )
            else:
                break

        print("total t gates:" + str(n_total_t_gates))

        # get error rate after correction
        logical_cell_error_rate = self._logical_cell_error_rate(code_distance)
        space_time_volume = self.get_logical_st_volume(
            n_total_t_gates, graph_data, code_distance
        )

        total_logical_error_rate = logical_cell_error_rate * space_time_volume

        # get number of physical qubits needed for the computation
        n_physical_qubits = self._get_n_physical_qubits(graph_data, code_distance)

        # get total time to run algorithm
        time_per_circuit_in_seconds = self._get_time_per_circuit_in_seconds(
            graph_data, code_distance, n_total_t_gates
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
        if self.decoder_model:
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
            decoder_info = None

        return GraphResourceInfo(
            code_distance=code_distance,
            logical_error_rate=total_logical_error_rate,
            # estimate the number of logical qubits using max node degree
            n_logical_qubits=graph_data.max_graph_degree,
            total_time_in_seconds=total_time_in_seconds,
            n_physical_qubits=n_physical_qubits,
            decoder_info=decoder_info,
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
            return resource_info
        else:
            raise NotImplementedError(
                "Resource estimation without combining subgraphs is not yet "
                "supported."
            )
