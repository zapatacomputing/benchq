################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import os
import pathlib

import networkx as nx
import numpy as np
import pytest
import stim
from numba import njit
from orquestra.integrations.qiskit.conversions import import_from_qiskit
from orquestra.quantum.circuits import CNOT, CZ, Circuit, H, S, T, X
from qiskit import QuantumCircuit

from benchq.compilation.circuits import (
    compile_to_native_gates,
    pyliqtr_transpile_to_clifford_t,
)
from benchq.compilation.graph_states import jl


def to_julia_set(python_set):
    """Convert a Python set of integers to a Julia Set{UInt32}."""
    return jl.Set[jl.UInt32]([jl.UInt32(e) for e in python_set])


def to_julia_vector_of_sets(python_list_of_sets):
    """Convert a Python list of sets of integers to a Julia Vector{Set{UInt32}}."""
    return jl.Vector[jl.Set[jl.UInt32]]([to_julia_set(s) for s in python_list_of_sets])


def test_generate_extension_graph():
    # Define the edge_data and nodes in Python
    edge_data = [{3}, {3}, {1, 2, 4}, {3, 5}, {4}]
    nodes = {1, 2, 5}

    # Define the expected outputs
    expected_max_adj_list_size = 1
    expected_min_adj_list_size = 0

    # Convert Python sets and lists to Julia-compatible formats using utility functions
    edge_data_julia_vector = to_julia_vector_of_sets(edge_data)
    nodes_julia = to_julia_set(nodes)

    # Call the Julia function
    output, node_to_vertex_map = jl.generate_extension_graph(
        edge_data_julia_vector, nodes_julia
    )
    output_adj_list = output.fadjlist

    # then
    assert (
        max([len(neighbors) for neighbors in output_adj_list])
        == expected_max_adj_list_size
    )
    assert (
        min([len(neighbors) for neighbors in output_adj_list])
        == expected_min_adj_list_size
    )


def test_compute_all_to_all_tocks():
    # Define the edge_data and nodes in Python
    edge_data = [{3}, {3}, {1, 2, 4}, {3, 5}, {4}]
    nodes = {1, 2, 5}

    # Define the expected outputs
    expected_all_to_all_tocks = 2

    # Convert Python sets and lists to Julia-compatible formats using utility functions
    edge_data_julia_vector = to_julia_vector_of_sets(edge_data)
    nodes_julia = to_julia_set(nodes)

    # Call the Julia function
    output = jl.compute_all_to_all_tocks_to_prepare_subgraph(
        edge_data_julia_vector, nodes_julia
    )

    # then
    assert output == expected_all_to_all_tocks
