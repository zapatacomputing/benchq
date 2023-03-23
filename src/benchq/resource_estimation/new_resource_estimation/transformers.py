import json

from ...compilation import get_algorithmic_graph, pyliqtr_transpile_to_clifford_t
from ...data_structures import QuantumProgram
from .structs import GraphPartition


### There is probably a better name for this
def default_transformer(program: QuantumProgram, error_budget):
    graphs_list = []
    data_qubits_map_list = []
    # We assign the same amount of error budget to gate synthesis and error correction.
    synthesis_error_budget = (
        error_budget["synthesis_error_rate"] * error_budget["total_error"]
    )
    # TODO: add gate synthesis
    for circuit in program.subroutines:
        # TA 2 part: FTQC compilation
        clifford_t_circuit = pyliqtr_transpile_to_clifford_t(
            circuit, synthesis_accuracy=synthesis_error_budget
        )
        graphs_list.append(get_algorithmic_graph(clifford_t_circuit))
        with open("icm_output.json", "r") as f:
            output_dict = json.load(f)
            data_qubits_map = output_dict["data_qubits_map"]
        data_qubits_map_list.append(data_qubits_map)

    return GraphPartition(program, graphs_list, data_qubits_map_list)
