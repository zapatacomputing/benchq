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
class ResourceInfo:
    synthesis_multiplier: float
    code_distance: int
    logical_error_rate: float
    max_graph_degree: int
    n_nodes: int
    n_measurement_steps: int
    total_time: float
    max_decodable_distance: Optional[int]
    decoder_power: Optional[float]
    decoder_area: Optional[float]

    @property
    def n_physical_qubits(self) -> int:
        return 12 * self.max_graph_degree * 2 * self.code_distance**2


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

    N_TOCKS_PER_T_GATE_FACTORY = 15 * 16

    def _logical_cell_failure_rate(self, distance: int) -> float:
        if self.decoder_model:
            decoder_error_rate = self.decoder_model.error_rate(distance)
        else:
            decoder_error_rate = 0
        return (
            # 0.3 and 70 come from numerical simulations
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

    def _ec_error_rate_synthesized(self, distance: int, n_nodes: int) -> float:
        return (
            self._logical_cell_failure_rate(distance)
            * self.get_logical_st_volume(n_nodes)
        )

    def _ec_error_rate_unsynthesized(self, distance: int, n_nodes: int) -> float:
        _, ec_error_rate = self.balance_logical_error_rate_and_synthesis_accuracy(
            n_nodes, distance
        )
        return ec_error_rate

    def get_logical_st_volume(self, n_operations):
        return 12 * n_operations * self.N_TOCKS_PER_T_GATE_FACTORY * n_operations

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

        ec_error_rate_func = (
            self._ec_error_rate_synthesized
            if synthesized
            else self._ec_error_rate_unsynthesized
        )

        code_distance = self._minimize_code_distance(
            n_nodes, error_budget, ec_error_rate_func
        )
        max_degree = max(deg for _, deg in graph.degree())
        logical_cell_error_rate = self._logical_cell_failure_rate(code_distance)
        n_measurement_steps = len(substrate_scheduler(graph).measurement_steps)

        # Isolate differences betweeen synthesized and not synthesized case
        if synthesized:
            total_logical_error_rate = (
                logical_cell_error_rate * self.get_logical_st_volume(max_degree)
            )
            synthesis_multiplier = 1
        else:
            (
                synthesis_accuracy,
                total_logical_error_rate,
            ) = self.balance_logical_error_rate_and_synthesis_accuracy(
                n_nodes, code_distance
            )
            synthesis_multiplier = 12 * np.log2(1 / synthesis_accuracy)
        time_of_logical_t_gate = (
            6 * self.hw_model.physical_gate_time_in_seconds * code_distance
        )

        wall_time = (
            time_of_logical_t_gate
            * self.N_TOCKS_PER_T_GATE_FACTORY
            * n_measurement_steps
            * synthesis_multiplier
        )
        if self.decoder_model:
            decoder_power = self.get_logical_st_volume(
                max_degree
            ) * self.decoder_model.power(code_distance)
            decoder_area = max_degree * self.decoder_model.area(code_distance)
            max_decodable_distance = self.find_max_decodable_distance()
        else:
            decoder_power = None
            decoder_area = None
            max_decodable_distance = None

        return ResourceInfo(
            synthesis_multiplier=synthesis_multiplier,
            code_distance=code_distance,
            logical_error_rate=total_logical_error_rate,
            max_graph_degree=max_degree,
            n_nodes=n_nodes,
            n_measurement_steps=n_measurement_steps,
            total_time=wall_time,
            decoder_power=decoder_power,
            decoder_area=decoder_area,
            max_decodable_distance=max_decodable_distance,
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
