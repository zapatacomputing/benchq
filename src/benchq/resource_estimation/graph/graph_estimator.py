from dataclasses import dataclass
from typing import Optional

import networkx as nx
import numpy as np
from graph_state_generation.optimizers import greedy_stabilizer_measurement_scheduler
from graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler

from ...data_structures import AlgorithmDescription, DecoderModel, GraphPartition
from ...data_structures.hardware_architecture_models import BasicArchitectureModel

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
    decoder_power: Optional[float]
    decoder_area: Optional[float]

    def __repr__(self):
        necessary_info = [
            "code_distance",
            "logical_error_rate",
            "n_logical_qubits",
            "total_time_in_seconds",
            "decoder_power",
            "decoder_area",
            "n_measurement_steps",
            "n_physical_qubits",
        ]
        return "\n".join(f"{info}: {getattr(self, info)}" for info in necessary_info)


class GraphResourceEstimator:
    def __init__(
        self,
        hw_model: BasicArchitectureModel,
        decoder_model: Optional[DecoderModel] = None,
    ):
        self.hw_model = hw_model
        self.decoder_model = decoder_model

    N_TOCKS_PER_T_GATE_FACTORY = 15
    # We are not sure if names below are the best choice
    # 21 comes from Game of surface codes (Litinski):
    # https://quantum-journal.org/papers/q-2019-03-05-128/
    # We are not sure where does 12 come from
    BOX_WIDTH = 21
    # litinski box is 21x11 but we add one more row for the qubits used to compute
    BOX_HEIGHT = 12

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
        n_t_gates: int,
        max_graph_degree: int,
        ec_failure_tolerance: float,
        min_d: int = 4,
        max_d: int = 100,
    ) -> int:
        for distance in range(min_d, max_d):
            ec_error_rate_at_this_distance = 1 - (
                1 - self._logical_cell_error_rate(distance)
            ) ** self.get_logical_st_volume(n_t_gates, max_graph_degree)

            if ec_error_rate_at_this_distance < ec_failure_tolerance:
                return distance

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

    def get_logical_st_volume(self, n_t_gates: int, max_graph_degree: int):
        num_boxes = np.ceil((max_graph_degree + 1) / self.BOX_WIDTH)
        space = self.BOX_WIDTH * self.BOX_HEIGHT * num_boxes
        # Time component assuming all graph nodes are measured sequentially
        time = self.N_TOCKS_PER_T_GATE_FACTORY * n_t_gates
        return space * time

    def find_max_decodable_distance(self, min_d=4, max_d=100):
        max_distance = 0
        for distance in range(min_d, max_d):
            time_for_logical_operation = (
                6 * self.hw_model.physical_gate_time_in_seconds * distance
            )
            if self.decoder_model.delay(distance) < time_for_logical_operation:
                max_distance = distance

        return max_distance

    def _estimate_resources_from_graph_data(
        self,
        graph_data: GraphData,
        algorithm_description: AlgorithmDescription,
    ) -> ResourceInfo:
        if graph_data.n_rotation_gates != 0:
            per_gate_synthesis_accuracy = 1 - (
                1 - algorithm_description.error_budget.synthesis_failure_tolerance
            ) ** (1 / graph_data.n_rotation_gates)

            n_t_gates_used_at_measurement = (
                graph_data.n_rotation_gates
                * self.SYNTHESIS_SCALING
                * np.log2(1 / per_gate_synthesis_accuracy)
            )
        else:
            n_t_gates_used_at_measurement = 0

        n_total_t_gates = graph_data.n_t_gates + n_t_gates_used_at_measurement

        code_distance = self._minimize_code_distance(
            n_total_t_gates,
            graph_data.max_graph_degree,
            algorithm_description.error_budget.ec_failure_tolerance,
        )

        # get error rate after correction
        logical_cell_error_rate = self._logical_cell_error_rate(code_distance)
        space_time_volume = self.get_logical_st_volume(
            n_total_t_gates, graph_data.max_graph_degree
        )
        total_logical_error_rate = logical_cell_error_rate * space_time_volume

        # get number of physical qubits needed for the computation
        num_boxes = np.ceil((graph_data.max_graph_degree + 1) / self.BOX_WIDTH)
        patch_size = 2 * code_distance**2
        n_physical_qubits = self.BOX_WIDTH * self.BOX_HEIGHT * num_boxes * patch_size

        # get total time to run algorithm
        time_of_logical_t_gate_in_seconds = (
            6 * self.hw_model.physical_gate_time_in_seconds * code_distance
        )
        time_per_circuit_in_seconds = (
            graph_data.n_measurement_steps * time_of_logical_t_gate_in_seconds
            + time_of_logical_t_gate_in_seconds
            * self.N_TOCKS_PER_T_GATE_FACTORY
            * n_total_t_gates
        )
        total_time_in_seconds = (
            time_per_circuit_in_seconds * algorithm_description.n_calls
        )

        # get decoder requirements
        if self.decoder_model:
            decoder_power = space_time_volume * self.decoder_model.power(code_distance)
            decoder_area = graph_data.max_graph_degree * self.decoder_model.area(
                code_distance
            )
            max_decodable_distance = self.find_max_decodable_distance()
        else:
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
            decoder_power=decoder_power,
            decoder_area=decoder_area,
            max_decodable_distance=max_decodable_distance,
        )

    def estimate(self, algorithm_description: AlgorithmDescription) -> ResourceInfo:
        assert isinstance(algorithm_description.program, GraphPartition)
        if len(algorithm_description.program.subgraphs) == 1:
            graph_data = self._get_graph_data_for_single_graph(
                algorithm_description.program
            )
            resource_info = self._estimate_resources_from_graph_data(
                graph_data, algorithm_description
            )
            return resource_info
        else:
            raise NotImplementedError(
                "Resource estimation without combining subgraphs is not yet "
                "supported."
            )
