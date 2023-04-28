from copy import copy

import numpy as np
import pytest
from orquestra.quantum.circuits import CNOT, RZ, Circuit, H

from benchq.data_structures import AlgorithmDescription, ErrorBudget, QuantumProgram
from benchq.data_structures.hardware_architecture_models import BasicArchitectureModel
from benchq.resource_estimation.graph import (
    ExtrapolationResourceEstimator,
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_custom_extrapolation_pipeline,
    run_custom_resource_estimation_pipeline,
    simplify_rotations,
    synthesize_clifford_t,
)
from benchq.vizualization_tools import plot_extrapolations

# Below is code snippet for inspecting the extrapolations visually
# you can paste it directly into the terminal when a test fails with
# the python debugger.
# plot_extrapolations(extrapolated_resource_estimates, steps_to_extrapolate_from, n_measurement_steps_fit_type, gsc_resource_estimates) # noqa: E501


@pytest.fixture(params=[False, True])
def use_delayed_gate_synthesis(request):
    return request.param


def _get_transformers(use_delayed_gate_synthesis, error_budget):
    if not use_delayed_gate_synthesis:
        transformers = [
            synthesize_clifford_t(error_budget),
            create_big_graph_from_subcircuits(),
        ]
    else:
        transformers = [
            simplify_rotations,
            create_big_graph_from_subcircuits(),
        ]
    return transformers


@pytest.mark.parametrize(
    "quantum_program,steps_to_extrapolate_from,n_measurement_steps_fit_type",
    [
        (
            QuantumProgram(
                [
                    Circuit([H(0), RZ(np.pi / 14)(0), CNOT(0, 1)]),
                    Circuit([H(0), H(1), RZ(np.pi / 14)(0)]),
                ],
                5,
                lambda x: [0] + [1] * x + [0],
            ),
            [2, 3, 4],
            "linear",
        ),
        (
            QuantumProgram(
                [
                    Circuit([H(0), RZ(np.pi / 14)(0), CNOT(0, 1)]),
                    Circuit([H(0), H(1), RZ(np.pi / 14)(0)]),
                ],
                10,
                lambda x: [0] + [1] * x + [0],
            ),
            [2, 3, 4],
            "linear",
        ),
        (
            QuantumProgram(
                [
                    Circuit([H(0), RZ(np.pi / 14)(0), CNOT(0, 1)]),
                    Circuit([H(0), H(1), RZ(np.pi / 14)(0)]),
                    Circuit([H(0), H(1), CNOT(0, 1)]),
                ],
                8,
                lambda x: [0] + [1, 2] * x + [0],
            ),
            [1, 2, 3, 5],
            "linear",
        ),
    ],
)
def test_get_resource_estimations_for_small_program_gives_correct_results(
    quantum_program,
    steps_to_extrapolate_from,
    use_delayed_gate_synthesis,
    n_measurement_steps_fit_type,
):
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
    error_budget = ErrorBudget(
        ultimate_failure_tolerance=1e-2, circuit_generation_weight=0
    )
    algorithm_description = AlgorithmDescription(quantum_program, error_budget, 1)
    transformers = _get_transformers(use_delayed_gate_synthesis, error_budget)

    extrapolated_resource_estimates = run_custom_extrapolation_pipeline(
        copy(algorithm_description),
        estimator=ExtrapolationResourceEstimator(
            architecture_model,
            steps_to_extrapolate_from,
            n_measurement_steps_fit_type=n_measurement_steps_fit_type,
        ),
        transformers=transformers,
    )
    gsc_resource_estimates = run_custom_resource_estimation_pipeline(
        copy(algorithm_description),
        estimator=GraphResourceEstimator(architecture_model),
        transformers=transformers,
    )

    attributes_to_compare_harshly = [
        "n_nodes",
        "total_time_in_seconds",
        "n_physical_qubits",
    ]
    for attribute in attributes_to_compare_harshly:
        assert np.isclose(
            getattr(extrapolated_resource_estimates, attribute),
            getattr(gsc_resource_estimates, attribute),
            rtol=1e-2,
        )
    # assert that the number of measurement steps grows with the steps
    attributes_to_compare_loosely = [
        "n_logical_qubits",
        "n_measurement_steps",
        "code_distance",
    ]
    for attribute in attributes_to_compare_loosely:
        assert (
            abs(
                getattr(extrapolated_resource_estimates, attribute)
                - getattr(gsc_resource_estimates, attribute)
            )
            <= 3
        )


@pytest.mark.parametrize(
    "quantum_program,steps_to_extrapolate_from,n_measurement_steps_fit_type",
    [
        (
            QuantumProgram(
                [
                    Circuit([H(0), RZ(np.pi / 14)(0), CNOT(0, 1)]),
                    Circuit([H(0), H(1), RZ(np.pi / 14)(0)]),
                ],
                1001,
                lambda x: [0] + [1] * x + [0],
            ),
            [1, 2, 3, 5, 10, 20],
            "logarithmic",
        ),
        (
            QuantumProgram(
                [
                    Circuit([H(0), RZ(np.pi / 14)(0), CNOT(0, 1)]),
                    Circuit([H(0), H(1), RZ(np.pi / 14)(0)]),
                    Circuit([H(0), H(1), CNOT(0, 1)]),
                ],
                200,
                lambda x: [0] + [1, 2] * x + [0],
            ),
            [1, 2, 3, 5, 7, 10, 15, 25],
            "linear",
        ),
    ],
)
def test_get_resource_estimations_for_large_program_gives_correct_results(
    quantum_program,
    steps_to_extrapolate_from,
    use_delayed_gate_synthesis,
    n_measurement_steps_fit_type,
):
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
    error_budget = ErrorBudget(
        ultimate_failure_tolerance=1e-2, circuit_generation_weight=0
    )
    algorithm_description = AlgorithmDescription(quantum_program, error_budget, 1)
    transformers = _get_transformers(use_delayed_gate_synthesis, error_budget)

    extrapolated_resource_estimates = run_custom_extrapolation_pipeline(
        copy(algorithm_description),
        estimator=ExtrapolationResourceEstimator(
            architecture_model,
            steps_to_extrapolate_from,
            n_measurement_steps_fit_type=n_measurement_steps_fit_type,
        ),
        transformers=transformers,
    )
    gsc_resource_estimates = run_custom_resource_estimation_pipeline(
        copy(algorithm_description),
        estimator=GraphResourceEstimator(architecture_model),
        transformers=transformers,
    )

    attributes_to_compare_relatively = [
        "n_nodes",
        "total_time_in_seconds",
        "n_physical_qubits",
        "n_logical_qubits",
    ]
    for attribute in attributes_to_compare_relatively:
        assert np.isclose(
            getattr(extrapolated_resource_estimates, attribute),
            getattr(gsc_resource_estimates, attribute),
            rtol=1e-1,
        )

    assert (
        abs(
            extrapolated_resource_estimates.code_distance
            - gsc_resource_estimates.code_distance
        )
        <= 3
    )
    assert (
        abs(
            extrapolated_resource_estimates.n_measurement_steps
            - gsc_resource_estimates.n_measurement_steps
        )
        <= 10
    )


def test_better_architecture_does_not_require_more_resources(
    use_delayed_gate_synthesis,
):
    low_noise_architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-4,
        physical_gate_time_in_seconds=1e-6,
    )
    high_noise_architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
    error_budget = ErrorBudget(
        ultimate_failure_tolerance=1e-2, circuit_generation_weight=0
    )
    transformers = _get_transformers(use_delayed_gate_synthesis, error_budget)

    circuit = Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    quantum_program = QuantumProgram(
        subroutines=[circuit],
        steps=100,
        calculate_subroutine_sequence=lambda x: [0] * x,
    )
    algorithm_description = AlgorithmDescription(quantum_program, error_budget, 1)
    low_noise_resource_estimates = run_custom_extrapolation_pipeline(
        copy(algorithm_description),
        estimator=ExtrapolationResourceEstimator(
            low_noise_architecture_model, [1, 2, 3, 4]
        ),
        transformers=transformers,
    )

    high_noise_resource_estimates = run_custom_extrapolation_pipeline(
        copy(algorithm_description),
        estimator=ExtrapolationResourceEstimator(
            high_noise_architecture_model, [1, 2, 3, 4]
        ),
        transformers=transformers,
    )

    assert (
        low_noise_resource_estimates.n_physical_qubits
        <= high_noise_resource_estimates.n_physical_qubits
    )
    assert (
        low_noise_resource_estimates.code_distance
        <= high_noise_resource_estimates.code_distance
    )
    assert (
        low_noise_resource_estimates.total_time_in_seconds
        <= high_noise_resource_estimates.total_time_in_seconds
    )


def test_higher_error_budget_does_not_require_more_resources(
    use_delayed_gate_synthesis,
):
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )
    low_failure_tolerance = 1e-3
    high_failure_tolerance = 1e-2

    low_error_budget = ErrorBudget(
        ultimate_failure_tolerance=low_failure_tolerance, circuit_generation_weight=0
    )
    high_error_budget = ErrorBudget(
        ultimate_failure_tolerance=high_failure_tolerance, circuit_generation_weight=0
    )
    low_error_transformers = _get_transformers(
        use_delayed_gate_synthesis, low_error_budget
    )
    high_error_transformers = _get_transformers(
        use_delayed_gate_synthesis, high_error_budget
    )

    circuit = Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    quantum_program = QuantumProgram(
        subroutines=[circuit],
        steps=100,
        calculate_subroutine_sequence=lambda x: [0] * x,
    )
    algorithm_description_low_error_budget = AlgorithmDescription(
        quantum_program, low_error_budget, 1
    )
    algorithm_description_high_error_budget = AlgorithmDescription(
        quantum_program, high_error_budget, 1
    )

    low_error_resource_estimates = run_custom_extrapolation_pipeline(
        algorithm_description_low_error_budget,
        estimator=ExtrapolationResourceEstimator(architecture_model, [1, 2, 3, 4]),
        transformers=low_error_transformers,
    )

    high_error_resource_estimates = run_custom_extrapolation_pipeline(
        algorithm_description_high_error_budget,
        estimator=ExtrapolationResourceEstimator(architecture_model, [1, 2, 3, 4]),
        transformers=high_error_transformers,
    )

    assert (
        high_error_resource_estimates.n_physical_qubits
        <= low_error_resource_estimates.n_physical_qubits
    )
    assert (
        high_error_resource_estimates.code_distance
        <= low_error_resource_estimates.code_distance
    )
    assert (
        high_error_resource_estimates.total_time_in_seconds
        <= low_error_resource_estimates.total_time_in_seconds
    )
