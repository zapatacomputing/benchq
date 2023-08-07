from functools import wraps
from typing import Optional
from unittest.mock import ANY, MagicMock, patch

import pytest
from mlflow import MlflowClient

from benchq.mlflow import create_mlflow_scf_callback
from benchq.problem_ingestion.molecule_instance_generation import (
    ChemistryApplicationInstance,
    SCFConvergenceError,
    generate_hydrogen_chain_instance,
)


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
    scf_options = None,
    mlflow_experiment_name = None,
    orq_workspace_id = None,
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
        scf_options=scf_options,
        mlflow_experiment_name=mlflow_experiment_name,
        orq_workspace_id=orq_workspace_id,
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


def apply_sdk_patches(func):
    @wraps(func)
    @patch(
        "benchq.problem_ingestion.molecule_instance_generation"
        ".sdk.mlflow.get_tracking_token",
        autospec=True,
        return_value="fake",
    )
    @patch(
        "benchq.problem_ingestion.molecule_instance_generation"
        ".sdk.mlflow.get_tracking_uri",
        autospec=True,
        return_value=None,
    )
    def _(*args, **kwargs):
        return func(*args, **kwargs)

    return _


@patch(
    "benchq.problem_ingestion.molecule_instance_generation.MlflowClient.log_param",
    autospec=True,
)
@patch(
    "benchq.problem_ingestion.molecule_instance_generation.MlflowClient.log_metric",
    autospec=True,
)
@apply_sdk_patches
def test_get_active_space_hamiltonian_logs_to_mlflow_no_specified_callback(
    mock_uri_function,
    mock_token_function,
    mock_log_metric,
    mock_log_param,
):
    # Given
    new_hydrogen_chain_instance = generate_hydrogen_chain_instance(
        2, mlflow_experiment_name="pytest"
    )

    # When
    _ = new_hydrogen_chain_instance.get_active_space_hamiltonian()

    # Then
    mock_log_param.assert_called()
    mock_log_metric.assert_called()

    mock_log_param.assert_any_call(
        ANY,  # First param is "self" which in this case is MlflowClient object
        ANY,  # Second param is random run_id
        "geometry",  # key
        [("H", (0, 0, 0.0)), ("H", (0, 0, 1.3))],  # val
    )
    mock_log_param.assert_any_call(ANY, ANY, "basis", "6-31g")

    # last param (value) depends on optimization, so could be different run-to-run
    mock_log_metric.assert_any_call(ANY, ANY, "last_hf_e", ANY)
    mock_log_metric.assert_any_call(ANY, ANY, "cput0_0", ANY)


@patch("mlflow.MlflowClient", autospec=True)
@apply_sdk_patches
def test_get_active_space_hamiltonian_logs_to_mlflow_with_specified_callback(
    mock_uri_function,
    mock_token_function,
    mock_client,
):
    # Given
    experiment_name = mock_client.create_experiment(
        "test_get_active_space_hamiltonian_logs_to_mlflow_with_specified_callback",
    )
    experiment = mock_client.get_experiment_by_name(name=experiment_name)
    run_id = mock_client.create_run(experiment.experiment_id).info.run_id
    scf_callback = create_mlflow_scf_callback(mock_client, run_id)
    scf_options = {"callback": scf_callback}
    new_hydrogen_chain_instance = generate_hydrogen_chain_instance(
        2,
        mlflow_experiment_name="pytest",
        scf_options=scf_options,
        orq_workspace_id="mlflow-benchq-testing-dd0cb1",
    )

    # When
    _ = new_hydrogen_chain_instance.get_active_space_hamiltonian()

    # Then
    mock_client.log_metric.assert_called()

    # last param (value) depends on optimization, so could be different run-to-run
    mock_client.log_metric.assert_any_call(ANY, "last_hf_e", ANY)
    mock_client.log_metric.assert_any_call(ANY, "cput0_0", ANY)


@patch(
    "benchq.problem_ingestion.molecule_instance_generation.MlflowClient.log_param",
    autospec=True,
)
@patch(
    "benchq.problem_ingestion.molecule_instance_generation.MlflowClient.log_metric",
    autospec=True,
)
@apply_sdk_patches
def test_get_active_space_hamiltonian_logs_to_mlflow_with_scf_options_no_callback(
    mock_uri_function,
    mock_token_function,
    mock_log_metric,
    mock_log_param,
):
    # Given
    new_hydrogen_chain_instance = generate_hydrogen_chain_instance(
        2,
        mlflow_experiment_name="pytest",
        scf_options={"max_cycle": 100},
    )

    # When
    _ = new_hydrogen_chain_instance.get_active_space_hamiltonian()

    # Then
    mock_log_param.assert_called()
    mock_log_metric.assert_called()

    mock_log_param.assert_any_call(
        ANY,  # First param is "self" which in this case is MlflowClient object
        ANY,  # Second param is random run_id
        "geometry",  # key
        [("H", (0, 0, 0.0)), ("H", (0, 0, 1.3))],  # val
    )
    mock_log_param.assert_any_call(ANY, ANY, "basis", "6-31g")

    # last param (value) depends on optimization, so could be different run-to-run
    mock_log_metric.assert_any_call(ANY, ANY, "last_hf_e", ANY)
    mock_log_metric.assert_any_call(ANY, ANY, "cput0_0", ANY)


@patch(
    "benchq.problem_ingestion.molecule_instance_generation.MlflowClient.log_param",
    autospec=True,
)
@patch(
    "benchq.problem_ingestion.molecule_instance_generation.MlflowClient.log_metric",
    autospec=True,
)
@apply_sdk_patches
def test_get_occupied_and_active_indicies_with_FNO_logs_to_mlflow_no_specified_callback(
    mock_uri_function,
    mock_token_function,
    mock_log_metric,
    mock_log_param,
):
    # Given
    fno_water_instance_frozen_core = _fno_water_instance(
        freeze_core=True, mlflow_experiment_name="pytest"
    )

    # When
    (
        molecular_data,
        occupied_indices,
        active_indicies,
    ) = fno_water_instance_frozen_core.get_occupied_and_active_indicies_with_FNO()

    # Then
    mock_log_param.assert_called()
    mock_log_metric.assert_called()

    mock_log_param.assert_any_call(
        ANY,  # First param is "self" which in this case is MlflowClient object
        ANY,  # Second param is random run_id
        "geometry",  # key
        [
            ("O", (0.0, -0.075791844, 0.0)),
            ("H", (0.866811829, 0.601435779, 0.0)),
            ("H", (-0.866811829, 0.601435779, 0.0)),
        ],  # val
    )
    mock_log_param.assert_any_call(ANY, ANY, "basis", "6-31g")

    # last param (value) depends on optimization, so could be different run-to-run
    mock_log_metric.assert_any_call(ANY, ANY, "last_hf_e", ANY)
    mock_log_metric.assert_any_call(ANY, ANY, "cput0_0", ANY)


@patch("mlflow.MlflowClient", autospec=True)
@apply_sdk_patches
def test_get_occupied_and_active_indicies_w_FNO_log_to_mlflow_w_given_callback(
    mock_uri_function,
    mock_token_function,
    mock_client,
):
    # Given
    experiment_name = mock_client.create_experiment(
        "test_get_occupied_and_active_indicies_w_FNO_log_to_mlflow_w_given_callback",
    )
    experiment = mock_client.get_experiment_by_name(name=experiment_name)
    run_id = mock_client.create_run(experiment.experiment_id).info.run_id
    scf_callback = create_mlflow_scf_callback(mock_client, run_id)
    scf_options = {"callback": scf_callback}
    fno_water_instance_frozen_core = _fno_water_instance(
        freeze_core=True,
        scf_options=scf_options,
        orq_workspace_id="mlflow-benchq-testing-dd0cb1",
    )

    # When
    (
        molecular_data,
        occupied_indices,
        active_indicies,
    ) = fno_water_instance_frozen_core.get_occupied_and_active_indicies_with_FNO()

    # Then
    mock_client.log_metric.assert_called()

    # last param (value) depends on optimization, so could be different run-to-run
    mock_client.log_metric.assert_any_call(ANY, "last_hf_e", ANY)
    mock_client.log_metric.assert_any_call(ANY, "cput0_0", ANY)


@patch(
    "benchq.problem_ingestion.molecule_instance_generation.MlflowClient.log_param",
    autospec=True,
)
@patch(
    "benchq.problem_ingestion.molecule_instance_generation.MlflowClient.log_metric",
    autospec=True,
)
@apply_sdk_patches
def test_get_occupied_and_active_indicies_with_FNO_log_mlflow_w_scf_opt_no_callback(
    mock_uri_function,
    mock_token_function,
    mock_log_metric,
    mock_log_param,
):
    # Given
    fno_water_instance_frozen_core = _fno_water_instance(
        freeze_core=True,
        mlflow_experiment_name="pytest",
        scf_options={"max_cycle": 100},
    )

    # When
    (
        molecular_data,
        occupied_indices,
        active_indicies,
    ) = fno_water_instance_frozen_core.get_occupied_and_active_indicies_with_FNO()

    # Then
    mock_log_param.assert_called()
    mock_log_metric.assert_called()

    mock_log_param.assert_any_call(
        ANY,  # First param is "self" which in this case is MlflowClient object
        ANY,  # Second param is random run_id
        "geometry",  # key
        [
            ("O", (0.0, -0.075791844, 0.0)),
            ("H", (0.866811829, 0.601435779, 0.0)),
            ("H", (-0.866811829, 0.601435779, 0.0)),
        ],  # val
    )
    mock_log_param.assert_any_call(ANY, ANY, "basis", "6-31g")

    # last param (value) depends on optimization, so could be different run-to-run
    mock_log_metric.assert_any_call(ANY, ANY, "last_hf_e", ANY)
    mock_log_metric.assert_any_call(ANY, ANY, "cput0_0", ANY)


@patch(
    "benchq.problem_ingestion.molecule_instance_generation.MlflowClient.log_param",
    autospec=True,
)
@patch(
    "benchq.problem_ingestion.molecule_instance_generation.MlflowClient.log_metric",
    autospec=True,
)
@apply_sdk_patches
def test_get_active_space_meanfield_object_logs_to_mlflow_no_specified_callback(
    mock_uri_function,
    mock_token_function,
    mock_log_metric,
    mock_log_param,
):
    # Given
    new_hydrogen_chain_instance = generate_hydrogen_chain_instance(
        2, mlflow_experiment_name="pytest"
    )

    # When
    _ = new_hydrogen_chain_instance.get_active_space_meanfield_object()

    # Then
    mock_log_param.assert_called()
    mock_log_metric.assert_called()

    mock_log_param.assert_any_call(
        ANY,  # First param is "self" which in this case is MlflowClient object
        ANY,  # Second param is random run_id
        "geometry",  # key
        [("H", (0, 0, 0.0)), ("H", (0, 0, 1.3))],  # val
    )
    mock_log_param.assert_any_call(ANY, ANY, "basis", "6-31g")

    # last param (value) depends on optimization, so could be different run-to-run
    mock_log_metric.assert_any_call(ANY, ANY, "last_hf_e", ANY)
    mock_log_metric.assert_any_call(ANY, ANY, "cput0_0", ANY)


@patch("mlflow.MlflowClient", autospec=True)
@apply_sdk_patches
def test_get_active_space_meanfield_object_logs_to_mlflow_with_specified_callback(
    mock_uri_function,
    mock_token_function,
    mock_client,
):
    # Given
    experiment_name = mock_client.create_experiment(
        "test_get_active_space_hamiltonian_logs_to_mlflow_with_specified_callback",
    )
    experiment = mock_client.get_experiment_by_name(name=experiment_name)
    run_id = mock_client.create_run(experiment.experiment_id).info.run_id
    scf_callback = create_mlflow_scf_callback(mock_client, run_id)
    scf_options = {"callback": scf_callback}
    new_hydrogen_chain_instance = generate_hydrogen_chain_instance(
        2,
        mlflow_experiment_name="pytest",
        scf_options=scf_options,
        orq_workspace_id="mlflow-benchq-testing-dd0cb1",
    )

    # When
    _ = new_hydrogen_chain_instance.get_active_space_meanfield_object()

    # Then
    mock_client.log_metric.assert_called()

    # last param (value) depends on optimization, so could be different run-to-run
    mock_client.log_metric.assert_any_call(ANY, "last_hf_e", ANY)
    mock_client.log_metric.assert_any_call(ANY, "cput0_0", ANY)


@patch(
    "benchq.problem_ingestion.molecule_instance_generation.MlflowClient.log_param",
    autospec=True,
)
@patch(
    "benchq.problem_ingestion.molecule_instance_generation.MlflowClient.log_metric",
    autospec=True,
)
@apply_sdk_patches
def test_get_active_space_meanfield_object_logs_to_mlflow_with_scf_options_no_callback(
    mock_uri_function,
    mock_token_function,
    mock_log_metric,
    mock_log_param,
):
    # Given
    new_hydrogen_chain_instance = generate_hydrogen_chain_instance(
        2,
        mlflow_experiment_name="pytest",
        scf_options={"max_cycle": 100},
    )

    # When
    _ = new_hydrogen_chain_instance.get_active_space_meanfield_object()

    # Then
    mock_log_param.assert_called()
    mock_log_metric.assert_called()

    mock_log_param.assert_any_call(
        ANY,  # First param is "self" which in this case is MlflowClient object
        ANY,  # Second param is random run_id
        "geometry",  # key
        [("H", (0, 0, 0.0)), ("H", (0, 0, 1.3))],  # val
    )
    mock_log_param.assert_any_call(ANY, ANY, "basis", "6-31g")

    # last param (value) depends on optimization, so could be different run-to-run
    mock_log_metric.assert_any_call(ANY, ANY, "last_hf_e", ANY)
    mock_log_metric.assert_any_call(ANY, ANY, "cput0_0", ANY)
