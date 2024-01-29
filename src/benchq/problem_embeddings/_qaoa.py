#####################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################

import numpy as np
from orquestra.quantum.circuits import Circuit
from orquestra.quantum.operators import PauliSum
from orquestra.vqa.algorithms.qaoa import QAOA

from .quantum_program import QuantumProgram


def get_qaoa_circuit(hamiltonian: PauliSum, n_layers: int = 1) -> Circuit:
    """Given a hamiltonian, generate a QAOA circuit for it. All of the parameters
    describing rotations in the circuit are set to be random. Note: this function
    returns a circuit with different randomized values for each layer, whereas
    get_qaoa_program returns a circuit with the same randomized values for each layer.

    Input:
          hamiltonian (np.array): hamiltonian to simulate
          n_layers (int): Number of layers in QAOA circuits
    Output:
          a QAOA circuit with random parameters for the QUBO instance
    """

    qaoa = QAOA.default(cost_hamiltonian=hamiltonian, n_layers=n_layers)
    random_params = np.random.uniform(-np.pi, np.pi, 2 * n_layers)
    return qaoa.get_circuit(random_params)


def get_qaoa_program(hamiltonian: PauliSum, n_layers: int = 1) -> QuantumProgram:
    """Given a hamiltonian, generate a QAOA circuit for it. All of the parameters
    describing rotations in the circuit are set to be random. At this point, it is
    best to run this with delayed_gate_synthesis=True, because the T gates one gets
    from decomposing the QAOA circuit are not meaningful, only the number of them
    matters. Note: this function returns a circuit with the same randomized values
    for each layer, where as get_qaoa_circuit returns a circuit with the different
    randomized values for each layer.

    Input:
          hamiltonian (np.array): hamiltonian to simulate
          n_layers (int): Number of layers in QAOA circuits
    Output:
          a QAOA circuit with random parameters for the QUBO instance
    """

    qaoa = QAOA.default(cost_hamiltonian=hamiltonian, n_layers=1)
    random_params = np.random.uniform(-np.pi, np.pi, 2)
    circuit = qaoa.get_circuit(random_params)
    return QuantumProgram([circuit], n_layers, lambda x: [0] * x)
