import warnings

import numpy as np
from pyLIQTR.utils.Hamiltonian import Hamiltonian

from ...algorithms.data_structures import AlgorithmImplementation, ErrorBudget
from ...conversions import SUPPORTED_OPERATORS, get_pyliqtr_operator
from ...problem_embeddings.qsp import get_qsp_program


def _n_block_encodings(hamiltonian: Hamiltonian, precision: float) -> int:
    return int(np.ceil(np.pi * (hamiltonian.alpha) / (precision)))


def qpe_gsee_algorithm(
    hamiltonian: SUPPORTED_OPERATORS, precision: float, failure_tolerance: float
) -> AlgorithmImplementation:
    warnings.warn("This is experimental implementation, use at your own risk.")
    hamiltonian = get_pyliqtr_operator(hamiltonian)
    n_block_encodings = _n_block_encodings(hamiltonian, precision)
    program = get_qsp_program(hamiltonian, n_block_encodings)
    error_budget = ErrorBudget.from_even_split(failure_tolerance)
    n_shots = np.ceil(np.log(1 / error_budget.algorithm_failure_tolerance))
    return AlgorithmImplementation(program, error_budget, n_shots)
