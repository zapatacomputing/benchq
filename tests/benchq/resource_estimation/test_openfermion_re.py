import pytest
from openfermion.resource_estimates.molecule import pyscf_to_cas

from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)
from benchq.resource_estimation.openfermion_re import (
    get_double_factorized_qpe_toffoli_and_qubit_cost,
    get_physical_cost,
    get_single_factorized_qpe_toffoli_and_qubit_cost,
)


@pytest.mark.parametrize(
    "avas_atomic_orbitals,avas_minao",
    [
        (None, None),
        (["H 1s", "H 2s"], "sto-3g"),
    ],
)
def test_sf_qpe_logical_qubit_count_is_larger_than_number_of_spin_orbitals(
    avas_atomic_orbitals, avas_minao
):
    instance = generate_hydrogen_chain_instance(8)
    instance.avas_atomic_orbitals = avas_atomic_orbitals
    instance.avas_minao = avas_minao
    mean_field_object = instance.get_active_space_meanfield_object()
    h1, eri_full, _, _, _ = pyscf_to_cas(mean_field_object)

    num_toffoli, num_qubits = get_single_factorized_qpe_toffoli_and_qubit_cost(
        h1, eri_full, 20
    )
    assert num_qubits > 2 * eri_full.shape[0]


@pytest.mark.parametrize(
    "avas_atomic_orbitals,avas_minao",
    [
        (None, None),
        (["H 1s", "H 2s"], "sto-3g"),
    ],
)
def test_df_qpe_logical_qubit_count_is_larger_than_number_of_spin_orbitals(
    avas_atomic_orbitals, avas_minao
):
    instance = generate_hydrogen_chain_instance(8)
    instance.avas_atomic_orbitals = avas_atomic_orbitals
    instance.avas_minao = avas_minao
    mean_field_object = instance.get_active_space_meanfield_object()
    h1, eri_full, _, _, _ = pyscf_to_cas(mean_field_object)

    num_toffoli, num_qubits = get_double_factorized_qpe_toffoli_and_qubit_cost(
        h1, eri_full, 1e-6
    )
    assert num_qubits > 2 * eri_full.shape[0]


def _get_asymmetric_hamiltonian():
    instance = generate_hydrogen_chain_instance(8)
    instance.avas_atomic_orbitals = ["H 1s", "H 2s"]
    instance.avas_minao = "sto-3g"
    mean_field_object = instance.get_active_space_meanfield_object()
    h1, eri_full, _, _, _ = pyscf_to_cas(mean_field_object)
    eri_full[0, 1, 2, 3] += 0.1
    return h1, eri_full


def test_single_factorization_raises_exception_for_invalid_eri():
    h1, eri_full = _get_asymmetric_hamiltonian()
    with pytest.raises(ValueError):
        get_single_factorized_qpe_toffoli_and_qubit_cost(h1, eri_full, 20)


def test_double_factorization_raises_exception_for_invalid_eri():
    h1, eri_full = _get_asymmetric_hamiltonian()
    with pytest.raises(ValueError):
        get_double_factorized_qpe_toffoli_and_qubit_cost(h1, eri_full, 1e-6)


def test_physical_qubits_larger_than_logical_qubits():
    n_toffoli = 100
    n_logical_qubits = 100
    resource_estimate = get_physical_cost(n_toffoli, n_logical_qubits)
    assert resource_estimate.n_physical_qubits > n_logical_qubits
