import json
from functools import singledispatch

from ...compilation import (
    get_algorithmic_graph,
    pyliqtr_transpile_to_clifford_t,
    simplify_rotations,
)
from ...data_structures import QuantumProgram
from .structs import GraphPartition


def synthesize_clifford_t(program: QuantumProgram, error_budget) -> GraphPartition:
    graphs_list = []
    data_qubits_map_list = []
    # We assign the same amount of error budget to gate synthesis and error correction.
    synthesis_error_budget = (
        error_budget["synthesis_error_rate"] * error_budget["total_error"]
    )
    for circuit in program.subroutines:
        clifford_t_circuit = pyliqtr_transpile_to_clifford_t(
            circuit, synthesis_accuracy=synthesis_error_budget
        )
        graphs_list.append(get_algorithmic_graph(clifford_t_circuit))
        with open("icm_output.json", "r") as f:
            output_dict = json.load(f)
            data_qubits_map = output_dict["data_qubits_map"]
        data_qubits_map_list.append(data_qubits_map)

    return GraphPartition(program, graphs_list, data_qubits_map_list, synthesized=True)


def simplify_only(program: QuantumProgram, error_budget) -> GraphPartition:
    graphs_list = []
    data_qubits_map_list = []

    for circuit in program.subroutines:
        simplified_circuit = simplify_rotations(circuit)
        graphs_list.append(get_algorithmic_graph(simplified_circuit))
        with open("icm_output.json", "r") as f:
            output_dict = json.load(f)
            data_qubits_map = output_dict["data_qubits_map"]
        data_qubits_map_list.append(data_qubits_map)

    return GraphPartition(program, graphs_list, data_qubits_map_list, synthesized=False)
