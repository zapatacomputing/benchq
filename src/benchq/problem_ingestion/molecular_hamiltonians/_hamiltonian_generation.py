################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
import os
import warnings
from copy import deepcopy
from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

import openfermion
import urllib3
from mlflow import MlflowClient
from openfermion import MolecularData

with warnings.catch_warnings():
    warnings.filterwarnings(
        "ignore",
        message="\n\n"
        "  `numpy.distutils` is deprecated since NumPy 1.23.0, as a result\n",
    )

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

from ...mlflow.data_logging import _flatten_dict, create_mlflow_scf_callback


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
        warnings.filterwarnings(
            "ignore", message="The 'sym_pos' keyword is deprecated and should be"
        )
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


def _truncate_with_fno(
    active_space_spec: ActiveSpaceSpecification,
    molecule: gto.Mole,
    mean_field_object: scf.hf.SCF,
) -> Tuple[gto.Mole, scf.hf.SCF]:
    """Truncates a meanfield object by reducing the virtual space using
    the frozen natural orbital (FNO) method.

    Args:
        active_space_spec: The active space specification.
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


def _run_pyscf(
    mol_spec: MoleculeSpecification,
    active_space_spec: ActiveSpaceSpecification,
    scf_options: Optional[Dict[str, Any]] = None,
    mlflow_experiment_name: Optional[str] = None,
    orq_workspace_id: Optional[str] = None,
) -> Tuple[gto.Mole, scf.hf.SCF]:
    """Run an SCF calculation using PySCF and return the results as a meanfield
    object.

    Note that this method will apply AVAS but does not account for occupied_indices
    and active_indices.

    Args:
        mol_spec: The molecule specification.
        active_space_spec: The active space specification.
        scf_options: Dictionary with optional parameters to pass to PySCF.
        mlflow_experiment_name: See MolecularHamiltonianGenerator.
        orq_workspace_id: See MolecularHamiltonianGenerator.

    Returns:
        Tuple whose first element is the PySCF molecule object after AVAS or FNO
            reduction and whose second is the meanfield object containing the SCF
            solution.

    Raises:
        SCFConvergenceError: If the SCF calculation does not converge.
        ValueError: If mlflow_experiment_name is set but orq_workspace_id is not or
            scf_options contains a "callback" key.
    """
    molecule = _get_pyscf_molecule(mol_spec)
    mean_field_object = (scf.RHF if mol_spec.multiplicity == 1 else scf.ROHF)(molecule)
    mean_field_object.max_memory = 1e6  # set allowed memory high so tests pass

    updated_scf_options = {}
    if scf_options is not None:
        updated_scf_options.update(scf_options)

    if mlflow_experiment_name is not None:
        if orq_workspace_id is None:
            raise ValueError(
                "orq_workspace_id must be set if mlflow_experiment_name is set."
            )
        os.environ["MLFLOW_TRACKING_TOKEN"] = sdk.mlflow.get_tracking_token()
        urllib3.disable_warnings()

        flat_mol_dict = _flatten_dict(asdict(mol_spec))
        flat_active_dict = _flatten_dict(asdict(active_space_spec))

        if scf_options is not None and "callback" in scf_options:
            raise ValueError(
                "scf_options should not contain a 'callback' key if"
                "mlflow_experiment_name is set."
            )

        client, run_id = _create_mlflow_setup(mlflow_experiment_name, orq_workspace_id)

        for key, val in flat_mol_dict.items():
            client.log_param(run_id, key, val)
        for key, val in flat_active_dict.items():
            client.log_param(run_id, key, val)

        updated_scf_options["callback"] = create_mlflow_scf_callback(client, run_id)

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="The 'sym_pos' keyword is deprecated and should be",
        )
        mean_field_object.run(**updated_scf_options)

    if not mean_field_object.converged:
        raise SCFConvergenceError()

    if active_space_spec.avas_atomic_orbitals or active_space_spec.avas_minao:
        molecule, mean_field_object = truncate_with_avas(
            mean_field_object,
            active_space_spec.avas_atomic_orbitals,
            active_space_spec.avas_minao,
        )
    if (
        active_space_spec.fno_percentage_occupation_number
        or active_space_spec.fno_threshold
        or active_space_spec.fno_n_virtual_natural_orbitals
    ):
        molecule, mean_field_object = _truncate_with_fno(
            active_space_spec, molecule, mean_field_object
        )
    return molecule, mean_field_object


def get_active_space_hamiltonian(
    mol_spec: MoleculeSpecification,
    active_space_spec: ActiveSpaceSpecification,
    scf_options: Optional[Dict[str, Any]] = None,
    mlflow_experiment_name: Optional[str] = None,
    orq_workspace_id: Optional[str] = None,
) -> openfermion.InteractionOperator:
    """Generate the fermionic Hamiltonian corresponding to the instance's
    active space.

    The active space will be reduced with AVAS if the instance has AVAS
    attributes set, and further reduced to the orbitals specified by
    occupied_indices and active_indices attributes. Alternatively, the active
    space will be reduced with FNO if the FNO attribute is set.

    Args:
        mol_spec: The molecule specification.
        active_space_spec: The active space specification.
        scf_options: Dictionary with optional parameters to pass to PySCF.
        mlflow_experiment_name: See MolecularHamiltonianGenerator.
        orq_workspace_id: See MolecularHamiltonianGenerator.

    Returns:
        The fermionic Hamiltonian corresponding to the instance's active space. Note
            that the active space will account for both AVAS and the
            occupied_indices/active_indices attributes.

    Raises:
        SCFConvergenceError: If the SCF calculation does not converge.
    """

    molecular_data = _get_molecular_data(
        mol_spec=mol_spec,
        active_space_spec=active_space_spec,
        scf_options=scf_options,
        mlflow_experiment_name=mlflow_experiment_name,
        orq_workspace_id=orq_workspace_id,
    )
    occupied_idx = active_space_spec.occupied_indices

    if active_space_spec.freeze_core:
        n_frozen_core = mp.MP2(molecular_data._pyscf_data["scf"]).set_frozen().frozen
        if n_frozen_core > 0:
            occupied_idx = list(range(n_frozen_core))

    return molecular_data.get_molecular_hamiltonian(
        occupied_indices=occupied_idx,
        active_indices=active_space_spec.active_indices,
    )


def get_active_space_meanfield_object(
    mol_spec: MoleculeSpecification,
    active_space_spec: ActiveSpaceSpecification,
    scf_options: Optional[Dict[str, Any]] = None,
    mlflow_experiment_name: Optional[str] = None,
    orq_workspace_id: Optional[str] = None,
) -> scf.hf.SCF:
    """Run an SCF calculation using PySCF and return the results as a meanfield
    object.

    Currently, this method does not support the occupied_indices and active_indices
    attributes, as well as the FNO attributes and will raise an exception if they
    are set.

    Args:
    mol_spec: The molecule specification.
    active_space_spec: The active space specification.
    scf_options: Dictionary with optional parameters to pass to PySCF.
    mlflow_experiment_name: See MolecularHamiltonianGenerator.
    orq_workspace_id: See MolecularHamiltonianGenerator.

    Returns:
        A meanfield object corresponding to the instance's active space, accounting
            for AVAS.

    Raises:
        SCFConvergenceError: If the SCF calculation does not converge.
    """
    if (
        active_space_spec.active_indices
        or active_space_spec.occupied_indices
        or active_space_spec.fno_percentage_occupation_number
        or active_space_spec.fno_threshold
        or active_space_spec.fno_n_virtual_natural_orbitals
    ):
        raise ValueError(
            "Generating the meanfield object for application instances with "
            "active and occupied indices, as well as with the FNO approach  "
            " is not currently supported."
        )
    return _run_pyscf(
        mol_spec=mol_spec,
        active_space_spec=active_space_spec,
        scf_options=scf_options,
        mlflow_experiment_name=mlflow_experiment_name,
        orq_workspace_id=orq_workspace_id,
    )[1]


def _get_molecular_data(
    mol_spec: MoleculeSpecification,
    active_space_spec: ActiveSpaceSpecification,
    scf_options: Optional[Dict[str, Any]] = None,
    mlflow_experiment_name: Optional[str] = None,
    orq_workspace_id: Optional[str] = None,
) -> PyscfMolecularData:
    """Given a PySCF meanfield object and molecule, return a PyscfMolecularData
    object.

    Returns:
        A PyscfMolecularData object corresponding to the meanfield object and
            molecule.

    Raises:
        SCFConvergenceError: If the SCF calculation does not converge.
    """
    molecular_data = MolecularData(
        geometry=mol_spec.geometry,
        basis=mol_spec.basis,
        multiplicity=mol_spec.multiplicity,
        charge=mol_spec.charge,
    )

    molecule, mean_field_object = _run_pyscf(
        mol_spec=mol_spec,
        active_space_spec=active_space_spec,
        scf_options=scf_options,
        orq_workspace_id=orq_workspace_id,
        mlflow_experiment_name=mlflow_experiment_name,
    )
    molecular_data.n_orbitals = int(molecule.nao)
    molecular_data.n_qubits = 2 * molecular_data.n_orbitals
    molecular_data.nuclear_repulsion = float(molecule.energy_nuc())

    molecular_data.hf_energy = float(mean_field_object.e_tot)

    molecular_data._pyscf_data = {  # type: ignore
        "mol": molecule,
        "scf": mean_field_object,
    }

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


class MolecularHamiltonianGenerator:
    """Class for generating molecular Hamiltonians.

    A class for generating a fermionic Hamiltonian for a given molecular geometry and
    choice of active space. Note that the active space can be specified in one of the
    following ways:

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

    To log PySCF progress after each SCF cycle to MLflow, set mlflow_experiment_name and
    orq_workspace_id. The workspace must have MLflow enabled, and you must be either
    logged in to the cluster or running a remote workflow on the cluster. See the
    `Orquestra documentation <https://docs.orquestra.io/>`_ for more information. Also
    note that scf_options must not have a "callback" key if mlflow_experiment_name and
    orq_workspace_id are set.


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
        scf_options: dictionary with parameters for PySCF calculations.
        mlflow_experiment_name: The name of the MLflow experiment to log PySCF progress
            to. If a value is provided, then orq_workspace_id also must be provided.
        orq_workspace_id: The ID of the Orquestra workspace to log PySCF progress to.
            If a value is provided, then mlflow_experiment_name also must be provided.
    """

    mol_spec: MoleculeSpecification
    active_space_spec: ActiveSpaceSpecification
    scf_options: Optional[Dict[str, Any]]
    mlflow_experiment_name: Optional[str]
    orq_workspace_id: Optional[str]

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
        self.scf_options = scf_options
        self.mlflow_experiment_name = mlflow_experiment_name
        self.orq_workspace_id = orq_workspace_id

    def get_pyscf_molecule(self) -> gto.Mole:
        return _get_pyscf_molecule(self.mol_spec)

    def get_active_space_hamiltonian(self) -> openfermion.InteractionOperator:
        return get_active_space_hamiltonian(
            mol_spec=self.mol_spec,
            active_space_spec=self.active_space_spec,
            scf_options=self.scf_options,
            mlflow_experiment_name=self.mlflow_experiment_name,
            orq_workspace_id=self.orq_workspace_id,
        )

    def get_active_space_meanfield_object(self) -> scf.hf.SCF:
        return get_active_space_meanfield_object(
            mol_spec=self.mol_spec,
            active_space_spec=self.active_space_spec,
            scf_options=self.scf_options,
            mlflow_experiment_name=self.mlflow_experiment_name,
            orq_workspace_id=self.orq_workspace_id,
        )
