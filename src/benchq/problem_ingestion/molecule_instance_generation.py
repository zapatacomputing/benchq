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
from openfermionpyscf import run_pyscf
from pyscf import gto, scf
from typing import List, Tuple, Optional

from dataclasses import dataclass


@dataclass
class ChemistryApplicationInstance:
    """Class for representing chemistry application instances."""

    geometry: List[Tuple[str, Tuple[float, float, float]]]
    basis: str
    multiplicity: int
    charge: int
    avas_atomic_orbital_list: Optional[List[str]] = None
    avas_minao: Optional[str] = None
    n_active_electrons: Optional[int] = None
    n_active_orbitals: Optional[int] = None

    def get_molecular_data(self) -> MolecularData:
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
            n_active_electrons=self.n_active_electrons,
            n_active_orbitals=self.n_active_orbitals,
        )

    def get_avas_meanfield_object(self) -> scf.hf.SCF:
        """Generates a meanfield object from the instance data."""
        return generate_mean_field_object_from_molecule(
            self.generate_molecular_data(),
            self.avas_atomic_orbital_list,
            self.avas_minao,
        )


def generate_mean_field_object_from_molecule(molecule, ao_list, minao="ccpvtz"):
    ### TODO: Consider passing the HF method as an argument in the function
    # mean_field_object = scf.UHF(molecule)
    # mean_field_object = scf.ROHF(molecule)
    mean_field_object = scf.ROHF(molecule)
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
        avas_atomic_orbital_list=[
            "H 1s",
            "H 2s",
        ]
        * number_of_hydrogens,
        avas_minao="sto-3g",
    )


def generate_h2o_mean_field_object():

    molecule = gto.M(
        atom="""O    0.000000      -0.075791844    0.000000
                H    0.866811829    0.601435779    0.000000
                H   -0.866811829    0.601435779    0.000000
            """,
        basis="augccpvtz",
        symmetry=False,
        charge=1,
        spin=1,
    )

    ao_list = ["H 1s", "O 2s", "O 2p", "O 3s", "O 3p"]

    return generate_mean_field_object_from_molecule(molecule, ao_list)


def generate_cyclic_ozone_hamiltonian():
    # Compute geometry of cyclic ozone
    bond_len = 1.465  # Angstroms
    bond_angle = np.deg2rad(59.9)

    x = bond_len * np.sin(bond_angle / 2)
    y = bond_len * np.cos(bond_angle / 2)

    geometry = [("O", (x, -y / 2, 0)), ("O", (-x, -y / 2, 0)), ("O", (0, y / 2, 0))]

    basis = "cc-pvtz"
    multiplicity = 3  # Cyclic ozone triplet ground state
    charge = 0  # Cyclic ozone is a neutral molecule

    # Generate and populate instance of MolecularData for cyclic ozone
    o3_molecule = openfermion.MolecularData(
        geometry,
        basis,
        multiplicity,
        charge,
        description="Cyclic Ozone",
        symmetry=False,
    )
    o3_molecule = run_pyscf(
        o3_molecule, run_fci=False, run_ccsd=False, run_cisd=False, run_mp2=False
    )

    # Get molecular Hamiltonian in an active space of
    # 24 spin orbitals = 12 spatial orbitals
    active_space_start = 3
    active_space_stop = 15

    o3_molecular_hamiltonian = o3_molecule.get_molecular_hamiltonian(
        occupied_indices=range(active_space_start),
        active_indices=range(active_space_start, active_space_stop),
    )
    return o3_molecular_hamiltonian


def generate_cyclic_ozone_mean_field_object():
    # Compute geometry of cyclic ozone
    bond_len = 1.465  # Angstroms
    bond_angle = np.deg2rad(59.9)

    x = bond_len * np.sin(bond_angle / 2)
    y = bond_len * np.cos(bond_angle / 2)

    geometry = [("O", (x, -y / 2, 0)), ("O", (-x, -y / 2, 0)), ("O", (0, y / 2, 0))]

    basis = "sto-3g"
    # basis = "6-31g"
    # basis = "cc-pvtz"
    # basis = "cc-pvdz"
    multiplicity = 3  # Cyclic ozone triplet ground state
    # charge = 0  # Cyclic ozone is a neutral molecule

    o3_molecule = gto.M(
        atom=geometry,
        basis=basis,
        symmetry=False,
        charge=0,
        spin=multiplicity - 1,
    )

    # ao_list = ["O 2s", "O 2p", "O 3s", "O 3p"]
    ao_list = [
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
    ]
    # ao_list = [
    #     "O 2s",
    #     "O 2p",
    #     "O 2s",
    #     "O 2p",
    #     "O 2s",
    #     "O 2p",
    # ]
    # ao_list = [
    #     "O 2s",
    #     "O 2p",
    # ]
    # ao_list = [
    #     "O 1s",
    #     "O 2s",
    #     "O 2p",
    #     "O 1s",
    #     "O 2s",
    #     "O 2p",
    #     "O 1s",
    #     "O 2s",
    #     "O 2p",
    # ]
    # ao_list = []

    # # Generate and populate instance of MolecularData for cyclic ozone
    # o3_molecule = openfermion.MolecularData(
    #     geometry, basis, multiplicity, charge, description="Cyclic Ozone"
    # )
    # o3_molecule = run_pyscf(
    #     o3_molecule, run_fci=False, run_ccsd=False, run_cisd=False, run_mp2=False
    # )
    return generate_mean_field_object_from_molecule(o3_molecule, ao_list)


def generate_c60_geometry():

    # A short script for constructing molecular geometries for OpenFermion
    # from .xyz files using PySCF
    mol = gto.M(atom="C60-Ih.xyz")
    c60_coords = mol.atom_coords(unit="ANG")

    geometry = []
    for [x, y, z] in c60_coords:
        geometry.append(("C", (x, y, z)))
    print(geometry)
    return geometry
