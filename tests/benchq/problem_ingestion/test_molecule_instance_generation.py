import pytest

from benchq.problem_ingestion.molecule_instance_generation import (
    ChemistryApplicationInstance,
    generate_hydrogen_chain_instance,
)


@pytest.mark.parametrize(
    "instance,expected_number_of_qubits",
    [
        (generate_hydrogen_chain_instance(1), 2 * 2 * 1),
        (generate_hydrogen_chain_instance(2), 2 * 2 * 2),
        (generate_hydrogen_chain_instance(13, basis="STO-3G"), 2 * 1 * 13),
    ],
)
def test_hamiltonian_has_correct_number_of_qubits(
    instance: ChemistryApplicationInstance, expected_number_of_qubits: int
):
    hamiltonian = instance.get_active_space_hamiltonian()
    assert hamiltonian.n_qubits == expected_number_of_qubits


def test_get_active_space_hamiltonian_raises_error_for_unsupported_instance():
    instance = generate_hydrogen_chain_instance(2)
    instance.avas_atomic_orbitals = ["H 1s", "H 2s"]
    instance.avas_minao = "sto-3g"
    with pytest.raises(ValueError):
        instance.get_active_space_hamiltonian()


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
