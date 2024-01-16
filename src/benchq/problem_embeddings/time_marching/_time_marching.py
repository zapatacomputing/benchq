###############################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
###############################################################################
# Implementation of an algorithm for LDE solver based on the research paper
# "Time-marching based quantum solvers for time-dependent linear differential equations"
# (https://arxiv.org/abs/2208.06941)
from math import ceil
from typing import Tuple

import numpy as np
from orquestra.integrations.qiskit.conversions import (
    export_to_qiskit,
    import_from_qiskit,
)
from orquestra.quantum.circuits import PHASE, RZ, SX, Circuit, X
from qiskit import QuantumCircuit, transpile

from ..qsp._lin_and_dong_qsp import build_qsp_circuit
from ..quantum_program import QuantumProgram
from .compression_gadget import get_add_dagger, get_add_l
from .matrix_properties import get_degree, get_kappa, get_num_of_grid_points


def get_prep(grid_point: int, k: int, beta: float) -> Tuple[Circuit, Circuit]:
    """Constructs unitaries that prepare states COEF_k and COEF_k_prime
        corresponding to the z_k.

    Args:
        grid_point (int): a current grid point of out the total k points.
        k (int): The number of the grid points to approximate the countour
            integral.
        beta (float): bounding parameter of the matrix.

    Returns:
        prep, prep_prime (Circuit): unitary corresponding to
            PREP and PREP_prime.
    """

    alpha = beta / 2.0
    theta = np.arcsin(np.sqrt((alpha) / (beta + alpha)))  # theta/2
    prep = Circuit()
    prep_prime = Circuit()
    phi = np.pi * grid_point / k

    # decompose using U3
    prep += PHASE(-3 * phi / 2 - theta / 2 - np.pi / 2)(0)
    prep += RZ(-phi + np.pi)(0)  # P gate
    prep += SX.dagger(0)
    prep += RZ(2 * theta + np.pi)(0)
    prep += SX(0)

    prep_prime += PHASE(-3 * phi / 2 - theta / 2 - np.pi / 2)(0)
    prep_prime += RZ(phi + np.pi)(0)
    prep_prime += SX.dagger(0)
    prep_prime += RZ(-2 * theta + np.pi)(0)
    prep_prime += SX(0)

    return prep, prep_prime


def control_prep(k: int, beta: float) -> Tuple[Circuit, Circuit]:
    """Constructs the control-PREP and control-PREP_prime unitaries.

    Args:
        k (int): The numper of the grid points to approximate
            the countour integral.
        beta (float): bounding parameter of the matrix.

    Returns:
        c_prep, c_prep_prime (Circuit): control-unitaries of
            PREP and PREP_prime.
    """

    if k <= 0:
        raise ValueError("The number of grid points should be non-negative.")

    n_controlled_qubits = int(np.ceil(np.log2(k)))
    c_prep = Circuit()
    c_prep_prime = Circuit()

    for grid_point in range(k):
        binary = bin(grid_point)[2::]
        reversed_bin = binary[::-1]
        ones = [ind for ind, digit in enumerate(reversed_bin) if digit == "1"]

        c_prep += Circuit([X(i) for i in range(n_controlled_qubits) if i not in ones])
        c_prep_prime += Circuit(
            [X(i) for i in range(n_controlled_qubits) if i not in ones]
        )

        prep, prep_prime = get_prep(grid_point, k, beta)
        for qubit in range(n_controlled_qubits):
            prep = prep.controlled(qubit)
            prep_prime = prep_prime.controlled(qubit)

        c_prep += prep
        c_prep_prime += prep_prime
        c_prep += Circuit([X(i) for i in range(n_controlled_qubits) if i not in ones])
        c_prep_prime += Circuit(
            [X(i) for i in range(n_controlled_qubits) if i not in ones]
        )

    return c_prep, c_prep_prime


def inverse_block_encoding(
    be_matrix: Circuit, matrix_norm: float, time: float, beta: float, epsilon: float
) -> Circuit:
    """Constructs SEL_inv, an inverse of the block encoding, utilizing the QSP.
    SEL_inv represents the inverse of a single time step evolution of the LDE,
    and is described by 1/(z-z0) as given in the Cauchy's formula for contour integral.

    Args:
        be_matrix (Circuit): the block encoding of a matrix.
        matrix_norm (float): Frobenius norm of the matrix that is
            to be block encoded.
        time (float): the time interval one seeks solution
            for a differntial equation.
        beta (float): a bounding parameter of the matrix.
        epsilon (float): an accuracy for the polynomial approximation.

    Returns:
        sel_inverse (Circuit): an Orquestra quantum circuit representing
            the inverse of block encoding.
    """

    # number of grid points
    k = get_num_of_grid_points(matrix_norm, epsilon, beta)
    kappa = get_kappa(matrix_norm, time)
    num_phis = get_degree(kappa, epsilon)
    # generate arbitrary phases
    phi_seq = np.linspace(-np.pi, np.pi, num_phis)

    prep, prep_prime = control_prep(k=k, beta=beta)
    prep_prime_dag = prep_prime.inverse()
    grid_qubits = ceil(np.log2(k))

    # contruct the circuit representing SEL
    sel = Circuit()
    sel += prep
    shifted_be_matrix = Circuit(
        [
            op.gate(*[qubit + grid_qubits for qubit in op.qubit_indices])
            for op in be_matrix.operations
        ]
    )
    shifted_be_matrix = shifted_be_matrix.controlled(grid_qubits - 1)
    sel += shifted_be_matrix
    sel += prep_prime_dag

    # Construct QSP circuit in Qiskit
    qsp_qubits = sel.n_qubits + 1
    qiskit_sel = export_to_qiskit(sel)
    sel_inverse = build_qsp_circuit(qsp_qubits, qiskit_sel, phi_seq, realpart=True)

    return import_from_qiskit(sel_inverse)


def get_prep_int(
    matrix_norm: float, beta: float, epsilon: float
) -> Tuple[Circuit, Circuit]:
    """Constructs unitaries that prepare states COEF_int and COEF_int_prime
        to encode the amplitude coefficients. COEF_int_prime is complex conjugate
        of COEF_int.

    Args:
        matrix_norm (float): Frobenius norm of the matrix that is
            to be block encoded.
        beta (float): bounding parameter of the matrix.
        epsilon (float): an accuracy for the polynomial approximation.

    Returns:
        prep_int, prep__int_prime (Circuit): unitaries corresponding to
            PREP_int and PREP_int_prime.
    """

    k = get_num_of_grid_points(matrix_norm, epsilon, beta)
    num_qubits = ceil(np.log2(k))

    z_k = [beta * np.exp(2 * np.pi * 1.0j * i / k) for i in range(k)]
    # construct COEF_int and PRIME_int
    unnorm_state = np.sqrt(z_k * np.exp(z_k))
    norm_state = unnorm_state / np.linalg.norm(unnorm_state)
    coef_int = np.pad(norm_state, (0, 2**num_qubits - k))  # pad with 0's

    prep_int = QuantumCircuit(num_qubits)
    prep_int.initialize(coef_int, prep_int.qubits)
    prep_int = transpile(prep_int, basis_gates=["rz", "h", "cx"])

    # construct COEF_int_prime and PRIME_int_prime
    unnorm_state_prime = np.conjugate(unnorm_state)
    norm_state_prime = unnorm_state_prime / np.linalg.norm(unnorm_state_prime)
    coef_int_prime = np.pad(norm_state_prime, (0, 2**num_qubits - k))

    prep_int_prime = QuantumCircuit(num_qubits)
    prep_int_prime.initialize(coef_int_prime, prep_int_prime.qubits)
    prep_int_prime = transpile(prep_int_prime, basis_gates=["rz", "h", "cx"])

    return import_from_qiskit(prep_int), import_from_qiskit(prep_int_prime)


def matrix_exponentiation(
    be_matrix: Circuit, matrix_norm: float, time: float, beta: float, epsilon: float
) -> Circuit:
    """Constructs the quantum circuit for a single time step in the
    time-marching algorithm - construct the approximation f_K(A)=exp(A).

    The PREP_int unitary acts on ceil(log2(K)) qubits starting from the second qubit.
    The SEL_inv unitary acts on all qubits.
    The PREP_int_prime_dag unitary acts on ceil(log2(K)) qubits starting from
    the second qubit.

    The unitaries are appended in the following order
    PREP_int * SEL_inv * PREP_int_prime_dag.

    Args:
        be_matrix (Circuit): the block encoding of a matrix.
        matrix_norm (float): the norm of the matrix that is
            to be block encoded.
        time (float): the time interval one seeks solution
            for a differntial equation.
        beta (float): an upper bound for the largest eigenvalue of the block encoding.
        epsilon (float): an accuracy for the polynomial approximation.

    Returns:
        matrix_exp (Circuit): a quantum circuit corresponding to
            the approximation exp(A)=f(A).
    """
    prep_int, prep_int_prime = get_prep_int(matrix_norm, beta, epsilon)
    sel_inverse = inverse_block_encoding(be_matrix, matrix_norm, time, beta, epsilon)
    # shifting indices
    shifted_prep_int = Circuit(
        [
            op.gate(*[qubit + 1 for qubit in op.qubit_indices])
            for op in prep_int.operations
        ]
    )
    shifted_prep_dag = Circuit(
        [
            op.gate(*[qubit + 1 for qubit in op.qubit_indices])
            for op in prep_int_prime.inverse().operations
        ]
    )
    # appending quantum circuits in the order: PREP_int * SEL_inv * PREP_int_prime_dag.
    matrix_exp = Circuit()
    matrix_exp += shifted_prep_int
    matrix_exp += sel_inverse
    matrix_exp += shifted_prep_dag

    return matrix_exp


def get_time_marching_program(
    phases,
    L: int,
    n: int,
    be_matrix: Circuit,
    matrix_norm: float,
    time: float,
    beta: float,
    epsilon: float,
) -> QuantumProgram:
    """Coherently multiply unitaries representing a single time step such that
    the result of the multiplication is the solution to the given differential equation.
    To propagate the differential equation in time with a high probability,
    use the compression gadget and the uniform singular value amplification as
    described in Sections (2.3-2.4) and Appendices (C-D) of the research paper
    (https://arxiv.org/abs/2208.06941).

    Args:
        phases (): a sequence of phase angles used to construct QSVT procedure
            with an odd polynomial.
        L (int): number of time steps.
        n (int): size of the matrix that governs differential equation.
        be_matrix (Circuit): the block encoding of a matrix.
        matrix_norm (float): the norm of the matrix that is to be block encoded.
        time (float): the time interval one seeks solution for a differntial equation.
        beta (float): an upper bound for the largest eigenvalue of the block encoding.
        epsilon (float): an accuracy for the polynomial approximation.

    Return:
        long_time_propagator (QuantumProgram): an QuantumProgram instance representing
            a quantum circuit for the time-marching algorithm.
    """
    qubits_to_shift = ceil(np.log2(L)) + 1
    add_dagger = get_add_dagger(L)

    # Assuming a uniform time interval.
    single_time_step = matrix_exponentiation(
        be_matrix, matrix_norm, time, beta, epsilon
    )
    qsp_qubits = single_time_step.n_qubits + 1
    amplified_single_time_step = import_from_qiskit(
        build_qsp_circuit(
            qsp_qubits, export_to_qiskit(single_time_step), phases, realpart=True
        )
    )
    amplified_shifted = Circuit(
        [
            op.gate(*[qubit + qubits_to_shift for qubit in op.qubit_indices])
            for op in amplified_single_time_step.operations
        ]
    )

    short_time_propagator = Circuit()
    short_time_propagator += amplified_shifted
    num_control_qubits = qsp_qubits - n
    for q in range(num_control_qubits):
        control_add_dag = add_dagger.controlled(qubits_to_shift + q)
    short_time_propagator += control_add_dag

    return QuantumProgram(
        [get_add_l(L), short_time_propagator], L, lambda x: [0] + [1] * x
    )
