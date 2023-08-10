from . import jl
from .julia_utils import get_nx_graph_from_rbs_adj_list
from ..resource_estimation.graph import GraphResourceEstimator
from ..data_structures import (
    GraphPartition,
    BASIC_SC_ARCHITECTURE_MODEL,
    QuantumProgram,
)
from icecream import ic


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

    ic(iteration_prop)

    estimated_time = rbs_iteration_time / iteration_prop
    ic(estimated_time)
    time_overrun = estimated_time - max_allowed_time
    # max value for float is approx 10^308, avoid going past that
    if time_overrun > 300:
        time_overrun = 300
    ic(time_overrun)

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
        ic(graph_data.max_graph_degree)
        return (10**time_overrun) + graph_data.max_graph_degree - 1
    elif space_or_time == "time":
        ic(graph_data.n_measurement_steps)
        return (10**time_overrun) + graph_data.n_measurement_steps - 1
    else:
        raise ValueError(
            f"space_or_time must be 'space' or 'time'. Instead got {space_or_time}"
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
