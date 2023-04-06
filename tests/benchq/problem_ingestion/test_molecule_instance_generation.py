import pytest

from benchq.problem_ingestion.molecule_instance_generation import (
    ChemistryApplicationInstance,
    generate_hydrogen_chain_instance,
)


def _generate_avas_hydrogen_chain_instance(n_hydrogens):
    avas_hydrogen_chain_instance = generate_hydrogen_chain_instance(n_hydrogens)
    avas_hydrogen_chain_instance.avas_atomic_orbitals = ["H 1s"]
    avas_hydrogen_chain_instance.avas_minao = "sto-3g"
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
    instance = generate_hydrogen_chain_instance(number_of_hydrogens=number_of_hydrogens)
    instance.avas_atomic_orbitals = ["H 1s", "H 2s"]
    instance.avas_minao = "sto-3g"
    total_number_of_orbitals = 2 * number_of_hydrogens
    mean_field_object = instance.get_active_space_meanfield_object()
    assert mean_field_object.mo_coeff.shape[0] < total_number_of_orbitals
    assert mean_field_object.mo_coeff.shape[1] < total_number_of_orbitals


def test_get_active_space_meanfield_object_raises_error_for_unsupported_instance():
    instance = generate_hydrogen_chain_instance(2)
    instance.active_indices = [1, 2]
    instance.occupied_indices = [0]
    with pytest.raises(ValueError):
        instance.get_active_space_meanfield_object()


@pytest.fixture
def fno_water_instance():
    water_instance = ChemistryApplicationInstance(
        geometry=[
            ("O", (0.000000, -0.075791844, 0.000000)),
            ("H", (0.866811829, 0.601435779, 0.000000)),
            ("H", (-0.866811829, 0.601435779, 0.000000)),
        ],
        basis="6-31g",
        charge=0,
        multiplicity=1,
        fno_percentage_occupation_number=0.9,
    )

    yield water_instance


def test_get_occupied_and_active_indicies_with_FNO_frozen_core(fno_water_instance):
    fno_water_instance.freeze_core = True

    (
        molecular_data,
        occupied_indices,
        active_indicies,
    ) = fno_water_instance.get_occupied_and_active_indicies_with_FNO()

    assert len(occupied_indices) == 1
    assert len(active_indicies) < molecular_data.n_orbitals


def test_get_occupied_and_active_indicies_with_FNO_no_freeze_core(fno_water_instance):
    fno_water_instance.freeze_core = False

    (
        molecular_data,
        occupied_indices,
        active_indicies,
    ) = fno_water_instance.get_occupied_and_active_indicies_with_FNO()

    assert len(occupied_indices) == 0
    assert len(active_indicies) < molecular_data.n_orbitals


def test_get_occupied_and_active_indicies_with_FNO_no_virtual_frozen_orbitals(
    fno_water_instance,
):
    fno_water_instance.fno_percentage_occupation_number = 0.0

    (
        molecular_data,
        occupied_indices,
        active_indicies,
    ) = fno_water_instance.get_occupied_and_active_indicies_with_FNO()

    assert len(occupied_indices) == 0
    assert len(active_indicies) < molecular_data.n_orbitals
