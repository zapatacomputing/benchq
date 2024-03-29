import time

import networkx as nx
from graph_state_generation.optimizers import (
    fast_maximal_independent_set_stabilizer_reduction,
    greedy_stabilizer_measurement_scheduler,
)
from graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler
from benchq.visualization_tools.plot_substrate_scheduling import (
    remove_isolated_nodes_from_graph,
)


def python_substrate_scheduler(
    asg, preset: str, verbose: bool = False
) -> TwoRowSubstrateScheduler:
    """A simple interface for running the substrate scheduler. Can be run quickly or
    optimized for smaller runtime. Using the "optimized" preset can halve the number
    of measurement steps, but takes about 100x longer to run. It's probably only
    suitable for graphs with less than 10^5 nodes.

    Args:
        graph (nx.Graph): Graph to create substrate schedule for.
        preset (str): Can optimize for speed ("fast") or for smaller number of
            measurement steps ("optimized").

    Returns:
        TwoRowSubstrateScheduler: A substrate scheduler object with the schedule
            already created.
    """
    graph = get_nx_graph_from_adj_list(asg["edge_data"])
    cleaned_graph = remove_isolated_nodes_from_graph(graph)[1]

    if verbose:
        print("starting substrate scheduler")
    start = time.time()
    if preset == "fast":
        compiler = TwoRowSubstrateScheduler(
            cleaned_graph,
            stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
        )
    if preset == "optimized":
        compiler = TwoRowSubstrateScheduler(
            cleaned_graph,
            pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
            stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
        )
    compiler.run()
    end = time.time()
    if verbose:
        print("substrate scheduler took", end - start, "seconds")
    return compiler


def get_n_measurement_steps(optimization, graph, verbose: bool = False) -> int:
    compiler = python_substrate_scheduler(graph, optimization, verbose)
    n_measurement_steps = len(compiler.measurement_steps)
    return n_measurement_steps


def get_nx_graph_from_adj_list(adj: list) -> nx.Graph:
    graph = nx.empty_graph(len(adj))
    for vertex_id, neighbors in enumerate(adj):
        for neighbor in neighbors:
            graph.add_edge(vertex_id, neighbor)

    return graph
