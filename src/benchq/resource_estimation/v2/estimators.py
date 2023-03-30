from dataclasses import dataclass
from functools import singledispatchmethod
from typing import Callable

import more_itertools
import networkx as nx
import numpy as np
from graph_state_generation.optimizers import greedy_stabilizer_measurement_scheduler
from graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler

from ...data_structures.hardware_architecture_models import BasicArchitectureModel
from ..graph_compilation_rotations import (
    balance_logical_error_rate_and_synthesis_accuracy,
)
from .structs import GraphPartition


def combine_subcomponent_graphs(partition: GraphPartition):
    program_graph = partition.subgraphs[partition.program.subroutine_sequence[0]]
    node_relabeling = {}
    prev_graph_size = 0

    for prev_i, curr_i in more_itertools.windowed(
        partition.program.subroutine_sequence, 2
    ):
        data_qubits = partition.data_qubits_map_list[prev_i]  # type:ignore
        curr_graph = partition.subgraphs[curr_i]  # type: ignore

        # shift labels so curr_graph has no labels in common with program_graph
        curr_graph = nx.relabel_nodes(
            curr_graph,
            lambda x: str(int(x) + len(program_graph)),
        )
        # keep track of which nodes should be contracted to connect data qubits
        for j, data_qubit in enumerate(data_qubits):
            node_relabeling[data_qubit + prev_graph_size] = j + len(program_graph)

        prev_graph_size = len(program_graph)
        program_graph = nx.compose(program_graph, curr_graph)

    for node_1, node_2 in node_relabeling.items():
        program_graph = nx.contracted_nodes(program_graph, str(node_2), str(node_1))

    program_graph = nx.convert_node_labels_to_integers(program_graph)

    return program_graph


def substrate_scheduler(graph: nx.Graph) -> TwoRowSubstrateScheduler:
    connected_graph = graph.copy()
    connected_graph.remove_nodes_from(list(nx.isolates(graph)))  # remove isolated nodes
    connected_graph = nx.convert_node_labels_to_integers(connected_graph)
    scheduler_only_compiler = TwoRowSubstrateScheduler(
        connected_graph, stabilizer_scheduler=greedy_stabilizer_measurement_scheduler
    )
    scheduler_only_compiler.run()
    return scheduler_only_compiler


# TODO: should we split this into algo and resources part?
@dataclass
class ResourceInfo:  # Think of a better name (EstimatedResources? Resources?)
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

    def _ec_error_rate_synthesized(self, distance: int, n_nodes: int) -> float:
        return (
            self._logical_operation_error_rate(distance) * 12 * n_nodes * 240 * n_nodes
        )

    def _ec_error_rate_unsynthesized(self, distance: int, n_nodes: int) -> float:
        _, ec_error_rate = balance_logical_error_rate_and_synthesis_accuracy(
            n_nodes, distance, self.hw_model.physical_gate_error_rate
        )
        return ec_error_rate

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
        logical_operation_error_rate = (
            code_distance
            * 0.3
            * (70 * self.hw_model.physical_gate_error_rate) ** ((code_distance + 1) / 2)
        )

        n_measurement_steps = self._get_n_measurement_steps(graph)

        ec_multiplier = 240 * code_distance * n_measurement_steps

        # Isoalate differences betweeen synthesized and not synthesized case
        if synthesized:
            logical_error_rate = (
                logical_operation_error_rate * 12 * n_nodes * 240 * n_nodes
            )
            synthesis_multiplier = 1
        else:
            (
                synthesis_accuracy,
                logical_error_rate,
            ) = balance_logical_error_rate_and_synthesis_accuracy(
                n_nodes, code_distance, self.hw_model.physical_gate_error_rate
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

    @singledispatchmethod
    def estimate(self, problem: GraphPartition, error_budget):
        n_nodes = problem.n_nodes

        if len(problem.subgraphs) == 1:
            return self._estimate_resource_for_graph(
                problem.subgraphs[0], n_nodes, problem.synthesized, error_budget
            )
        else:
            if self.combine_partition:
                program_graph = combine_subcomponent_graphs(problem)
                return self._estimate_resource_for_graph(
                    program_graph, n_nodes, problem.synthesized, error_budget
                )
            else:
                raise NotImplementedError(
                    "Resource estimation without combining subgraphs is not yet "
                    "supported."
                )
            # use dummy graph
            # resource_estimates = get_resource_estimations_for_graph(
            #     nx.path_graph(n_nodes),
            #     self.hw_model,
            #     error_budget["tolerable_circuit_error_rate"],
            #     plot=False,
            #     is_subgraph=True,
            # )
            # resource_estimates = get_substrate_scheduler_estimates_for_subcomponents(
            #     problem.subgraphs,
            #     problem.program,
            #     self.hw_model,
            #     resource_estimates,
            # )
