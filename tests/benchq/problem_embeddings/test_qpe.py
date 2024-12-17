import warnings

import numpy as np
import pytest

with warnings.catch_warnings():
    warnings.filterwarnings(
        "ignore",
        message="\n\n"
        "  `numpy.distutils` is deprecated since NumPy 1.23.0, as a result\n",
    )
    # openfermion throws deprecation warning thru pyscf and numpy
    # Could be fixed by using old setuptools, but there would be dependency conflict

    # We also need to disable GC for pyscf. It causes resources warnings
    import pyscf

    pyscf.gto.mole.DISABLE_GC = True

    from openfermion.resource_estimates.molecule import pyscf_to_cas

from benchq.problem_embeddings.qpe import (
    get_double_factorized_qpe_toffoli_and_qubit_cost,
    get_single_factorized_qpe_toffoli_and_qubit_cost,
)
from benchq.problem_ingestion.molecular_hamiltonians import (
    get_hydrogen_chain_hamiltonian_generator,
)
from benchq.quantum_hardware_modeling import BasicArchitectureModel
from benchq.resource_estimators.openfermion_estimator import openfermion_estimator


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
    instance = get_hydrogen_chain_hamiltonian_generator(8)
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
    instance = get_hydrogen_chain_hamiltonian_generator(8)
    instance.avas_atomic_orbitals = avas_atomic_orbitals
    instance.avas_minao = avas_minao
    mean_field_object = instance.get_active_space_meanfield_object()
    h1, eri_full, _, _, _ = pyscf_to_cas(mean_field_object)

    num_toffoli, num_qubits = get_double_factorized_qpe_toffoli_and_qubit_cost(
        h1, eri_full, 1e-6
    )
    assert num_qubits > 2 * eri_full.shape[0]


def _get_asymmetric_hamiltonian():
    instance = get_hydrogen_chain_hamiltonian_generator(8)
    instance.avas_atomic_orbitals = ["H 1s", "H 2s"]
    instance.avas_minao = "sto-3g"
    mean_field_object = instance.get_active_space_meanfield_object()
    h1, eri_full, _, _, _ = pyscf_to_cas(mean_field_object)
    eri_full[0, 1, 2, 3] += 0.1
    return h1, eri_full


def test_single_factorized_qpe_raises_exception_for_invalid_eri():
    h1, eri_full = _get_asymmetric_hamiltonian()
    with pytest.raises(ValueError):
        get_single_factorized_qpe_toffoli_and_qubit_cost(h1, eri_full, 20)


def test_double_factorized_qpe_raises_exception_for_invalid_eri():
    h1, eri_full = _get_asymmetric_hamiltonian()
    with pytest.raises(ValueError):
        get_double_factorized_qpe_toffoli_and_qubit_cost(h1, eri_full, 1e-6)


def test_physical_qubits_larger_than_logical_qubits():
    n_toffoli = 100
    n_logical_qubits = 100
    BAM = BasicArchitectureModel
    BAM.physical_qubit_error_rate = 1.0e-4
    BAM.surface_code_cycle_time_in_seconds = 1e-7

    resource_estimate = openfermion_estimator(
        num_toffoli=n_toffoli,
        num_logical_qubits=n_logical_qubits,
        architecture_model=BAM,
        hardware_failure_tolerance=1e-1,
    )
    assert resource_estimate.n_physical_qubits > n_logical_qubits


@pytest.mark.parametrize(
    "scc_time_low,scc_time_high",
    [
        (0.000001, 0.000008),
        (0.000004, 0.000009),
        (0.000001, 0.000009),
        (0.000005, 0.000010),
    ],
)
def test_monotonicity_of_duration_wrt_scc_time(scc_time_low, scc_time_high):
    """
    This tests if duration (run-time) increases as surface code cycle time increases
    """
    n_toffoli = 100
    n_logical_qubits = 100
    BAM_fast = BasicArchitectureModel
    BAM_fast.physical_qubit_error_rate = 1.0e-4
    BAM_fast.surface_code_cycle_time_in_seconds = scc_time_low
    resource_estimates_low = openfermion_estimator(
        num_toffoli=n_toffoli,
        num_logical_qubits=n_logical_qubits,
        architecture_model=BAM_fast,
        hardware_failure_tolerance=1e-1,
    )
    BAM_slow = BasicArchitectureModel
    BAM_slow.physical_qubit_error_rate = 1.0e-4
    BAM_slow.surface_code_cycle_time_in_seconds = scc_time_high
    resource_estimates_high = openfermion_estimator(
        num_toffoli=n_toffoli,
        num_logical_qubits=n_logical_qubits,
        architecture_model=BAM_slow,
        hardware_failure_tolerance=1e-1,
    )
    assert (
        resource_estimates_high.total_time_in_seconds
        > resource_estimates_low.total_time_in_seconds
    )


@pytest.mark.parametrize(
    "scc_time_low,scc_time_high",
    [
        (0.000001, 0.000008),
        (0.000004, 0.000009),
        (0.000001, 0.000009),
        (0.000005, 0.000010),
    ],
)
def test_linearity_of_duration_wrt_scc_time(scc_time_low, scc_time_high):
    """
    This tests if duration (run-time) proportionately
    increases wrt surface code cycle time
    """

    n_toffoli = 100
    n_logical_qubits = 100
    BAM_fast = BasicArchitectureModel
    BAM_fast.physical_qubit_error_rate = 1.0e-4
    BAM_fast.surface_code_cycle_time_in_seconds = scc_time_low

    resource_estimates_low = openfermion_estimator(
        num_toffoli=n_toffoli,
        num_logical_qubits=n_logical_qubits,
        architecture_model=BAM_fast,
        hardware_failure_tolerance=1e-1,
    )
    BAM_slow = BasicArchitectureModel
    BAM_slow.physical_qubit_error_rate = 1.0e-4
    BAM_slow.surface_code_cycle_time_in_seconds = scc_time_high
    resource_estimates_high = openfermion_estimator(
        num_toffoli=n_toffoli,
        num_logical_qubits=n_logical_qubits,
        architecture_model=BAM_slow,
        hardware_failure_tolerance=1e-1,
    )

    np.testing.assert_allclose(
        resource_estimates_high.total_time_in_seconds / scc_time_high,
        resource_estimates_low.total_time_in_seconds / scc_time_low,
    )


@pytest.mark.parametrize(
    "num_toffoli,num_t",
    [
        (20, 20),
        (40, 40),
        (20, 30),
    ],
)
def test_ratio_of_failure_prob_of_magicstateFactory(num_toffoli, num_t):
    """
    This ascertains if ratio of failure rate of magic state factory for a ckt
    with only Toffoli gates and of a ckt with only T gates is 1:1, given the same
    physical error rate and surface code cycle time.

    """
    num_logical_qubits = 12
    BAM = BasicArchitectureModel
    BAM.physical_qubit_error_rate = 1.0e-4
    BAM.surface_code_cycle_time_in_seconds = 2e-6

    best_toffoli = openfermion_estimator(
        num_logical_qubits=num_logical_qubits,
        num_toffoli=num_toffoli,
        architecture_model=BAM,
        hardware_failure_tolerance=1e-1,
    )
    best_T = openfermion_estimator(
        num_logical_qubits=num_logical_qubits,
        num_t=num_t,
        architecture_model=BAM,
        hardware_failure_tolerance=1e-1,
    )

    assert (
        best_toffoli.extra.fail_rate_msFactory / best_T.extra.fail_rate_msFactory == 1.0
    )


@pytest.mark.parametrize(
    "n_toffoli,n_T",
    [
        (20, 20),
        (40, 40),
    ],
)
def test_calc_of_algorithm_failure_prob(n_toffoli, n_T):
    """
    X+Yf - 2*(X/2+Yf/2) = 0, where X+Yf and X/2+Yf/2 are
    algorithm Failurf prob for Toffoli and T cases respectively,
    where X -> data failure, Yf -> distillation
    failure, Y=#Toffoli gate=#T gates and f is 1 CCZ error.
    If failure rate is calculated correctly,
    to ascertain if algorithm failure probability is calculated correctly
    for both toffoli and T.
    """
    num_logical_qubits = 12
    BAM = BasicArchitectureModel
    BAM.physical_qubit_error_rate = 1.0e-4
    BAM.surface_code_cycle_time_in_seconds = 2e-6
    best_toffoli = openfermion_estimator(
        num_logical_qubits=num_logical_qubits,
        num_toffoli=n_toffoli,
        architecture_model=BAM,
        hardware_failure_tolerance=1e-1,
    )
    best_T = openfermion_estimator(
        num_logical_qubits=num_logical_qubits,
        num_t=n_T,
        architecture_model=BAM,
        hardware_failure_tolerance=1e-1,
    )

    np.testing.assert_almost_equal(
        (
            best_toffoli.total_circuit_failure_rate
            - 2 * best_T.total_circuit_failure_rate
        ),
        0,
        decimal=5,
    )


def test_algorithm_failure_prob_calculation():
    """
    To ascertain if algorithm failure probability is
    calculated correctly for a ckt with (num_toffoli=20,
    num_t=20) and for a ckt with (num_toffoli=30,
    num_t=0)
    """
    num_logical_qubits = 12
    BAM = BasicArchitectureModel
    BAM.physical_qubit_error_rate = 1.0e-4
    BAM.surface_code_cycle_time_in_seconds = 2e-6
    best_cost_toffoli = openfermion_estimator(
        num_logical_qubits=num_logical_qubits,
        num_toffoli=20,
        num_t=20,
        architecture_model=BAM,
        hardware_failure_tolerance=1e-1,
    )
    best_cost_t = openfermion_estimator(
        num_logical_qubits=num_logical_qubits,
        num_toffoli=30,
        num_t=0,
        architecture_model=BAM,
        hardware_failure_tolerance=1e-1,
    )
    exp_error_rate = best_cost_toffoli.total_circuit_failure_rate
    obt_error_rate = best_cost_t.total_circuit_failure_rate
    np.testing.assert_almost_equal(exp_error_rate, obt_error_rate)  # type: ignore


def test_default_values():
    """
    If physical_error_rate != default value,
    this ascertains if both num_t=0 and num_toffoli=0,
    then it must throw an error. This basically tests
    the 'else statement' in iter_known_factories()
    """

    num_logical_qubits = 12
    BAM = BasicArchitectureModel
    BAM.physical_qubit_error_rate = 1.0e-4
    BAM.surface_code_cycle_time_in_seconds = 2 * 1e-6
    with pytest.raises(ValueError) as dvalue:
        a, b = openfermion_estimator(
            num_logical_qubits=num_logical_qubits,
            architecture_model=BAM,
            hardware_failure_tolerance=1e-1,
        )

    assert dvalue.type == ValueError


def test_all_default_values():
    """
    If physical_error_rate == default value,
    this ascertains if both num_t=0 and num_toffoli=0,
    then it must throw an error. This basically tests
    the 'if statement' in iter_known_factories()
    """
    num_logical_qubits = 12
    with pytest.raises(ValueError) as dvalue:
        openfermion_estimator(
            num_logical_qubits=num_logical_qubits,
            hardware_failure_tolerance=1e-1,
        )

    assert dvalue.type == ValueError


def test_default_scc_time():
    num_logical_qubits = 12
    """
    This test will verify attributes of
    default Architecture Model i.e. BASIC_SC_ARCHITECTURE_MODEL
    """
    cost = openfermion_estimator(
        num_logical_qubits=num_logical_qubits,
        num_t=25,
        num_toffoli=25,
        hardware_failure_tolerance=1e-1,
    )
    assert cost.extra.physical_qubit_error_rate == 1e-3
    assert cost.extra.scc_time == 1e-6


def test_openfermion_estimator_supports_large_circuits():
    n_logical_qubits = 4e3
    n_toffoli = 1e12
    resource_estimate = openfermion_estimator(
        n_logical_qubits, n_toffoli, hardware_failure_tolerance=1e-1
    )
    assert resource_estimate.n_physical_qubits > n_logical_qubits
