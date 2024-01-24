################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import random

import networkx as nx
from orquestra.integrations.cirq.conversions import from_openfermion

# At this stage of development we are aware that there are some issues with methods
# 2 and 3 and they do not necessarily yield correct results.
from pyLIQTR.QSP.Hamiltonian import Hamiltonian as pyH

from benchq.conversions import pyliqtr_to_openfermion


def generate_ising_hamiltonian_on_kitaev_lattice(lattice_size, weight_prob=1):
    g = nx.generators.lattice.hexagonal_lattice_graph(lattice_size, lattice_size)
    assign_hexagon_labels(g)
    g = nx.convert_node_labels_to_integers(g)
    H = nx_kitaev_terms(g, weight_prob)

    H_kitaev = pyH(H)
    H_kitaev = from_openfermion(pyliqtr_to_openfermion(H_kitaev))
    return H_kitaev


def generate_ising_hamiltonian_on_triangular_lattice(
    lattice_size, longitudinal_weight_prob=1, transverse_weight_prob=1
):
    g = nx_triangle_lattice(lattice_size)
    g = nx.convert_node_labels_to_integers(g)
    H_transverse = nx_transverse_ising_terms(g, transverse_weight_prob)
    H_longitudinal = nx_longitudinal_ising_terms(g, longitudinal_weight_prob)
    H_triangle = pyH(H_transverse + H_longitudinal)
    H_triangle = from_openfermion(pyliqtr_to_openfermion(H_triangle))
    return H_triangle


def generate_ising_hamiltonian_on_cubic_lattice(
    lattice_size, longitudinal_weight_prob=0.5, transverse_weight_prob=1
):
    g = nx.grid_graph(dim=(lattice_size, lattice_size, lattice_size))
    g = nx.convert_node_labels_to_integers(g)
    H_transverse = nx_transverse_ising_terms(g, transverse_weight_prob)
    H_longitudinal = nx_longitudinal_ising_terms(g, longitudinal_weight_prob)

    H_cubic = pyH(H_transverse + H_longitudinal)
    H_cubic = from_openfermion(pyliqtr_to_openfermion(H_cubic))
    return H_cubic


def assign_hexagon_labels(g):
    for n1, n2 in g.edges:
        # start by making sure that the edges are ordered correctly
        r1, c1 = n1
        r2, c2 = n2
        if r2 - r1 < 0 or c2 - c1 < 0:
            swap_r2 = r1
            swap_c2 = c1
            r1 = r2
            c1 = c2
            r2 = swap_r2
            c2 = swap_c2

        # now that they are ordered correctly, we can assign labels
        label = ""
        if c1 == c2:
            label = "Z"
        elif ((r1 % 2) + (c1 % 2)) % 2 == 0:  # apparently you can differentiate X and Y
            # labels based off nx's node label parity.  Huh.
            label = "Y"
        else:
            label = "X"

        g[n1][n2]["label"] = label


def nx_kitaev_terms(g, p):
    H = []
    n = len(g.nodes)
    for n1, n2, d in g.edges(data=True):
        label = d["label"]
        weight = 1 if random.random() < p else -1
        string = n * "I"
        for i in range(len(g)):
            if i == n1 or i == n2:
                string = string[:i] + label + string[i + 1 :]
            else:
                pass
        H.append((string, weight))
    return H


def nx_triangle_lattice(lattice_size):
    g = nx.generators.lattice.grid_2d_graph(lattice_size, lattice_size)
    for i in range(lattice_size - 1):
        for j in range(lattice_size - 1):
            g.add_edge((i, j), (i + 1, j + 1))
    return g


def nx_longitudinal_ising_terms(g, p, magnitude=1):
    H_longitudinal = []
    n = len(g.nodes)
    for n1, n2 in g.edges:
        weight = magnitude if random.random() < p else -magnitude
        string = n * "I"
        for i in range(len(g)):
            if i == n1 or i == n2:
                string = string[:i] + "Z" + string[i + 1 :]
            else:
                pass
        H_longitudinal.append((string, weight))
    return H_longitudinal


def nx_transverse_ising_terms(g, p, magnitude=0.1):
    H_transverse = []
    n = len(g)
    for i in range(n):
        w = magnitude if random.random() < p else -magnitude
        string = n * "I"
        for k in range(n):
            if i == k:
                string = string[:i] + "X" + string[i + 1 :]
            else:
                pass
        H_transverse.append((string, w))
    return H_transverse
