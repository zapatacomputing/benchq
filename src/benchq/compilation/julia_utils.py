################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import time

import networkx as nx
from orquestra.quantum.circuits import Circuit

from .initialize_julia import jl


def get_nx_graph_from_rbs_adj_list(adj: list) -> nx.Graph:
    graph = nx.empty_graph(len(adj))
    for vertex_id, neighbors in enumerate(adj):
        for neighbor in neighbors:
            graph.add_edge(vertex_id, neighbor)

    return graph


def get_algorithmic_graph_from_ruby_slippers(circuit: Circuit) -> nx.Graph:
    return get_ruby_slippers_compiler(True)(circuit)


def get_ruby_slippers_compiler(
    verbose: bool = True,
    takes_graph_input: bool = True,
    gives_graph_output: bool = True,
    layering_optimization: str = "Time",
    max_num_qubits: int = 1,
    teleportation_threshold: int = 40,
    teleportation_distance: int = 4,
    min_neighbor_degree: int = 6,
    max_num_neighbors_to_search: int = int(1e5),
    decomposition_strategy: int = 0,
    max_graph_size: int = 1e7,
):
    def _run_compiler(circuit: Circuit) -> nx.Graph:
        (
            asg,
            num_consumption_tocks,
            num_logical_qubits,
            _,
        ) = jl.run_ruby_slippers(
            circuit,
            verbose=verbose,
            takes_graph_input=takes_graph_input,
            gives_graph_output=gives_graph_output,
            layering_optimization=layering_optimization,
            max_num_qubits=max_num_qubits,
            teleportation_threshold=teleportation_threshold,
            teleportation_distance=teleportation_distance,
            min_neighbor_degree=min_neighbor_degree,
            max_num_neighbors_to_search=max_num_neighbors_to_search,
            decomposition_strategy=decomposition_strategy,
            max_graph_size=max_graph_size,
        )

        print("getting networkx graph from vertices")
        start = time.time()
        graph = get_nx_graph_from_rbs_adj_list(asg["edge_data"])
        end = time.time()
        print("time: ", end - start)

        return graph

    return _run_compiler


def get_algorithmic_graph_from_Jabalizer(circuit: Circuit) -> nx.Graph:
    svec, op_seq, icm_output, data_qubits_map = jl.run_jabalizer(circuit)
    return create_graph_from_stabilizers(svec)


def create_graph_from_stabilizers(svec):
    G = nx.Graph()
    siz = len(svec)
    for i in range(siz):
        z = svec[i].Z
        for j in range(i + 1, siz):
            if z[j]:
                G.add_edge(i, j)
    return G


def get_algorithmic_graph_and_icm_output(circuit):
    svec, op_seq, icm_output, data_qubits_map = jl.run_jabalizer(circuit)
    return create_graph_from_stabilizers(svec), op_seq, icm_output, data_qubits_map
