from dataclasses import dataclass
from typing import Callable

import networkx as nx
import numpy as np
from graph_state_generation.optimizers import greedy_stabilizer_measurement_scheduler
from graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler

from ...data_structures.hardware_architecture_models import BasicArchitectureModel
from .structs import GraphPartition

INITIAL_SYNTHESIS_ACCURACY = 0.0001


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
    n_measurement_steps: int
    total_time: float

    @property
    def n_physical_qubits(self) -> int:
        return 12 * self.n_logical_qubits * 2 * self.code_distance**2

    @property
    def logical_st_volume(self) -> float:
        return 12 * self.n_nodes * 240 * self.n_nodes * self.synthesis_multiplier


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
    def __init__(
        self, hw_model: BasicArchitectureModel, combine_partition: bool = True
    ):
        self.hw_model = hw_model
        self.combine_partition = combine_partition

    def _logical_operation_error_rate(self, distance: int) -> float:
        return (
            distance
            * 0.3
            * (70 * self.hw_model.physical_gate_error_rate) ** ((distance + 1) / 2)
        )

    def _minimize_code_distance(
        self,
        n_nodes: int,
        error_budget,
        error_rate: Callable[[int, int], float],
        min_d: int = 4,
        max_d: int = 100,
    ) -> int:
        target_error_rate = error_budget["total_error"] * error_budget["ec_error_rate"]

        for distance in range(min_d, max_d):
            if error_rate(distance, n_nodes) < target_error_rate:
                return distance

        raise RuntimeError(f"Not found good error rates under distance code: {max_d}.")

    def _get_n_measurement_steps(self, graph) -> int:
        return len(substrate_scheduler(graph).measurement_steps)

    def _ec_error_rate_delayed_gate_synthesis(
        self, distance: int, n_nodes: int
    ) -> float:
        return (
            self._logical_operation_error_rate(distance) * 12 * n_nodes * 240 * n_nodes
        )

    def _ec_error_rate(self, distance: int, n_nodes: int) -> float:
        _, ec_error_rate = self.balance_logical_error_rate_and_synthesis_accuracy(
            n_nodes, distance
        )
        return ec_error_rate

    # TODO: We need to make sure it's doing scientifically what it should be doing
    def balance_logical_error_rate_and_synthesis_accuracy(self, n_nodes, distance):
        """
        This function is basically finding such a value of synthesis error rate, that
        it is 1/(12*N) smaller than circuit error rate, where N is the number of nodes
        in the graph.
        """
        current_synthesis_accuracy = INITIAL_SYNTHESIS_ACCURACY
        for _ in range(20):
            ec_error_rate = self._ec_error_rate_delayed_gate_synthesis(
                distance,
                n_nodes,
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

        ec_error_rate = (
            self._ec_error_rate_delayed_gate_synthesis
            if delayed_gate_synthesis
            else self._ec_error_rate
        )

        # Change to code distance
        code_distance = self._minimize_code_distance(
            graph_data.n_nodes, error_budget, ec_error_rate
        )
        logical_operation_error_rate = self._logical_operation_error_rate(code_distance)

        ec_multiplier = 240 * code_distance * graph_data.n_measurement_steps

        # Isolate differences betweeen delayed_gate_synthesis and not delayed_gate_synthesis case
        if not delayed_gate_synthesis:
            logical_error_rate = (
                logical_operation_error_rate
                * 12
                * graph_data.n_nodes
                * 240
                * graph_data.n_nodes
            )
            synthesis_multiplier = 1
        else:
            (
                synthesis_accuracy,
                logical_error_rate,
            ) = self.balance_logical_error_rate_and_synthesis_accuracy(
                graph_data.n_nodes, code_distance
            )
            synthesis_multiplier = 12 * np.log2(1 / synthesis_accuracy)

        wall_time = (
            6
            * ec_multiplier
            * self.hw_model.physical_gate_time_in_seconds
            * synthesis_multiplier
        )

        return ResourceInfo(
            synthesis_multiplier=synthesis_multiplier,
            code_distance=code_distance,
            logical_error_rate=logical_error_rate,
            # estimate the number of logical qubits using max node degree
            n_logical_qubits=graph_data.max_node_degree,
            n_nodes=graph_data.n_nodes,
            n_measurement_steps=graph_data.n_measurement_steps,
            total_time=wall_time,
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
