import pytest
from openfermion.resource_estimates.molecule import pyscf_to_cas

from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)
from benchq.resource_estimation import get_single_factorized_qpe_resource_estimate
import datetime


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
    print("Resource estimates:", qpe_resource_estimates.n_physical_qubits)
    assert (
        qpe_resource_estimates.n_physical_qubits > 2 * mean_field_object._eri.shape[0]
    )


@pytest.mark.parametrize(
    "SCC_time_low,SCC_time_high",
    [
        (datetime.timedelta(seconds=0.000001), datetime.timedelta(seconds=0.000008)),
        (datetime.timedelta(seconds=0.000004), datetime.timedelta(seconds=0.000009)),
        (datetime.timedelta(seconds=0.000004), datetime.timedelta(seconds=0.000009)),
        (datetime.timedelta(seconds=0.000005), datetime.timedelta(seconds=0.000010)),
    ],
)
def test_monotonicity_of_duration_wrt_SCC_time(SCC_time_low, SCC_time_high):
    instance = generate_hydrogen_chain_instance(8)
    instance.avas_atomic_orbitals = ["H 1s", "H 2s"]
    instance.avas_minao = "sto-3g"
    mean_field_object = instance.get_active_space_meanfield_object()
    h1, eri_full, _, _, _ = pyscf_to_cas(mean_field_object)

    qpe_resource_estimates_low = get_single_factorized_qpe_resource_estimate(
        h1, eri_full, 20, SCC_time_low
    )

    qpe_resource_estimates_high = get_single_factorized_qpe_resource_estimate(
        h1, eri_full, 20, SCC_time_high
    )

    # assert  (qpe_resource_estimates_low_1.total_time_in_seconds == qpe_resource_estimates_low_1.total_time_in_seconds)
    print(
        "High, low: ",
        qpe_resource_estimates_high.total_time_in_seconds,
        qpe_resource_estimates_low.total_time_in_seconds,
    )
    assert (
        qpe_resource_estimates_high.total_time_in_seconds
        > qpe_resource_estimates_low.total_time_in_seconds
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
