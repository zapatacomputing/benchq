from dataclasses import dataclass
from functools import singledispatchmethod


import numpy as np
import networkx as nx

from benchq.data_structures.hardware_architecture_models import BasicArchitectureModel


# TODO: add other resources
# Why dataclass?
# - good when the structure does not vary from call to call
# - safer then dictionaries
# Why not dataclass?
# - you need to write it (xD)
# - if contents of given data structure vary, you have to do some additoinal work (or use dict)
#
# Overall I would use dataclasses whenever we have to provide some structured input/return
# structured output which is non-scalar.
@dataclass
class Resources:
    wall_time: float


@dataclass
class ErrorBudget:
    synthesis: float
    ec: float

    # Note: this class ist just demo, update total_error/component errors accordingly
    @property
    def total_error(self):
        return self.synthesis + self.ec


def main_2():
    program = get_qsp_program()
    error_budget = ErrorBudget(synthesis=1e-3, ec=1e-3)
    hardware_model = BasicArchitectureModel()
    decoder_model = BasicArchitectureModel()
    specs = {
        "use_full_circuit": False,
        "gate_synthesis": True,
        "graph_stitching": "Full/simplified/None",
        "use_partial": True,
    }

    resource_estimations = get_resource_estimations_1(
        program,
        error_budget,
        transform=transform_program,
        combine=combine_graphs,  # default None
        # Last tile: resource estimator
        estimator=ResourceEstimator(hw_model=hardware_model),
    )


def get_resource_estimations_1(
    program, error_budget, synthesize, transform, combine, estimator
):
    stuff = combine(...)
    return estimator.estimate(stuff, synthesize)


@singledispatch
def transform_program(program: QuantumProgram, synthesize_gates) -> List[Graphs]:
    pass


@transform_program.register
def transform_circuit(circuit: QuantumCircuit, synthesize_gates) -> List[Graphs]:
    pass


def _calculate_wall_time_for_synthesized_gates():
    pass


def _calculate_wall_time_for_non_synthesized_gates():
    pass


class ResourceEstimator:
    def __init__(self, hw_model, synthesis_accuracy):
        self.hw_model = hw_model
        self.synthesis_accuracy = synthesis_accuracy

    def _synthesis_multiplier(self, synthesized):
        return 12 * np.log2(1 / self.synthesis_accuracy) if synthesized else 1

    def _ec_multiplier(self, distance, n_measurements):
        return 240 * distance * n_measurements

    def _calculate_wall_time(
        self, distance: float, n_measurements: int, synthesized: bool
    ) -> float:
        # This formula is probably wrong, check it!
        return (
            self._synthesis_multiplier(synthesized)
            * self._ec_multiplier(distance, n_measurements)
            * n_measurements
        )

    def _calculate_distance(self, max_degree):
        # TODO: actually implement this
        return 2

    def _get_n_measurements(self) -> int:
        # TODO: implement this
        return 10

    def _estimate_from_graph(self, graph: nx.Graph, synthesized, is_subgraph: bool):
        max_degree = max(deg for _, deg in graph.degree())
        distance = self._calculate_distance(max_degree)
        n_measurements = self._get_n_measurements()
        walltime = self._calculate_wall_time(distance, n_measurements, synthesized)

    @singledispatchmethod
    def estimate(self, obj, synthesized: bool):
        raise NotImplementedError()

    # Don't implement one of the following if given estimaiton method does not
    # work with given input
    @estimate.register
    def estimate_from_graphs(self, graphs: Iterable[nx.Graph], synthesized: bool):
        partial_results = []
        for graph in graphs:
            partial_results.append(self.estimate_from_graph(graph, synthesized))

        return self._combine_partial_results(partial_results)

    @estimate.register
    def estimate_from_graph(self, graph: nx.Graph, synthesized):
        graph_description = get_graph_description_from_graph(graph)
        ss_results = substrate_scheduler(graph)
        self.estimate_from_description(graph_description, synthesized, ss_results)
        pass

    @estimate.register
    def estimate_from_description(
        self, description: GraphDescription, synthesized: bool, ss_results=None
    ):
        pass
