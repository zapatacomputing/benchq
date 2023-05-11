from dataclasses import dataclass
from math import ceil
from typing import Optional

import networkx as nx
import numpy as np
from graph_state_generation.optimizers import greedy_stabilizer_measurement_scheduler
from graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler

from ...data_structures import (
    AlgorithmImplementation,
    BasicArchitectureModel,
    DecoderModel,
    GraphPartition,
)
from ..magic_state_distillation import get_specs_for_t_state_widget

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


@dataclass
class GraphData:
    """Contains minimal set of data to get a resource estimate for a graph."""

    max_graph_degree: int
    n_nodes: int
    n_t_gates: int
    n_rotation_gates: int
    n_measurement_steps: int


@dataclass
class ResourceInfo:
    """Contains all resource estimated for a problem instance."""

    code_distance: int
    logical_error_rate: float
    n_logical_qubits: int
    n_nodes: int
    n_t_gates: int
    n_rotation_gates: int
    n_physical_qubits: int
    n_measurement_steps: int
    total_time_in_seconds: float
    max_decodable_distance: Optional[int]
    decoder_total_energy_consumption: Optional[float]
    decoder_power: Optional[float]
    decoder_area: Optional[float]

    @property
    def graph_data(self) -> GraphData:
        return GraphData(
            max_graph_degree=self.n_logical_qubits,
            n_nodes=self.n_nodes,
            n_t_gates=self.n_t_gates,
            n_rotation_gates=self.n_rotation_gates,
            n_measurement_steps=self.n_measurement_steps,
        )

    def __repr__(self):
        necessary_info = [
            "code_distance",
            "logical_error_rate",
            "n_logical_qubits",
            "total_time_in_seconds",
            "decoder_total_energy_consumption",
            "decoder_power",
            "decoder_area",
            "n_measurement_steps",
            "n_physical_qubits",
        ]
        return "\n".join(f"{info}: {getattr(self, info)}" for info in necessary_info)


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
        distillation_widget: str = "(15-to-1)_7,3,3",
        optimization: str = "time",
    ):
        self.hw_model = hw_model
        self.decoder_model = decoder_model
        self.widget_specs = get_specs_for_t_state_widget(distillation_widget)
        self.optimization = optimization

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
        # For example, check that we are properly including/excluding
        # the distillation spacetime volume
        space = 2 * graph_data.max_graph_degree
        # Time component assuming all graph nodes are measured sequentially
        time = (
            graph_data.n_measurement_steps * code_distance
            + (self.widget_specs["time"] + code_distance) * n_total_t_gates
        )
        st_volume = space * time
        return st_volume

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
        if n_rotation_gates != 0:
            per_gate_synthesis_accuracy = 1 - (1 - synthesis_failure_tolerance) ** (
                1 / n_rotation_gates
            )

            n_t_gates_used_at_measurement = ceil(
                n_rotation_gates
                * self.SYNTHESIS_SCALING
                * np.log2(1 / per_gate_synthesis_accuracy)
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
        if self.optimization == "time":
            return (
                6
                * self.hw_model.physical_gate_time_in_seconds
                * (
                    graph_data.n_measurement_steps * code_distance
                    + self.widget_specs["time"]
                    + code_distance
                )
            )
        elif self.optimization == "space":
            return (
                6
                * self.hw_model.physical_gate_time_in_seconds
                * (
                    graph_data.n_measurement_steps * code_distance
                    + (self.widget_specs["time"] + code_distance) * n_total_t_gates
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
        if self.optimization == "time":
            # assumes (20-to-4) widget, which is a good approximation for other widgets
            time_optimal_n_measurement_steps = graph_data.n_measurement_steps / 4
            patch_size = 2 * code_distance**2
            return (
                graph_data.max_graph_degree * patch_size
                + 2 ** (0.5)
                * time_optimal_n_measurement_steps
                * self.widget_specs["space"][0]
                + self.widget_specs["qubits"] * time_optimal_n_measurement_steps
            )
        elif self.optimization == "space":
            patch_size = 2 * code_distance**2
            return (
                2 * graph_data.max_graph_degree * patch_size
                + self.widget_specs["qubits"]
            )
        else:
            raise NotImplementedError(
                "Must use either time or space optimal estimator."
            )

    def estimate_resources_from_graph_data(
        self,
        graph_data: GraphData,
        algorithm_implementation: AlgorithmImplementation,
    ) -> ResourceInfo:
        n_total_t_gates = self.get_n_total_t_gates(
            graph_data.n_t_gates,
            graph_data.n_rotation_gates,
            algorithm_implementation.error_budget.synthesis_failure_tolerance,
        )

        code_distance = self._minimize_code_distance(
            n_total_t_gates,
            graph_data,
            algorithm_implementation.error_budget.ec_failure_tolerance,
        )

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
        else:
            decoder_total_energy_consumption = None
            decoder_power = None
            decoder_area = None
            max_decodable_distance = None
        return ResourceInfo(
            code_distance=code_distance,
            logical_error_rate=total_logical_error_rate,
            # estimate the number of logical qubits using max node degree
            n_logical_qubits=graph_data.max_graph_degree,
            n_nodes=graph_data.n_nodes,
            n_t_gates=graph_data.n_t_gates,
            n_rotation_gates=graph_data.n_rotation_gates,
            n_measurement_steps=graph_data.n_measurement_steps,
            total_time_in_seconds=total_time_in_seconds,
            n_physical_qubits=n_physical_qubits,
            decoder_total_energy_consumption=decoder_total_energy_consumption,
            decoder_power=decoder_power,
            decoder_area=decoder_area,
            max_decodable_distance=max_decodable_distance,
        )

    def estimate(
        self, algorithm_implementation: AlgorithmImplementation
    ) -> ResourceInfo:
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
