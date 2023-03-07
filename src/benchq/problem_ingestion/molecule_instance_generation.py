################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

import numpy as np
import openfermion
from openfermion import MolecularData
from openfermion.resource_estimates.molecule import (
    avas_active_space,
    localize,
    stability,
)
from openfermionpyscf import PyscfMolecularData, run_pyscf
from pyscf import scf


@dataclass
class ChemistryApplicationInstance:
    """Class for representing chemistry application instances.

    A chemistry application instance is a specification of how to generate a fermionic
    Hamiltonian, including information such as the molecular geometry and choice of
    active space. Note that the active space can be specified either through the use of
    Atomic Valence Active Space (AVAS) or by specifying the indices of the occupied and
    active orbitals.

    Attributes:
        geometry: A list of tuples of the form (atom, (x, y, z)) where atom is the
            atom type and (x, y, z) are the coordinates of the atom.
        basis: The basis set to use for the calculation.
        multiplicity: The spin multiplicity of the molecule.
        charge: The charge of the molecule.
        avas_atomic_orbitals: A list of atomic orbitals to use for  (AVAS).
        avas_minao: The minimum active orbital to use for AVAS.
        occupied_indices: A list of molecular orbitals not in the active space that
            should be assumed to be fully occupied.
        active_indices: A list of molecular orbitals to include in the active space.
    """

    geometry: List[Tuple[str, Tuple[float, float, float]]]
    basis: str
    multiplicity: int
    charge: int
    avas_atomic_orbitals: Optional[Iterable[str]] = None
    avas_minao: Optional[str] = None
    occupied_indices: Optional[Iterable[int]] = None
    active_indices: Optional[Iterable[int]] = None

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

    def get_active_space_hamiltonian(self) -> openfermion.InteractionOperator:
        """Generates an interaction operator from the instance data."""
        if self.avas_atomic_orbitals or self.avas_minao:
            raise ValueError(
                "Generating the active space Hamiltonian for application instances"
                "with AVAS is not currently supported."
            )
        return self.get_molecular_data().get_molecular_hamiltonian(
            occupied_indices=self.occupied_indices,
            active_indices=self.active_indices,
        )

    def get_active_space_meanfield_object(self) -> scf.hf.SCF:
        """Generates a meanfield object from the instance data."""
        if self.active_indices or self.occupied_indices:
            raise ValueError(
                "Generating the meanfield object for application instances with"
                "active and occupied indices is not currently supported."
            )
        return truncate_with_avas(
            self.get_molecular_data()._pyscf_data["scf"],
            self.avas_atomic_orbitals,
            self.avas_minao,
        )


def truncate_with_avas(
    mean_field_object: scf.hf.SCF,
    ao_list: Optional[Iterable[str]] = None,
    minao: Optional[str] = None,
):
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
    )


WATER_MOLECULE = ChemistryApplicationInstance(
    geometry=[
        ("O", (0.000000, -0.075791844, 0.000000)),
        ("H", (0.866811829, 0.601435779, 0.000000)),
        ("H", (-0.866811829, 0.601435779, 0.000000)),
    ],
    basis="6-31g",
    charge=0,
    multiplicity=1,
    avas_atomic_orbitals=["H 1s", "O 2s", "O 2p", "O 3s", "O 3p"],
    avas_minao="STO-3G",
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
    occupied_indices=range(3),
    active_indices=range(3, 15),
)
