from dataclasses import dataclass
from typing import Callable, Optional

import networkx as nx
import numpy as np
from graph_state_generation.optimizers import greedy_stabilizer_measurement_scheduler
from graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler

from ...data_structures import BasicArchitectureModel, DecoderModel
from .structs import GraphPartition

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

    max_node_degree: int
    n_nodes: int
    n_measurement_steps: int


@dataclass
class ResourceInfo:
    """Contains all resource estimated for a problem instance."""

    synthesis_multiplier: float
    code_distance: int
    logical_error_rate: float
    n_logical_qubits: int
    n_nodes: int
    n_physical_qubits: int
    n_measurement_steps: int
    total_time: float
    max_decodable_distance: Optional[int]
    decoder_power: Optional[float]
    decoder_area: Optional[float]

    def __repr__(self):
        necessary_info = [
            "code_distance",
            "logical_error_rate",
            "n_logical_qubits",
            "total_time",
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
        combine_partition: bool = True,
    ):
        self.hw_model = hw_model
        self.combine_partition = combine_partition
        self.decoder_model = decoder_model

    N_TOCKS_PER_T_GATE_FACTORY = 15
    # We are not sure if names below are the best choice
    # 21 comes from Game of surface codes (Litinski):
    # https://quantum-journal.org/papers/q-2019-03-05-128/
    # We are not sure where does 12 come from
    BOX_WIDTH = 21
    BOX_HEIGHT = 12

    # Assumes gridsynth scaling and full Euler angle decompositions
    SYNTHESIS_SCALING = 3 * 4

    def _logical_cell_failure_rate(self, distance: int) -> float:
        return (
            # 0.3 and 70 come from numerical simulations
            distance
            * 0.3
            * (70 * self.hw_model.physical_gate_error_rate) ** ((distance + 1) / 2)
        )

    def _minimize_code_distance(
        self,
        n_nodes: int,
        max_node_degree: int,
        error_budget,
        error_rate: Callable[[int, int, int], float],
        min_d: int = 4,
        max_d: int = 100,
    ) -> int:
        target_error_rate = error_budget["total_error"] * error_budget["ec_error_rate"]

        for distance in range(min_d, max_d):
            if error_rate(distance, n_nodes, max_node_degree) < target_error_rate:
                return distance

        raise RuntimeError(f"Not found good error rates under distance code: {max_d}.")

    def _get_n_measurement_steps(self, graph) -> int:
        return len(substrate_scheduler(graph).measurement_steps)

    def _ec_error_rate_delayed_gate_synthesis(
        self, distance: int, n_nodes: int, max_node_degree: int
    ) -> float:
        _, ec_error_rate = self.balance_logical_error_rate_and_synthesis_accuracy(
            n_nodes, distance, max_node_degree
        )
        return ec_error_rate

    def _ec_error_rate(
        self, distance: int, n_nodes: int, max_node_degree: int
    ) -> float:
        return self._logical_cell_failure_rate(distance) * self.get_logical_st_volume(
            n_nodes, max_node_degree
        )

    def get_logical_st_volume(self, n_nodes: int, max_node_degree: int):
        num_boxes = np.ceil((max_node_degree + 1) / self.BOX_WIDTH)
        space = self.BOX_WIDTH * self.BOX_HEIGHT * num_boxes
        # Time component assuming all graph nodes are measured sequentially
        time = self.N_TOCKS_PER_T_GATE_FACTORY * n_nodes
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

    # TODO: We need to make sure it's doing scientifically what it should be doing
    def balance_logical_error_rate_and_synthesis_accuracy(
        self, n_nodes, distance, max_node_degree
    ):
        """
        This function is basically finding such a value of synthesis error rate, that
        it is 1/(12*N) smaller than circuit error rate, where N is the number of nodes
        in the graph.
        """
        current_synthesis_accuracy = INITIAL_SYNTHESIS_ACCURACY
        for _ in range(20):
            ec_error_rate = self._ec_error_rate(
                distance,
                n_nodes,
                max_node_degree,
            )
            new_synthesis_accuracy = (1 / (12 * n_nodes)) * ec_error_rate
            # This is for cases where the algorithm diverges terribly, to avoid
            # "divide by 0" and similar warnings.
            # TODO: Hacky! We should come up with a more stable solution in future!
            if new_synthesis_accuracy <= 0 or np.isnan(new_synthesis_accuracy):
                return np.inf, np.inf

            current_synthesis_accuracy = new_synthesis_accuracy
        return current_synthesis_accuracy, ec_error_rate

    def _get_graph_data(self, graph: nx.Graph, n_nodes: int) -> GraphData:
        max_node_degree = max(deg for _, deg in graph.degree())
        n_nodes = n_nodes
        n_measurement_steps = self._get_n_measurement_steps(graph)
        return GraphData(
            max_node_degree=max_node_degree,
            n_nodes=n_nodes,
            n_measurement_steps=n_measurement_steps,
        )

    def _estimate_resources_from_graph_data(
        self, graph_data: GraphData, delayed_gate_synthesis: bool, error_budget
    ) -> ResourceInfo:
        ec_error_rate_func = (
            self._ec_error_rate_delayed_gate_synthesis
            if delayed_gate_synthesis
            else self._ec_error_rate
        )

        code_distance = self._minimize_code_distance(
            graph_data.n_nodes,
            graph_data.max_node_degree,
            error_budget,
            ec_error_rate_func,
        )
        space_time_volume = self.get_logical_st_volume(
            graph_data.n_nodes, graph_data.max_node_degree
        )
        logical_cell_error_rate = self._logical_cell_failure_rate(code_distance)

        # Isolate differences between synthesized and not synthesized case
        if not delayed_gate_synthesis:
            total_logical_error_rate = logical_cell_error_rate * space_time_volume
            synthesis_multiplier = 1
        else:
            (
                synthesis_accuracy,
                total_logical_error_rate,
            ) = self.balance_logical_error_rate_and_synthesis_accuracy(
                graph_data.n_nodes, code_distance, graph_data.max_node_degree
            )

            synthesis_multiplier = self.SYNTHESIS_SCALING * np.log2(
                1 / synthesis_accuracy
            )

        time_of_logical_t_gate = (
            6 * self.hw_model.physical_gate_time_in_seconds * code_distance
        )

        num_boxes = np.ceil((graph_data.max_node_degree + 1) / self.BOX_WIDTH)
        patch_size = 2 * code_distance**2
        n_physical_qubits = self.BOX_WIDTH * self.BOX_HEIGHT * num_boxes * patch_size

        wall_time = (
            graph_data.n_measurement_steps * time_of_logical_t_gate
            + time_of_logical_t_gate
            * self.N_TOCKS_PER_T_GATE_FACTORY
            * graph_data.n_nodes
            * synthesis_multiplier
        )

        if self.decoder_model:
            decoder_power = space_time_volume * self.decoder_model.power(code_distance)
            decoder_area = graph_data.max_node_degree * self.decoder_model.area(
                code_distance
            )
            max_decodable_distance = self.find_max_decodable_distance()
        else:
            decoder_power = None
            decoder_area = None
            max_decodable_distance = None

        return ResourceInfo(
            synthesis_multiplier=synthesis_multiplier,
            code_distance=code_distance,
            logical_error_rate=total_logical_error_rate,
            # estimate the number of logical qubits using max node degree
            n_logical_qubits=graph_data.max_node_degree,
            n_nodes=graph_data.n_nodes,
            n_measurement_steps=graph_data.n_measurement_steps,
            total_time=wall_time,
            n_physical_qubits=n_physical_qubits,
            decoder_power=decoder_power,
            decoder_area=decoder_area,
            max_decodable_distance=max_decodable_distance,
        )

    def estimate(self, problem: GraphPartition, error_budget):
        n_nodes = problem.n_nodes
        if len(problem.subgraphs) == 1:
            graph_data = self._get_graph_data(problem.subgraphs[0], n_nodes)
            return self._estimate_resources_from_graph_data(
                graph_data,
                problem.delayed_gate_synthesis,
                error_budget,
            )
        else:
            raise NotImplementedError(
                "Resource estimation without combining subgraphs is not yet "
                "supported."
            )
