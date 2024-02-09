################################################################################
# © Copyright 2024 Zapata Computing Inc.
################################################################################
from typing import List, Optional, Tuple

import numpy as np

from benchq.problem_ingestion.molecular_hamiltonians._hamiltonian_generation import (
    MolecularHamiltonianGenerator,
)


def get_hydrogen_chain_hamiltonian_generator(
    number_of_hydrogens: int,
    basis: str = "6-31g",
    bond_distance: float = 1.3,
    active_indices: Optional[List[int]] = None,
    occupied_indices: Optional[List[int]] = None,
    avas_atomic_orbitals: Optional[List[str]] = None,
    avas_minao: Optional[str] = None,
    scf_options: Optional[dict] = None,
    mlflow_experiment_name: Optional[str] = None,
    orq_workspace_id: Optional[str] = None,
) -> MolecularHamiltonianGenerator:
    """Generate a hydrogen chain Hamiltonian generator.

    Args:
        number_of_hydrogens: The number of hydrogen atoms in the chain.
        basis: The basis set to use for the calculation.
        bond_distance: The distance between the hydrogen atoms (Angstrom).
        active_indices: A list of molecular orbitals to include in the active space.
        occupied_indices: A list of molecular orbitals not in the active space that
            should be assumed to be fully occupied.
        avas_atomic_orbitals: A list of atomic orbitals to use for AVAS.
        avas_minao: The minimum active orbital to use for AVAS.
        scf_options: dictionary with parameters for PySCF calculations
        mlflow_experiment_name: See MolecularHamiltonianGenerator.
        orq_workspace_id: See MolecularHamiltonianGenerator.
    """
    return MolecularHamiltonianGenerator(
        geometry=[("H", (0, 0, i * bond_distance)) for i in range(number_of_hydrogens)],
        basis=basis,
        charge=0,
        multiplicity=number_of_hydrogens % 2 + 1,
        active_indices=active_indices,
        occupied_indices=occupied_indices,
        avas_atomic_orbitals=avas_atomic_orbitals,
        avas_minao=avas_minao,
        scf_options=scf_options,
        mlflow_experiment_name=mlflow_experiment_name,
        orq_workspace_id=orq_workspace_id,
    )


WATER_MOLECULE = MolecularHamiltonianGenerator(
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


CYCLIC_OZONE_MOLECULE = MolecularHamiltonianGenerator(
    geometry=get_cyclic_ozone_geometry(),
    basis="cc-pvtz",
    multiplicity=3,
    charge=0,
    occupied_indices=range(3),
    active_indices=range(3, 15),
)
