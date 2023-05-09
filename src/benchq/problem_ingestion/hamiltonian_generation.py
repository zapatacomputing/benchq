################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
import numpy as np
import openfermion as of
import pyLIQTR.sim_methods.quantum_ops as qops
from orquestra.integrations.cirq.conversions import from_openfermion
from orquestra.quantum.operators import PauliSum

# At this stage of development we are aware that there are some issues with methods
# 2 and 3 and they do not necessarily yield correct results.
from pyLIQTR.QSP.Hamiltonian import Hamiltonian as pyH

from benchq.conversions import pyliqtr_to_openfermion

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


def generate_jw_qubit_hamiltonian_from_mol_data(chemistry_instance) -> PauliSum:
    hamiltonian = chemistry_instance.get_active_space_hamiltonian()

    # # Convert to a FermionOperator
    # hamiltonian_ferm_op = of.get_fermion_operator(hamiltonian)

    # Map to QubitOperator using the JWT
    hamiltonian_jw = of.jordan_wigner(hamiltonian)
    # hamiltonian_jw = of.jordan_wigner(hamiltonian_ferm_op)

    return from_openfermion(hamiltonian_jw)


def generate_1d_heisenberg_hamiltonian(N):

    # Setting J/h's
    # Adjusting these from zero to nonzero may also increase the circuit depth,
    # since additional terms in the Hamiltonian are introduced.
    J_z = 1.0
    J_x = 1.1 * J_z
    J_y = J_x
    h_x = -1.0 * J_z
    h_y = 0.0 * J_z
    h_z = 0.0 * J_z

    tuples, types, coeffs = qops.params_heisenberg_1d(
        N,
        J_x=J_x,
        J_y=J_y,
        J_z=J_z,
        h_x=h_x,
        h_y=h_y,
        h_z=h_z,
        periodic=False,
    )

    sclf = np.sum(np.abs(coeffs))

    ham_strings = qops.ps_text_full_set(tuples, types, N, Coeffs=coeffs / sclf)
    qsp_H = pyH(ham_strings)
    pauli_sum = from_openfermion(pyliqtr_to_openfermion(qsp_H))
    for term in pauli_sum.terms:
        term.coefficient = term.coefficient.real
    return pauli_sum
