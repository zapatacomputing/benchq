################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
import random
from itertools import combinations
from typing import Tuple

import networkx as nx
import openfermion as of
from openfermionpyscf import generate_molecular_hamiltonian
from orquestra.integrations.cirq.conversions._openfermion_conversions import (
    from_openfermion,
)
from orquestra.quantum.operators import PauliSum, PauliTerm

# TODO: export openfermion to cirq
### General generators


def generate_fermi_hubbard_jw_qubit_hamiltonian(
    x_dimension: int,
    y_dimension: int,
    tunneling: float,
    coulomb: float,
    chemical_potential: float = 0.0,
    spinless: bool = False,
) -> PauliSum:

    hubbard_model = of.fermi_hubbard(
        x_dimension,
        y_dimension,
        tunneling,
        coulomb,
        chemical_potential,
        spinless,
    )

    # Map to QubitOperator using the JWT
    hamiltonian_jw = of.jordan_wigner(hubbard_model)

    return from_openfermion(hamiltonian_jw)


def generate_jw_qubit_hamiltonian_from_mol_data(
    molecular_data, occupied_indices=None, active_indices=None
) -> PauliSum:

    hamiltonian = molecular_data.get_molecular_hamiltonian(
        occupied_indices=occupied_indices, active_indices=active_indices
    )

    # # Convert to a FermionOperator
    # hamiltonian_ferm_op = of.get_fermion_operator(hamiltonian)

    # Map to QubitOperator using the JWT
    hamiltonian_jw = of.jordan_wigner(hamiltonian)
    # hamiltonian_jw = of.jordan_wigner(hamiltonian_ferm_op)

    return from_openfermion(hamiltonian_jw)
