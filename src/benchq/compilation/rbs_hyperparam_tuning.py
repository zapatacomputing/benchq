from . import jl
from .julia_utils import get_nx_graph_from_rbs_adj_list
from ..resource_estimation.graph import GraphResourceEstimator
from ..data_structures import (
    GraphPartition,
    BASIC_SC_ARCHITECTURE_MODEL,
    QuantumProgram,
)
from icecream import ic
import optuna


def space_time_cost_function_from_rbs(
    rbs_iteration_time,
    max_allowed_time,
    space_or_time,
    circuit,
    verbose=False,
    max_graph_size=None,
    teleportation_threshold=40,
    teleportation_distance=4,
    min_neighbors=6,
    max_num_neighbors_to_search=1e5,
    decomposition_strategy=1,
):
    _, adj, iteration_prop = jl.run_ruby_slippers(
        circuit,
        verbose,
        max_graph_size,
        teleportation_threshold,
        teleportation_distance,
        min_neighbors,
        max_num_neighbors_to_search,
        decomposition_strategy,
        rbs_iteration_time,
    )

    estimated_time = rbs_iteration_time / iteration_prop
    time_overrun = estimated_time - max_allowed_time
    # max value for float is approx 10^308, avoid going past that
    if time_overrun > 300:
        time_overrun = 300

    # get graph data
    nx_graph = get_nx_graph_from_rbs_adj_list(adj)
    quantum_program = QuantumProgram(
        [circuit],
        1,
        lambda x: [0] * x,
    )
    graph_partition = GraphPartition(program=quantum_program, subgraphs=[nx_graph])
    empty_graph_re = GraphResourceEstimator(BASIC_SC_ARCHITECTURE_MODEL)
    graph_data = empty_graph_re._get_graph_data_for_single_graph(graph_partition)

    if space_or_time == "space":
        return (10**time_overrun) + graph_data.max_graph_degree - 1
    elif space_or_time == "time":
        return (10**time_overrun) + graph_data.n_measurement_steps - 1
    elif space_or_time == "space&time":
        return ((10**time_overrun) + graph_data.max_graph_degree - 1,
                (10**time_overrun) + graph_data.n_measurement_steps - 1)
    else:
        raise ValueError(
            "space_or_time must be 'space', 'time', or 'space&time'."
            "Instead got " + str(space_or_time)
        )


def estimated_time_cost_function_from_rbs(
    rbs_iteration_time,
    circuit,
    verbose=False,
    max_graph_size=None,
    teleportation_threshold=40,
    teleportation_distance=4,
    min_neighbors=6,
    max_num_neighbors_to_search=1e5,
    decomposition_strategy=1,
):
    _, adj, iteration_prop = jl.run_ruby_slippers(
        circuit,
        verbose,
        max_graph_size,
        teleportation_threshold,
        teleportation_distance,
        min_neighbors,
        max_num_neighbors_to_search,
        decomposition_strategy,
        rbs_iteration_time,
    )

    return rbs_iteration_time / iteration_prop


def create_space_time_objective_function(rbs_iteration_time, max_allowed_time, space_or_time, circuit):
    def objective(trial):
        teleportation_threshold = trial.suggest_int("teleportation_threshold", 10, 70)
        teleportation_distance = trial.suggest_int("teleportation_distance", 1, 7)
        min_neighbors = trial.suggest_int("min_neighbors", 1, 11)
        max_num_neighbors_to_search = trial.suggest_int("max_num_neighbors_to_search", 10000, 100000)
        decomposition_strategy = trial.suggest_categorical("decomposition_strategy", [0, 1])

        return space_time_cost_function_from_rbs(
            rbs_iteration_time=rbs_iteration_time,
            max_allowed_time=max_allowed_time,
            space_or_time=space_or_time,
            circuit=circuit,
            verbose=False,
            max_graph_size=None,
            teleportation_threshold=teleportation_threshold,
            teleportation_distance=teleportation_distance,
            min_neighbors=min_neighbors,
            max_num_neighbors_to_search=max_num_neighbors_to_search,
            decomposition_strategy=decomposition_strategy,
        )
    return objective


def create_estimated_rbs_time_objective(rbs_iteration_time, circuit):
    def objective(trial):
        teleportation_threshold = trial.suggest_int("teleportation_threshold", 10, 70)
        teleportation_distance = trial.suggest_int("teleportation_distance", 1, 7)
        min_neighbors = trial.suggest_int("min_neighbors", 1, 11)
        max_num_neighbors_to_search = trial.suggest_int("max_num_neighbors_to_search", 10000, 100000)
        decomposition_strategy = trial.suggest_categorical("decomposition_strategy", [0, 1])

        return estimated_time_cost_function_from_rbs(
            rbs_iteration_time=rbs_iteration_time,
            circuit=circuit,
            verbose=False,
            max_graph_size=None,
            teleportation_threshold=teleportation_threshold,
            teleportation_distance=teleportation_distance,
            min_neighbors=min_neighbors,
            max_num_neighbors_to_search=max_num_neighbors_to_search,
            decomposition_strategy=decomposition_strategy,
        )
    return objective

def get_optimal_hyperparams_for_space(rbs_iteration_time, max_allowed_time, circuit, n_trials,):
    objective = create_space_time_objective_function(rbs_iteration_time, max_allowed_time, "space", circuit,)
    study = optuna.create_study()
    study.optimize(objective, n_trials=n_trials, catch=(IndexError,))

    return study.best_params

def get_optimal_hyperparams_for_time(rbs_iteration_time, max_allowed_time, circuit, n_trials,):
    objective = create_space_time_objective_function(rbs_iteration_time, max_allowed_time, "time", circuit,)
    study = optuna.create_study()
    study.optimize(objective, n_trials=n_trials, catch=(IndexError,))

    return study.best_params


def get_optimal_hyperparams_for_space_and_time(rbs_iteration_time, max_allowed_time, circuit, n_trials, space_weight,):
    objective = create_space_time_objective_function(rbs_iteration_time, max_allowed_time, "space&time", circuit,)
    study = optuna.create_study(directions=["minimize", "minimize"])
    study.optimize(objective, n_trials=n_trials, catch=(IndexError,))

    best_params = {}
    best_score = 100000000

    for trial in study.best_trials:
        new_score = trial.values[0] * space_weight + trial.values[1] * (1 - space_weight)
        if new_score < best_score:
            best_score = new_score
            best_params = trial.params

    return best_params


def get_optimal_hyperparams_for_estimated_rbs_time(rbs_iteration_time, circuit, n_trials):
    objective = create_estimated_rbs_time_objective(rbs_iteration_time, circuit)
    study = optuna.create_study()
    study.optimize(objective, n_trials=n_trials, catch=(IndexError,))

    return study.best_params

