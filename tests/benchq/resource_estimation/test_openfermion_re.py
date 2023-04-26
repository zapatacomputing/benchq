from benchq.resource_estimation import get_qpe_resource_estimates_from_mean_field_object
from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)
import pytest


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
    qpe_resource_estimates = get_qpe_resource_estimates_from_mean_field_object(
        mean_field_object
    )
    assert (
        qpe_resource_estimates["physical_qubit_count"]
        > 2 * mean_field_object._eri.shape[0]
    )
