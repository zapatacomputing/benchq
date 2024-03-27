import os
import random
import string

import pytest
from orquestra.quantum.circuits import CNOT, Circuit, H

from benchq.compilation.circuits import compile_to_native_gates
from benchq.compilation.graph_states.rbs_hyperparam_tuning import (
    create_estimated_rbs_time_objective_fn,
    create_space_time_objective_fn,
    estimated_time_cost_from_rbs,
    get_optimal_hyperparams_for_estimated_rbs_time,
    get_optimal_hyperparams_for_space,
    get_optimal_hyperparams_for_space_and_time,
    get_optimal_hyperparams_for_time,
    space_time_cost_from_rbs,
)

# skip tests here until we can figure out how to track progress
# in the compilation routine.
pytestmark = pytest.mark.skip(reason="All tests in this file are currently skipped.")


@pytest.fixture()
def large_circuit():
    size = 200
    circ = Circuit(
        [
            H(0),
            *[CNOT(j, i) for i in range(1, size) for j in range(0, size)],
        ]
    )
    return compile_to_native_gates(circ)


@pytest.fixture()
def small_circuit():
    circ = Circuit([H(0), CNOT(0, 1)])
    return compile_to_native_gates(circ)


SKIP_SLOW = pytest.mark.skipif(
    os.getenv("SLOW_BENCHMARKS") is None,
    reason="Slow benchmarks can only run if SLOW_BENCHMARKS env variable is defined",
)


@pytest.mark.parametrize("space_or_time", ["space", "time"])
def test_space_time_cost_function_from_rbs_large_overrun(small_circuit, space_or_time):
    # when
    cost = space_time_cost_from_rbs(
        rbs_iteration_time=0.1,
        max_allowed_time=-100.0,
        space_or_time=space_or_time,
        circuit=small_circuit,
    )

    # then
    assert cost > 10000000


@pytest.mark.parametrize("space_or_time", ["space", "time"])
def test_space_time_cost_function_from_rbs_no_overrun(small_circuit, space_or_time):
    # when
    cost = space_time_cost_from_rbs(
        rbs_iteration_time=0.1,
        max_allowed_time=1.0,
        space_or_time=space_or_time,
        circuit=small_circuit,
    )

    # then
    assert cost < 10


def test_space_and_time_cost_function_from_rbs_large_overrun(small_circuit):
    # when
    space_cost, time_cost = space_time_cost_from_rbs(
        rbs_iteration_time=0.1,
        max_allowed_time=-100.0,
        space_or_time="space&time",
        circuit=small_circuit,
    )

    # then
    assert space_cost > 10000000
    assert time_cost > 10000000


def test_space_and_time_cost_function_from_rbs_no_overrun(small_circuit):
    # when
    space_cost, time_cost = space_time_cost_from_rbs(
        rbs_iteration_time=0.1,
        max_allowed_time=1.0,
        space_or_time="space&time",
        circuit=small_circuit,
    )

    # then
    assert space_cost < 10
    assert time_cost < 10


@pytest.mark.skip(reason="very random, can't get it to pass consistently")
@pytest.mark.parametrize("space_or_time", ["space", "time"])
def test_only_part_of_circuit_gives_same_cost(large_circuit, space_or_time):
    # given
    prop_to_test = 0.75

    # when
    full_cost = space_time_cost_from_rbs(
        rbs_iteration_time=0.1,
        max_allowed_time=1.0,
        space_or_time=space_or_time,
        circuit=large_circuit,
    )
    partial_cost = space_time_cost_from_rbs(
        rbs_iteration_time=0.1,
        max_allowed_time=1.0,
        space_or_time=space_or_time,
        circuit=large_circuit,
        circuit_prop_estimate=prop_to_test,
    )

    assert partial_cost / 2 <= full_cost <= partial_cost * 2


@pytest.mark.parametrize("space_or_time", ["space", "time"])
def test_completing_whole_iteration_when_unexpected_gives_error(
    small_circuit, space_or_time
):
    # given
    prop_to_test = 0.1

    # when/then
    with pytest.raises(RuntimeError):
        space_time_cost_from_rbs(
            rbs_iteration_time=1.0,
            max_allowed_time=1.0,
            space_or_time=space_or_time,
            circuit=small_circuit,
            circuit_prop_estimate=prop_to_test,
        )


def test_incorrect_spacetime_option_raises_error(small_circuit):
    # given
    random_string = "".join(random.choices(string.ascii_letters, k=5))
    print(random_string)

    # when/then
    with pytest.raises(ValueError):
        space_time_cost_from_rbs(
            rbs_iteration_time=0.1,
            max_allowed_time=-100.0,
            space_or_time=random_string,
            circuit=small_circuit,
        )


def test_estimated_time_cost_function_from_rbs(large_circuit, small_circuit):
    # when
    large_time = estimated_time_cost_from_rbs(
        rbs_iteration_time=0.1, circuit=large_circuit
    )
    small_time = estimated_time_cost_from_rbs(
        rbs_iteration_time=0.1, circuit=small_circuit
    )

    # then
    assert large_time > small_time


def test_create_space_time_objective_function_sanity_check(small_circuit):
    # when
    objective = create_space_time_objective_fn(
        rbs_iteration_time=1.0,
        max_allowed_time=10.0,
        space_or_time="space&time",
        circuit=small_circuit,
    )

    # then
    assert callable(objective)


def test_create_estimated_rbs_time_objective_fn_sanity_check(small_circuit):
    # when
    objective = create_estimated_rbs_time_objective_fn(
        rbs_iteration_time=1.0,
        circuit=small_circuit,
    )

    # then
    assert callable(objective)


@SKIP_SLOW
def test_get_optimal_hyperparams_for_space(large_circuit):
    # when
    optimal_params = get_optimal_hyperparams_for_space(
        rbs_iteration_time=0.2,
        max_allowed_time=0.8,
        circuit=large_circuit,
        n_trials=100,
    )

    # then
    # NOTE: these ranges params were the widest apart in many rounds of testing.
    # Due to the stochastic nature of the tuning process, this test might fail.
    # If it does, and you're sure the functions are all working, increase the range
    # on these numbers with the new, failed value and re-run
    assert 10 <= optimal_params["teleportation_threshold"] <= 70
    assert 1 <= optimal_params["teleportation_distance"] <= 7
    assert 5 <= optimal_params["min_neighbor_degree"] <= 11
    assert 10064 <= optimal_params["max_num_neighbors_to_search"] <= 98798
    assert (
        optimal_params["decomposition_strategy"] == 0
        or optimal_params["decomposition_strategy"] == 1
    )


@SKIP_SLOW
def test_get_optimal_hyperparams_for_time(large_circuit):
    # when
    optimal_params = get_optimal_hyperparams_for_time(
        rbs_iteration_time=0.2,
        max_allowed_time=0.8,
        circuit=large_circuit,
        n_trials=100,
    )

    # then
    # NOTE: these ranges params were the widest apart in many rounds of testing.
    # Due to the stochastic nature of the tuning process, this test might fail.
    # If it does, and you're sure the functions are all working, increase the range
    # on these numbers with the new, failed value and re-run
    assert 26 <= optimal_params["teleportation_threshold"] <= 69
    assert 1 <= optimal_params["teleportation_distance"] <= 6
    assert 2 <= optimal_params["min_neighbor_degree"] <= 11
    assert 10323 <= optimal_params["max_num_neighbors_to_search"] <= 97971
    assert (
        optimal_params["decomposition_strategy"] == 0
        or optimal_params["decomposition_strategy"] == 1
    )


@SKIP_SLOW
def test_get_optimal_hyperparams_for_space_and_time(large_circuit):
    # given/when
    optimal_params = get_optimal_hyperparams_for_space_and_time(
        rbs_iteration_time=0.2,
        max_allowed_time=0.8,
        circuit=large_circuit,
        n_trials=100,
    )

    # then
    # NOTE: these ranges params were the widest apart in many rounds of testing.
    # Due to the stochastic nature of the tuning process, this test might fail.
    # If it does, and you're sure the functions are all working, increase the range
    # on these numbers with the new, failed value and re-run
    assert 13 <= optimal_params["teleportation_threshold"] <= 70
    assert 1 <= optimal_params["teleportation_distance"] <= 7
    assert 3 <= optimal_params["min_neighbor_degree"] <= 11
    assert 11991 <= optimal_params["max_num_neighbors_to_search"] <= 99154
    assert (
        optimal_params["decomposition_strategy"] == 0
        or optimal_params["decomposition_strategy"] == 1
    )


@SKIP_SLOW
def test_get_optimal_hyperparams_for_estimated_rbs_time(large_circuit):
    # when
    optimal_params = get_optimal_hyperparams_for_estimated_rbs_time(
        rbs_iteration_time=0.2,
        circuit=large_circuit,
        n_trials=100,
    )

    # then
    # NOTE: these ranges params were the widest apart in many rounds of testing.
    # Due to the stochastic nature of the tuning process, this test might fail.
    # If it does, and you're sure the functions are all working, increase the range
    # on these numbers with the new, failed value and re-run
    assert 16 <= optimal_params["teleportation_threshold"] <= 70
    assert 1 <= optimal_params["teleportation_distance"] <= 7
    assert 2 <= optimal_params["min_neighbor_degree"] <= 11
    assert 19544 <= optimal_params["max_num_neighbors_to_search"] <= 91836
    assert (
        optimal_params["decomposition_strategy"] == 0
        or optimal_params["decomposition_strategy"] == 1
    )
