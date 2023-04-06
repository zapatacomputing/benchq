from dataclasses import dataclass
from typing import Callable

import networkx as nx
import numpy as np
from graph_state_generation.optimizers import greedy_stabilizer_measurement_scheduler
from graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler

from ...data_structures.hardware_architecture_models import BasicArchitectureModel
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
class ResourceInfo:
    synthesis_multiplier: float
    code_distance: int
    logical_error_rate: float
    max_graph_degree: int
    n_nodes: int
    n_measurement_steps: int
    total_time: float

    @property
    def n_physical_qubits(self) -> int:
        return 12 * self.max_graph_degree * 2 * self.code_distance**2

    @property
    def logical_st_volume(self) -> float:
        return 12 * self.n_nodes * 240 * self.n_nodes * self.synthesis_multiplier


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

    def _ec_error_rate_synthesized(self, distance: int, n_nodes: int) -> float:
        return (
            self._logical_operation_error_rate(distance) * 12 * n_nodes * 240 * n_nodes
        )

    def _ec_error_rate_unsynthesized(self, distance: int, n_nodes: int) -> float:
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
            ec_error_rate = self._ec_error_rate_synthesized(
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

    def _estimate_resource_for_graph(
        self, graph: nx.Graph, n_nodes: int, synthesized: bool, error_budget
    ) -> ResourceInfo:

        ec_error_rate = (
            self._ec_error_rate_synthesized
            if synthesized
            else self._ec_error_rate_unsynthesized
        )

        # Change to code distance
        code_distance = self._minimize_code_distance(
            n_nodes, error_budget, ec_error_rate
        )
        max_degree = max(deg for _, deg in graph.degree())
        logical_operation_error_rate = self._logical_operation_error_rate(code_distance)

        n_measurement_steps = self._get_n_measurement_steps(graph)

        ec_multiplier = 240 * code_distance * n_measurement_steps

        # Isolate differences betweeen synthesized and not synthesized case
        if synthesized:
            logical_error_rate = (
                logical_operation_error_rate * 12 * n_nodes * 240 * n_nodes
            )
            synthesis_multiplier = 1
        else:
            (
                synthesis_accuracy,
                logical_error_rate,
            ) = self.balance_logical_error_rate_and_synthesis_accuracy(
                n_nodes, code_distance
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
            max_graph_degree=max_degree,
            n_nodes=n_nodes,
            n_measurement_steps=n_measurement_steps,
            total_time=wall_time,
        )

    def estimate(self, problem: GraphPartition, error_budget):
        n_nodes = problem.n_nodes
        if len(problem.subgraphs) == 1:
            return self._estimate_resource_for_graph(
                problem.subgraphs[0], n_nodes, problem.synthesized, error_budget
            )
        else:
            raise NotImplementedError(
                "Resource estimation without combining subgraphs is not yet "
                "supported."
            )
