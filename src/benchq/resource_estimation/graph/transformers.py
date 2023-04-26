from typing import Callable

from ...compilation import (
    get_algorithmic_graph_from_graph_sim_mini,
    pyliqtr_transpile_to_clifford_t,
)
from ...compilation import simplify_rotations as _simplify_rotations
from ...data_structures import ErrorBudget, QuantumProgram, get_program_from_circuit
from .structs import GraphPartition


def synthesize_clifford_t(
    error_budget: ErrorBudget,
) -> Callable[[QuantumProgram], QuantumProgram]:
    def _transformer(program: QuantumProgram) -> QuantumProgram:
        circuits = [
            pyliqtr_transpile_to_clifford_t(
                circuit, circuit_precision=error_budget.synthesis_failure_tolerance
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
    delayed_gate_synthesis: bool,
    graph_production_method=get_algorithmic_graph_from_graph_sim_mini,
) -> Callable[[QuantumProgram], GraphPartition]:
    def _transformer(program: QuantumProgram) -> GraphPartition:
        graphs_list = [
            graph_production_method(circuit) for circuit in program.subroutines
        ]
        return GraphPartition(
            program, graphs_list, delayed_gate_synthesis=delayed_gate_synthesis
        )

    return _transformer


def create_big_graph_from_subcircuits(
    delayed_gate_synthesis: bool,
    graph_production_method=get_algorithmic_graph_from_graph_sim_mini,
) -> Callable[[QuantumProgram], GraphPartition]:
    def _transformer(program: QuantumProgram) -> GraphPartition:
        big_circuit = program.full_circuit
        new_program = get_program_from_circuit(big_circuit)
        graph = graph_production_method(big_circuit)
        return GraphPartition(
            new_program, [graph], delayed_gate_synthesis=delayed_gate_synthesis
        )

    return _transformer
