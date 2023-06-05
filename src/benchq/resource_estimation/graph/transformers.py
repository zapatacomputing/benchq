from typing import Callable, Sequence

from ...compilation import (
    get_algorithmic_graph_from_graph_sim_mini,
    pyliqtr_transpile_to_clifford_t,
)
from ...compilation import simplify_rotations as _simplify_rotations
from ...data_structures import (
    ErrorBudget,
    GraphPartition,
    QuantumProgram,
    get_program_from_circuit,
)


def _distribute_transpilation_failure_tolerance(
    program: QuantumProgram, total_transpilation_failure_tolerance: float
) -> Sequence[float]:
    n_rots_per_subroutine = [
        program.count_gates_in_subroutine(i, ["RX", "RY", "RZ"])
        for i in range(len(program.subroutines))
    ]
    # Not using program n_rotation_gates because we already computed partial
    # counts for subroutines.
    n_total_rots = sum(
        n_rotations * multi
        for n_rotations, multi in zip(n_rots_per_subroutine, program.multiplicities)
    )

    return (
        [0 for _ in program.subroutines]
        if n_total_rots == 0
        else [
            total_transpilation_failure_tolerance * count / n_total_rots
            for count in n_rots_per_subroutine
        ]
    )


def synthesize_clifford_t(
    error_budget: ErrorBudget,
) -> Callable[[QuantumProgram], QuantumProgram]:
    def _transformer(program: QuantumProgram) -> QuantumProgram:
        tolerances = _distribute_transpilation_failure_tolerance(
            program, error_budget.transpilation_failure_tolerance
        )
        circuits = [
            pyliqtr_transpile_to_clifford_t(circuit, circuit_precision=tolerance)
            for circuit, tolerance in zip(program.subroutines, tolerances)
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
    graph_production_method=get_algorithmic_graph_from_graph_sim_mini,
) -> Callable[[QuantumProgram], GraphPartition]:
    def _transformer(program: QuantumProgram) -> GraphPartition:
        graphs_list = [
            graph_production_method(circuit) for circuit in program.subroutines
        ]
        return GraphPartition(program, graphs_list)

    return _transformer


def create_big_graph_from_subcircuits(
    graph_production_method=get_algorithmic_graph_from_graph_sim_mini,
) -> Callable[[QuantumProgram], GraphPartition]:
    def _transformer(program: QuantumProgram) -> GraphPartition:
        big_circuit = program.full_circuit
        new_program = get_program_from_circuit(big_circuit)
        graph = graph_production_method(big_circuit)
        return GraphPartition(new_program, [graph])

    return _transformer
