import cmath
import math
import random
from typing import Optional, Union

import numpy as np
from openfermion import count_qubits
from openfermion.ops import QubitOperator
from orquestra.integrations.cirq.conversions import to_openfermion
from orquestra.integrations.qiskit.conversions import import_from_qiskit
from orquestra.quantum.operators import PauliRepresentation, PauliSum
from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit.library import PhaseGate, RZGate

from ..data_structures import QuantumProgram, get_program_from_circuit


def get_angles_for_taylor_steps(taylor_steps):
    coefficients_and_angles = []
    words = get_pauliword_list(taylor_steps)
    for i, word in enumerate(words):
        coefficient = get_pauli_word_coefficient(word)
        coefficients_and_angles.append(
            tuple((coefficient, cmath.polar(coefficient)[1]))
        )
    return coefficients_and_angles


def generate_random_initial_state(n_qubits):
    """Makes a random Hartree-Fock initial state as input to LCU algorithm.
    Useful for testing purposes, and can be used as a general template
    for making HF states."""

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


def get_pauli_word_tuple(pauli: QubitOperator):
    """Given a single pauli word Pauli, extract the tuple representing the word."""
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
    """Given a single pauli word (pauli), extract its coefficient."""
    coeffs = list(pauli.terms.values())
    if len(coeffs) != 1:
        raise (ValueError("P given is not a single pauli word"))
    return coeffs[0]


def get_pauli_word(pauli: QubitOperator):
    """Given a single pauli word (pauli), extract the same word with coefficient 1."""
    words = list(pauli.terms.keys())
    if len(words) != 1:
        raise (ValueError("P given is not a single pauli word"))
    return QubitOperator(words[0])


def get_unitaries(taylor_sequences: list):
    """Given a list of pauli words, extracts the individual pauli operators
    in each word and the qubits they act on.
    """
    ### instantiate empty list to contain
    unitaries_and_qubits = []

    for i, terms in enumerate(taylor_sequences):
        for j, pauli in enumerate(terms):
            unitaries_and_qubits.append(get_pauli_word_tuple(pauli))

    return unitaries_and_qubits


def generate_taylor_series(
    hamiltonian: Union[PauliRepresentation, QubitOperator],
    order: int,
    time: float,
    steps: int,
) -> QubitOperator:
    """Generates the taylor series expansion of e^(-iHt/r) upt to order k.
    t is duration of simulation, and r is the number of timesteps in the simulation"""
    if isinstance(hamiltonian, PauliSum):
        hamiltonian = to_openfermion(hamiltonian)
    ### just defining imaginary unit here for convenience ###
    im = 1j
    ### list each order in the taylor series ###
    orders = list(range(order + 1))
    ### return a list of taylor sequences up to order k, for each time step ###
    lcu = QubitOperator()
    for order in orders:
        lcu += (((time / steps) ** order) / math.factorial(order)) * (
            (-im) * hamiltonian
        ) ** order

    return lcu


def generate_prepare_circuits(taylor_expansion: QubitOperator):
    """Returns prepare circuit for the coefficients in the taylor series expansion,
    as well as the unitaries to be applied to input initial state."""
    ### create a vector of the coefficients of the pauli words
    # in the taylor series expansion
    non_normalized = []
    coeffs = list(taylor_expansion.terms.values())
    coeff_magnitude = [abs(term) for term in coeffs]
    prefactor = sum(coeff_magnitude)
    paulis = get_pauliword_list(taylor_expansion)
    state_vector = []
    single_terms = []
    for i, p in enumerate(paulis):
        coefficient = get_pauli_word_coefficient(p)

        ### If coefficient, c_i is complex add |c_i| to amplitude vector
        if isinstance(coefficient, complex) or coefficient < 0:
            state_vector.append(np.sqrt(abs(coefficient)) / np.sqrt(prefactor))
        else:
            state_vector.append(cmath.sqrt(coefficient) / np.sqrt(prefactor))
        single_terms.append(get_pauli_word(p))
        non_normalized.append(abs(coefficient))

    ### if the number of terms is not a power of two, pad with zeros
    # to make state vector length a power of 2
    if not np.log2(len(state_vector)).is_integer():
        n_qubits = int(np.ceil(np.log2(len(state_vector))))
        state_vector.extend([0] * (2**n_qubits - len(state_vector)))
        non_normalized.extend([0] * (2**n_qubits - len(state_vector)))
    elif int(np.ceil(np.log2(len(state_vector)))) == 0:
        n_qubits = 1
        state_vector.extend([0] * (2**n_qubits - len(state_vector)))
        non_normalized.extend([0] * (2**n_qubits - len(state_vector)))

    n_qubits = np.log2(len(state_vector))
    ### normalize the state vector
    norm = np.linalg.norm(state_vector)
    normalized_state_vector = np.array(state_vector) / norm
    ### now generate a circuit that will prepare desired linear comb. of basis states
    q = QuantumRegister(n_qubits, name="q")
    prep = QuantumCircuit(q)
    prep.initialize(normalized_state_vector, qubits=q)
    # We need to transpile the circuit to the basis_gates in order
    # to perform resource estimation.
    prep = transpile(
        prep, basis_gates=["id", "rx", "ry", "rz", "h", "cx"], optimization_level=2
    )
    return prep, single_terms


def select_and_prep_dagger(
    unitaries_and_qubits: list,
    coefficients: list,
    prepare_circuit: QuantumCircuit,
    initial_state: QuantumCircuit,
):
    """Given a list of pauli words, a prepare circuit, and an input initial state,
    returns the SELECT operator for LCU,
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
        """ "For complex coefficients of form Z=|r|(cos(theta) + isin(theta)),
        loads in the complex phase to the controlled unitaries using controlled
        phase-shift. Where a controlled phase shift of theta is achieved
        using CPhase_shift(theta) = P(theta)XP(theta)X"""
        mc_phase = PhaseGate(theta).control(n_ancillae, label=None)
        qubits = list(range(0, n_ancillae))
        qubits.append(control + n_ancillae)
        lcu_circuit.append(mc_phase, qubits)
        mcx(control, n_ancillae, lcu_circuit)
        lcu_circuit.append(mc_phase, qubits)
        mcx(control, n_ancillae, lcu_circuit)

    for i, paulis in enumerate(unitaries_and_qubits):
        bit_string = format(i, "b").zfill(n_ancillae)[::-1]

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


def generate_lcu_taylorization_program(
    operator: PauliRepresentation,
    time: int = 1,
    steps: int = 2,
    order: int = 15,
    initial_state: Optional[QuantumCircuit] = None,
) -> QuantumProgram:
    # We could calculate steps automatically
    # see eq 4 in https://arxiv.org/pdf/1412.4687.pdf
    taylor_series = generate_taylor_series(
        operator, order=order, time=time, steps=steps
    )

    n_qubits = count_qubits(operator)
    if initial_state is None:
        initial_state = generate_random_initial_state(n_qubits)[1]
    prepare_circuit, terms = generate_prepare_circuits(
        taylor_series
    )  # This goes to ancilla qubits
    unitaries_and_qubits = get_unitaries(terms)
    coefficients_and_angles = get_angles_for_taylor_steps(taylor_series)

    lcu_circuit = select_and_prep_dagger(
        unitaries_and_qubits,
        coefficients_and_angles,
        prepare_circuit,
        initial_state,
    )
    lcu_circuit = import_from_qiskit(lcu_circuit)
    return get_program_from_circuit(lcu_circuit)
