import pytest
from orquestra.quantum.operators import PauliTerm

from benchq.algorithms import (
    qsp_time_evolution_algorithm,
    trotter_time_evolution_algorithm,
)


@pytest.fixture(params=[trotter_time_evolution_algorithm, qsp_time_evolution_algorithm])
def te_alg_generator(request):
    return request.param


def test_qsp_te_alg_creates_correct_alg_description():
    hamiltonian = PauliTerm("X0*Y1*Z2") + PauliTerm("Y0*X1*Z2") + PauliTerm("Z0*Z1*Z2")

    time = 1.0
    failure_tolerance = 0.1
    algorithm = qsp_time_evolution_algorithm(hamiltonian, time, failure_tolerance)

    assert algorithm.n_calls == 1
    assert algorithm.error_budget.total_failure_tolerance == failure_tolerance


def test_te_alg_creates_longer_circuit_for_longer_time(te_alg_generator):
    hamiltonian = PauliTerm("X0*Y1*Z2") + PauliTerm("Y0*X1*Z2") + PauliTerm("Z0*Z1*Z2")

    time = 1.0
    failure_tolerance = 0.1
    short_algorithm = te_alg_generator(hamiltonian, time, failure_tolerance)

    time = 5.0
    long_algorithm = te_alg_generator(hamiltonian, time, failure_tolerance)

    assert short_algorithm.program.steps < long_algorithm.program.steps


def test_te_alg_creates_longer_circuit_for_lower_failure_tolerance(te_alg_generator):
    hamiltonian = PauliTerm("X0*Y1*Z2") + PauliTerm("Y0*X1*Z2") + PauliTerm("Z0*Z1*Z2")

    time = 1.0
    high_failure_tolerance = 0.1
    short_algorithm = te_alg_generator(hamiltonian, time, high_failure_tolerance)

    low_failure_tolerance = 0.0001
    long_algorithm = te_alg_generator(hamiltonian, time, low_failure_tolerance)

    assert short_algorithm.program.steps < long_algorithm.program.steps
