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

from benchq.problem_embeddings.block_encodings.double_factorized_hamiltonian import (
    get_double_factorized_hamiltonian_block_encoding,
)
from benchq.problem_ingestion.molecular_hamiltonians import (
    get_hydrogen_chain_hamiltonian_generator,
)


@pytest.mark.parametrize(
    "avas_atomic_orbitals,avas_minao",
    [
        (None, None),
        (["H 1s", "H 2s"], "sto-3g"),
    ],
)
def test_df_block_encoding_logical_qubit_count_is_larger_than_number_of_spin_orbitals(
    avas_atomic_orbitals, avas_minao
):
    instance = get_hydrogen_chain_hamiltonian_generator(8)
    instance.avas_atomic_orbitals = avas_atomic_orbitals
    instance.avas_minao = avas_minao
    mean_field_object = instance.get_active_space_meanfield_object()
    h1, eri_full, _, _, _ = pyscf_to_cas(mean_field_object)

    (num_toffoli, num_qubits, lam) = get_double_factorized_hamiltonian_block_encoding(
        h1, eri_full, 1e-6
    )
    assert num_qubits > 2 * eri_full.shape[0]


@pytest.mark.parametrize(
    "avas_atomic_orbitals,avas_minao",
    [
        (None, None),
        (["H 1s", "H 2s"], "sto-3g"),
    ],
)
def test_df_block_encoding_lambda_scales_with_hamiltonian(
    avas_atomic_orbitals, avas_minao
):
    instance = get_hydrogen_chain_hamiltonian_generator(8)
    instance.avas_atomic_orbitals = avas_atomic_orbitals
    instance.avas_minao = avas_minao
    mean_field_object = instance.get_active_space_meanfield_object()
    h1, eri_full, _, _, _ = pyscf_to_cas(mean_field_object)

    threshold = 1e-6
    scale_factor = 10

    (num_toffoli, num_qubits, lam) = get_double_factorized_hamiltonian_block_encoding(
        h1, eri_full, threshold
    )

    (
        scaled_num_toffoli,
        scaled_num_qubits,
        scaled_lam,
    ) = get_double_factorized_hamiltonian_block_encoding(
        scale_factor * h1, scale_factor * eri_full, scale_factor * threshold
    )

    assert scaled_num_qubits == num_qubits
    assert scaled_num_toffoli == num_toffoli
    assert np.isclose(scaled_lam, scale_factor * lam, rtol=1e-3)


def _get_asymmetric_hamiltonian():
    instance = get_hydrogen_chain_hamiltonian_generator(8)
    instance.avas_atomic_orbitals = ["H 1s", "H 2s"]
    instance.avas_minao = "sto-3g"
    mean_field_object = instance.get_active_space_meanfield_object()
    h1, eri_full, _, _, _ = pyscf_to_cas(mean_field_object)
    eri_full[0, 1, 2, 3] += 0.1
    return h1, eri_full


def test_double_factorized_block_encoding_raises_exception_for_invalid_eri():
    h1, eri_full = _get_asymmetric_hamiltonian()
    with pytest.raises(ValueError):
        get_double_factorized_hamiltonian_block_encoding(h1, eri_full, 1e-6)
