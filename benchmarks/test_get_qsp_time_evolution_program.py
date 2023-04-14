import os
from pathlib import Path

import pytest

from benchq.algorithms.time_evolution import get_qsp_time_evolution_program
from benchq.problem_ingestion import (
    generate_jw_qubit_hamiltonian_from_mol_data,
    get_vlasov_hamiltonian,
)
from benchq.problem_ingestion.hamiltonian_generation import fast_load_qubit_op
from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)

SKIP_SLOW = pytest.mark.skipif(
    os.getenv("SLOW_BENCHMARKS") is None,
    reason="Slow benchmarks can only run if SLOW_BENCHMARKS env variable is defined",
)


def vlasov_test_case():
    # Parameters from operator taken from examples/qsp_vlasov.py
    k = 2.0
    alpha = 0.6
    nu = 0.0
    N = 2

    dt = 0.1
    tmax = 5
    sclf = 1
    required_precision = 1e-3 / 3

    operator = get_vlasov_hamiltonian(k, alpha, nu, N)

    return pytest.param(operator, required_precision, dt, tmax, sclf, id="vlasov")


def jw_test_cases():
    dt = 0.5
    tmax = 5
    sclf = 1
    required_precision = 1e-3 / 2

    return [
        pytest.param(
            generate_jw_qubit_hamiltonian_from_mol_data(
                generate_hydrogen_chain_instance(n_hydrogens)
            ),
            required_precision,
            dt,
            tmax,
            sclf,
            id=f"jw-{n_hydrogens}",
        )
        for n_hydrogens in (2,)
    ]


def fast_load_test_cases():
    def _load_hamiltonian(name):
        return fast_load_qubit_op(
            str(Path(__file__).parent / f"../examples/small_molecules/{name}.json")
        )

    dt = 0.05  # Integration timestep
    tmax = 5  # Maximal timestep
    sclf = 1
    required_precision = 1e-2

    return [
        pytest.param(
            _load_hamiltonian(name),
            required_precision,
            dt,
            tmax,
            sclf,
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
    "operator, required_precision, dt, tmax, sclf",
    [vlasov_test_case(), *jw_test_cases(), *fast_load_test_cases()],
)
def test_get_qsp_program(benchmark, operator, required_precision, dt, tmax, sclf):
    benchmark(
        get_qsp_time_evolution_program, operator, required_precision, dt, tmax, sclf
    )
