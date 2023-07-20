import numpy
import pytest

from benchq.resource_estimation import cost_estimator


@pytest.mark.parametrize(
    "SCC_time_low,SCC_time_high",
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
def test_monotonicity_of_duration_wrtSurfaceCC_time(SCC_time_low, SCC_time_high):
    num_logical_qubits = 12
    num_toffoli = 15
    physical_error_rate = 1.0e-4
    best_cost_low, best_params_low = cost_estimator(
        num_logical_qubits,
        num_toffoli=num_toffoli,
        surface_code_cycle_time=SCC_time_low,
        physical_error_rate=physical_error_rate,
    )
    best_cost_high, best_params_high = cost_estimator(
        num_logical_qubits,
        num_toffoli=num_toffoli,
        surface_code_cycle_time=SCC_time_high,
        physical_error_rate=physical_error_rate,
    )
    assert best_cost_high.duration > best_cost_low.duration


@pytest.mark.parametrize(
    "SCC_time_low,SCC_time_high",
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
def test_linearity_wrtSurfaceCC_time(SCC_time_low, SCC_time_high):
    num_logical_qubits = 12
    num_T = 13
    physical_error_rate = 1.0e-4
    best_cost_low, best_params_low = cost_estimator(
        num_logical_qubits,
        num_T=num_T,
        surface_code_cycle_time=SCC_time_low,
        physical_error_rate=physical_error_rate,
    )
    best_cost_high, best_params_high = cost_estimator(
        num_logical_qubits,
        num_T=num_T,
        surface_code_cycle_time=SCC_time_high,
        physical_error_rate=physical_error_rate,
    )

    numpy.testing.assert_almost_equal(
        best_cost_high.duration / SCC_time_high, best_cost_low.duration / SCC_time_low
    )


@pytest.mark.parametrize(
    "num_toffoli,num_T",
    [
        (20, 20),
        (40, 40),
        (20, 30),
    ],
)
def test_ratio_of_failure_prob(num_toffoli, num_T):
    num_logical_qubits = 12
    SCC_time = 0.000002
    physical_error_rate = 1.0e-4
    best_cost_toffoli, best_params_toffoli = cost_estimator(
        num_logical_qubits=num_logical_qubits,
        num_toffoli=num_toffoli,
        surface_code_cycle_time=SCC_time,
        physical_error_rate=physical_error_rate,
    )
    best_cost_T, best_params_T = cost_estimator(
        num_logical_qubits=num_logical_qubits,
        num_T=num_T,
        surface_code_cycle_time=SCC_time,
        physical_error_rate=physical_error_rate,
    )
    """
    This ascertains if ratio of failure rate of Toffoli
    and T Magic State factories is 2:1
    """

    assert (
        best_params_toffoli.magic_state_factory.failure_rate
        / best_params_T.magic_state_factory.failure_rate
        == 2.0
    )


@pytest.mark.parametrize(
    "num_toffoli,num_T",
    [
        (20, 20),
        (40, 40),
    ],
)
def test_algorithm_failure_prob_calculation(num_toffoli, num_T):
    num_logical_qubits = 12
    SCC_time = 0.000002
    physical_error_rate = 1.0e-4
    best_cost_toffoli, best_params_toffoli = cost_estimator(
        num_logical_qubits=num_logical_qubits,
        num_toffoli=num_toffoli,
        surface_code_cycle_time=SCC_time,
        physical_error_rate=physical_error_rate,
    )
    best_cost_T, best_params_T = cost_estimator(
        num_logical_qubits=num_logical_qubits,
        num_T=num_T,
        surface_code_cycle_time=SCC_time,
        physical_error_rate=physical_error_rate,
    )
    numpy.testing.assert_almost_equal(
        2
        * (
            best_cost_toffoli.algorithm_failure_probability
            - best_cost_T.algorithm_failure_probability
        )
        / num_toffoli,
        best_params_toffoli.magic_state_factory.failure_rate,
    )
    """
    X+Yf - (X+Yf/2) = Yf/2, where X+Yf and X+Yf/2 are
    Algorithm Failure Prob for Toffoli and T cases respectively,
    where X -> data failure, Yf -> distillation failure,
      Y=#Toffoli gate=#T gates and f is 1 CCZ error.
    If failure rate is calculated correctly, to ascertain
    if Algorithm Failure Probability is calculated correctly
    for both toffoli and T.
    """

    numpy.testing.assert_almost_equal(
        (
            best_cost_toffoli.algorithm_failure_probability
            - best_cost_T.algorithm_failure_probability
        )
        / num_T,
        best_params_T.magic_state_factory.failure_rate,
    )


def test_default_T_factories():
    num_logical_qubits = 12
    SCC_time = 0.000002
    physical_error_rate = 1.0e-3
    # Default Magic State Factory details used based
    # on this physical error rate.
    num_T = 200
    num_toffoli = 140
    best_cost_T, best_params_T = cost_estimator(
        num_logical_qubits=num_logical_qubits,
        num_T=num_T,
        surface_code_cycle_time=SCC_time,
        physical_error_rate=physical_error_rate,
    )
    best_cost, best_params_toffoli = cost_estimator(
        num_logical_qubits=num_logical_qubits,
        num_toffoli=num_toffoli,
        surface_code_cycle_time=SCC_time,
        physical_error_rate=physical_error_rate,
    )
    assert (
        best_params_T.magic_state_factory.rounds == 186
        and best_params_T.magic_state_factory.failure_rate == 3.6000000000000003e-16
    )
    assert (
        best_params_toffoli.magic_state_factory.rounds == 186
        and best_params_toffoli.magic_state_factory.failure_rate
        == 3.6000000000000003e-16
    )


def test_default_values():
    num_logical_qubits = 12
    physical_error_rate = 1.0e-4
    """
    If physical_error_rate != default value,
    this ascertains if both num_T=0 and num_toffoli=0,
    then it must throw an error.
    """
    with pytest.raises(SystemExit) as dvalue:
        a, b = cost_estimator(
            num_logical_qubits=num_logical_qubits,
            physical_error_rate=physical_error_rate,
        )

    assert dvalue.type == SystemExit
    assert dvalue.value.code == 1


def test_all_default_values():
    num_logical_qubits = 12
    """
    If physical_error_rate == default value,
    this ascertains if both num_T=0 and num_toffoli=0,
    then it must throw an error.
    """
    with pytest.raises(SystemExit) as dvalue:
        a, b = cost_estimator(
            num_logical_qubits=num_logical_qubits,
        )

    assert dvalue.type == SystemExit
    assert dvalue.value.code == 1
