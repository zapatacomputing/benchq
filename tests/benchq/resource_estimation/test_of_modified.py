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
    best_cost_low, best_params_low = cost_estimator(
        num_logical_qubits, num_toffoli, SCC_time_low
    )
    best_cost_high, best_params_high = cost_estimator(
        num_logical_qubits, num_toffoli, SCC_time_high
    )

    print("High, low: ", best_cost_high.duration, best_cost_low.duration)
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
    num_toffoli = 15
    best_cost_low, best_params_low = cost_estimator(
        num_logical_qubits, num_toffoli, SCC_time_low
    )
    best_cost_high, best_params_high = cost_estimator(
        num_logical_qubits, num_toffoli, SCC_time_high
    )

    numpy.testing.assert_almost_equal(
        best_cost_high.duration / SCC_time_high, best_cost_low.duration / SCC_time_low
    )
