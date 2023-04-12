from typing import Callable

from ...compilation import (
    get_algorithmic_graph_from_graph_sim_mini,
    get_algorithmic_graph_from_Jabalizer,
    pyliqtr_transpile_to_clifford_t,
)
from ...compilation import simplify_rotations as _simplify_rotations
from ...data_structures import QuantumProgram, get_program_from_circuit
from .structs import GraphPartition


def synthesize_clifford_t(error_budget) -> Callable[[QuantumProgram], QuantumProgram]:
    def _transformer(program: QuantumProgram) -> QuantumProgram:
        synthesis_error_budget = (
            error_budget["synthesis_error_rate"] * error_budget["total_error"]
        )
        circuits = [
            pyliqtr_transpile_to_clifford_t(
                circuit, circuit_precision=synthesis_error_budget
            )
            for circuit in program.subroutines
        ]
        return program.replace_circuits(circuits)

    return _transformer


def simplify_rotations(program: QuantumProgram) -> QuantumProgram:
    circuits = [_simplify_rotations(circuit) for circuit in program.subroutines]
    return QuantumProgram(
        circuits,
        steps=program.steps,
        calculate_subroutine_sequence=program.calculate_subroutine_sequence,
    )


def create_graphs_for_subcircuits(
    synthesized: bool, graph_production_method=get_algorithmic_graph_from_graph_sim_mini
) -> Callable[[QuantumProgram], GraphPartition]:
    def _transformer(program: QuantumProgram) -> GraphPartition:
        graphs_list = [
            graph_production_method(circuit) for circuit in program.subroutines
        ]
        return GraphPartition(program, graphs_list, synthesized=synthesized)

    return _transformer


def create_big_graph_from_subcircuits(
    synthesized: bool, graph_production_method=get_algorithmic_graph_from_graph_sim_mini
) -> Callable[[QuantumProgram], GraphPartition]:
    def _transformer(program: QuantumProgram) -> GraphPartition:
        big_circuit = program.full_circuit
        new_program = get_program_from_circuit(big_circuit)
        graph = graph_production_method(big_circuit)
        return GraphPartition(new_program, [graph], synthesized=synthesized)

    return _transformer
