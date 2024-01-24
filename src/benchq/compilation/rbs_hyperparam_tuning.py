from math import ceil

import networkx as nx
import optuna
from orquestra.quantum.circuits import Circuit, H

from ..algorithms.data_structures import GraphPartition
from ..problem_embeddings.quantum_program import QuantumProgram
from ..quantum_hardware_modeling import BASIC_SC_ARCHITECTURE_MODEL
from ..resource_estimators.graph_estimators import GraphResourceEstimator
from . import jl, transpile_to_native_gates
from .julia_utils import get_nx_graph_from_rbs_adj_list


def space_time_cost_from_rbs(
    rbs_iteration_time: float,
    max_allowed_time: float,
    space_or_time: str,
    circuit: Circuit,
    verbose=False,
    max_graph_size=None,
    teleportation_threshold=40,
    teleportation_distance=4,
    min_neighbors=6,
    max_num_neighbors_to_search=1e5,
    decomposition_strategy=1,
    circuit_prop_estimate=1.0,
):
    """
    Runs Ruby Slippers (RBS) and uses the resulting graph to get estimates
    of circuit cost complexity in terms of time, space, or both. This is a
    low-level function. Unless you mean to use it, recommended to
    use one of the functions beginning with "get_optimal_hyperparams_for_"

    Args:
        rbs_iteration_time (float): amount of time to let RBS run for
        max_allowed_time (float): maximum time you want RBS to run when you
            eventually find the whole graph
        space_or_time (str): "space" returns the cost for space, "time" for
            time, and "space&time" for both
        circuit (Circuit): the circuit to run RBS on
        verbose (bool): true for verbose, false for quiet
        max_graph_size (int): maximum number of nodes in the graph state
        teleportation_threshold (int): RBS hyperparam, see ruby_slippers.jl
        teleportation_distance (int): RBS hyperparam, see ruby_slippers.jl
        min_neighbors (int): RBS hyperparam, see ruby_slippers.jl
        max_num_neighbors_to_search (int): RBS hyperparam, see ruby_slippers.jl
        decomposition_strategy (int): RBS hyperparam, see ruby_slippers.jl
        circuit_prop_estimate (float): copying a large circuit to julia can take
            a long time due to turning it into a string and back, so estimate how
            much of the circuit RBS will get through before rbs_iteration_time
            runs out, and supply that here to speed up optimization

    Returns:
        space_cost (float) OR time_cost (float) when space_or_time == "space" or "time"
        (space_cost, time_cost) (float, float) when space_or_time == "space&time"
    """
    new_circuit = circuit
    if circuit_prop_estimate != 1.0:
        num_op = ceil(len(circuit.operations) * circuit_prop_estimate)
        new_circuit = Circuit(circuit.operations[:num_op])

    _, adj, proportion_of_circuit_completed = jl.run_ruby_slippers(
        new_circuit,
        verbose,
        max_graph_size,
        teleportation_threshold,
        teleportation_distance,
        min_neighbors,
        max_num_neighbors_to_search,
        decomposition_strategy,
        rbs_iteration_time,
    )

    if proportion_of_circuit_completed == 1.0 and circuit_prop_estimate != 1.0:
        raise RuntimeError(
            "Reached the end of rbs iteration with reduced circuit size. Either "
            "increase circuit_prop_estimate, decrease rbs_iteration_time, or both."
        )

    estimated_time = rbs_iteration_time / proportion_of_circuit_completed
    time_overrun = estimated_time - max_allowed_time
    # max value for float is approx 10^308, avoid going past that
    if time_overrun > 300:
        time_overrun = 300

    # get graph data
    nx_graph = get_nx_graph_from_rbs_adj_list(adj)
    # remove isolated nodes
    isolated_nodes = list(nx.isolates(nx_graph))
    nx_graph.remove_nodes_from(isolated_nodes)
    nx_graph = nx.convert_node_labels_to_integers(nx_graph)

    dummy_circuit = Circuit([H(0)])

    quantum_program = QuantumProgram(
        [dummy_circuit],
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
        return (
            (10**time_overrun) + graph_data.max_graph_degree - 1,
            (10**time_overrun) + graph_data.n_measurement_steps - 1,
        )
    else:
        raise ValueError(
            "space_or_time must be 'space', 'time', or 'space&time'."
            "Instead got " + str(space_or_time)
        )


def estimated_time_cost_from_rbs(
    rbs_iteration_time: float,
    circuit: Circuit,
    verbose=False,
    max_graph_size=None,
    teleportation_threshold=40,
    teleportation_distance=4,
    min_neighbors=6,
    max_num_neighbors_to_search=1e5,
    decomposition_strategy=1,
    circuit_prop_estimate=1.0,
):
    """
    Runs Ruby Slippers (RBS) and uses the resulting graph to get estimate
    of how long RBS would take to compile the whole circuit. This is a
    low-level function. Unless you mean to use it, recommended to
    use one of the functions beginning with "get_optimal_hyperparams_for_"

    Args:
        rbs_iteration_time (float): amount of time to let RBS run for
        circuit (Circuit): the circuit to run RBS on
        verbose (bool): true for verbose, false for quiet
        max_graph_size (int): maximum number of nodes in the graph state
        teleportation_threshold (int): RBS hyperparam, see ruby_slippers.jl
        teleportation_distance (int): RBS hyperparam, see ruby_slippers.jl
        min_neighbors (int): RBS hyperparam, see ruby_slippers.jl
        max_num_neighbors_to_search (int): RBS hyperparam, see ruby_slippers.jl
        decomposition_strategy (int): RBS hyperparam, see ruby_slippers.jl
        circuit_prop_estimate (float): copying a large circuit to julia can take
            a long time due to turning it into a string and back, so estimate how
            much of the circuit RBS will get through before rbs_iteration_time
            runs out, and supply that here to speed up optimization

    Returns:
        total estimated time to perform RBS on the whole circuit (float)
    """
    new_circuit = circuit
    if circuit_prop_estimate != 1.0:
        num_op = ceil(len(circuit.operations) * circuit_prop_estimate)
        new_circuit = Circuit(circuit.operations[:num_op])

    _, _, proportion_of_circuit_completed = jl.run_ruby_slippers(
        new_circuit,
        verbose,
        max_graph_size,
        teleportation_threshold,
        teleportation_distance,
        min_neighbors,
        max_num_neighbors_to_search,
        decomposition_strategy,
        rbs_iteration_time,
    )

    return rbs_iteration_time / (
        proportion_of_circuit_completed * circuit_prop_estimate
    )


def create_space_time_objective_fn(
    rbs_iteration_time: float,
    max_allowed_time: float,
    space_or_time: str,
    circuit: Circuit,
    circuit_prop_estimate: float = 1.0,
):
    """
    Creates objective function for optuna to use in optimizing for either
    space or time. Mid-level function, unless you mean to, recommended to
    use one of the functions beginning with "get_optimal_hyperparams_for_"

    Args:
        rbs_iteration_time (float): amount of time to let RBS run for
        max_allowed_time (float): maximum time you want RBS to run when you
            eventually find the whole graph
        space_or_time (str): "space" returns the cost for space, "time" for
            time, and "space&time" for both
        circuit (Circuit): the circuit to run RBS on
        circuit_prop_estimate (float): copying a large circuit to julia can take
            a long time due to turning it into a string and back, so estimate how
            much of the circuit RBS will get through before rbs_iteration_time
            runs out, and supply that here to speed up optimization

    Returns:
        callable function which accepts an optuna "trial" and returns the cost
    """

    def objective(trial):
        teleportation_threshold = trial.suggest_int("teleportation_threshold", 10, 70)
        teleportation_distance = trial.suggest_int("teleportation_distance", 1, 7)
        min_neighbors = trial.suggest_int("min_neighbors", 1, 11)
        max_num_neighbors_to_search = trial.suggest_int(
            "max_num_neighbors_to_search", 10000, 100000
        )
        decomposition_strategy = trial.suggest_categorical(
            "decomposition_strategy", [0, 1]
        )

        return space_time_cost_from_rbs(
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
            circuit_prop_estimate=circuit_prop_estimate,
        )

    return objective


def create_estimated_rbs_time_objective_fn(
    rbs_iteration_time: float,
    circuit: Circuit,
    circuit_prop_estimate: float = 1.0,
):
    """
    Creates objective function for optuna to use in optimizing for estimated
    total RBS time. Mid-level function, unless you mean to, recommended to
    use one of the functions beginning with "get_optimal_hyperparams_for_"

    Args:
        rbs_iteration_time (float): amount of time to let RBS run for
        circuit (Circuit): the circuit to run RBS on
        circuit_prop_estimate (float): copying a large circuit to julia can take
            a long time due to turning it into a string and back, so estimate how
            much of the circuit RBS will get through before rbs_iteration_time
            runs out, and supply that here to speed up optimization

    Returns:
        callable function which accepts an optuna "trial" and returns the cost
    """

    def objective(trial):
        teleportation_threshold = trial.suggest_int("teleportation_threshold", 10, 70)
        teleportation_distance = trial.suggest_int("teleportation_distance", 1, 7)
        min_neighbors = trial.suggest_int("min_neighbors", 1, 11)
        max_num_neighbors_to_search = trial.suggest_int(
            "max_num_neighbors_to_search", 10000, 100000
        )
        decomposition_strategy = trial.suggest_categorical(
            "decomposition_strategy", [0, 1]
        )

        return estimated_time_cost_from_rbs(
            rbs_iteration_time=rbs_iteration_time,
            circuit=circuit,
            verbose=False,
            max_graph_size=None,
            teleportation_threshold=teleportation_threshold,
            teleportation_distance=teleportation_distance,
            min_neighbors=min_neighbors,
            max_num_neighbors_to_search=max_num_neighbors_to_search,
            decomposition_strategy=decomposition_strategy,
            circuit_prop_estimate=circuit_prop_estimate,
        )

    return objective


def get_optimal_hyperparams_for_space(
    rbs_iteration_time: float,
    max_allowed_time: float,
    circuit: Circuit,
    n_trials: int,
    circuit_prop_estimate: float = 1.0,
):
    """
    Function to get optimal hyperparameters for space complexity after running
    RBS.

    Args:
        rbs_iteration_time (float): amount of time to let RBS run for in each trial
        max_allowed_time (float): maximum time you want RBS to run when you
            eventually find the whole graph
        circuit (Circuit): the circuit to run RBS on
        n_trials (int): total number of trials to run when optimizing
        circuit_prop_estimate (float): copying a large circuit to julia can take
            a long time due to turning it into a string and back, so estimate how
            much of the circuit RBS will get through before rbs_iteration_time
            runs out, and supply that here to speed up optimization

    Returns:
        the best hyperparameters found during optimization
    """
    objective = create_space_time_objective_fn(
        rbs_iteration_time,
        max_allowed_time,
        "space",
        circuit,
        circuit_prop_estimate,
    )
    study = optuna.create_study()
    study.optimize(objective, n_trials=n_trials)

    return study.best_params


def get_optimal_hyperparams_for_time(
    rbs_iteration_time: float,
    max_allowed_time: float,
    circuit: Circuit,
    n_trials: int,
    circuit_prop_estimate: float = 1.0,
):
    """
    Function to get optimal hyperparameters for time complexity after running
    RBS.

    Args:
        rbs_iteration_time (float): amount of time to let RBS run for in each trial
        max_allowed_time (float): maximum time you want RBS to run when you
            eventually find the whole graph
        circuit (Circuit): the circuit to run RBS on
        n_trials (int): total number of trials to run when optimizing
        circuit_prop_estimate (float): copying a large circuit to julia can take
            a long time due to turning it into a string and back, so estimate how
            much of the circuit RBS will get through before rbs_iteration_time
            runs out, and supply that here to speed up optimization

    Returns:
        the best hyperparameters found during optimization
    """
    transpiled_circ = transpile_to_native_gates(circuit)
    objective = create_space_time_objective_fn(
        rbs_iteration_time,
        max_allowed_time,
        "time",
        transpiled_circ,
        circuit_prop_estimate,
    )
    study = optuna.create_study()
    study.optimize(objective, n_trials=n_trials)

    return study.best_params


def get_optimal_hyperparams_for_space_and_time(
    rbs_iteration_time: float,
    max_allowed_time: float,
    circuit: Circuit,
    n_trials: int,
    space_weight: float = 0.5,
    circuit_prop_estimate: float = 1.0,
):
    """
    Function to get optimal hyperparameters for both space and time complexity
    after running RBS.

    Args:
        rbs_iteration_time (float): amount of time to let RBS run for in each trial
        max_allowed_time (float): maximum time you want RBS to run when you
            eventually find the whole graph
        circuit (Circuit): the circuit to run RBS on
        n_trials (int): total number of trials to run when optimizing
        space_weight (float): between 0 and 1. The closer to 1, the more weight on
            the space cost, the closer to 0, the more weight on the time cost
        circuit_prop_estimate (float): copying a large circuit to julia can take
            a long time due to turning it into a string and back, so estimate how
            much of the circuit RBS will get through before rbs_iteration_time
            runs out, and supply that here to speed up optimization

    Returns:
        the best hyperparameters (based on space_weight) found during optimization
    """
    transpiled_circ = transpile_to_native_gates(circuit)
    objective = create_space_time_objective_fn(
        rbs_iteration_time,
        max_allowed_time,
        "space&time",
        transpiled_circ,
        circuit_prop_estimate,
    )
    study = optuna.create_study(directions=["minimize", "minimize"])
    study.optimize(objective, n_trials=n_trials)

    best_params = {}
    best_score = 100000000

    for trial in study.best_trials:
        # That 5 is based on some observations that (generally) as the best space
        # score decreased by 1, the best time score increases by 5. That is, to make
        # it closer to an even trade-off, space should be weighted 5x more by
        # default and the user can of course adjust using the space_weight param
        new_score = trial.values[0] * space_weight * 5 + trial.values[1] * (
            1 - space_weight
        )
        if new_score < best_score:
            best_score = new_score
            best_params = trial.params

    return best_params


def get_optimal_hyperparams_for_estimated_rbs_time(
    rbs_iteration_time: float,
    circuit: Circuit,
    n_trials: int,
    circuit_prop_estimate: float = 1.0,
):
    """
    Function to get optimal hyperparameters for estimated total time to run RBS

    Args:
        rbs_iteration_time (float): amount of time to let RBS run for in each trial
        circuit (Circuit): the circuit to run RBS on
        n_trials (int): total number of trials to run when optimizing
        circuit_prop_estimate (float): copying a large circuit to julia can take
            a long time due to turning it into a string and back, so estimate how
            much of the circuit RBS will get through before rbs_iteration_time
            runs out, and supply that here to speed up optimization

    Returns:
        the best hyperparameters found during optimization
    """
    transpiled_circ = transpile_to_native_gates(circuit)
    objective = create_estimated_rbs_time_objective_fn(
        rbs_iteration_time, transpiled_circ, circuit_prop_estimate
    )
    study = optuna.create_study()
    study.optimize(objective, n_trials=n_trials, catch=(IndexError,))

    return study.best_params
