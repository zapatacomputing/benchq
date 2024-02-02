from typing import Optional
from unittest.mock import ANY, patch

import pytest

from benchq.mlflow.data_logging import create_mlflow_scf_callback
from benchq.problem_ingestion.molecular_hamiltonians import (
    MolecularHamiltonianGenerator,
    SCFConvergenceError,
    get_hydrogen_chain_hamiltonian_generator,
)
from benchq.problem_ingestion.molecular_hamiltonians._hamiltonian_generation import (
    _get_molecular_data,
)


def _generate_avas_hydrogen_chain_instance(n_hydrogens):
    avas_hydrogen_chain_instance = get_hydrogen_chain_hamiltonian_generator(
        n_hydrogens,
        avas_atomic_orbitals=["H 1s"],
        avas_minao="sto-3g",
    )
    return avas_hydrogen_chain_instance


@pytest.mark.parametrize(
    "instance,expected_number_of_qubits",
    [
        (get_hydrogen_chain_hamiltonian_generator(2), 2 * 2 * 2),
        (get_hydrogen_chain_hamiltonian_generator(13, basis="STO-3G"), 2 * 1 * 13),
        (_generate_avas_hydrogen_chain_instance(2), 4),
    ],
)
def test_hamiltonian_has_correct_number_of_qubits(
    instance: MolecularHamiltonianGenerator, expected_number_of_qubits: int
):
    hamiltonian = instance.get_active_space_hamiltonian()
    assert hamiltonian.n_qubits == expected_number_of_qubits


def test_active_space_mean_field_object_has_valid_number_of_orbitals_with_avas_():
    number_of_hydrogens = 2
    instance = get_hydrogen_chain_hamiltonian_generator(
        number_of_hydrogens=number_of_hydrogens,
        avas_atomic_orbitals=["H 1s", "H 2s"],
        avas_minao="sto-3g",
    )
    total_number_of_orbitals = 2 * number_of_hydrogens
    mean_field_object = instance.get_active_space_meanfield_object()
    assert mean_field_object.mo_coeff.shape[0] < total_number_of_orbitals
    assert mean_field_object.mo_coeff.shape[1] < total_number_of_orbitals


def test_get_active_space_meanfield_object_raises_error_for_unsupported_instance():
    instance = get_hydrogen_chain_hamiltonian_generator(
        2,
        active_indices=[1, 2],
        occupied_indices=[0],
    )
    with pytest.raises(ValueError):
        instance.get_active_space_meanfield_object()


def test_mean_field_object_has_valid_scf_options():
    instance = get_hydrogen_chain_hamiltonian_generator(
        2, scf_options={"conv_tol": 1e-08, "level_shift": 0.4}
    )
    mean_field_object = instance.get_active_space_meanfield_object()
    assert mean_field_object.conv_tol == 1e-08
    assert mean_field_object.level_shift == 0.4


def test_mean_field_object_has_valid_default_scf_options():
    instance = get_hydrogen_chain_hamiltonian_generator(2)
    mean_field_object = instance.get_active_space_meanfield_object()
    assert mean_field_object.conv_tol == 1e-09
    assert mean_field_object.level_shift == 0


def _water_instance(
    freeze_core: Optional[bool] = None,
    fno_percentage_occupation_number=None,
    scf_options=None,
    mlflow_experiment_name=None,
    orq_workspace_id=None,
):
    water_instance = MolecularHamiltonianGenerator(
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


def test_get_molecular_data_with_FNO_frozen_core():
    standard_water_instance = _water_instance()
    n_orbitals_no_fno_no_fzc = _get_molecular_data(
        standard_water_instance.mol_spec, standard_water_instance.active_space_spec
    ).n_orbitals

    fno_water_instance = _water_instance(fno_percentage_occupation_number=0.9)
    fno_water_instance.freeze_core = True

    molecular_data = _get_molecular_data(
        fno_water_instance.mol_spec, fno_water_instance.active_space_spec
    )

    assert molecular_data.n_orbitals < n_orbitals_no_fno_no_fzc


def test_get_molecular_data_with_fno_no_frozen_core():
    standard_water_instance = _water_instance()
    n_orbitals_no_fno_no_fzc = _get_molecular_data(
        standard_water_instance.mol_spec, standard_water_instance.active_space_spec
    ).n_orbitals

    fno_water_instance = _water_instance(fno_percentage_occupation_number=0.9)
    molecular_data = _get_molecular_data(
        fno_water_instance.mol_spec, fno_water_instance.active_space_spec
    )

    assert molecular_data.n_orbitals < n_orbitals_no_fno_no_fzc


@pytest.mark.parametrize(
    "method", ["get_active_space_meanfield_object", "get_active_space_hamiltonian"]
)
def test_get_active_space_meanfield_object_raises_scf_convergence_error(method):
    instance = get_hydrogen_chain_hamiltonian_generator(2, scf_options={"max_cycle": 1})
    with pytest.raises(SCFConvergenceError):
        getattr(instance, method)()

SRC = "benchq.problem_ingestion.molecular_hamiltonians._hamiltonian_generation"

@pytest.fixture
def patch_sdk_token():
    with patch(
        SRC,
        "sdk.mlflow.get_tracking_token",
        autospec=True,
        return_value="fake",
    ) as patched_token:
        yield patched_token


@pytest.fixture
def patch_sdk_uri():
    with patch(
        SRC,
        "sdk.mlflow.get_tracking_uri",
        autospec=True,
        return_value=None,
    ) as patched_uri:
        yield patched_uri


@pytest.fixture
def patch_log_metric():
    with patch(
        SRC,
        "MlflowClient.log_metric",
        autospec=True,
    ) as patched_log_metric:
        yield patched_log_metric


@pytest.fixture
def patch_log_param():
    with patch(
        SRC,
        "MlflowClient.log_param",
        autospec=True,
    ) as patched_log_param:
        yield patched_log_param


@pytest.fixture
def patch_local_client():
    with patch("mlflow.MlflowClient", autospec=True) as patched_client:
        yield patched_client


def stop_all(list_of_mocks):
    for mock in list_of_mocks:
        mock.stop()


def test_get_active_space_hamiltonian_logs_to_mlflow_no_specified_callback(
    patch_log_metric,
    patch_log_param,
    patch_sdk_token,
    patch_sdk_uri,
):
    # Given
    new_hydrogen_chain_instance = get_hydrogen_chain_hamiltonian_generator(
        2,
        mlflow_experiment_name="pytest",
        orq_workspace_id="testing",
    )

    # When
    _ = new_hydrogen_chain_instance.get_active_space_hamiltonian()

    # Then
    patch_log_param.assert_called()
    patch_log_metric.assert_called()

    patch_log_param.assert_any_call(
        ANY,  # First param is "self" which in this case is MlflowClient object
        ANY,  # Second param is random run_id
        "geometry",  # key
        [("H", (0, 0, 0.0)), ("H", (0, 0, 1.3))],  # val
    )
    patch_log_param.assert_any_call(ANY, ANY, "basis", "6-31g")

    # last param (value) depends on optimization, so could be different run-to-run
    patch_log_metric.assert_any_call(ANY, ANY, "last_hf_e", ANY)
    patch_log_metric.assert_any_call(ANY, ANY, "cput0_0", ANY)


def test_get_active_space_hamiltonian_logs_to_mlflow_with_specified_callback(
    patch_sdk_token,
    patch_sdk_uri,
    patch_local_client,
):
    # Given
    experiment_name = patch_local_client.create_experiment(
        "test_get_active_space_hamiltonian_logs_to_mlflow_with_specified_callback",
    )
    experiment = patch_local_client.get_experiment_by_name(name=experiment_name)
    run_id = patch_local_client.create_run(experiment.experiment_id).info.run_id
    scf_callback = create_mlflow_scf_callback(patch_local_client, run_id)
    scf_options = {"callback": scf_callback}
    new_hydrogen_chain_instance = get_hydrogen_chain_hamiltonian_generator(
        2,
        mlflow_experiment_name="pytest",
        scf_options=scf_options,
        orq_workspace_id="testing",
    )

    # When
    _ = new_hydrogen_chain_instance.get_active_space_hamiltonian()

    # Then
    patch_local_client.log_metric.assert_called()

    # last param (value) depends on optimization, so could be different run-to-run
    patch_local_client.log_metric.assert_any_call(ANY, "last_hf_e", ANY)
    patch_local_client.log_metric.assert_any_call(ANY, "cput0_0", ANY)


def test_get_active_space_hamiltonian_logs_to_mlflow_with_scf_options_no_callback(
    patch_log_metric,
    patch_log_param,
    patch_sdk_token,
    patch_sdk_uri,
):
    # Given
    new_hydrogen_chain_instance = get_hydrogen_chain_hamiltonian_generator(
        2,
        mlflow_experiment_name="pytest",
        orq_workspace_id="testing",
        scf_options={"max_cycle": 100},
    )

    # When
    _ = new_hydrogen_chain_instance.get_active_space_hamiltonian()

    # Then
    patch_log_param.assert_called()
    patch_log_metric.assert_called()

    patch_log_param.assert_any_call(
        ANY,  # First param is "self" which in this case is MlflowClient object
        ANY,  # Second param is random run_id
        "geometry",  # key
        [("H", (0, 0, 0.0)), ("H", (0, 0, 1.3))],  # val
    )
    patch_log_param.assert_any_call(ANY, ANY, "basis", "6-31g")

    # last param (value) depends on optimization, so could be different run-to-run
    patch_log_metric.assert_any_call(ANY, ANY, "last_hf_e", ANY)
    patch_log_metric.assert_any_call(ANY, ANY, "cput0_0", ANY)


def test_get_active_space_meanfield_object_logs_to_mlflow_no_specified_callback(
    patch_log_metric,
    patch_log_param,
    patch_sdk_token,
    patch_sdk_uri,
):
    # Given
    new_hydrogen_chain_instance = get_hydrogen_chain_hamiltonian_generator(
        2,
        mlflow_experiment_name="pytest",
        orq_workspace_id="testing",
    )

    # When
    _ = new_hydrogen_chain_instance.get_active_space_meanfield_object()

    # Then
    patch_log_param.assert_called()
    patch_log_metric.assert_called()

    patch_log_param.assert_any_call(
        ANY,  # First param is "self" which in this case is MlflowClient object
        ANY,  # Second param is random run_id
        "geometry",  # key
        [("H", (0, 0, 0.0)), ("H", (0, 0, 1.3))],  # val
    )
    patch_log_param.assert_any_call(ANY, ANY, "basis", "6-31g")

    # last param (value) depends on optimization, so could be different run-to-run
    patch_log_metric.assert_any_call(ANY, ANY, "last_hf_e", ANY)
    patch_log_metric.assert_any_call(ANY, ANY, "cput0_0", ANY)


def test_get_active_space_meanfield_object_logs_to_mlflow_with_specified_callback(
    patch_sdk_token,
    patch_sdk_uri,
    patch_local_client,
):
    # Given
    experiment_name = patch_local_client.create_experiment(
        "test_get_active_space_hamiltonian_logs_to_mlflow_with_specified_callback",
    )
    experiment = patch_local_client.get_experiment_by_name(name=experiment_name)
    run_id = patch_local_client.create_run(experiment.experiment_id).info.run_id
    scf_callback = create_mlflow_scf_callback(patch_local_client, run_id)
    scf_options = {"callback": scf_callback}
    new_hydrogen_chain_instance = get_hydrogen_chain_hamiltonian_generator(
        2,
        mlflow_experiment_name="pytest",
        orq_workspace_id="testing",
        scf_options=scf_options,
    )

    # When
    _ = new_hydrogen_chain_instance.get_active_space_meanfield_object()

    # Then
    patch_local_client.log_metric.assert_called()

    # last param (value) depends on optimization, so could be different run-to-run
    patch_local_client.log_metric.assert_any_call(ANY, "last_hf_e", ANY)
    patch_local_client.log_metric.assert_any_call(ANY, "cput0_0", ANY)


def test_get_active_space_meanfield_object_logs_to_mlflow_with_scf_options_no_callback(
    patch_log_metric,
    patch_log_param,
    patch_sdk_token,
    patch_sdk_uri,
):
    # Given
    new_hydrogen_chain_instance = get_hydrogen_chain_hamiltonian_generator(
        2,
        mlflow_experiment_name="pytest",
        orq_workspace_id="testing",
        scf_options={"max_cycle": 100},
    )

    # When
    _ = new_hydrogen_chain_instance.get_active_space_meanfield_object()

    # Then
    patch_log_param.assert_called()
    patch_log_metric.assert_called()

    patch_log_param.assert_any_call(
        ANY,  # First param is "self" which in this case is MlflowClient object
        ANY,  # Second param is random run_id
        "geometry",  # key
        [("H", (0, 0, 0.0)), ("H", (0, 0, 1.3))],  # val
    )
    patch_log_param.assert_any_call(ANY, ANY, "basis", "6-31g")

    # last param (value) depends on optimization, so could be different run-to-run
    patch_log_metric.assert_any_call(ANY, ANY, "last_hf_e", ANY)
    patch_log_metric.assert_any_call(ANY, ANY, "cput0_0", ANY)
