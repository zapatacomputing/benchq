################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple
from functools import reduce

import numpy as np
import openfermion
from openfermion import MolecularData
from openfermion.resource_estimates.molecule import (
    avas_active_space,
    localize,
    stability,
)
from openfermionpyscf import PyscfMolecularData
from pyscf import gto, mp, scf, ao2mo
import psutil


class SCFConvergenceError(Exception):
    pass


@dataclass
class ChemistryApplicationInstance:
    """Class for representing chemistry application instances.

    A chemistry application instance is a specification of how to generate a fermionic
    Hamiltonian, including information such as the molecular geometry and choice of
    active space. Note that the active space can be specified in one of the following
    ways:

    1. the use of Atomic Valence Active Space (AVAS),

    2. by specifying the indices of the occupied and active orbitals,

        If freeze_core option is True, chemical frozen core orbitals
        are choosen for occuped_indicies.

    3. by using the frozen natural orbital (FNO) approach.
       In this case, a user needs to set one of the FNO parameters:
            - fno_percentage_occupation_number
            - fno_threshold
            - fno_n_virtual_natural_orbitals
        to decide how much virtual space will be kept for the active space.

        If freeze_core option is True, chemical frozen core orbitals
        are choosen for occuped_indicies.


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
        freeze_core: A boolean specifying whether frozen core orbitals are selected
                    for calculations.
        fno_percentage_occupation_number: Percentage of total occupation number.
        fno_threshold: Threshold on NO occupation numbers.
        fno_n_virtual_natural_orbitals: Number of virtual NOs to keep.
    """

    geometry: List[Tuple[str, Tuple[float, float, float]]]
    basis: str
    multiplicity: int
    charge: int
    avas_atomic_orbitals: Optional[Iterable[str]] = None
    avas_minao: Optional[str] = None
    occupied_indices: Optional[Iterable[int]] = None
    active_indices: Optional[Iterable[int]] = None
    freeze_core: Optional[bool] = None
    fno_percentage_occupation_number: Optional[float] = None
    fno_threshold: Optional[float] = None
    fno_n_virtual_natural_orbitals: Optional[int] = None
    scf_options: Optional[dict] = None

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
            Tuple whose first element is the PySCF molecule object after AVAS or FNO
              reduction and whose second is the meanfield object containing the SCF solution.

        Raises:
            SCFConvergenceError: If the SCF calculation does not converge.
        """
        molecule = self.get_pyscf_molecule()
        mean_field_object = (scf.RHF if self.multiplicity ==
                             1 else scf.ROHF)(molecule)

        if self.scf_options is not None:
            mean_field_object.run(**self.scf_options)
        else:
            mean_field_object.run()

        if not mean_field_object.converged:
            raise SCFConvergenceError()

        if self.avas_atomic_orbitals or self.avas_minao:
            molecule, mean_field_object = truncate_with_avas(
                mean_field_object,
                self.avas_atomic_orbitals,
                self.avas_minao,
            )

        if (
            self.fno_percentage_occupation_number
            or self.fno_threshold
            or self.fno_n_virtual_natural_orbitals
        ):
            molecule, mean_field_object = self._truncate_with_fno(
                molecule, mean_field_object
            )
            print("DBG.. _truncate_with_fno() completed")

            # Get memory usage in bytes
            memory_usage = psutil.Process().memory_info().rss
            # Convert memory usage to megabytes
            memory_usage_mb = memory_usage / (1024 * 1024)
            print(f"Memory Usage: {memory_usage_mb:.2f} MB")

        return molecule, mean_field_object

    def get_active_space_hamiltonian(self) -> openfermion.InteractionOperator:
        """Generate the fermionic Hamiltonian corresponding to the instance's
        active space.

        The active space will be reduced with AVAS if the instance has AVAS
        attributes set, and further reduced to the orbitals specified by
        occupied_indices and active_indices attributes. Alternatively, the active
        space will be reduced with FNO if the FNO attribute is set.

        Returns:
            The fermionic Hamiltonian corresponding to the instance's active space. Note
                that the active space will account for both AVAS and the
                occupied_indices/active_indices attributes.

        Raises:
            SCFConvergenceError: If the SCF calculation does not converge.
        """

        molecular_data = self._get_molecular_data()

        if self.freeze_core:
            n_frozen_core = self._set_frozen_core_orbitals(
                molecular_data).frozen
            if n_frozen_core > 0:
                self.occupied_indices = list(range(n_frozen_core))

        return molecular_data.get_molecular_hamiltonian(
            occupied_indices=self.occupied_indices,
            active_indices=self.active_indices,
        )

    def get_active_space_meanfield_object(self) -> scf.hf.SCF:
        """Run an SCF calculation using PySCF and return the results as a meanfield
        object.

        Currently, this method does not support the occupied_indices and active_indices
        attributes, as well as the FNO attributes and will raise an exception if they
        are set.

        Returns:
            A meanfield object corresponding to the instance's active space, accounting
                for AVAS.

        Raises:
            SCFConvergenceError: If the SCF calculation does not converge.
        """
        if (
            self.active_indices
            or self.occupied_indices
            or self.fno_percentage_occupation_number
            or self.fno_threshold
            or self.fno_n_virtual_natural_orbitals
        ):
            raise ValueError(
                "Generating the meanfield object for application instances with "
                "active and occupied indices, as well as with the FNO approach  "
                " is not currently supported."
            )
        return self._run_pyscf()[1]

    def _get_molecular_data(self):
        """Given a PySCF meanfield object and molecule, return a PyscfMolecularData
        object.

        Returns:
            A PyscfMolecularData object corresponding to the meanfield object and
                molecule.

        Raises:
            SCFConvergenceError: If the SCF calculation does not converge.
        """
        molecular_data = MolecularData(
            geometry=self.geometry,
            basis=self.basis,
            multiplicity=self.multiplicity,
            charge=self.charge,
        )

        molecule, mean_field_object = self._run_pyscf()
        molecular_data.n_orbitals = int(molecule.nao)
        molecular_data.n_qubits = 2 * molecular_data.n_orbitals
        molecular_data.nuclear_repulsion = float(molecule.energy_nuc())

        molecular_data.hf_energy = float(mean_field_object.e_tot)

        molecular_data._pyscf_data = pyscf_data = {}
        pyscf_data["mol"] = molecule
        pyscf_data["scf"] = mean_field_object

        molecular_data.canonical_orbitals = mean_field_object.mo_coeff.astype(
            float)
        molecular_data.orbital_energies = mean_field_object.mo_energy.astype(
            float)

        print("DBG... before compute_integrals()")

        # Get memory usage in bytes
        memory_usage = psutil.Process().memory_info().rss
        # Convert memory usage to megabytes
        memory_usage_mb = memory_usage / (1024 * 1024)
        print(f"Memory Usage: {memory_usage_mb:.2f} MB")

        one_body_integrals, two_body_integrals = compute_integrals(
            mean_field_object._eri, mean_field_object
        )
        print("DBG... after compute_integrals()")
        molecular_data.one_body_integrals = one_body_integrals
        molecular_data.two_body_integrals = two_body_integrals
        molecular_data.overlap_integrals = mean_field_object.get_ovlp()

        pyscf_molecular_data = PyscfMolecularData.__new__(PyscfMolecularData)
        pyscf_molecular_data.__dict__.update(molecule.__dict__)

        return molecular_data

    def _set_frozen_core_orbitals(self, mean_field_object) -> mp.mp2.MP2:
        """
        Set auto-generated chemical core orbitals.

        Args:
            mean_field_object: The PySCF meanfield object.

        Returns
            The mp2 object.
        """
        mp2 = mp.MP2(mean_field_object).set_frozen()
        return mp2

    def _truncate_with_fno(
        self,
        molecule: gto.Mole,
        mean_field_object: scf.hf.SCF,
    ) -> Tuple[gto.Mole, scf.hf.SCF]:
        """Truncates a meanfield object by reducing the virtual space using
        the frozen natural orbital (FNO) method.

        Args:
            molecule: The PySCF molecule object.
            mean_field_object: The meanfield object to be truncated.

        Returns:
            Tuple whose first element is the PySCF molecule object after FNO vertual space
              reduction and whose second is the meanfield object containing the SCF solution.
        """

        if molecule.multiplicity != 1:
            raise ValueError("RO-MP2 is not available.")

        n_frozen_core_orbitals = 0

        if self.freeze_core and self.occupied_indices:
            raise ValueError(
                "Both freeze core and occupied_indices were set!"
                "Those options are exclusive. Please select either one."
            )

        elif self.freeze_core and not self.occupied_indices:
            mp2 = self._set_frozen_core_orbitals(mean_field_object)
            n_frozen_core_orbitals = mp2.frozen

        elif self.occupied_indices and not self.freeze_core:
            mp2 = mp.MP2(mean_field_object).set(frozen=self.occupied_indices)
            n_frozen_core_orbitals = len(list(self.occupied_indices))

        else:
            mp2 = mp.MP2(mean_field_object)

        mp2.verbose = 4
        print("DBG.. Before running MP2...")
        mp2 = mp2.density_fit().run()
        print("DBG.. Before running MP2 completed")

        frozen_natural_orbitals, natural_orbital_coefficients = mp2.make_fno(
            self.fno_threshold,
            self.fno_percentage_occupation_number,
            self.fno_n_virtual_natural_orbitals,
        )

        print("DBG.. make_fno() completed")
        if len(frozen_natural_orbitals) != 0:
            mean_field_object.mo_coeff = natural_orbital_coefficients[
                :, : -len(frozen_natural_orbitals)
            ]
        else:
            mean_field_object.mo_coeff = natural_orbital_coefficients

        # Calculate the number of orbitals after truncation with fno
        molecule._nao = mean_field_object.mo_coeff.shape[1]

        print("FNO threshold: ", self.fno_percentage_occupation_number)
        print("Number of orbitals:", molecule._nao)

        return molecule, mean_field_object


def truncate_with_avas(
    mean_field_object: scf.hf.SCF,
    ao_list: Optional[Iterable[str]] = None,
    minao: Optional[str] = None,
) -> Tuple[gto.Mole, scf.hf.SCF]:
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


def compute_integrals(pyscf_molecule, pyscf_scf):
    """
    Compute the 1-electron and 2-electron integrals.

    Args:
        pyscf_molecule: A pyscf molecule instance.
        pyscf_scf: A PySCF "SCF" calculation object.

    Returns:
        one_electron_integrals: An N by N array storing h_{pq}
        two_electron_integrals: An N by N by N by N array storing h_{pqrs}.
    """
    # Get one electrons integrals.
    print("GBD.. Inside compute_integrals ")
    # Get memory usage in bytes
    memory_usage = psutil.Process().memory_info().rss
    # Convert memory usage to megabytes
    memory_usage_mb = memory_usage / (1024 * 1024)
    print(f"Memory Usage: {memory_usage_mb:.2f} MB")

    n_orbitals = pyscf_scf.mo_coeff.shape[1]
    one_electron_compressed = reduce(np.dot, (pyscf_scf.mo_coeff.T,
                                              pyscf_scf.get_hcore(),
                                              pyscf_scf.mo_coeff))
    one_electron_integrals = one_electron_compressed.reshape(
        n_orbitals, n_orbitals).astype(float)

    print("GBD.. One electron integrals completed... ")
    # Get memory usage in bytes
    memory_usage = psutil.Process().memory_info().rss
    # Convert memory usage to megabytes
    memory_usage_mb = memory_usage / (1024 * 1024)
    print(f"Memory Usage: {memory_usage_mb:.2f} MB")

    # Get two electron integrals in compressed format.
    two_electron_integrals = ao2mo.kernel(pyscf_molecule,
                                          pyscf_scf.mo_coeff)

    print("GBD.. Two electron integrals completed... p1")
    # Get memory usage in bytes
    memory_usage = psutil.Process().memory_info().rss
    # Convert memory usage to megabytes
    memory_usage_mb = memory_usage / (1024 * 1024)
    print(f"Memory Usage: {memory_usage_mb:.2f} MB")

    two_electron_integrals = ao2mo.restore(
        1,  # no permutation symmetry
        two_electron_integrals, n_orbitals)
    # See PQRS convention in OpenFermion.hamiltonians._molecular_data
    # h[p,q,r,s] = (ps|qr)

    print("GBD.. Two electron integrals completed... p2")
    # Get memory usage in bytes
    memory_usage = psutil.Process().memory_info().rss
    # Convert memory usage to megabytes
    memory_usage_mb = memory_usage / (1024 * 1024)
    print(f"Memory Usage: {memory_usage_mb:.2f} MB")

    two_electron_integrals = np.asarray(
        two_electron_integrals.transpose(0, 2, 3, 1), order='C')

    print("GBD.. Two electron integrals completed... p3")
    # Get memory usage in bytes
    memory_usage = psutil.Process().memory_info().rss
    # Convert memory usage to megabytes
    memory_usage_mb = memory_usage / (1024 * 1024)
    print(f"Memory Usage: {memory_usage_mb:.2f} MB")

    # Return.
    return one_electron_integrals, two_electron_integrals


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
        geometry=[("H", (0, 0, i * bond_distance))
                  for i in range(number_of_hydrogens)],
        basis=basis,
        charge=0,
        multiplicity=number_of_hydrogens % 2 + 1,
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
