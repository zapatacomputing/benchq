import pytest

import random
import string

from orquestra.quantum.circuits import CNOT, CZ, Circuit, H

from benchq.compilation.rbs_hyperparam_tuning import (
    space_time_cost_from_rbs,
    estimated_time_cost_from_rbs,
    create_space_time_objective_fn,
    create_estimated_rbs_time_objective_fn,
    get_optimal_hyperparams_for_space,
    get_optimal_hyperparams_for_time,
    get_optimal_hyperparams_for_space_and_time,
    get_optimal_hyperparams_for_estimated_rbs_time,
)

from benchq.compilation import transpile_to_native_gates


@pytest.fixture()
def large_circuit():
    size = 500
    circ = Circuit(
        [
            H(0),
            *[CNOT(j, i) for i in range(1, size) for j in range(0, size)],
        ]
    )
    return transpile_to_native_gates(circ)


@pytest.fixture()
def small_circuit():
    circ = Circuit([H(0), CNOT(0, 1)])
    return transpile_to_native_gates(circ)


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


def test_incorrect_spacetime_option_raises_error(small_circuit):
    # given
    random_string = "".join(random.choices(string.ascii_letters, k=5))

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


def test_create_estimated_rbs_time_objectiv_fn_sanity_check(small_circuit):
    # when
    objective = create_estimated_rbs_time_objective_fn(
        rbs_iteration_time=1.0,
        circuit=small_circuit,
    )

    # then
    assert callable(objective)


@pytest.mark.skip(reason="takes multiple minutes to run")
def test_get_optimal_hyperparams_for_space(large_circuit):
    # when
    optimal_params = get_optimal_hyperparams_for_space(
        rbs_iteration_time=0.2,
        max_allowed_time=0.8,
        circuit=large_circuit,
        n_trials=100,
    )

    # then
    # NOTE: these ranges params were the widest apart in many rounds of testing
    # due to the stochastic nature of the tuning process, this test might fail.
    # If it does, and you're sure the functions are all working, increase the range
    # on these numbers with the new, failed value and re-run
    assert optimal_params["teleportation_threshold"] == 10
    assert 4 <= optimal_params["teleportation_distance"] <= 7
    assert 3 <= optimal_params["min_neighbors"] <= 9
    assert 17642 <= optimal_params["max_num_neighbors_to_search"] <= 57220
    assert (
        optimal_params["decomposition_strategy"] == 0
        or optimal_params["decomposition_strategy"] == 1
    )


@pytest.mark.skip(reason="takes multiple minutes to run")
def test_get_optimal_hyperparams_for_time(large_circuit):
    # when
    optimal_params = get_optimal_hyperparams_for_time(
        rbs_iteration_time=0.2,
        max_allowed_time=0.8,
        circuit=large_circuit,
        n_trials=100,
    )

    # then
    # NOTE: these ranges params were the widest apart in many rounds of testing
    # due to the stochastic nature of the tuning process, this test might fail.
    # If it does, and you're sure the functions are all working, increase the range
    # on these numbers with the new, failed value and re-run
    assert 55 <= optimal_params["teleportation_threshold"] <= 62
    assert 1 <= optimal_params["teleportation_distance"] <= 5
    assert 4 <= optimal_params["min_neighbors"] <= 9
    assert 14771 <= optimal_params["max_num_neighbors_to_search"] <= 77630
    assert (
        optimal_params["decomposition_strategy"] == 0
        or optimal_params["decomposition_strategy"] == 1
    )


def test_get_optimal_hyperparams_for_space_and_time(large_circuit):
    # TODO: complete this when get_optimal_hyperparams_for_space_and_time is finished
    assert True


@pytest.mark.skip(reason="takes multiple minutes to run")
def test_get_optimal_hyperparams_for_estimated_rbs_time(large_circuit):
    # when
    optimal_params = get_optimal_hyperparams_for_estimated_rbs_time(
        rbs_iteration_time=0.2,
        circuit=large_circuit,
        n_trials=100,
    )

    # then
    # NOTE: these ranges params were the widest apart in many rounds of testing
    # due to the stochastic nature of the tuning process, this test might fail.
    # If it does, and you're sure the functions are all working, increase the range
    # on these numbers with the new, failed value and re-run
    assert 25 <= optimal_params["teleportation_threshold"] <= 62
    assert 3 <= optimal_params["teleportation_distance"] <= 7
    assert 1 <= optimal_params["min_neighbors"] <= 9
    assert 49276 <= optimal_params["max_num_neighbors_to_search"] <= 95100
    assert optimal_params["decomposition_strategy"] == 0
