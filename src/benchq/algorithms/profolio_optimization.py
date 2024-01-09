#####################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
from orquestra.quantum.operators import PauliSum

from ..problem_embeddings._qaoa import get_qaoa_program
from .data_structures import AlgorithmImplementation, ErrorBudget


def get_qaoa_optimization_algorithm(
    hamiltonian: PauliSum, n_layers: int = 1, failure_tolerance: float = 1e-3
):
    """Returns a program that implements QAOA for optimizing a portfolio
    of stocks which is described by the hamiltonian. We do not optimize the
    parameters of the QAOA circuit, but rather just run it with random
    parameters. Since the cost of each layer is determined by the precision
    of the rotation, not the degree of rotation, we can just run the circuit
    with random parameters and get a good estimate of the resources needed
    to run the circuit.

    Args:
        hamiltonian: Hamiltonian defining the problem
        n_layers: number of layers in the QAOA circuit
        failure_tolerance: how often the algorithm can fail
    """
    program = get_qaoa_program(hamiltonian, n_layers)
    return AlgorithmImplementation(
        program, ErrorBudget.from_even_split(failure_tolerance), 1
    )
