import pytest
from openfermion.resource_estimates.molecule import pyscf_to_cas

from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)
from benchq.resource_estimation import get_single_factorized_qpe_resource_estimate


@pytest.mark.parametrize(
    "avas_atomic_orbitals,avas_minao",
    [
        (None, None),
        (["H 1s", "H 2s"], "sto-3g"),
    ],
)
def test_physical_qubit_count_is_larger_than_number_of_spin_orbitals(
    avas_atomic_orbitals, avas_minao
):
    instance = generate_hydrogen_chain_instance(8)
    instance.avas_atomic_orbitals = avas_atomic_orbitals
    instance.avas_minao = avas_minao
    mean_field_object = instance.get_active_space_meanfield_object()
    h1, eri_full, _, _, _ = pyscf_to_cas(mean_field_object)

    qpe_resource_estimates = get_single_factorized_qpe_resource_estimate(
        h1, eri_full, 20
    )
    assert (
        qpe_resource_estimates["physical_qubit_count"]
        > 2 * mean_field_object._eri.shape[0]
    )


def test_invalid_eri_raise_exception():
    instance = generate_hydrogen_chain_instance(8)
    instance.avas_atomic_orbitals = ["H 1s", "H 2s"]
    instance.avas_minao = "sto-3g"
    mean_field_object = instance.get_active_space_meanfield_object()
    h1, eri_full, _, _, _ = pyscf_to_cas(mean_field_object)
    eri_full[0, 1, 2, 3] += 0.1
    with pytest.raises(ValueError):
        get_single_factorized_qpe_resource_estimate(h1, eri_full, 20)
