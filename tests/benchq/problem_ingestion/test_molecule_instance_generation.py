import pytest

from unittest.mock import patch, ANY, MagicMock

from benchq.problem_ingestion.molecule_instance_generation import (
    ChemistryApplicationInstance,
    SCFConvergenceError,
    generate_hydrogen_chain_instance,
)
from benchq.mlflow import create_mlflow_scf_callback

from mlflow import MlflowClient


def _generate_avas_hydrogen_chain_instance(n_hydrogens):
    avas_hydrogen_chain_instance = generate_hydrogen_chain_instance(
        n_hydrogens,
        avas_atomic_orbitals=["H 1s"],
        avas_minao="sto-3g",
    )
    return avas_hydrogen_chain_instance


@pytest.mark.parametrize(
    "instance,expected_number_of_qubits",
    [
        (generate_hydrogen_chain_instance(2), 2 * 2 * 2),
        (generate_hydrogen_chain_instance(13, basis="STO-3G"), 2 * 1 * 13),
        (_generate_avas_hydrogen_chain_instance(2), 4),
    ],
)
def test_hamiltonian_has_correct_number_of_qubits(
    instance: ChemistryApplicationInstance, expected_number_of_qubits: int
):
    hamiltonian = instance.get_active_space_hamiltonian()
    assert hamiltonian.n_qubits == expected_number_of_qubits


def test_active_space_mean_field_object_has_valid_number_of_orbitals_with_avas_():
    number_of_hydrogens = 2
    instance = generate_hydrogen_chain_instance(
        number_of_hydrogens=number_of_hydrogens,
        avas_atomic_orbitals=["H 1s", "H 2s"],
        avas_minao="sto-3g",
    )
    total_number_of_orbitals = 2 * number_of_hydrogens
    mean_field_object = instance.get_active_space_meanfield_object()
    assert mean_field_object.mo_coeff.shape[0] < total_number_of_orbitals
    assert mean_field_object.mo_coeff.shape[1] < total_number_of_orbitals


def test_get_active_space_meanfield_object_raises_error_for_unsupported_instance():
    instance = generate_hydrogen_chain_instance(
        2,
        active_indices=[1, 2],
        occupied_indices=[0],
    )
    with pytest.raises(ValueError):
        instance.get_active_space_meanfield_object()


def test_mean_field_object_has_valid_scf_options():
    instance = generate_hydrogen_chain_instance(
        2, scf_options={"conv_tol": 1e-08, "level_shift": 0.4}
    )
    mean_field_object = instance.get_active_space_meanfield_object()
    assert mean_field_object.conv_tol == 1e-08
    assert mean_field_object.level_shift == 0.4


def test_mean_field_object_has_valid_default_scf_options():
    instance = generate_hydrogen_chain_instance(2)
    mean_field_object = instance.get_active_space_meanfield_object()
    assert mean_field_object.conv_tol == 1e-09
    assert mean_field_object.level_shift == 0


def _fno_water_instance(
    freeze_core: bool = None,
    fno_percentage_occupation_number: float = 0.9,
):
    water_instance = ChemistryApplicationInstance(
        geometry=[
            ("O", (0.000000, -0.075791844, 0.000000)),
            ("H", (0.866811829, 0.601435779, 0.000000)),
            ("H", (-0.866811829, 0.601435779, 0.000000)),
        ],
        basis="6-31g",
        charge=0,
        multiplicity=1,
        fno_percentage_occupation_number=fno_percentage_occupation_number,
        freeze_core=freeze_core,
    )

    return water_instance


def test_get_occupied_and_active_indicies_with_FNO_frozen_core():
    fno_water_instance_frozen_core = _fno_water_instance(freeze_core=True)
    (
        molecular_data,
        occupied_indices,
        active_indicies,
    ) = fno_water_instance_frozen_core.get_occupied_and_active_indicies_with_FNO()

    assert len(occupied_indices) == 1
    assert len(active_indicies) < molecular_data.n_orbitals


def test_get_occupied_and_active_indicies_with_FNO_no_freeze_core():
    fno_water_instance_thawed_core = _fno_water_instance(freeze_core=False)
    (
        molecular_data,
        occupied_indices,
        active_indicies,
    ) = fno_water_instance_thawed_core.get_occupied_and_active_indicies_with_FNO()

    assert len(occupied_indices) == 0
    assert len(active_indicies) < molecular_data.n_orbitals


def test_get_occupied_and_active_indicies_with_FNO_no_virtual_frozen_orbitals():
    fno_water_instance = _fno_water_instance(fno_percentage_occupation_number=0.0)

    (
        molecular_data,
        occupied_indices,
        active_indicies,
    ) = fno_water_instance.get_occupied_and_active_indicies_with_FNO()

    assert len(occupied_indices) == 0
    assert len(active_indicies) < molecular_data.n_orbitals


@pytest.mark.parametrize(
    "method", ["get_active_space_meanfield_object", "get_active_space_hamiltonian"]
)
def test_get_active_space_meanfield_object_raises_scf_convergence_error(method):
    instance = generate_hydrogen_chain_instance(2, scf_options={"max_cycle": 1})
    with pytest.raises(SCFConvergenceError):
        getattr(instance, method)()


@patch(
    "benchq.problem_ingestion.molecule_instance_generation.MlflowClient",
    autospec=True,
)
@patch(
    "benchq.problem_ingestion.molecule_instance_generation.sdk.mlflow.get_tracking_token",
    autospec=True,
    return_value="fake",
)
@patch(
    "benchq.problem_ingestion.molecule_instance_generation.sdk.mlflow.get_tracking_uri",
    autospec=True,
    return_value="fake",
)
def test_get_active_space_hamiltonian_logs_to_mlflow_no_specified_callback(
    mock_uri_function,
    mock_token_function,
    mock_client,
):
    # Given
    new_hydrogen_chain_instance = generate_hydrogen_chain_instance(
        2, mlflow_experiment_name="pytest"
    )

    mock_client.create_run = MagicMock()

    # When
    ham = new_hydrogen_chain_instance.get_active_space_hamiltonian()

    # Then
    mock_client.get_experiment_by_name.assert_called()
    mock_client.log_param.assert_called()
    mock_client.log_metric.assert_called()
    mock_client.log_metric.assert_any_call(ANY, "last_hf_e", 1.0)
