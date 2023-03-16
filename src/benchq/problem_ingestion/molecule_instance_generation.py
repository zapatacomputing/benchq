################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

import numpy as np
import openfermion
from openfermion.resource_estimates.molecule import (
    avas_active_space,
    localize,
    stability,
)
from openfermion import MolecularData
from openfermionpyscf import PyscfMolecularData
from openfermionpyscf._run_pyscf import compute_integrals
from pyscf import scf, gto


@dataclass
class ChemistryApplicationInstance:
    """Class for representing chemistry application instances.

    A chemistry application instance is a specification of how to generate a fermionic
    Hamiltonian, including information such as the molecular geometry and choice of
    active space. Note that the active space can be specified either through the use of
    Atomic Valence Active Space (AVAS) or by specifying the indices of the occupied and
    active orbitals.

    Args:
        geometry: A list of tuples of the form (atom, (x, y, z)) where atom is the
            atom type and (x, y, z) are the coordinates of the atom in Angstroms.
        basis: The basis set to use for the calculation.
        multiplicity: The spin multiplicity of the molecule.
        charge: The charge of the molecule.
        avas_atomic_orbitals: A list of atomic orbitals to use for (AVAS).
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

    def get_pyscf_molecule(self) -> gto.Mole:
        "Generate the PySCF molecule object describing the system to be calculated."
        pyscf_molecule = gto.Mole()
        pyscf_molecule.atom = self.geometry
        pyscf_molecule.basis = self.basis
        pyscf_molecule.spin = self.multiplicity - 1
        pyscf_molecule.charge = self.charge
        pyscf_molecule.symmetry = False
        pyscf_molecule.build()
        return pyscf_molecule

    def _run_pyscf(self) -> Tuple[gto.Mole, scf.hf.SCF]:
        """Run an SCF calculation using PySCF and return the results as a meanfield
        object.

        Note that this method will apply AVAS but does not account for occupied_indices
        and active_indices.

        Returns:
            Tuple whose first element is the PySCF molecule object after AVAS reduction
                and whose second is the meanfield object containing the SCF solution.
        """
        molecule = self.get_pyscf_molecule()
        mean_field_object = (scf.RHF if self.multiplicity == 1 else scf.ROHF)(molecule)
        mean_field_object.run()
        if self.avas_atomic_orbitals or self.avas_minao:
            molecule, mean_field_object = truncate_with_avas(
                mean_field_object,
                self.avas_atomic_orbitals,
                self.avas_minao,
            )
        return molecule, mean_field_object

    def get_active_space_hamiltonian(self) -> openfermion.InteractionOperator:
        """Generate the fermionic Hamiltonian corresponding to the instance's
        active space.

        Returns:
            The fermionic Hamiltonian corresponding to the instance's active space. Note
                that the active space will account for both AVAS and the
                occupied_indices/active_indices attributes.
        """
        return self._get_molecular_data().get_molecular_hamiltonian(
            occupied_indices=self.occupied_indices,
            active_indices=self.active_indices,
        )

    def get_active_space_meanfield_object(self) -> scf.hf.SCF:
        """Run an SCF calculation using PySCF and return the results as a meanfield
        object.

        Currently, this method does not support the occupied_indices and active_indices
        attributes and will raise an exception if they are set.

        Returns:
            A meanfield object corresponding to the instance's active space, accounting
                for AVAS."""
        if self.active_indices or self.occupied_indices:
            raise ValueError(
                "Generating the meanfield object for application instances with"
                "active and occupied indices is not currently supported."
            )
        return self._run_pyscf()[1]

    def _get_molecular_data(self):
        """Given a PySCF meanfield object and molecule, return a PyscfMolecularData object.

        Args:
            molecule: The PySCF molecule object.
            mean_field_object: The meanfield object representing the SCF solution.

        Returns:
            A PyscfMolecularData object corresponding to the meanfield object and molecule.
        """
        molecular_data = MolecularData(
            geometry=self.geometry,
            basis=self.basis,
            multiplicity=self.multiplicity,
            charge=self.charge,
        )
        molecule, mean_field_object = self._run_pyscf()
        molecular_data.n_orbitals = int(molecule.nao_nr())
        molecular_data.n_qubits = 2 * molecular_data.n_orbitals
        molecular_data.nuclear_repulsion = float(molecule.energy_nuc())

        molecular_data.hf_energy = float(mean_field_object.e_tot)

        molecular_data._pyscf_data = pyscf_data = {}
        pyscf_data["mol"] = molecule
        pyscf_data["scf"] = mean_field_object

        molecular_data.canonical_orbitals = mean_field_object.mo_coeff.astype(float)
        molecular_data.orbital_energies = mean_field_object.mo_energy.astype(float)

        one_body_integrals, two_body_integrals = compute_integrals(
            molecule, mean_field_object
        )
        molecular_data.one_body_integrals = one_body_integrals
        molecular_data.two_body_integrals = two_body_integrals
        molecular_data.overlap_integrals = mean_field_object.get_ovlp()


        pyscf_molecular_data = PyscfMolecularData.__new__(PyscfMolecularData)
        pyscf_molecular_data.__dict__.update(molecule.__dict__)
        return molecular_data


def truncate_with_avas(
    mean_field_object: scf.hf.SCF,
    ao_list: Optional[Iterable[str]] = None,
    minao: Optional[str] = None,
):
    """Truncates a meanfield object to a specific active space that captures the
    essential chemistry.

    Args:
        mean_field_object: The meanfield object to be truncated.
        ao_list: A list of atomic orbitals to use for AVAS.
        minao: The minimum active orbital to use for AVAS.
    """
    mean_field_object.verbose = 4

    # make sure wave function is stable before we proceed
    mean_field_object = stability(mean_field_object)

    # localize before automatically selecting active space with AVAS
    mean_field_object = localize(
        mean_field_object, loc_type="pm"
    )  # default is loc_type ='pm' (Pipek-Mezey)

    return avas_active_space(mean_field_object, ao_list=ao_list, minao=minao)


def generate_hydrogen_chain_instance(
    number_of_hydrogens: int,
    basis: str = "6-31g",
    bond_distance: float = 1.3,
) -> ChemistryApplicationInstance:
    """Generate a hydrogen chain application instance.

    Args:
        number_of_hydrogens: The number of hydrogen atoms in the chain.
        basis: The basis set to use for the calculation.
        bond_distance: The distance between the hydrogen atoms (Angstrom).
    """
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
    """Get the geometry of a cyclic ozone molecule."""
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
