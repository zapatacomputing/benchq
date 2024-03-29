import os
import zipfile
from pathlib import Path

import openfermion
import pytest

from benchq.algorithms.time_evolution import _n_block_encodings_for_time_evolution
from benchq.conversions import get_pyliqtr_operator
from benchq.problem_embeddings.qsp import get_qsp_program
from benchq.problem_ingestion import get_hamiltonian_from_file, get_vlasov_hamiltonian
from benchq.problem_ingestion.molecule_hamiltonians import (
    generate_hydrogen_chain_instance,
)

SKIP_SLOW = pytest.mark.skipif(
    os.getenv("SLOW_BENCHMARKS") is None,
    reason="Slow benchmarks can only run if SLOW_BENCHMARKS env variable is defined",
)


def vlasov_test_case():
    k = 2.0
    alpha = 0.6
    nu = 0.0
    N = 2

    evolution_time = 5
    failure_tolerance = 1e-3

    operator = get_vlasov_hamiltonian(k, alpha, nu, N)
    pyliqtr_operator = get_pyliqtr_operator(operator)

    n_block_encodings = _n_block_encodings_for_time_evolution(
        pyliqtr_operator, evolution_time, failure_tolerance
    )

    return pytest.param(operator, n_block_encodings, id="vlasov")


def jw_test_case():
    evolution_time = 5
    failure_tolerance = 1e-3
    n_hydrogens = 2

    instance = generate_hydrogen_chain_instance(n_hydrogens)
    interaction_operator = instance.get_active_space_hamiltonian()
    jw_operator = openfermion.jordan_wigner(interaction_operator)
    pyliqtr_jw_operator = get_pyliqtr_operator(jw_operator)

    n_block_encodings = _n_block_encodings_for_time_evolution(
        pyliqtr_jw_operator, evolution_time, failure_tolerance
    )

    return pytest.param(
        pyliqtr_jw_operator,
        n_block_encodings,
        id=f"jw-{n_hydrogens}",
    )


def fast_load_hamiltonians():
    evolution_time = 5
    failure_tolerance = 1e-3
    base_location = "./examples/data/"
    zip_location = base_location + "small_molecules.zip"

    with zipfile.ZipFile(zip_location, "r") as zip_ref:
        zip_ref.extractall(base_location)

    def _load_hamiltonian(name):
        return get_hamiltonian_from_file(
            str(
                Path(__file__).parent / f"../{base_location}/"
                f"small_molecules/{name}.json"
            )
        )

    return [
        pytest.param(
            (operator := get_pyliqtr_operator(_load_hamiltonian(name))),
            _n_block_encodings_for_time_evolution(
                operator, evolution_time, failure_tolerance
            ),
            id=name,
            marks=SKIP_SLOW,
        )
        for name in (
            "C2H2-8-canonical_qubitop",
            "CH4-8-NOs_qubitop",
            "C2H4-12-NOs_qubitop",
        )
    ]


@pytest.mark.benchmark
@pytest.mark.parametrize(
    "operator, n_block_encodings",
    [vlasov_test_case(), jw_test_case(), *fast_load_hamiltonians()],
)
def test_get_qsp_program(benchmark, operator, n_block_encodings):
    benchmark(get_qsp_program, operator, n_block_encodings)
