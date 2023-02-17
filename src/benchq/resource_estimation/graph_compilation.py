################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import json
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

# Starting point for the optimization of synthesis gate cost
INITIAL_SYNTHESIS_ERROR_RATE = 0.0001


def calculate_wall_time(synthesis_error_rate, distance, n_nodes, physical_gate_time):
    return (
        2880
        * n_nodes
        * np.log2(1 / synthesis_error_rate)
        * distance
        * 6
        * physical_gate_time
    )


def is_circuit_in_the_right_format(circuit: Circuit) -> bool:
    for operation in circuit.operations:
        # TODO: refactor to be less hacky
        if operation.gate.name not in CLIFFORD_GATES + ["T", "RZ", "RX"]:
            return False

    return True


def get_logical_st_volume(n_nodes, synthesis_error_rate):
    return 12 * n_nodes * 2880 * n_nodes * np.ceil(np.log2(1 / synthesis_error_rate))


# class BaseCellModel:
#     def get_failure_rate(self, distance, physical_gate_error_rate):
#         return distance * 0.3 * (70 * physical_gate_error_rate) ** ((distance + 1) /2)


# We called it "base cell failure rate" before.
# New name makes more sense to us, but perhaps we've been misguided
def logical_operation_error_rate(distance, physical_gate_error_rate):
    # Will be updated through Alexandru and Joe's work
    return distance * 0.3 * (70 * physical_gate_error_rate) ** ((distance + 1) / 2)


# This is total error rate due to imperfection of the hardware
def calculate_total_logical_error_rate(
    distance, physical_gate_error_rate, n_nodes, synthesis_error_rate
):
    return logical_operation_error_rate(
        distance, physical_gate_error_rate
    ) * get_logical_st_volume(n_nodes, synthesis_error_rate)


# TODO: We need to make sure it's doing scientifically what it should be doing
def balance_logical_and_synthesis_error_rates(
    n_nodes, distance, physical_gate_error_rate
):
    """
    This function is basically finding such a value of synthesis error rate, that it is
    1/(12*N) smaller than circuit error rate, where N is the number of nodes
    in the graph.
    """
    current_synthesis_error_rate = INITIAL_SYNTHESIS_ERROR_RATE
    for _ in range(20):
        logical_error_rate = calculate_total_logical_error_rate(
            distance,
            physical_gate_error_rate,
            n_nodes,
            current_synthesis_error_rate,
        )
        new_synthesis_error_rate = (1 / (12 * n_nodes)) * logical_error_rate
        # This is for cases where the algorithm diverges terribly, to avoid
        # "divide by 0" and similar warnings.
        # TODO: Hacky! We should come up with a more stable solution in future!
        if new_synthesis_error_rate <= 0 or np.isnan(new_synthesis_error_rate):
            return np.inf, np.inf

        current_synthesis_error_rate = new_synthesis_error_rate
    return current_synthesis_error_rate, logical_error_rate


def find_min_viable_distance(
    n_nodes,
    physical_gate_error_rate,
    tolerable_logical_error_rate,
    min_d=4,
    max_d=100,
):
    min_viable_distance = None
    for distance in range(min_d, max_d):
        (
            synthesis_error_rate,
            logical_error_rate,
        ) = balance_logical_and_synthesis_error_rates(
            n_nodes, distance, physical_gate_error_rate
        )
        print(distance, logical_error_rate)
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
    verbose: bool = False,
):
    n_nodes = len(graph.nodes)
    physical_gate_error_rate = architecture_model.physical_gate_error_rate
    physical_gate_time_in_seconds = architecture_model.physical_gate_time_in_seconds

    (n_measurement_steps, measurement_steps, connected_graph) = substrate_scheduler(
        graph, verbose
    )

    min_viable_distance = find_min_viable_distance(
        n_nodes,
        physical_gate_error_rate,
        tolerable_logical_error_rate,
    )

    (
        synthesis_error_rate,
        final_logical_error_rate,
    ) = balance_logical_and_synthesis_error_rates(
        n_nodes,
        min_viable_distance,
        physical_gate_error_rate,
    )

    total_time = calculate_wall_time(
        synthesis_error_rate,
        min_viable_distance,
        n_nodes,
        physical_gate_time_in_seconds,
    )

    physical_qubit_count = 12 * n_nodes * 2 * min_viable_distance**2
    resources_in_cells = get_logical_st_volume(n_nodes, synthesis_error_rate)
    results_dict = {
        "logical_error_rate": final_logical_error_rate,
        "total_time": total_time,
        "physical_qubit_count": physical_qubit_count,
        "min_viable_distance": min_viable_distance,
        "synthesis_error_rate": synthesis_error_rate,
        "resources_in_cells": resources_in_cells,
        "n_measurement_steps": n_measurement_steps,
        "graph_degree": max([degree for node, degree in graph.degree()]),
    }

    if verbose:
        results_dict["graph"] = connected_graph
        results_dict["measurement_steps"] = measurement_steps
        plot_graph_state_with_measurement_steps(connected_graph, measurement_steps)

    return results_dict


def substrate_scheduler(graph: nx.Graph, verbose: bool = False):
    connected_graph = graph.copy()
    connected_graph.remove_nodes_from(list(nx.isolates(graph)))  # remove isolated nodes
    connected_graph = nx.convert_node_labels_to_integers(connected_graph)

    scheduler_only_compiler = TwoRowSubstrateScheduler(
        connected_graph, stabilizer_scheduler=greedy_stabilizer_measurement_scheduler
    )
    scheduler_only_compiler.run()

    if verbose:
        try:
            scheduler_only_compiler.visualization()
        except NotImplementedError:
            warnings.warn("Graph is too large to be ascii visualized.")

    measurement_steps = scheduler_only_compiler.measurement_steps

    return (len(measurement_steps), measurement_steps, connected_graph)


def get_resource_estimations_for_program(
    quantum_program,
    error_budget,
    architecture_model,
    use_full_program_graph: bool = False,
    verbose: bool = False,
):
    """_summary_

    Args:
        quantum_program: _description_
        error_budget: _description_
        architecture_model: _description_
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
        graphs_list.append(get_algorithmic_graph(clifford_t_circuit, verbose))
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
        verbose=verbose,
    )


def resource_estimations_for_subcomponents(
    graphs_list,
    data_qubits_map_list,
    quantum_program,
    architecture_model,
    tolerable_circuit_error_rate,
    use_full_program_graph: bool = False,
    verbose: bool = False,
):
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
            program_graph, architecture_model, tolerable_circuit_error_rate, verbose
        )
    else:
        # use dummy graph
        resource_estimates = get_resource_estimations_for_graph(
            nx.path_graph(n_nodes),
            architecture_model,
            tolerable_circuit_error_rate,
            verbose=False,
        )
        resource_estimates = get_substrate_scheduler_estimates_for_subcomponents(
            graphs_list,
            quantum_program,
            data_qubits_map_list,
            resource_estimates,
            verbose,
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
    for prev, curr in more_itertools.windowed(quantum_program.subroutine_sequence, 2):
        data_qubits = data_qubits_map_list[prev]  # type: ignore
        curr_graph = graphs_list[curr]  # type: ignore

        # shift labels so curr_graph has no labels in common with program_graph
        curr_graph = nx.relabel_nodes(
            curr_graph,
            lambda x: str(int(x) + len(program_graph)),
        )
        # keep track of which nodes should be contracted to connect data qubits
        for i, data_qubit in enumerate(data_qubits):
            node_relabeling[data_qubit + prev_graph_size] = i + len(program_graph)

        prev_graph_size = len(program_graph)
        program_graph = nx.compose(program_graph, curr_graph)

    for node_1, node_2 in node_relabeling.items():
        program_graph = nx.contracted_nodes(program_graph, str(node_2), str(node_1))

    program_graph = nx.convert_node_labels_to_integers(program_graph)

    return program_graph


def get_substrate_scheduler_estimates_for_subcomponents(
    graphs_list,
    quantum_program,
    data_qubits_map_list=None,
    resource_estimates={},
    verbose: bool = False,
):
    if data_qubits_map_list is None:
        data_qubits_map_list = [[] * len(graphs_list)]

    # sum substrate scheduler resource estimates for each subcomponent
    total_n_measurement_steps = 0
    total_measurement_steps = []
    total_connected_graph = nx.Graph()
    graph_degree = 0
    for graph, data_qubits, multiplicity in zip(
        graphs_list, data_qubits_map_list, quantum_program.multiplicities
    ):
        (
            n_measurement_steps,
            measurement_steps,
            connected_graph,
        ) = substrate_scheduler(graph, verbose)
        total_n_measurement_steps += n_measurement_steps * multiplicity
        total_measurement_steps += [measurement_steps]
        graph_degree = max(graph_degree, *[degree for node, degree in graph.degree()])
        if graph.degree(data_qubits) == graph_degree:
            warnings.warn(
                "Node with largest degree lies on an edge. "
                "Graph degree might be an underestimate. "
                "If this message is triggered, Simon owes Athena a bottle of whiskey."
            )

    resource_estimates["n_measurement_steps"] = total_n_measurement_steps
    resource_estimates["graph_degree"] = graph_degree
    if verbose:
        resource_estimates["measurement_steps"] = total_measurement_steps
        plot_graph_state_with_measurement_steps(
            total_connected_graph, total_measurement_steps
        )
    return resource_estimates
