import pytest

from benchq.problem_ingestion import (
    WATER_MOLECULE,
    ChemistryApplicationInstance,
    generate_hydrogen_chain_instance,
)


@pytest.mark.parametrize(
    "instance,expected_number_of_qubits",
    [
        (generate_hydrogen_chain_instance(1), 2 * 2 * 1),
        (generate_hydrogen_chain_instance(2), 2 * 2 * 2),
    ],
)
def test_hamiltonian_has_correct_number_of_qubits(
    instance: ChemistryApplicationInstance, expected_number_of_qubits: int
):
    hamiltonian = instance.get_active_space_hamiltonian()
    assert hamiltonian.n_qubits == expected_number_of_qubits


@pytest.mark.parametrize(
    "instance,max_number_of_orbitals",
    [
        (WATER_MOLECULE, 2 * 2 + 1 + 3 * 2),
    ],
)
def test_active_space_mean_field_object_has_valid_number_of_orbitals(
    instance: ChemistryApplicationInstance, max_number_of_orbitals: int
):
    mean_field_object = instance.get_active_space_meanfield_object()
    assert mean_field_object.mo_coeff.shape[0] <= max_number_of_orbitals
    assert mean_field_object.mo_coeff.shape[1] <= max_number_of_orbitals
