################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
import os
import warnings
from copy import deepcopy
from dataclasses import asdict, dataclass
from typing import Iterable, List, Optional, Tuple

import numpy as np
import openfermion
import urllib3  # type: ignore
from mlflow import MlflowClient  # type: ignore
from openfermion import MolecularData

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # we need to disable pyscf GC as it throws around bunch of warnings
    import pyscf

    pyscf.gto.mole.DISABLE_GC = True

    from openfermion.resource_estimates.molecule import (
        avas_active_space,
        localize,
        stability,
    )

from openfermionpyscf import PyscfMolecularData
from openfermionpyscf._run_pyscf import compute_integrals
from orquestra import sdk
from pyscf import gto, mp, scf

from ..mlflow import _flatten_dict, create_mlflow_scf_callback


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

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        mean_field_object = localize(
            mean_field_object, loc_type="pm"
        )  # default is loc_type ='pm' (Pipek-Mezey)
        active_space = avas_active_space(
            mean_field_object, ao_list=ao_list, minao=minao
        )

    return active_space


def _create_mlflow_setup(
    mlflow_experiment_name: str, orq_workspace_id: str
) -> Tuple[MlflowClient, str]:
    client = MlflowClient(
        tracking_uri=sdk.mlflow.get_tracking_uri(workspace_id=orq_workspace_id)
    )

    experiment = client.get_experiment_by_name(name=mlflow_experiment_name)
    if experiment is None:
        client.create_experiment(mlflow_experiment_name)
        experiment = client.get_experiment_by_name(name=mlflow_experiment_name)

    run = client.create_run(experiment.experiment_id)

    return client, run.info.run_id


class SCFConvergenceError(Exception):
    pass


@dataclass(frozen=True)
class MoleculeSpecification:
    geometry: List[Tuple[str, Tuple[float, float, float]]]
    basis: str
    multiplicity: int
    charge: int


@dataclass(frozen=True)
class ActiveSpaceSpecification:
    avas_atomic_orbitals: Optional[Iterable[str]] = None
    avas_minao: Optional[str] = None
    occupied_indices: Optional[Iterable[int]] = None
    active_indices: Optional[Iterable[int]] = None
    freeze_core: Optional[bool] = None
    fno_percentage_occupation_number: Optional[float] = None
    fno_threshold: Optional[float] = None
    fno_n_virtual_natural_orbitals: Optional[int] = None


@dataclass(frozen=True)
class SCFInfo:
    mol_spec: MoleculeSpecification
    active_space_spec: ActiveSpaceSpecification
    scf_options: Optional[dict] = None
    mlflow_experiment_name: Optional[str] = None
    orq_workspace_id: Optional[str] = None


def _truncate_with_fno(
    active_space_spec,
    molecule: gto.Mole,
    mean_field_object: scf.hf.SCF,
) -> Tuple[gto.Mole, scf.hf.SCF]:
    """Truncates a meanfield object by reducing the virtual space using
    the frozen natural orbital (FNO) method.

    Args:
        molecule: The PySCF molecule object.
        mean_field_object: The meanfield object to be truncated.

    Returns:
        Tuple whose first element is the PySCF molecule object after FNO
        vertual space reduction and whose second is the meanfield object
        containing the SCF solution.
    """

    if molecule.multiplicity != 1:
        raise ValueError("RO-MP2 is not available.")

    if active_space_spec.freeze_core and active_space_spec.occupied_indices:
        raise ValueError(
            "Both freeze core and occupied_indices were set!"
            "Those options are exclusive. Please select either one."
        )

    elif active_space_spec.freeze_core and not active_space_spec.occupied_indices:
        mp2 = mp.MP2(mean_field_object).set_frozen()

    elif active_space_spec.occupied_indices and not active_space_spec.freeze_core:
        mp2 = mp.MP2(mean_field_object).set(frozen=active_space_spec.occupied_indices)

    else:
        mp2 = mp.MP2(mean_field_object)

    mp2.verbose = 4
    mp2.density_fit().run()

    frozen_natural_orbitals, natural_orbital_coefficients = mp2.make_fno(
        active_space_spec.fno_threshold,
        active_space_spec.fno_percentage_occupation_number,
        active_space_spec.fno_n_virtual_natural_orbitals,
    )

    if len(frozen_natural_orbitals) != 0:
        mean_field_object.mo_coeff = natural_orbital_coefficients[
            :, : -len(frozen_natural_orbitals)
        ]
    else:
        mean_field_object.mo_coeff = natural_orbital_coefficients

    # Calculate the number of orbitals after truncation with fno
    molecule.nao = mean_field_object.mo_coeff.shape[1]

    print("Number of FNOs: ", len(frozen_natural_orbitals))
    print("Number of orbitals after truncation with FNO:", molecule.nao)

    return molecule, mean_field_object


def _get_pyscf_molecule(mol_spec: MoleculeSpecification) -> gto.Mole:
    "Generate the PySCF molecule object describing the system to be calculated."
    pyscf_molecule = gto.Mole()
    pyscf_molecule.atom = mol_spec.geometry
    pyscf_molecule.basis = mol_spec.basis
    pyscf_molecule.spin = mol_spec.multiplicity - 1
    pyscf_molecule.charge = mol_spec.charge
    pyscf_molecule.symmetry = False
    pyscf_molecule.build()
    return pyscf_molecule


def _run_pyscf(scf_info: SCFInfo) -> Tuple[gto.Mole, scf.hf.SCF]:
    """Run an SCF calculation using PySCF and return the results as a meanfield
    object.

    Note that this method will apply AVAS but does not account for occupied_indices
    and active_indices.

    Args:
        log_to_mlflow: if supplied, will log metrics from SCF calculation to mlflow

    Returns:
        Tuple whose first element is the PySCF molecule object after AVAS or FNO
            reduction and whose second is the meanfield object containing the SCF
            solution.

    Raises:
        SCFConvergenceError: If the SCF calculation does not converge.
    """
    molecule = _get_pyscf_molecule(scf_info.mol_spec)
    mean_field_object = (scf.RHF if scf_info.mol_spec.multiplicity == 1 else scf.ROHF)(
        molecule
    )
    mean_field_object.max_memory = 1e6  # set allowed memory high so tests pass

    run_id = None

    if scf_info.mlflow_experiment_name is not None:
        os.environ["MLFLOW_TRACKING_TOKEN"] = sdk.mlflow.get_tracking_token()
        urllib3.disable_warnings()

        flat_mol_dict = _flatten_dict(asdict(scf_info.mol_spec))
        flat_active_dict = _flatten_dict(asdict(scf_info.active_space_spec))

        if scf_info.scf_options is not None:
            if "callback" in scf_info.scf_options:
                # we want to log to mlflow, AND we've defined the
                # callback in scf_options
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=DeprecationWarning)
                    mean_field_object.run(**scf_info.scf_options)
            else:
                # we want to log to mlflow, BUT haven't defined the
                # callback in scf_options
                if not isinstance(scf_info.orq_workspace_id, str):
                    raise TypeError(
                        "orq_workspace_id is not a str, it is "
                        + str(type(scf_info.orq_workspace_id))
                        + " Did you remember to pass that in "
                        "to the ChemistryApplicationInstance?"
                    )
                client, run_id = _create_mlflow_setup(
                    scf_info.mlflow_experiment_name, scf_info.orq_workspace_id
                )

                for key, val in flat_mol_dict.items():
                    client.log_param(run_id, key, val)
                for key, val in flat_active_dict.items():
                    client.log_param(run_id, key, val)
                temp_options = deepcopy(scf_info.scf_options)
                temp_options["callback"] = create_mlflow_scf_callback(client, run_id)
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=DeprecationWarning)
                    mean_field_object.run(**temp_options)
        else:
            # we want to log to mlflow, but haven't defined scf_options
            if not isinstance(scf_info.orq_workspace_id, str):
                raise TypeError(
                    "orq_workspace_id is not a str, it is "
                    + str(type(scf_info.orq_workspace_id))
                    + " Did you remember to pass that in "
                    "to the ChemistryApplicationInstance?"
                )
            client, run_id = _create_mlflow_setup(
                scf_info.mlflow_experiment_name, scf_info.orq_workspace_id
            )

            for key, val in flat_mol_dict.items():
                client.log_param(run_id, key, val)
            for key, val in flat_active_dict.items():
                client.log_param(run_id, key, val)
            temp_options = {"callback": create_mlflow_scf_callback(client, run_id)}
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                mean_field_object.run(**temp_options)
    else:
        if scf_info.scf_options is not None:
            # we don't want to run on mlflow, but we've specified scf_options
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                mean_field_object.run(**scf_info.scf_options)
        else:
            # we don't want to run on mlflow, and haven't specified scf_options
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                mean_field_object.run()

    if not mean_field_object.converged:
        raise SCFConvergenceError()

    if (
        scf_info.active_space_spec.avas_atomic_orbitals
        or scf_info.active_space_spec.avas_minao
    ):
        molecule, mean_field_object = truncate_with_avas(
            mean_field_object,
            scf_info.active_space_spec.avas_atomic_orbitals,
            scf_info.active_space_spec.avas_minao,
        )
    if (
        scf_info.active_space_spec.fno_percentage_occupation_number
        or scf_info.active_space_spec.fno_threshold
        or scf_info.active_space_spec.fno_n_virtual_natural_orbitals
    ):
        molecule, mean_field_object = _truncate_with_fno(
            scf_info.active_space_spec, molecule, mean_field_object
        )
    return molecule, mean_field_object


class ActiveSpaceGenerator:
    def __init__(
        self,
        scf_info: SCFInfo,
    ):
        self.scf_info = scf_info

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
        occupied_idx = self.scf_info.active_space_spec.occupied_indices

        if self.scf_info.active_space_spec.freeze_core:
            n_frozen_core = (
                mp.MP2(molecular_data._pyscf_data["scf"]).set_frozen().frozen
            )
            if n_frozen_core > 0:
                occupied_idx = list(range(n_frozen_core))

        return molecular_data.get_molecular_hamiltonian(
            occupied_indices=occupied_idx,
            active_indices=self.scf_info.active_space_spec.active_indices,
        )

    def get_active_space_meanfield_object(
        self,
    ) -> scf.hf.SCF:
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
            self.scf_info.active_space_spec.active_indices
            or self.scf_info.active_space_spec.occupied_indices
            or self.scf_info.active_space_spec.fno_percentage_occupation_number
            or self.scf_info.active_space_spec.fno_threshold
            or self.scf_info.active_space_spec.fno_n_virtual_natural_orbitals
        ):
            raise ValueError(
                "Generating the meanfield object for application instances with "
                "active and occupied indices, as well as with the FNO approach  "
                " is not currently supported."
            )
        return _run_pyscf(self.scf_info)[1]

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
            geometry=self.scf_info.mol_spec.geometry,
            basis=self.scf_info.mol_spec.basis,
            multiplicity=self.scf_info.mol_spec.multiplicity,
            charge=self.scf_info.mol_spec.charge,
        )

        molecule, mean_field_object = _run_pyscf(self.scf_info)
        molecular_data.n_orbitals = int(molecule.nao)
        molecular_data.n_qubits = 2 * molecular_data.n_orbitals
        molecular_data.nuclear_repulsion = float(molecule.energy_nuc())

        molecular_data.hf_energy = float(mean_field_object.e_tot)

        molecular_data._pyscf_data = pyscf_data = {}
        pyscf_data["mol"] = molecule
        pyscf_data["scf"] = mean_field_object

        molecular_data.canonical_orbitals = mean_field_object.mo_coeff.astype(float)
        molecular_data.orbital_energies = mean_field_object.mo_energy.astype(float)

        one_body_integrals, two_body_integrals = compute_integrals(
            mean_field_object._eri, mean_field_object
        )
        molecular_data.one_body_integrals = one_body_integrals
        molecular_data.two_body_integrals = two_body_integrals
        molecular_data.overlap_integrals = mean_field_object.get_ovlp()

        pyscf_molecular_data = PyscfMolecularData.__new__(PyscfMolecularData)
        pyscf_molecular_data.__dict__.update(molecule.__dict__)

        return molecular_data


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
        scf_options: dictionary with parameters for pySCF calculations
        mlflow_experiment_name: if supplied, pySCF calculations will be logged to
            mlflow. See orq_workspace_id also
        orq_workspace_id: orquestra workspace ID. Required to log mlflow info
    """

    mol_spec: MoleculeSpecification
    active_space_spec: ActiveSpaceSpecification
    scf_info: SCFInfo
    active_space_gen: ActiveSpaceGenerator

    def __init__(
        self,
        geometry: List[Tuple[str, Tuple[float, float, float]]],
        basis: str,
        multiplicity: int,
        charge: int,
        avas_atomic_orbitals: Optional[Iterable[str]] = None,
        avas_minao: Optional[str] = None,
        occupied_indices: Optional[Iterable[int]] = None,
        active_indices: Optional[Iterable[int]] = None,
        freeze_core: Optional[bool] = None,
        fno_percentage_occupation_number: Optional[float] = None,
        fno_threshold: Optional[float] = None,
        fno_n_virtual_natural_orbitals: Optional[int] = None,
        scf_options: Optional[dict] = None,
        mlflow_experiment_name: Optional[str] = None,
        orq_workspace_id: Optional[str] = None,
    ):
        self.mol_spec = MoleculeSpecification(
            geometry=geometry,
            basis=basis,
            multiplicity=multiplicity,
            charge=charge,
        )
        self.active_space_spec = ActiveSpaceSpecification(
            avas_atomic_orbitals=avas_atomic_orbitals,
            avas_minao=avas_minao,
            occupied_indices=occupied_indices,
            active_indices=active_indices,
            freeze_core=freeze_core,
            fno_percentage_occupation_number=fno_percentage_occupation_number,
            fno_threshold=fno_threshold,
            fno_n_virtual_natural_orbitals=fno_n_virtual_natural_orbitals,
        )
        self.scf_info = SCFInfo(
            mol_spec=self.mol_spec,
            active_space_spec=self.active_space_spec,
            scf_options=scf_options,
            mlflow_experiment_name=mlflow_experiment_name,
            orq_workspace_id=orq_workspace_id,
        )
        self.active_space_gen = ActiveSpaceGenerator(scf_info=self.scf_info)

    def get_pyscf_molecule(self) -> gto.Mole:
        return _get_pyscf_molecule(self.mol_spec)

    def get_active_space_hamiltonian(self) -> openfermion.InteractionOperator:
        return self.active_space_gen.get_active_space_hamiltonian()

    def get_active_space_meanfield_object(self) -> scf.hf.SCF:
        return self.active_space_gen.get_active_space_meanfield_object()


def generate_hydrogen_chain_instance(
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
) -> ChemistryApplicationInstance:
    """Generate a hydrogen chain application instance.

    Args:
        number_of_hydrogens: The number of hydrogen atoms in the chain.
        basis: The basis set to use for the calculation.
        bond_distance: The distance between the hydrogen atoms (Angstrom).
        active_indices: A list of molecular orbitals to include in the active space.
        occupied_indices: A list of molecular orbitals not in the active space that
            should be assumed to be fully occupied.
        avas_atomic_orbitals: A list of atomic orbitals to use for (AVAS).
        avas_minao: The minimum active orbital to use for AVAS.
        scf_options: dictionary with parameters for pySCF calculations
        mlflow_experiment_name: if supplied, pySCF calculations will be logged to
            mlflow. See orq_workspace_id also
        orq_workspace_id: orquestra workspace ID. Required to log mlflow info
    """
    return ChemistryApplicationInstance(
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
