import numpy
import pytest

from benchq.resource_estimators.footprint_estimators.openfermion_estimator import (
    cost_estimator,
)


@pytest.mark.parametrize(
    "scc_time_low,scc_time_high",
    [
        (0.000001, 0.000002),
        (0.000003, 0.000004),
        (0.000001, 0.000009),
        (0.000005, 0.000028),
        (0.000005, 0.000010),
        (0.000015, 0.000016),
        (0.000007, 0.000009),
        (0.000001, 0.000008),
        (0.000004, 0.000009),
        (0.000001, 0.000009),
    ],
)
def test_monotonicity_of_duration_wrtSurfaceCC_time(scc_time_low, scc_time_high):
    """
    This tests if duration (run-time) increases as surface code cycle time increases
    """
    num_logical_qubits = 12
    num_toffoli = 15
    physical_error_rate = 1.0e-4
    best_cost_low, best_params_low = cost_estimator(
        num_logical_qubits,
        num_toffoli=num_toffoli,
        surface_code_cycle_time=scc_time_low,
        physical_error_rate=physical_error_rate,
        hardware_failure_tolerance=1e-1,
    )
    best_cost_high, best_params_high = cost_estimator(
        num_logical_qubits,
        num_toffoli=num_toffoli,
        surface_code_cycle_time=scc_time_high,
        physical_error_rate=physical_error_rate,
        hardware_failure_tolerance=1e-1,
    )
    assert best_cost_high.duration > best_cost_low.duration


@pytest.mark.parametrize(
    "scc_time_low,scc_time_high",
    [
        (0.000001, 0.000002),
        (0.000003, 0.000004),
        (0.000001, 0.000009),
        (0.000005, 0.000028),
        (0.000005, 0.000010),
        (0.000015, 0.000016),
        (0.000007, 0.000009),
        (0.000001, 0.000008),
        (0.000004, 0.000009),
        (0.000001, 0.000009),
    ],
)
def test_linearity_wrtSurfaceCC_time(scc_time_low, scc_time_high):
    """
    This tests if duration (run-time) proportionately
    increases wrt surface code cycle time
    """
    num_logical_qubits = 12
    num_t = 13
    physical_error_rate = 1.0e-4
    best_cost_low, best_params_low = cost_estimator(
        num_logical_qubits,
        num_t=num_t,
        surface_code_cycle_time=scc_time_low,
        physical_error_rate=physical_error_rate,
        hardware_failure_tolerance=1e-1,
    )
    best_cost_high, best_params_high = cost_estimator(
        num_logical_qubits,
        num_t=num_t,
        surface_code_cycle_time=scc_time_high,
        physical_error_rate=physical_error_rate,
        hardware_failure_tolerance=1e-1,
    )

    numpy.testing.assert_almost_equal(
        best_cost_high.duration / scc_time_high, best_cost_low.duration / scc_time_low
    )


@pytest.mark.parametrize(
    "num_toffoli,num_t",
    [
        (20, 20),
        (40, 40),
        (20, 30),
    ],
)
def test_ratio_of_failure_prob(num_toffoli, num_t):
    """
    This ascertains if ratio of failure rate of magic state factory for a ckt
    with only Toffoli gates and of a ckt with only T gates is 1:1, given the same
    physical error rate and surface code cycle time.

    """
    num_logical_qubits = 12
    scc_time = 0.000002
    physical_error_rate = 1.0e-4
    best_cost_toffoli, best_params_toffoli = cost_estimator(
        num_logical_qubits=num_logical_qubits,
        num_toffoli=num_toffoli,
        surface_code_cycle_time=scc_time,
        physical_error_rate=physical_error_rate,
        hardware_failure_tolerance=1e-1,
    )
    best_cost_t, best_params_t = cost_estimator(
        num_logical_qubits=num_logical_qubits,
        num_t=num_t,
        surface_code_cycle_time=scc_time,
        physical_error_rate=physical_error_rate,
        hardware_failure_tolerance=1e-1,
    )

    assert (
        best_params_toffoli.magic_state_factory.distilled_magic_state_error_rate
        / best_params_t.magic_state_factory.distilled_magic_state_error_rate
        == 1.0
    )


@pytest.mark.parametrize(
    "num_toffoli,num_t",
    [
        (20, 20),
        (40, 40),
    ],
)
def test_calc_of_algorithm_failure_prob(num_toffoli, num_t):
    """
    X+Yf - 2*(X/2+Yf/2) = 0, where X+Yf and (X+Yf)/2 are
    Algorithm Failure Prob for toffoli and t cases respectively,
    where X -> data failure, Yf -> distillation failure,
      Y=#toffoli gate=#t gates and f is 1 CCZ error.
    If failure rate is calculated correctly, to ascertain
    if Algorithm Failure Probability is calculated correctly
    for both toffoli and t.
    """
    num_logical_qubits = 12
    scc_time = 0.000002
    physical_error_rate = 1.0e-4
    best_cost_toffoli, best_params_toffoli = cost_estimator(
        num_logical_qubits=num_logical_qubits,
        num_toffoli=num_toffoli,
        surface_code_cycle_time=scc_time,
        physical_error_rate=physical_error_rate,
        hardware_failure_tolerance=1e-1,
    )
    best_cost_t, best_params_t = cost_estimator(
        num_logical_qubits=num_logical_qubits,
        num_t=num_t,
        surface_code_cycle_time=scc_time,
        physical_error_rate=physical_error_rate,
        hardware_failure_tolerance=1e-1,
    )
    numpy.testing.assert_almost_equal(
        (
            best_cost_toffoli.algorithm_failure_probability
            - 2 * best_cost_t.algorithm_failure_probability
        ),
        0,
        decimal=5,
    )


def test_algorithm_failure_prob_calculation():
    """
    To ascertain if algorithm failure probability is
    calculated correctly for a ckt with (num_toffoli=20,
    num_t=20) and for a ckt with (num_toffoli=30,
    num_t=0)
    """
    num_logical_qubits = 12
    scc_time = 0.000002
    physical_error_rate = 1.0e-4
    best_cost_toffoli, best_params_toffoli = cost_estimator(
        num_logical_qubits=num_logical_qubits,
        num_toffoli=20,
        num_t=20,
        surface_code_cycle_time=scc_time,
        physical_error_rate=physical_error_rate,
        hardware_failure_tolerance=1e-1,
    )
    best_cost_t, best_params_t = cost_estimator(
        num_logical_qubits=num_logical_qubits,
        num_toffoli=30,
        num_t=0,
        surface_code_cycle_time=scc_time,
        physical_error_rate=physical_error_rate,
        hardware_failure_tolerance=1e-1,
    )
    numpy.testing.assert_almost_equal(
        best_cost_toffoli.algorithm_failure_probability,
        best_cost_t.algorithm_failure_probability,
    )


def test_default_values():
    """
    If physical_error_rate != default value,
    this ascertains if both num_t=0 and num_toffoli=0,
    then it must throw an error. This basically tests
    the 'else statement' in iter_known_factories()
    """
    num_logical_qubits = 12
    physical_error_rate = 1.0e-4
    with pytest.raises(ValueError) as dvalue:
        a, b = cost_estimator(
            num_logical_qubits=num_logical_qubits,
            physical_error_rate=physical_error_rate,
        )

    assert dvalue.type == ValueError


def test_all_default_values():
    """
    If physical_error_rate == default value,
     this ascertains if both num_t=0 and num_toffoli=0,
     then it must throw an error. This basically tests
     the 'if statement' in iter_known_factories()
    """
    num_logical_qubits = 12
    with pytest.raises(ValueError) as dvalue:
        a, b = cost_estimator(
            num_logical_qubits=num_logical_qubits,
        )

    assert dvalue.type == ValueError
