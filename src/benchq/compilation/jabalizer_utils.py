################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################

from juliacall import Main as jl

import os
import pathlib

import networkx as nx

def get_algorithmic_graph(circuit):
    jl.include(os.path.join(pathlib.Path(__file__).parent.resolve(), "jabalizer_wrapper.jl"))
    jl.run_jabalizer(circuit)
    return nx.read_adjlist("adjacency_list.nxl")
