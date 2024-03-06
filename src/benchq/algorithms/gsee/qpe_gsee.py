import warnings

import numpy as np
from orquestra.integrations.cirq.conversions import to_openfermion
from orquestra.quantum.operators import PauliRepresentation

from ...algorithms.data_structures import AlgorithmImplementation, ErrorBudget
from ...conversions import openfermion_to_pyliqtr
from ...problem_embeddings.qsp import get_qsp_program
from pyLIQTR.QSP.Hamiltonian import Hamiltonian


def _n_block_encodings(hamiltonian: Hamiltonian, precision: float) -> int:
    return int(np.ceil(np.pi * (hamiltonian.alpha) / (precision)))


def qpe_gsee_algorithm(
    hamiltonian: PauliRepresentation, precision: float, failure_tolerance: float
) -> AlgorithmImplementation:
    warnings.warn("This is experimental implementation, use at your own risk.")
    n_block_encodings = _n_block_encodings(hamiltonian, precision)
    program = get_qsp_program(hamiltonian, n_block_encodings)
    error_budget = ErrorBudget.from_even_split(failure_tolerance)
    n_shots = np.ceil(np.log(1 / error_budget.algorithm_failure_tolerance))
    return AlgorithmImplementation(program, error_budget, n_shots)
