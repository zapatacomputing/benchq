################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
import openfermion as of
from orquestra.integrations.cirq.conversions import from_openfermion
from orquestra.quantum.operators import PauliSum


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
