import h5py
import os
import numpy as np
from icecream import ic
from orquestra.quantum.operators import PauliSum, PauliTerm
from orquestra.vqa.algorithms import QAOA
from orquestra.integrations.qiskit.conversions import export_to_qiskit


# In a QUBO problem, we are given an n*n matrix Q and need to find x in {0,1}^n
# which minimizes x^T Q x. In the following code, we receive q_matrix = the
# matrix Q, and generate a QAOA circuit (with random paramerers) for it.

def get_hamiltonian_for_qubo(q_matrix):
    # Input:
    #       q_matrix: Q matrix of the QUBO instance
    # Output:
    #       the cost Hamiltonian for the QUBO instance

    assert q_matrix.shape[0] == q_matrix.shape[1]
    N = q_matrix.shape[0]
    q_matrix = (q_matrix + q_matrix.T) / 2.0
    pauli_terms = []

    for i in range(N):
        # diagonal terms
        diag_pauli_term1 = PauliTerm("I0", q_matrix[i][i] / 2.0)
        diag_pauli_term2 = PauliTerm(f"Z{i}", -q_matrix[i][i] / 2.0)
        pauli_terms.append(diag_pauli_term1)
        pauli_terms.append(diag_pauli_term2)

        for j in range(i):
            # off-diagonal terms
            off_diag_pauli_term1 = PauliTerm("I0", q_matrix[i][j] / 2.0)
            off_diag_pauli_term2 = PauliTerm(f"Z{i}", -q_matrix[i][j] / 2.0)
            off_diag_pauli_term3 = PauliTerm(f"Z{j}", -q_matrix[i][j] / 2.0)
            off_diag_pauli_term4 = PauliTerm(f"Z{i} * Z{j}", q_matrix[i][j] / 2.0)
            pauli_terms.append(off_diag_pauli_term1)
            pauli_terms.append(off_diag_pauli_term2)
            pauli_terms.append(off_diag_pauli_term3)
            pauli_terms.append(off_diag_pauli_term4)

    hamiltonian = PauliSum(pauli_terms).simplify()
    return hamiltonian


def test_get_hamiltonian_for_qubo():
    q_matrix = np.array([[1, -2], [0, -1]])
    hamiltonian = get_hamiltonian_for_qubo(q_matrix)
    # ic(hamiltonian)


def get_qaoa_circuit_for_qubo(q_matrix, n_layers=1):
    # Input:
    #       q_matrix: Q matrix of the QUBO instance
    #       n_layers: Number of layers in QAOA circuits
    # Output:
    #       a QAOA circuit with random parameters for the QUBO instance

    hamiltonian = get_hamiltonian_for_qubo(q_matrix)
    qaoa = QAOA.default(cost_hamiltonian=hamiltonian, n_layers=n_layers)
    random_params = np.random.uniform(-np.pi, np.pi, 2 * n_layers)
    circuit = qaoa.get_circuit(random_params)
    return circuit


def test_get_qaoa_circuit_for_qubo():
    q_matrix = np.array([[1, -2], [0, -1]])
    circuit = get_qaoa_circuit_for_qubo(q_matrix, n_layers=1)
    # ic(circuit)


def get_qaoa_circuits_for_qubos(root_dir, n_layers=1, max_qubo_size=100):
    # Input:
    #       root_dir: A directory that contains the hdf5 files that describe
    #                 the QUBO instances
    #       n_layers: Number of layers in QAOA circuits
    #       max_qubo_size: We only generate QAOA ciruicts for QUBO instances
    #                      with <= max_qubo_size variables. It takes long time
    #                      to generate QAOA circuits for large instances.
    # Output:
    #       the QAOA ciruicts are saved into QASM files which are named after
    #       the given data files

    list_files = os.listdir(root_dir)
    for file in list_files:
        if file[-5:] != ".hdf5":
            continue
        data = h5py.File(os.path.join(root_dir, file), 'r')
        q_matrix = np.array(data['q_matrix'][()])
        if q_matrix.shape[0] <= max_qubo_size:
            circuit = get_qaoa_circuit_for_qubo(q_matrix, n_layers=n_layers)
            result_file = os.path.splitext(file)[0] + ".qasm"
            export_to_qiskit(circuit).qasm(filename=os.path.join(root_dir, result_file))

# get_qaoa_circuits_for_qubos("./qubo_data", n_layers=1, max_qubo_size=100)
