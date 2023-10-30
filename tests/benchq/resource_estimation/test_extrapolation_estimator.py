from dataclasses import asdict, replace

import numpy as np
import pytest
from orquestra.quantum.circuits import CNOT, RZ, Circuit, H

from benchq.compilation import get_ruby_slippers_compiler
from benchq.data_structures import AlgorithmImplementation, ErrorBudget, QuantumProgram
from benchq.data_structures.hardware_architecture_models import (
    BASIC_SC_ARCHITECTURE_MODEL,
)
from benchq.resource_estimation.graph_estimator import (
    ExtrapolationResourceEstimator,
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_custom_extrapolation_pipeline,
    run_custom_resource_estimation_pipeline,
    synthesize_clifford_t,
    transpile_to_native_gates,
)

# Below is code snippet for inspecting the extrapolations visually
# you can paste it directly into the terminal when a test fails with
# the python debugger.
# from benchq.vizualization_tools import plot_extrapolations
# plot_extrapolations(extrapolated_resource_estimates, steps_to_extrapolate_from, n_measurement_steps_fit_type, gsc_resource_estimates) # noqa: E501

fast_ruby_slippers = get_ruby_slippers_compiler(
    teleportation_threshold=1e4,
    max_graph_size=1e5,
    decomposition_strategy=0,
)


@pytest.fixture(params=["time", "space"])
def optimization(request):
    return request.param


@pytest.fixture(params=[False, True])
def use_delayed_gate_synthesis(request):
    return request.param


def _get_transformers(use_delayed_gate_synthesis, error_budget):
    if not use_delayed_gate_synthesis:
        transformers = [
            transpile_to_native_gates,
            synthesize_clifford_t(error_budget),
            create_big_graph_from_subcircuits(fast_ruby_slippers),
        ]
    else:
        transformers = [
            transpile_to_native_gates,
            create_big_graph_from_subcircuits(fast_ruby_slippers),
        ]
    return transformers


def search_extra(this_dict, field):
    return this_dict.get(field, this_dict["extra"].get(field))


@pytest.mark.parametrize(
    "quantum_program,steps_to_extrapolate_from,n_measurement_steps_fit_type",
    [
        (
            QuantumProgram(
                [
                    Circuit([H(0), RZ(np.pi / 14)(0), CNOT(0, 1)]),
                    Circuit([H(0), H(1), RZ(np.pi / 14)(0)]),
                ],
                10,
                lambda x: [0] + [1] * x + [0],
            ),
            [2, 3, 4, 5],
            "logarithmic",
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
            [2, 3, 4, 5],
            "linear",
        ),
        (
            QuantumProgram(
                [
                    Circuit([H(0), RZ(np.pi / 14)(0), CNOT(0, 1)]),
                    Circuit([H(0), H(1), RZ(np.pi / 14)(0)]),
                    Circuit([H(0), H(1), CNOT(0, 1)]),
                ],
                20,
                lambda x: [0] + [1, 2] * x + [0],
            ),
            [2, 3, 4, 5, 10],
            "linear",
        ),
    ],
)
def test_get_resource_estimations_for_small_program_gives_correct_results(
    quantum_program,
    steps_to_extrapolate_from,
    use_delayed_gate_synthesis,
    n_measurement_steps_fit_type,
    optimization,
):
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL

    # set circuit generation weight to 0
    error_budget = ErrorBudget.from_weights(1e-2, 0, 1, 1)
    algorithm_implementation = AlgorithmImplementation(quantum_program, error_budget, 1)
    transformers = _get_transformers(use_delayed_gate_synthesis, error_budget)

    extrapolated_resource_estimates = run_custom_extrapolation_pipeline(
        algorithm_implementation,
        estimator=ExtrapolationResourceEstimator(
            architecture_model,
            steps_to_extrapolate_from,
            optimization=optimization,
            substrate_scheduler_preset="optimized",
            n_measurement_steps_fit_type=n_measurement_steps_fit_type,
        ),
        transformers=transformers,
    )
    gsc_resource_estimates = run_custom_resource_estimation_pipeline(
        algorithm_implementation,
        estimator=GraphResourceEstimator(
            architecture_model,
            optimization=optimization,
            substrate_scheduler_preset="optimized",
        ),
        transformers=transformers,
    )

    test_dict = asdict(extrapolated_resource_estimates)
    target_dict = asdict(gsc_resource_estimates)

    _fields_to_compare = [
        "n_nodes",
        "max_graph_degree",
        "code_distance",
        "n_measurement_steps",
    ]
    for field in _fields_to_compare:
        # esure that result isn't much lower than the target
        assert search_extra(test_dict, field) >= search_extra(target_dict, field) * 0.47
        # allow for larger margin of error when overestimating
        assert 3 * search_extra(target_dict, field) >= search_extra(test_dict, field)


@pytest.mark.parametrize(
    "quantum_program,steps_to_extrapolate_from,n_measurement_steps_fit_type",
    [
        (
            QuantumProgram(
                [
                    Circuit([H(0), RZ(np.pi / 14)(0), CNOT(0, 1)]),
                    Circuit([H(0), H(1), RZ(np.pi / 14)(0)]),
                ],
                1000,
                lambda x: [0] + [1] * x + [0],
            ),
            [10, 20, 50],
            "logarithmic",
        ),
        (
            QuantumProgram(
                [
                    Circuit([H(0), RZ(np.pi / 14)(0), CNOT(0, 1)]),
                    Circuit([H(0), H(1), RZ(np.pi / 14)(0)]),
                    Circuit([H(0), H(1), CNOT(0, 1)]),
                ],
                100,
                lambda x: [0] + [1, 2] * x + [0],
            ),
            [2, 3, 5, 7, 10, 15, 25],
            "linear",
        ),
    ],
)
def test_get_resource_estimations_for_large_program_gives_correct_results(
    quantum_program,
    steps_to_extrapolate_from,
    use_delayed_gate_synthesis,
    n_measurement_steps_fit_type,
    optimization,
):
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL
    # set circuit generation weight to 0
    error_budget = ErrorBudget.from_weights(1e-2, 0, 1, 1)
    algorithm_implementation = AlgorithmImplementation(quantum_program, error_budget, 1)
    transformers = _get_transformers(use_delayed_gate_synthesis, error_budget)

    extrapolated_resource_estimates = run_custom_extrapolation_pipeline(
        algorithm_implementation,
        estimator=ExtrapolationResourceEstimator(
            architecture_model,
            steps_to_extrapolate_from,
            n_measurement_steps_fit_type=n_measurement_steps_fit_type,
            optimization=optimization,
            max_graph_degree_fit_type="linear",
        ),
        transformers=transformers,
    )
    gsc_resource_estimates = run_custom_resource_estimation_pipeline(
        algorithm_implementation,
        estimator=GraphResourceEstimator(architecture_model, optimization=optimization),
        transformers=transformers,
    )

    test_dict = asdict(extrapolated_resource_estimates)
    target_dict = asdict(gsc_resource_estimates)

    _fields_to_compare_harshly = ["n_nodes", "n_logical_qubits", "n_measurement_steps"]
    for field in _fields_to_compare_harshly:
        # esure that result isn't much lower than the target
        assert search_extra(test_dict, field) >= search_extra(target_dict, field) * 0.5
        # allow for larger margin of error when overestimating
        assert 10 * search_extra(target_dict, field) >= search_extra(test_dict, field)

    assert (
        abs(
            extrapolated_resource_estimates.code_distance
            - gsc_resource_estimates.code_distance
        )
        <= 3
    )


def test_better_architecture_does_not_require_more_resources(
    use_delayed_gate_synthesis, optimization
):
    low_noise_architecture_model = replace(
        BASIC_SC_ARCHITECTURE_MODEL, physical_qubit_error_rate=1e-4
    )

    high_noise_architecture_model = BASIC_SC_ARCHITECTURE_MODEL

    # set circuit generation weight to 0
    error_budget = ErrorBudget.from_weights(1e-3, 0, 1, 1)
    transformers = _get_transformers(use_delayed_gate_synthesis, error_budget)

    circuit = Circuit([H(0), RZ(np.pi / 4)(0), CNOT(0, 1)])
    quantum_program = QuantumProgram(
        subroutines=[circuit],
        steps=100,
        calculate_subroutine_sequence=lambda x: [0] * x,
    )
    algorithm_implementation = AlgorithmImplementation(quantum_program, error_budget, 1)
    low_noise_resource_estimates = run_custom_extrapolation_pipeline(
        algorithm_implementation,
        estimator=ExtrapolationResourceEstimator(
            low_noise_architecture_model, [1, 2, 3, 4], optimization=optimization
        ),
        transformers=transformers,
    )

    high_noise_resource_estimates = run_custom_extrapolation_pipeline(
        algorithm_implementation,
        estimator=ExtrapolationResourceEstimator(
            high_noise_architecture_model, [1, 2, 3, 4], optimization=optimization
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
    use_delayed_gate_synthesis, optimization
):
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL
    low_failure_tolerance = 1e-3
    high_failure_tolerance = 1e-2

    # set circuit generation weight to 0
    low_error_budget = ErrorBudget.from_weights(low_failure_tolerance, 0, 1, 1)
    high_error_budget = ErrorBudget.from_weights(high_failure_tolerance, 0, 1, 1)

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
    algorithm_implementation_low_error_budget = AlgorithmImplementation(
        quantum_program, low_error_budget, 1
    )
    algorithm_implementation_high_error_budget = AlgorithmImplementation(
        quantum_program, high_error_budget, 1
    )

    low_error_resource_estimates = run_custom_extrapolation_pipeline(
        algorithm_implementation_low_error_budget,
        estimator=ExtrapolationResourceEstimator(
            architecture_model, [1, 2, 3, 4], optimization=optimization
        ),
        transformers=low_error_transformers,
    )

    high_error_resource_estimates = run_custom_extrapolation_pipeline(
        algorithm_implementation_high_error_budget,
        estimator=ExtrapolationResourceEstimator(
            architecture_model, [1, 2, 3, 4], optimization=optimization
        ),
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
