import random
from openfermion.ops import QubitOperator, FermionOperator
import math
import numpy as np
from qiskit import QuantumCircuit, transpile, QuantumRegister
from openfermion.transforms import jordan_wigner, bravyi_kitaev
import cmath
from qiskit.circuit.library import RZGate
from qiskit.circuit.library import PhaseGate


def generate_random_initial_state(n_qubits):
    """Makes a random Hartree-Fock initial state as input to LCU algorithm. Useful for testing purposes, and can be used
    as a general template for making HF states."""

    def rand_key(p):
        key1 = ""
        for i in range(p):
            temp = str(random.randint(0, 1))
            key1 += temp
        return key1

    str1 = rand_key(n_qubits)
    random_initial_state = []
    zero = np.array([1, 0])
    one = np.array([0, 1])
    for i in range(len(str1[::-1])):
        if i == 0:
            if str1[i] == "0":
                random_initial_state = np.concatenate(
                    (random_initial_state, zero), axis=0
                )
            else:
                random_initial_state = np.concatenate(
                    (random_initial_state, one), axis=0
                )

            continue

        if str1[i] == "0":
            random_initial_state = np.kron(random_initial_state, zero)
        else:
            random_initial_state = np.kron(random_initial_state, one)

    random_initial_state = np.array(random_initial_state)
    random_initial_state_circuit = QuantumCircuit(n_qubits)

    for i in range(len(str1) - 1, -1, -1):
        if str1[i] == "1":
            random_initial_state_circuit.x(i)

    return random_initial_state, random_initial_state_circuit, str1


def generate_fermi_hubbard_qubit_hamiltonian(
    hamiltonian: FermionOperator, transform: str
):
    """Given an OpenFermion FermionOperator type Hamiltonian generates a qubit hamiltonian using either
    Jordan Wigner or Brayi Kitaev transformation"""
    if transform.lower() == "jordan_wigner":
        hubbard_qubit_hamiltonian = jordan_wigner(hamiltonian)
    elif transform.lower() == "bravyi_kitaev":
        hubbard_qubit_hamiltonian = bravyi_kitaev(hamiltonian)
    else:
        raise ValueError(
            "Qubit Transform entered is not recognized. Accepted entries are: "
            '"Bravyi_Kitaev", or "Jordan_Wigner".'
        )
    return hubbard_qubit_hamiltonian


def get_pauli_word_tuple(pauli: QubitOperator):
    """Given a single pauli word Pauli, extract the tuple representing the word.
    """
    words = list(pauli.terms.keys())
    if len(words) != 1:
        raise (ValueError("Pauli given is not a single pauli word"))
    return words[0]


def get_pauliword_list(hamiltonian: QubitOperator, ignore_identity=False):
    """Obtain a list of pauli words in Hamiltonian."""
    pauli_words = []
    for pauli_word, val in hamiltonian.terms.items():
        if ignore_identity:
            if len(pauli_word) == 0:
                continue
        pauli_words.append(QubitOperator(term=pauli_word, coefficient=val))
    return pauli_words


def get_pauli_word_coefficient(pauli: QubitOperator):
    """Given a single pauli word (pauli), extract its coefficient.
    """
    coeffs = list(pauli.terms.values())
    if len(coeffs) != 1:
        raise (ValueError("P given is not a single pauli word"))
    return coeffs[0]


def get_pauli_word(pauli: QubitOperator):
    """Given a single pauli word (pauli), extract the same word with coefficient 1.
    """
    words = list(pauli.terms.keys())
    if len(words) != 1:
        raise (ValueError("P given is not a single pauli word"))
    return QubitOperator(words[0])


def get_unitaries(taylor_sequences: list):
    """Given a list of pauli words, extracts the individual pauli operators in each word and the qubits they act on."""
    ### instantiate empty list to contain
    unitaries_and_qubits = []

    for i, terms in enumerate(taylor_sequences):
        for j, pauli in enumerate(terms):
            unitaries_and_qubits.append(get_pauli_word_tuple(pauli))

    return unitaries_and_qubits


def generate_taylor_series(
    hamiltonian: QubitOperator, order: int, time: float, steps: int
):
    """Generates the taylor series expansion of e^(-iHt/r) upt to order k.
    t is duration of simulation, and r is the number of timesteps in the simulation"""
    ### just defining imaginary unit here for convenience ###
    im = 1j
    ### list each order in the taylor series ###
    orders = []
    for i in range(order + 1):
        orders.append(i)
    ### return a list of taylor sequences up to order k, for each time step ###
    lcu = QubitOperator()
    for j, order in enumerate(orders):
        lcu += (((time / steps) ** order) / math.factorial(order)) * (
            (-im) * hamiltonian
        ) ** order
    return lcu


def generate_prepare_circuits(taylor_expansion: QubitOperator):
    """Returns prepare circuit for the coefficients in the taylor series expansion, as well as the unitaries to be
    applied to input initial state. """
    ### create a vector of the coefficients of the pauli words in the taylor series expansion
    non_normalized = []
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
            non_normalized.append(abs(coefficient))

        ### if coefficent c_i < 0, add |c_i| to amplitude vector
        elif coefficient < 0:
            state_vector.append(np.sqrt(abs(coefficient)) / np.sqrt(prefactor))
            single_terms.append(get_pauli_word(p))
            non_normalized.append(abs(coefficient))
        else:
            state_vector.append(cmath.sqrt(coefficient) / np.sqrt(prefactor))
            single_terms.append(get_pauli_word(p))
            non_normalized.append(abs(coefficient))

    ### if the number of terms is not a power of two, pad with zeros to make state vector length a power of 2
    if not np.log2(len(state_vector)).is_integer():
        n_qubits = int(np.ceil(np.log2(len(state_vector))))
        state_vector.extend([0] * (2 ** n_qubits - len(state_vector)))
        non_normalized.extend([0] * (2 ** n_qubits - len(state_vector)))
    elif int(np.ceil(np.log2(len(state_vector)))) == 0:
        n_qubits = 1
        state_vector.extend([0] * (2 ** n_qubits - len(state_vector)))
        non_normalized.extend([0] * (2 ** n_qubits - len(state_vector)))
    state_vector = np.array(state_vector)
    n_qubits = np.log2(len(state_vector))
    ### normalize the state vector
    norm = np.linalg.norm(state_vector)
    normalized_state_vector = state_vector
    ### now generate a circuit that will prepare desired linear comb. of basis states
    q = QuantumRegister(n_qubits, name="q")
    prep = QuantumCircuit(q)
    prep.initialize(normalized_state_vector, [(*q)])

    ### here just transpiling into one set for now, just for testing purposes. Will add more choices.
    ### can choose optimization level from 1-3, gretaer optimization takes more time
    ### so just took middle ground of optimization level = 2
    prep = transpile(
        prep, basis_gates=["id", "rx", "ry", "rz", "h", "cx"], optimization_level=2
    )
    return prep, single_terms


def get_binary(i: int, n_qubits: int):
    """Returns the binary representation of basis states in LCU. This function is important for the controlled unitaries
    in the select operator work correctly"""
    getbinary = lambda x, n: format(x, "b").zfill(n)
    bit_string = getbinary(i, n_qubits)
    return bit_string


def select_and_prep_dagger(
    unitaries_and_qubits: list,
    coefficients: list,
    prepare_circuit: QuantumCircuit,
    initial_state: QuantumCircuit,
):
    """Given a list of pauli words, a prepare circuit, and an input initial state, returns the SELECT operator for LCU,
    as well as appending prepare dagger thus completing the circuit"""
    n_ancillae = len(prepare_circuit.qubits)
    n_qubits = len(initial_state.qubits)
    lcu_circuit = QuantumCircuit(n_ancillae + n_qubits)
    lcu_circuit = lcu_circuit.compose(prepare_circuit, range(0, n_ancillae))
    lcu_circuit = lcu_circuit.compose(
        initial_state, range(n_ancillae, n_ancillae + n_qubits)
    )

    def control_sequence(bit_string: str, lcu_circuit: QuantumCircuit):
        """Makes sure correct unitary U_j is applied controlled by basis state |j>"""
        for k in range(len(bit_string)):
            if bit_string[k] == "0":
                lcu_circuit.x(k)

    def mcz(control: int, n_ancillae: int, lcu_circuit: QuantumCircuit):
        """Applies controlled Z gate using rotation HXH = Z"""
        lcu_circuit.h(control + n_ancillae)
        lcu_circuit.mct(list(range(0, n_ancillae)), control + n_ancillae)
        lcu_circuit.h(control + n_ancillae)

    def mcx(control: int, n_ancillae: int, lcu_circuit: QuantumCircuit):
        """Applies controlled X gate"""
        lcu_circuit.mct(list(range(0, n_ancillae)), control + n_ancillae)

    def mcy(control: int, n_ancillae: int, lcu_circuit: QuantumCircuit):
        """Applies controlled Y gate using rotation HSXS^+H = Y"""
        lcu_circuit.h(control + n_ancillae)
        lcu_circuit.s(control + n_ancillae)
        lcu_circuit.mct(list(range(0, n_ancillae)), control + n_ancillae)
        lcu_circuit.sdg(control + n_ancillae)
        lcu_circuit.h(control + n_ancillae)

    def mc_phase_shift(
        theta, control: int, n_ancillae: int, lcu_circuit: QuantumCircuit
    ):
        """"For complex coefficients of form Z=|r|(cos(theta) + isin(theta)), loads in the complex phase to the
        controlled unitaries using controlled phase-shift. Where a controlled phase shift of theta is achieved
        using CPhase_shift(theta) = P(theta)XP(theta)X"""
        mc_phase = PhaseGate(theta).control(n_ancillae, label=None)
        qubits = list(range(0, n_ancillae))
        qubits.append(control + n_ancillae)
        lcu_circuit.append(mc_phase, qubits)
        mcx(control, n_ancillae, lcu_circuit)
        lcu_circuit.append(mc_phase, qubits)
        mcx(control, n_ancillae, lcu_circuit)

    for i, paulis in enumerate(unitaries_and_qubits):
        bit_string = get_binary(i, n_ancillae)[::-1]

        if len(paulis) == 0:
            if isinstance(coefficients[i][0], complex):
                control_sequence(bit_string, lcu_circuit)
                angle = coefficients[i][1]
                mc_phase_shift(angle, 0, n_ancillae, lcu_circuit)

            elif coefficients[i][0] < 0:
                control_sequence(bit_string, lcu_circuit)
                ccrz = RZGate(2 * np.pi).control(n_ancillae, label=None)
                qubits = list(range(0, n_ancillae))
                qubits.append(0 + n_ancillae)
                lcu_circuit.append(ccrz, qubits)

            if coefficients[i][0] == 1:
                continue

        for j, controlled in enumerate(paulis):
            if j == 0:
                control_sequence(bit_string, lcu_circuit)

                if isinstance(coefficients[i][0], complex):
                    angle = coefficients[i][1]
                    mc_phase_shift(angle, controlled[0], n_ancillae, lcu_circuit)

                elif coefficients[i][0] < 0:
                    ccrz = RZGate(2 * np.pi).control(n_ancillae, label=None)
                    qubits = list(range(0, n_ancillae))
                    qubits.append(controlled[0] + n_ancillae)
                    lcu_circuit.append(ccrz, qubits)

            if controlled[1].lower() == "z":
                mcz(controlled[0], n_ancillae, lcu_circuit)

            if controlled[1].lower() == "x":
                lcu_circuit.mct(list(range(0, n_ancillae)), controlled[0] + n_ancillae)

            if controlled[1].lower() == "y":
                mcy(controlled[0], n_ancillae, lcu_circuit)

        control_sequence(bit_string, lcu_circuit)

    lcu_circuit = lcu_circuit.compose(prepare_circuit.inverse(), range(0, n_ancillae))

    return lcu_circuit
