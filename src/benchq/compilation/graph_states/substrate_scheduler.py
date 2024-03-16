import time
import networkx as nx
from graph_state_generation.optimizers import (
    fast_maximal_independent_set_stabilizer_reduction,
    greedy_stabilizer_measurement_scheduler,
)
from graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler

from copy import copy
from typing import Tuple


def python_substrate_scheduler(
    graph: nx.Graph, preset: str, verbose: bool = False
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


def remove_isolated_nodes_from_graph(graph: nx.Graph) -> Tuple[int, nx.Graph]:
    cleaned_graph = copy(graph)
    isolated_nodes = list(nx.isolates(cleaned_graph))
    n_nodes_removed = len(isolated_nodes)

    cleaned_graph.remove_nodes_from(isolated_nodes)
    cleaned_graph = nx.convert_node_labels_to_integers(cleaned_graph)

    return n_nodes_removed, cleaned_graph
