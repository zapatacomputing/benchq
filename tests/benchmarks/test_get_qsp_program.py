from pathlib import Path
import pytest

from benchq.algorithms import get_qsp_program
from benchq.problem_ingestion import (
    generate_jw_qubit_hamiltonian_from_mol_data,
    get_vlasov_hamiltonian,
)
from benchq.problem_ingestion.hamiltonian_generation import fast_load_qubit_op
from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
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
    mode = "time_evolution"

    operator = get_vlasov_hamiltonian(k, alpha, nu, N)

    return pytest.param(operator, required_precision, dt, tmax, sclf, mode, id="vlasov")


def jw_test_cases():
    dt = 0.5
    tmax = 5
    sclf = 1
    required_precision = 1e-3 / 2
    mode = "gse"

    return [
        pytest.param(
            generate_jw_qubit_hamiltonian_from_mol_data(
                generate_hydrogen_chain_instance(n_hydrogens)
            ),
            required_precision,
            dt,
            tmax,
            sclf,
            mode,
            id=f"jw-{n_hydrogens}",
        )
        for n_hydrogens in (2,)
    ]


def fast_load_test_cases():
    def _load_hamiltonian(name):
        return fast_load_qubit_op(
            str(Path(__file__).parent / f"../../examples/small_molecules/{name}.json")
        )

    dt = 0.05  # Integration timestep
    tmax = 5  # Maximal timestep
    sclf = 1
    required_precision = 1e-2
    mode = "gse"

    return [
        pytest.param(_load_hamiltonian(name), required_precision, dt, tmax, sclf, mode, id=name)
        for name in (
            "C2H2-8-canonical_qubitop",
            "CH4-8-NOs_qubitop",
            "C2H4-12-NOs_qubitop",
        )
    ]


@pytest.mark.parametrize(
    "operator, required_precision, dt, tmax, sclf, mode",
    [vlasov_test_case(), *jw_test_cases(), *fast_load_test_cases()],
)
def test_get_qsp_program(benchmark, operator, required_precision, dt, tmax, sclf, mode):
    benchmark(get_qsp_program, operator, required_precision, dt, tmax, sclf, mode)
