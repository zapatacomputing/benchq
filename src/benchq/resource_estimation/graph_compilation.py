################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import json
import logging
import warnings
from typing import Any, List

import more_itertools
import networkx as nx
import numpy as np
from graph_state_generation.optimizers import greedy_stabilizer_measurement_scheduler
from graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler
from orquestra.quantum.circuits import Circuit

from benchq.vizualization_tools import plot_graph_state_with_measurement_steps

from ..compilation import get_algorithmic_graph, pyliqtr_transpile_to_clifford_t
from ..data_structures import QuantumProgram

LOGGER = logging.getLogger(__name__)


CLIFFORD_GATES = [
    "X",
    "H",
    "CNOT",
    "CZ",
    "SWAP",
    "H",
    "I",
    "S",
    "X",
    "Y",
    "Z",
]


def _get_max_graph_degree(graph):
    return max(*[degree for _, degree in graph.degree()])


def calculate_wall_time(distance, n_measurements, physical_gate_time):
    return 240 * n_measurements * distance * 6 * physical_gate_time


def is_circuit_in_the_right_format(circuit: Circuit) -> bool:
    for operation in circuit.operations:
        # TODO: refactor to be less hacky
        if operation.gate.name not in CLIFFORD_GATES + ["T", "RZ", "RX"]:
            return False

    return True


def get_logical_st_volume(n_nodes):
    return 12 * n_nodes * 240 * n_nodes


# We called it "base cell failure rate" before.
# New name makes more sense to us, but perhaps we've been misguided
def logical_operation_error_rate(distance, physical_gate_error_rate):
    # Will be updated through Alexandru and Joe's work
    return distance * 0.3 * (70 * physical_gate_error_rate) ** ((distance + 1) / 2)


# This is total error rate due to imperfection of the hardware
def calculate_total_logical_error_rate(distance, physical_gate_error_rate, n_nodes):
    return logical_operation_error_rate(
        distance, physical_gate_error_rate
    ) * get_logical_st_volume(n_nodes)


def find_min_viable_distance(
    n_nodes,
    physical_gate_error_rate,
    tolerable_logical_error_rate,
    min_d=4,
    max_d=100,
):
    min_viable_distance = None
    for distance in range(min_d, max_d):
        logical_error_rate = calculate_total_logical_error_rate(
            distance,
            physical_gate_error_rate,
            n_nodes,
        )

        if (
            logical_error_rate < tolerable_logical_error_rate
            and min_viable_distance is None
        ):
            min_viable_distance = distance

        if logical_error_rate < tolerable_logical_error_rate:
            return min_viable_distance

    raise RuntimeError(f"Not found good error rates under distance code: {max_d}.")


def get_resource_estimations_for_graph(
    graph: nx.Graph,
    architecture_model: Any,
    tolerable_logical_error_rate: float = 0.5,
    plot: bool = False,
    use_max_graph_degree=True,
):
    n_nodes = len(graph.nodes)
    max_graph_degree = _get_max_graph_degree(graph)
    physical_gate_error_rate = architecture_model.physical_gate_error_rate
    physical_gate_time_in_seconds = architecture_model.physical_gate_time_in_seconds

    scheduler_only_compiler = substrate_scheduler(graph)

    min_viable_distance = find_min_viable_distance(
        n_nodes,
        physical_gate_error_rate,
        tolerable_logical_error_rate,
    )

    logical_error_rate = calculate_total_logical_error_rate(
        min_viable_distance,
        physical_gate_error_rate,
        n_nodes,
    )

    n_measurements_steps = len(scheduler_only_compiler.measurement_steps)
    total_time = calculate_wall_time(
        min_viable_distance,
        n_nodes,
        physical_gate_time_in_seconds,
    )

    if use_max_graph_degree:
        physical_qubit_count = 12 * max_graph_degree * 2 * min_viable_distance**2
    else:
        physical_qubit_count = 12 * n_nodes * 2 * min_viable_distance**2
    resources_in_cells = get_logical_st_volume(n_nodes)
    results_dict = {
        "logical_error_rate": logical_error_rate,
        "total_time": total_time,
        "physical_qubit_count": physical_qubit_count,
        "min_viable_distance": min_viable_distance,
        "resources_in_cells": resources_in_cells,
        "n_measurement_steps": n_measurements_steps,
        "max_graph_degree": max_graph_degree,
        "n_nodes": n_nodes,
    }
    LOGGER.debug(scheduler_only_compiler.measurement_steps)

    if plot:
        plot_graph_state_with_measurement_steps(
            scheduler_only_compiler.connected_graph,
            scheduler_only_compiler.measurement_steps,
        )

    return results_dict


def substrate_scheduler(graph: nx.Graph):
    connected_graph = graph.copy()
    connected_graph.remove_nodes_from(list(nx.isolates(graph)))  # remove isolated nodes
    connected_graph = nx.convert_node_labels_to_integers(connected_graph)

    scheduler_only_compiler = TwoRowSubstrateScheduler(
        connected_graph, stabilizer_scheduler=greedy_stabilizer_measurement_scheduler
    )
    scheduler_only_compiler.run()

    return scheduler_only_compiler


def get_resource_estimations_for_program(
    quantum_program,
    error_budget,
    architecture_model,
    use_full_program_graph: bool = False,
    plot: bool = False,
):
    """
    Args:
        quantum_program (QuantumProgram): The program we wish toestimate resources for.
        error_budget (float): maximum allowable error in program.
        architecture_model (ArchetectureModel): Parameters describing th e performance
            of the architecture.
        use_full_program_graph (bool, optional): Choose whether to perform resource
            estimations using the graph of the full program or with the subcomponents.
            For large programs generating the graph may take too much time.
            Defaults to False.
        plot (bool, optional): Whether or not to plot the full graph with colors
            corresponding to measurement steps. Defaults to False.
    """
    graphs_list = []
    data_qubits_map_list = []
    # We assign the same amount of error budget to gate synthesis and error correction.
    synthesis_error_budget = error_budget / 2
    ec_error_budget = error_budget / 2

    for circuit in quantum_program.subroutines:
        # TA 2 part: FTQC compilation
        clifford_t_circuit = pyliqtr_transpile_to_clifford_t(
            circuit, synthesis_accuracy=synthesis_error_budget
        )
        graphs_list.append(get_algorithmic_graph(clifford_t_circuit))
        with open("icm_output.json", "r") as f:
            output_dict = json.load(f)
            data_qubits_map = output_dict["data_qubits_map"]
        data_qubits_map_list.append(data_qubits_map)

    return resource_estimations_for_subcomponents(
        graphs_list,
        data_qubits_map_list,
        quantum_program,
        architecture_model,
        ec_error_budget,
        use_full_program_graph=use_full_program_graph,
        plot=plot,
    )


def resource_estimations_for_subcomponents(
    graphs_list: List[nx.Graph],
    data_qubits_map_list: List[List[int]],
    quantum_program,
    architecture_model,
    tolerable_circuit_error_rate,
    use_full_program_graph: bool = False,
    plot: bool = False,
):
    """
    Args:
        graphs_list (List[nx.Graph]): A list of graphs for each subcomponent of the
            program.
        data_qubits_map_list (List[List[int]]): A list of lists describing where the
            data qubits are after each subroutine is called.
        quantum_program (QuantumProgram): The program we wish toestimate resources for.
        architecture_model (ArchetectureModel): Parameters describing th e performance
            of the archetecture.
        tolerable_circuit_error_rate (float): Error rate of the circuit.
        use_full_program_graph (bool, optional): Choose whether to perform resource
            estimations using the graph of the full program or with the subcomponents.
            For large programs generating the graph may take too much time.
            Defaults to False.
        plot (bool, optional): Whether or not to plot the full graph with colors
            corresponding to measurement steps. Defaults to False.
    """
    n_nodes = sum(
        len(graph) * multiplicity
        for graph, multiplicity in zip(graphs_list, quantum_program.multiplicities)
    )
    # account for double counting of data qubits coming from each graph
    n_nodes -= quantum_program.num_data_qubits * (
        len(quantum_program.subroutine_sequence) - 1
    )

    if use_full_program_graph:
        program_graph = combine_subcomponent_graphs(
            graphs_list, data_qubits_map_list, quantum_program
        )
        resource_estimates = get_resource_estimations_for_graph(
            program_graph, architecture_model, tolerable_circuit_error_rate, plot=plot
        )
    else:
        if plot:
            warnings.warn("Cannot plot graph when estimating from subcomponents.")
        # use dummy graph
        resource_estimates = get_resource_estimations_for_graph(
            nx.path_graph(n_nodes),
            architecture_model,
            tolerable_circuit_error_rate,
            plot=False,
        )
        resource_estimates = get_substrate_scheduler_estimates_for_subcomponents(
            graphs_list,
            quantum_program,
            architecture_model,
            data_qubits_map_list,
            resource_estimates,
        )

    resource_estimates["n_nodes"] = n_nodes
    resource_estimates["steps"] = quantum_program.steps

    return resource_estimates


def combine_subcomponent_graphs(
    graphs_list: List[nx.Graph],
    data_qubits_map_list: List[List[int]],
    quantum_program: QuantumProgram,
):
    """Given a list of graphs for each of the subcomponents, combine those graphs
    into single graph representing the entire quantum program.

    Args:
        graphs_list (List[nx.Graph]): _description_
        data_qubits_map_list (List[List[int]]): _description_
        quantum_program (QuantumProgram): _description_

    Returns:
        _type_: _description_
    """
    program_graph = graphs_list[quantum_program.subroutine_sequence[0]]
    node_relabeling = {}
    prev_graph_size = 0
    for prev_i, curr_i in more_itertools.windowed(
        quantum_program.subroutine_sequence, 2
    ):
        data_qubits = data_qubits_map_list[prev_i]  # type: ignore
        curr_graph = graphs_list[curr_i]  # type: ignore

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


def get_substrate_scheduler_estimates_for_subcomponents(
    graphs_list,
    quantum_program,
    architecture_model,
    data_qubits_map_list=None,
    resource_estimates={},
):
    if data_qubits_map_list is None:
        data_qubits_map_list = [[] * len(graphs_list)]

    # sum substrate scheduler resource estimates for each subcomponent
    total_n_measurement_steps = 0
    total_measurement_steps = []
    total_time = 0
    max_graph_degree = 0
    for graph, data_qubits, multiplicity in zip(
        graphs_list, data_qubits_map_list, quantum_program.multiplicities
    ):
        scheduler_only_compiler = substrate_scheduler(graph)
        total_n_measurement_steps += (
            len(scheduler_only_compiler.measurement_steps) * multiplicity
        )
        total_time += (
            calculate_wall_time(
                resource_estimates["min_viable_distance"],
                len(scheduler_only_compiler.measurement_steps),
                architecture_model.physical_gate_time_in_seconds,
            )
            * multiplicity
        )

        total_measurement_steps += [scheduler_only_compiler.measurement_steps]
        max_graph_degree = max(max_graph_degree, _get_max_graph_degree(graph))
        if graph.degree(data_qubits) == max_graph_degree:
            warnings.warn(
                "Node with largest degree lies on an edge. "
                "Graph degree might be an underestimate. "
                "If this message is triggered, Simon owes Athena a bottle of whiskey."
            )

    resource_estimates["n_measurement_steps"] = total_n_measurement_steps
    resource_estimates["max_graph_degree"] = max_graph_degree
    resource_estimates["total_time"] = total_time
    LOGGER.debug(total_measurement_steps)

    return resource_estimates
