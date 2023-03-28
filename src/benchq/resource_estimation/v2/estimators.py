import numpy as np

from functools import singledispatchmethod
import networkx as nx

from .structs import GraphPartition
from ..graph_compilation import (
    combine_subcomponent_graphs,
    get_resource_estimations_for_graph,
    get_substrate_scheduler_estimates_for_subcomponents,
    substrate_scheduler,
    _get_max_graph_degree,
)


class GraphResourceEstimator:
    def __init__(self, hw_model):
        self.hw_model = hw_model
        self.specs = {}

    def _synthesis_multiplier(self, error_budget):
        return (
            12
            * np.log2(
                1
                / (
                    error_budget["total_error"]
                    * error_budget["synthesis_error_rate"]
                )
            )
            if self.specs.get("gate_synthesis")
            else 1
        )

    def _ec_multiplier(self, distance, n_measurements):
        return 240 * distance * n_measurements

    def get_logical_st_volume(self, n_nodes):
        return 12 * n_nodes * 240 * n_nodes

    # We called it "base cell failure rate" before.
    # New name makes more sense to us, but perhaps we've been misguided
    def logical_operation_error_rate(self, distance):
        # Will be updated through Alexandru and Joe's work
        return (
            distance
            * 0.3
            * (70 * self.hw_model.physical_gate_error_rate) ** ((distance + 1) / 2)
        )

    def calculate_total_logical_error_rate(self, distance, n_nodes):
        return self.logical_operation_error_rate(distance) * self.get_logical_st_volume(
            n_nodes
        )

    def calculate_wall_time(self, distance: float, n_measurements: int, error_budget) -> float:
        # This formula is probably wrong, check it!
        return (
            self._synthesis_multiplier(error_budget)
            * self._ec_multiplier(distance, n_measurements)
            * n_measurements
        )

    def find_min_viable_distance(
        self,
        n_nodes,
        error_budget,
        min_d=4,
        max_d=100,
    ):
        min_viable_distance = None
        target_error_rate = (
            error_budget["total_error"] * error_budget["ec_error_rate"]
        )
        for distance in range(min_d, max_d):
            logical_error_rate = self.calculate_total_logical_error_rate(
                distance,
                n_nodes,
            )

            if logical_error_rate < target_error_rate and min_viable_distance is None:
                min_viable_distance = distance

            if logical_error_rate < target_error_rate:
                return min_viable_distance

        raise RuntimeError(f"Not found good error rates under distance code: {max_d}.")

    def _get_n_measurements(self, graph) -> int:
        scheduler_only_compiler = substrate_scheduler(graph)
        return len(scheduler_only_compiler.measurement_steps)

    def _get_n_physical_qubits(self, max_graph_degree, distance):
        return 12 * max_graph_degree * 2 * distance**2

    def get_resource_estimates(
        self, distance, n_nodes, max_graph_degree, n_measurements, error_budget
    ):
        results_dict = {
            "logical_error_rate": self.calculate_total_logical_error_rate(
                distance, n_nodes
            ),
            "total_time": self.calculate_wall_time(distance, n_measurements, error_budget),
            "physical_qubit_count": self._get_n_physical_qubits(
                max_graph_degree, distance
            ),
            "min_viable_distance": distance,
            "logical_st_volume": self.get_logical_st_volume(n_nodes),
            "n_measurement_steps": n_measurements,
            "max_graph_degree": max_graph_degree,
            "n_nodes": n_nodes,
        }
        return results_dict

    @singledispatchmethod
    def estimate(self, problem: GraphPartition, error_budget, use_full_program: bool):
        n_nodes = problem.n_nodes
        ### TODO
        ### Actually make use of self.get_resource_estimates
        if use_full_program:
            program_graph = combine_subcomponent_graphs(
                problem.subgraphs, problem.data_qubits_map_list, problem.program
            )
            max_graph_degree = _get_max_graph_degree(program_graph)
            scheduler_only_compiler = substrate_scheduler(program_graph)
            # resource_estimates = get_resource_estimations_for_graph(
            #     program_graph,
            #     self.hw_model,
            #     error_budget["tolerable_circuit_error_rate"],
            #     plot=False,
            # )
            distance = self.find_min_viable_distance(n_nodes, error_budget)
            n_measurements = len(scheduler_only_compiler.measurement_steps)
            resource_estimates = self.get_resource_estimates(
                distance, n_nodes, max_graph_degree, n_measurements, error_budget
            )
        else:
            # use dummy graph
            resource_estimates = get_resource_estimations_for_graph(
                nx.path_graph(n_nodes),
                self.hw_model,
                error_budget["tolerable_circuit_error_rate"],
                plot=False,
                is_subgraph=True,
            )
            resource_estimates = get_substrate_scheduler_estimates_for_subcomponents(
                problem.subgraphs,
                problem.program,
                self.hw_model,
                resource_estimates,
            )

        return resource_estimates
