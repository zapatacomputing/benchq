import warnings

import numpy as np
from orquestra.integrations.cirq.conversions import to_openfermion

from ..conversions import openfermion_to_pyliqtr
from ..data_structures import AlgorithmImplementation, ErrorBudget
from ..problem_embeddings import get_qsp_program


def _n_block_encodings(hamiltonian, precision):
    pyliqtr_operator = openfermion_to_pyliqtr(to_openfermion(hamiltonian))

    return int(np.ceil(np.pi * (pyliqtr_operator.alpha) / (precision)))


def qpe_gsee_algorithm(hamiltonian, precision, failure_tolerance):
    warnings.warn("This is experimental implementation, use at your own risk.")
    n_block_encodings = _n_block_encodings(hamiltonian, precision)
    program = get_qsp_program(hamiltonian, n_block_encodings)
    error_budget = ErrorBudget.from_even_split(failure_tolerance)
    n_calls = np.ceil(np.log(1 / error_budget.algorithm_failure_tolerance))
    return AlgorithmImplementation(program, error_budget, n_calls)
