################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import networkx as nx
from . import jl

def get_algorithmic_graph(circuit):
    jl.run_jabalizer(circuit)
    return nx.read_adjlist("adjacency_list.nxl")
