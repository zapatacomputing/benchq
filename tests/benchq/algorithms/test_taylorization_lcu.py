#####################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
import pytest
from openfermion.ops import QubitOperator, FermionOperator
from openfermion.linalg import get_sparse_operator
from scipy.sparse.linalg import expm_multiply
import numpy as np
from qiskit import QuantumCircuit, transpile, QuantumRegister, Aer
import cmath
import math
from taylorization_lcu_circuit_generation import *
from openfermion import fermi_hubbard
from openfermion.utils import count_qubits


### This script contains necessary tests for the functions that are defined in the file
### _taylorization_lcu.py


ham_1 = fermi_hubbard(
    x_dimension=1, y_dimension=1, tunneling=1, coulomb=1, periodic=False
)
ham_2 = fermi_hubbard(
    x_dimension=2, y_dimension=1, tunneling=2, coulomb=2, periodic=False
)
ham_3 = fermi_hubbard(
    x_dimension=2, y_dimension=1, tunneling=2, coulomb=0, periodic=False
)
ham_4 = fermi_hubbard(
    x_dimension=2, y_dimension=1, tunneling=0, coulomb=2, periodic=False
)

hamiltonians = [ham_1, ham_2, ham_3, ham_4]


@pytest.mark.parameterize("fermion_hamiltonian", hamiltonians)
def test_generate_fermi_hubbard_qubit_hamiltonian(fermion_hamiltonian):
    """Tests for generate_fermi_hubbard_qubit_hamiltonian function. The function should take a hamiltonian
    in the form of an OPenFermion FermionOperator class type and encode it as a qubit hamiltonian of the
    OpenFermion class type QubitOperator"""
    assert isinstance(
        fermion_hamiltonian, FermionOperator
    ), "Hamiltonian provided is not FermionOperator class type"
    qubit_hubbard = generate_fermi_hubbard_qubit_hamiltonian(
        fermion_hamiltonian, "Bravyi_Kitaev"
    )
    assert isinstance(
        qubit_hubbard, QubitOperator
    ), "qubit_hubbard is not a QubitOperator class type"
    qubit_hubbard = generate_fermi_hubbard_qubit_hamiltonian(
        fermion_hamiltonian, "Jordan_Wigner"
    )
    assert isinstance(
        qubit_hubbard, QubitOperator
    ), "qubit_hubbard is not a QubitOperator class type"
    return qubit_hubbard


ts = 1
steps = 2
orders = 15
params = []
for i in range(4):
    q_hamiltonian = generate_fermi_hubbard_qubit_hamiltonian(
        hamiltonians[i], "Bravyi_Kitaev"
    )
    params.append((ts, steps, orders, q_hamiltonian))


@pytest.mark.parametrize("time, steps, order, qubit_hubbard", params)
def test_generate_taylor_series(time, steps, order, qubit_hubbard):
    """Tests for the function generate_taylor_series function. the function generates the taylor series expansion
    of e^(-iHt/r) upt to order k. t is duration of simulation, and r is the number of timesteps in the simulation.
    Should take in a Hamiltonian of the OpenFermion QubitOperator class type and return another QubitOperator object."""
    n_qubits = count_qubits(qubit_hubbard)

    def is_float_or_int(variable):
        if isinstance(variable, float) or isinstance(variable, int):
            if variable > 0:
                return True
        else:
            return False

    assert isinstance(order, int), "Order of Taylor Series must be a positive integer."
    assert order >= 0, "Order of Taylor Series must be a positive integer."
    assert is_float_or_int(
        time
    ), "Time for simulation must be real valued and positive."
    assert time > 0, "Time for simulation must be real valued and positive."
    assert isinstance(steps, int), "Number of steps must be a positive integer"
    assert steps > 0, "Number of steps must be a positive integer"
    taylor_series = generate_taylor_series(
        qubit_hubbard, order=order, time=time, steps=steps
    )
    assert isinstance(
        taylor_series, QubitOperator
    ), "Taylor Series must be QubitOperator class type."
    assert count_qubits(taylor_series) == n_qubits


terms_list = []
coefficients_and_angles_list = []
params_for_test_select_and_prep_dagger = []
params_for_test_prepare_circuit = []

for i in range(4):
    coefficients_and_angles = []
    qubit_hubbard = params[i][3]
    t_series = generate_taylor_series(qubit_hubbard, order=15, time=1, steps=2)
    prepare, terms = generate_prepare_circuits(t_series)
    params_for_test_prepare_circuit.append((t_series, prepare, terms))

    words = get_pauliword_list(t_series)
    for j, word in enumerate(words):
        coefficient = get_pauli_word_coefficient(word)
        coefficients_and_angles.append(
            tuple((coefficient, cmath.polar(coefficient)[1]))
        )

    coefficients_and_angles_list.append(coefficients_and_angles)
    unitaries_and_qubits = get_unitaries(terms)
    params_for_test_select_and_prep_dagger.append(
        (
            qubit_hubbard,
            1,
            2,
            15,
            prepare,
            coefficients_and_angles,
            unitaries_and_qubits,
        )
    )


@pytest.mark.parametrize("taylor_series, prep, terms", params_for_test_prepare_circuit)
def test_generate_prepare_circuit(taylor_series, prep, unitaries):
    """Tests for the prepare circuit, which should take in a taylor series of e^(-iHt/r) of a QubitOperator object and
    return a quantum circuit of the QuantumCircuit object type, which prepares the correct vector of amplitudes
    (i.e. the magnitude of coefficients in taylor series) from the initialized all zero state. """

    def fidelity_prepare_circuit(
        taylor_expansion: QubitOperator, prepare_circuit: QuantumCircuit
    ):
        """"Checks the overlap between desired amplitudes of basis states, and the result of quantum circuit."""
        coeffs = list(taylor_expansion.terms.values())
        coeff_magnitude = []
        for i, term in enumerate(coeffs):
            coeff_magnitude.append(abs(term))
        prefactor = sum(coeff_magnitude)
        paulis = get_pauliword_list(taylor_expansion)
        state_vector = []
        single_terms = []
        for i, p in enumerate(paulis):
            coefficient = get_pauli_word_coefficient(p)

            ### If coefficient, c_i is complex add |c_i| to amplitude vector
            if isinstance(coefficient, complex):
                state_vector.append(np.sqrt(abs(coefficient)) / np.sqrt(prefactor))
                single_terms.append(get_pauli_word(p))

            ### if coefficent c_i < 0, add |c_i| to amplitude vector
            elif coefficient < 0:
                state_vector.append(np.sqrt(abs(coefficient)) / np.sqrt(prefactor))
                single_terms.append(get_pauli_word(p))
            else:
                state_vector.append(cmath.sqrt(coefficient) / np.sqrt(prefactor))
                single_terms.append(get_pauli_word(p))

        ### if the number of terms is not a power of two, pad with zeros to make state vector length a power of 2
        if not np.log2(len(state_vector)).is_integer():
            n_qubits = int(np.ceil(np.log2(len(state_vector))))
            state_vector.extend([0] * (2 ** n_qubits - len(state_vector)))
        elif int(np.ceil(np.log2(len(state_vector)))) == 0:
            n_qubits = 1
            state_vector.extend([0] * (2 ** n_qubits - len(state_vector)))
        state_vector = np.array(state_vector)
        normalized_state_vector = state_vector

        backend = Aer.get_backend("statevector_simulator")
        job = backend.run(prepare_circuit)

        result = job.result()

        outputstate = result.get_statevector(prepare_circuit, decimals=5)
        outputstate = np.array(outputstate)

        overlap = abs(np.inner(np.conjugate(normalized_state_vector), outputstate)) ** 2

        return math.isclose(overlap, 1, rel_tol=1e-4)

    n_ancillae = len(prep.qubits)
    assert isinstance(unitaries, list), "Error, 'terms' variable is not a list."
    assert len(unitaries) == len(taylor_series.terms), (
        "Number of terms for the select operator is not equal to number of "
        "terms in taylor series"
    )
    assert 2 ** n_ancillae >= len(
        taylor_series.terms
    ), "Error, not enough qubits in prepare circuits"
    assert fidelity_prepare_circuit(taylor_series, prep), (
        "Prepare circuit does not result in correct vector " "of amplitudes!"
    )


@pytest.mark.parametrize(
    "qubit_hamiltonian, "
    "time, steps, order, "
    "prepare_circuit,"
    "coeffs_and_angles, operators_and_qubits",
    params_for_test_select_and_prep_dagger,
)
def test_select_and_prep_dagger(
    q_ham, n_segments, delta_t, order, prepare, coeffs_and_angles, operators_and_qubits,
):
    """Test for the final output of LCU circuit algorithm. If this test passes, then the hamiltonian simulation
    circuit result matches the result of the exact solution, as determined by the overlap - up to some error."""
    n_qubits = count_qubits(q_ham)
    initial_state_string = ""
    for i in range(n_qubits):
        temp = str(1)
        initial_state_string += temp
    initial_state_vector = []
    zero = np.array([1, 0])
    one = np.array([0, 1])
    for i in range(len(initial_state_string[::-1])):
        if i == 0:
            if initial_state_string[i] == "0":
                initial_state_vector = np.concatenate(
                    (initial_state_vector, zero), axis=0
                )
            else:
                initial_state_vector = np.concatenate(
                    (initial_state_vector, one), axis=0
                )

            continue

        if initial_state_string[i] == "0":
            initial_state_vector = np.kron(initial_state_vector, zero)
        else:
            initial_state_vector = np.kron(initial_state_vector, one)

    initial_state_vector = np.array(initial_state_vector)
    initial_state_circuit = QuantumCircuit(n_qubits)

    for i in range(len(initial_state_string) - 1, -1, -1):
        if initial_state_string[i] == "1":
            initial_state_circuit.x(i)

    n_ancillae = int(len(prepare.qubits))

    def fidelity_select_and_prep_dagger(
        initial_state: np.ndarray,
        hamiltonian: QubitOperator,
        linear_comb_unitaries_circuit: QuantumCircuit,
        num_ancillae: int,
    ):
        hamiltonian_sparse = get_sparse_operator(hamiltonian)
        exact_evolution = expm_multiply(
            -1j * delta_t / n_segments * hamiltonian_sparse, initial_state
        )
        linear_comb_unitaries_circuit = linear_comb_unitaries_circuit.reverse_bits()

        ### defining all zero initial state
        q_0 = [1, 0]
        if num_ancillae == 1:
            for j in range(num_ancillae - 1):
                q_0.append(0)
        else:
            for j in range(2 ** num_ancillae - 2):
                q_0.append(0)

        q_0 = np.array(q_0)

        ## making projector |0><0|_a
        ancillae_projector = np.kron(
            np.outer(q_0, np.conjugate(q_0)), np.identity(2 ** n_qubits)
        )
        # Tensor exact evolution with ancillae all zero state
        exact_evolution = np.kron(q_0, exact_evolution)
        ###Normalize
        exact_evolution = exact_evolution / np.linalg.norm(exact_evolution)
        ###Transpile LCU circuit
        transpiled_circuit = transpile(
            linear_comb_unitaries_circuit,
            basis_gates=["id", "rx", "ry", "rz", "h", "cx"],
        )
        backend = Aer.get_backend("statevector_simulator")
        job = backend.run(transpiled_circuit)
        result = job.result()
        ###gettng result of circuit and computing overlap with the exact evolution
        output_state = np.array(result.get_statevector(transpiled_circuit, decimals=3))
        collapsed_state = np.matmul(ancillae_projector, output_state)
        collapsed_state = collapsed_state / np.linalg.norm(collapsed_state)
        overlap = abs(np.inner(np.conjugate(exact_evolution), collapsed_state)) ** 2
        error = 1 - overlap

        if error <= 1e-5:
            return True
        else:
            return False

    lcu_circuit = select_and_prep_dagger(
        operators_and_qubits, coeffs_and_angles, prepare, initial_state_circuit,
    )
    assert fidelity_select_and_prep_dagger(
        initial_state_vector, q_ham, lcu_circuit, n_ancillae
    ), "Lcu circuit is not resulting in the correct final output! (error is too high)"
