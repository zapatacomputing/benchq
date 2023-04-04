################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import networkx as nx

from . import jl


def create_graph_from_stabilizers(svec):
    G = nx.Graph()
    siz = len(svec)
    for i in range(siz):
        z = svec[i].Z
        for j in range(i + 1, siz):
            if z[j]:
                G.add_edge(i, j)
    return G


def get_algorithmic_graph(circuit):
    svec, op_seq, icm_output, data_qubits_map = jl.run_jabalizer(circuit)
    return create_adjlist_from_stabilizers(svec)


def get_algorithmic_graph_and_icm_output(circuit):
    svec, op_seq, icm_output, data_qubits_map = jl.run_jabalizer(circuit)
    return create_adjlist_from_stabilizers(svec), op_seq, icm_output, data_qubits_map
