################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
from typing import Any

import numpy as np
from orquestra.quantum.circuits import Circuit
from orquestra.quantum.decompositions import decompose_orquestra_circuit

from ..compilation import get_algorithmic_graph, pyliqtr_transpile_to_clifford_t

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
    n_nodes,
    architecture_model: Any,
    tolerable_logical_error_rate=0.5,
):
    physical_gate_error_rate = architecture_model.physical_gate_error_rate
    physical_gate_time_in_seconds = architecture_model.physical_gate_time_in_seconds

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
    return {
        "logical_error_rate": final_logical_error_rate,
        "total_time": total_time,
        "physical_qubit_count": physical_qubit_count,
        "min_viable_distance": min_viable_distance,
        "synthesis_error_rate": synthesis_error_rate,
        "resources_in_cells": resources_in_cells,
    }


def get_resource_estimations_for_program(
    quantum_program, error_budget, architecture_model
):
    """_summary_

    Args:
        quantum_program: _description_
        error_budget: _description_
        architecture_model: _description_
    """
    n_nodes_list = []
    # We assign the same amount of error budget to gate synthesis and error correction.
    synthesis_error_budget = error_budget / 2
    ec_error_budget = error_budget / 2

    for circuit in quantum_program.subroutines:
        # TA 2 part: FTQC compilation
        clifford_t_circuit = pyliqtr_transpile_to_clifford_t(
            circuit, synthesis_accuracy=synthesis_error_budget
        )
        graph = get_algorithmic_graph(clifford_t_circuit)
        n_nodes_list.append(len(graph))

    return resource_estimations_for_subcomponents(
        n_nodes_list,
        quantum_program,
        architecture_model,
        ec_error_budget,
    )


def resource_estimations_for_subcomponents(
    n_nodes_list, quantum_program, architecture_model, tolerable_circuit_error_rate
):
    total_n_nodes = sum(
        n_nodes * mult
        for n_nodes, mult in zip(n_nodes_list, quantum_program.multiplicities)
    )

    resource_estimates = get_resource_estimations_for_graph(
        total_n_nodes, architecture_model, tolerable_circuit_error_rate
    )
    resource_estimates["n_nodes"] = n_nodes_list
    resource_estimates["steps"] = quantum_program.steps

    return resource_estimates
