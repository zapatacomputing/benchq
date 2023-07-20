import datetime

import numpy
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
    physical_error_rate = 1.0e-4
    resource_estimate = get_physical_cost(
        num_toffoli=n_toffoli,
        num_logical_qubits=n_logical_qubits,
        physical_error_rate=physical_error_rate,
    )
    assert resource_estimate.n_physical_qubits > n_logical_qubits


@pytest.mark.parametrize(
    "SCC_time_low,SCC_time_high",
    [
        (datetime.timedelta(seconds=0.000001), datetime.timedelta(seconds=0.000008)),
        (datetime.timedelta(seconds=0.000004), datetime.timedelta(seconds=0.000009)),
        (datetime.timedelta(seconds=0.000001), datetime.timedelta(seconds=0.000009)),
        (datetime.timedelta(seconds=0.000005), datetime.timedelta(seconds=0.000010)),
    ],
)
def test_monotonicity_of_duration_wrt_SCC_time(SCC_time_low, SCC_time_high):
    n_toffoli = 100
    n_logical_qubits = 100
    physical_error_rate = 1.0e-4
    resource_estimates_low = get_physical_cost(
        num_toffoli=n_toffoli,
        num_logical_qubits=n_logical_qubits,
        surface_code_cycle_time=SCC_time_low,
        physical_error_rate=physical_error_rate,
    )
    resource_estimates_high = get_physical_cost(
        num_toffoli=n_toffoli,
        num_logical_qubits=n_logical_qubits,
        surface_code_cycle_time=SCC_time_high,
        physical_error_rate=physical_error_rate,
    )
    assert (
        resource_estimates_high.total_time_in_seconds
        > resource_estimates_low.total_time_in_seconds
    )


@pytest.mark.parametrize(
    "SCC_time_low,SCC_time_high",
    [
        (datetime.timedelta(microseconds=1), datetime.timedelta(microseconds=8)),
        (datetime.timedelta(microseconds=4), datetime.timedelta(microseconds=9)),
        (datetime.timedelta(microseconds=1), datetime.timedelta(microseconds=9)),
        (datetime.timedelta(microseconds=5), datetime.timedelta(microseconds=10)),
    ],
)
def test_linearity_of_duration_wrt_SCC_time(SCC_time_low, SCC_time_high):
    n_toffoli = 100
    n_logical_qubits = 100
    physical_error_rate = 1.0e-4
    resource_estimates_low = get_physical_cost(
        num_toffoli=n_toffoli,
        num_logical_qubits=n_logical_qubits,
        surface_code_cycle_time=SCC_time_low,
        physical_error_rate=physical_error_rate,
    )
    resource_estimates_high = get_physical_cost(
        num_toffoli=n_toffoli,
        num_logical_qubits=n_logical_qubits,
        surface_code_cycle_time=SCC_time_high,
        physical_error_rate=physical_error_rate,
    )

    numpy.testing.assert_allclose(
        resource_estimates_high.total_time_in_seconds / SCC_time_high.total_seconds(),
        resource_estimates_low.total_time_in_seconds / SCC_time_low.total_seconds(),
    )


@pytest.mark.parametrize(
    "num_toffoli,num_T",
    [
        (20, 20),
        (40, 40),
        (20, 30),
    ],
)
def test_ratio_of_failure_prob(num_toffoli, num_T):
    num_logical_qubits = 12
    SCC_time = datetime.timedelta(microseconds=2)
    physical_error_rate = 1.0e-4
    best_toffoli = get_physical_cost(
        num_logical_qubits=num_logical_qubits,
        num_toffoli=num_toffoli,
        surface_code_cycle_time=SCC_time,
        physical_error_rate=physical_error_rate,
    )
    best_T = get_physical_cost(
        num_logical_qubits=num_logical_qubits,
        num_T=num_T,
        surface_code_cycle_time=SCC_time,
        physical_error_rate=physical_error_rate,
    )
    """
    This ascertains if ratio of failure rate of Toffoli
    and T Magic State factories is 2:1
    """
    assert best_toffoli.extra.failure_prob / best_T.extra.failure_prob == 2.0


@pytest.mark.parametrize(
    "n_toffoli,n_T",
    [
        (20, 20),
        (40, 40),
    ],
)
def test_calc_of_Algorithm_Failure_Prob(n_toffoli, n_T):
    num_logical_qubits = 12
    SCC_time = datetime.timedelta(microseconds=2)
    physical_error_rate = 1.0e-4
    best_toffoli = get_physical_cost(
        num_logical_qubits=num_logical_qubits,
        num_toffoli=n_toffoli,
        surface_code_cycle_time=SCC_time,
        physical_error_rate=physical_error_rate,
    )
    best_T = get_physical_cost(
        num_logical_qubits=num_logical_qubits,
        num_T=n_T,
        surface_code_cycle_time=SCC_time,
        physical_error_rate=physical_error_rate,
    )
    """
    X+Yf - (X+Yf/2) = Yf/2, where X+Yf and X+Yf/2 are
    Algorithm Failure Prob for Toffoli and T cases respectively,
    where X -> data failure, Yf -> distillation
    failure, Y=#Toffoli gate=#T gates and f is 1 CCZ error.
    If failure rate is calculated correctly,
    to ascertain if Algorithm Failure Probability is calculated correctly
    for both toffoli and T.
    """

    numpy.testing.assert_almost_equal(
        2 * (best_toffoli.logical_error_rate - best_T.logical_error_rate) / n_toffoli,
        best_toffoli.extra.failure_prob,
    )

    numpy.testing.assert_almost_equal(
        (best_toffoli.logical_error_rate - best_T.logical_error_rate) / n_T,
        best_T.extra.failure_prob,
    )


def test_default_T_factories():
    num_logical_qubits = 12
    SCC_time = datetime.timedelta(microseconds=2)
    physical_error_rate = 1.0e-3
    # Default Magic State Factory details
    # used based on this physical error rate.
    num_T = 200
    num_toffoli = 140
    best_T = get_physical_cost(
        num_logical_qubits=num_logical_qubits,
        num_T=num_T,
        surface_code_cycle_time=SCC_time,
        physical_error_rate=physical_error_rate,
    )
    best_toffoli = get_physical_cost(
        num_logical_qubits=num_logical_qubits,
        num_toffoli=num_toffoli,
        surface_code_cycle_time=SCC_time,
        physical_error_rate=physical_error_rate,
    )
    assert (
        best_T.extra.rounds == 186
        and best_T.extra.failure_prob == 3.6000000000000003e-16
    )
    assert (
        best_toffoli.extra.rounds == 186
        and best_toffoli.extra.failure_prob == 3.6000000000000003e-16
    )


def test_default_values():
    num_logical_qubits = 12
    physical_error_rate = 1.0e-4
    """
    If physical_error_rate != default value,
    this ascertains if both num_T=0 and num_toffoli=0,
    then it must throw an error.
    """
    with pytest.raises(SystemExit) as dvalue:
        a, b = get_physical_cost(
            num_logical_qubits=num_logical_qubits,
            physical_error_rate=physical_error_rate,
        )

    assert dvalue.type == SystemExit
    assert dvalue.value.code == 1


def test_all_default_values():
    num_logical_qubits = 12
    """
    If physical_error_rate == default value,
    this ascertains if both num_T=0 and num_toffoli=0,
    then it must throw an error.
    """
    with pytest.raises(SystemExit) as dvalue:
        a, b = get_physical_cost(
            num_logical_qubits=num_logical_qubits,
        )

    assert dvalue.type == SystemExit
    assert dvalue.value.code == 1
