################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
import numpy as np
import openfermion
from openfermion import MolecularData
from openfermion.resource_estimates.molecule import (
    avas_active_space,
    localize,
    stability,
)
from openfermionpyscf import run_pyscf, PyscfMolecularData
from pyscf import scf
from typing import List, Tuple, Optional

from dataclasses import dataclass


@dataclass
class ChemistryApplicationInstance:
    """Class for representing chemistry application instances."""

    geometry: List[Tuple[str, Tuple[float, float, float]]]
    basis: str
    multiplicity: int
    charge: int
    avas_atomic_orbitals: Optional[List[str]] = None
    avas_minao: Optional[str] = None
    occupied_indices: Optional[List[int]] = None
    active_indices: Optional[List[int]] = None

    def get_molecular_data(self) -> PyscfMolecularData:
        """Generates a molecular data object from the instance data."""
        return run_pyscf(
            MolecularData(
                self.geometry,
                self.basis,
                self.multiplicity,
                self.charge,
            )
        )

    def get_molecular_hamiltonian(self) -> openfermion.InteractionOperator:
        """Generates an interaction operator from the instance data."""
        return self.get_molecular_data().get_molecular_hamiltonian(
            occupied_indices=self.occupied_indices,
            active_indices=self.active_indices,
        )

    def get_avas_meanfield_object(self) -> scf.hf.SCF:
        """Generates a meanfield object from the instance data."""
        return truncate_with_avas(
            self.get_molecular_data()._pyscf_data["scf"],
            self.avas_atomic_orbitals,
            self.avas_minao,
        )


def truncate_with_avas(mean_field_object: scf.hf.SCF, ao_list: List[str], minao: str="ccpvtz"):
    ### TODO: Consider passing the HF method as an argument in the function
    mean_field_object.verbose = 4
    mean_field_object.kernel()  # run the SCF

    # make sure wave function is stable before we proceed
    mean_field_object = stability(mean_field_object)

    # localize before automatically selecting active space with AVAS
    mean_field_object = localize(
        mean_field_object, loc_type="pm"
    )  # default is loc_type ='pm' (Pipek-Mezey)

    # Truncates to a specific active space that captures the essential chemistry
    molecule, mean_field_object = avas_active_space(
        mean_field_object, ao_list=ao_list, minao=minao
    )

    return mean_field_object


def generate_hydrogen_chain_instance(
    number_of_hydrogens: int,
    basis: str = "6-31g",
    bond_distance: float = 1.3,
) -> ChemistryApplicationInstance:
    return ChemistryApplicationInstance(
        geometry=[("H", (0, 0, i * bond_distance)) for i in range(number_of_hydrogens)],
        basis=basis,
        charge=0,
        multiplicity=number_of_hydrogens + 1,
        avas_atomic_orbitals=[
            "H 1s",
            "H 2s",
        ]
        * number_of_hydrogens,
        avas_minao="sto-3g",
    )


WATER_MOLECULE = ChemistryApplicationInstance(
    geometry=[
        ("O", (0.000000, -0.075791844, 0.000000)),
        ("H", (0.866811829, 0.601435779, 0.000000)),
        ("H", (-0.866811829, 0.601435779, 0.000000)),
    ],
    basis="augccpvtz",
    charge=0,
    multiplicity=1,
    avas_atomic_orbitals=["H 1s", "O 2s", "O 2p", "O 3s", "O 3p"],
)

def get_cyclic_ozone_geometry() -> List[Tuple[str, Tuple[float, float, float]]]:
    bond_len = 1.465  # Angstroms
    bond_angle = np.deg2rad(59.9)

    x = bond_len * np.sin(bond_angle / 2)
    y = bond_len * np.cos(bond_angle / 2)

    return [("O", (x, -y / 2, 0)), ("O", (-x, -y / 2, 0)), ("O", (0, y / 2, 0))]

CYCLIC_OZONE_MOLECULE = ChemistryApplicationInstance(
        geometry=get_cyclic_ozone_geometry(),
        basis="cc-pvtz",
        multiplicity=3,
        charge=0,
        avas_atomic_orbitals=[
            "O 1s",
            "O 2s",
            "O 2p",
            "O 3s",
            "O 3p",
            "O 1s",
            "O 2s",
            "O 2p",
            "O 3s",
            "O 3p",
            "O 1s",
            "O 2s",
            "O 2p",
            "O 3s",
            "O 3p",
        ],
        occupied_indices=range(3),
        active_indices=range(3, 15),
    )
