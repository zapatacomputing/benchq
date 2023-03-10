import numpy as np
from orquestra.quantum.circuits import CNOT, RZ, Circuit, H

from benchq.data_structures.hardware_architecture_models import BasicArchitectureModel
from benchq.data_structures.quantum_program import QuantumProgram
from benchq.resource_estimation.graph_compilation import (
    get_resource_estimations_for_program,
)


def test_get_resource_estimations_for_program_gives_correct_n_measurement_steps():
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
    error_budget = 1e-3
    circuit = Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    quantum_program = QuantumProgram(
        subroutines=[circuit], steps=1, calculate_subroutine_sequence=lambda x: [0]
    )
    gsc_resource_estimates = get_resource_estimations_for_program(
        quantum_program,
        error_budget,
        architecture_model,
        plot=True,
    )
    
    assert gsc_resource_estimates["n_measurement_steps"] == 3
    assert gsc_resource_estimates["n_nodes"] == 3
    assert gsc_resource_estimates["max_graph_degree"] == 2

    # Note that error_budget is a bound for the sum of the gate synthesis error and
    # logical error. Therefore the expression below is a loose upper bound for the
    # logical error rate.
    assert gsc_resource_estimates["logical_error_rate"] < error_budget
