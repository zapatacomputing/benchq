################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
# An example on resourse estimates for OLDE.
from typing import Iterable

import numpy as np
from orquestra.quantum.circuits import GateOperation, load_circuit, save_circuit
from orquestra.quantum.decompositions._decomposition import DecompositionRule

from benchq.algorithms.block_encodings.offset_tridiagonal import (
    get_offset_tridagonal_block_encoding,
)
from benchq.algorithms.lde_solver import get_kappa, long_time_propagator
from benchq.algorithms.utils.convex_optimization import optimize_chebyshev_coeff
from benchq.algorithms.utils.qsp_solver import qsp_solver
from benchq.compilation import (
    pyliqtr_transpile_to_clifford_t,
    transpile_to_native_gates,
)
from benchq.compilation.transpile_to_native_gates import decompose_benchq_circuit
from benchq.data_structures import get_program_from_circuit


class Remove_Multicontrol(DecompositionRule[GateOperation]):
    """Dummy gates decomposition for the multirotation gates."""

    def predicate(self, operation: GateOperation) -> bool:
        if operation.gate.name == "Control" and operation.gate.num_control_qubits > 1:
            return True
        return False

    def production(self, operation: GateOperation) -> Iterable[GateOperation]:
        return []


de_parameters = {
    "total_time": 0.1,
    "steps_number": 1,
    "a": 0.4,
    "b": 0,
    "c": 0,
    "matrix_size": 1,
    "error_cheb_expansion": 0.1,
    "epsilon_matrix_inversion": 1e-2,
    "beta_contour_integral": 1.3,
}


def run_time_marching():
    """A tutorial function intending to expalain how to run the time-marching solver.

    Note: please be patient. Constructing a circuit for a DE can take some time.
    The wait time will increase with the increase of the 'steps_number' and the accuracy
    on the solution. Consider to save and load circuit from saved files once
    the time-marching circuit is generated.

    Parameters to solve a differential equation:
        total_time (float): the time interval one seeks the solution to the IVP.
        steps_number (int): number of time steps in the time-marching solver.
        delta_t (float): a single time step.
        delta (float): an overshooting parameter for the Uniform Singular Value
            Amplification which is used to solve for phases of USVA.
        error_cheb_expansion (float): a desired accuracy of Chebyshev expansion.
        gamma_prime (): an upper bound on the singular values of the block encoding
            of Xi. Define: gamma_prime <= exp(delta_t * ||A||).

        a,b,c (float): entries of the offset tridagonal matrix A where matrix A governs
            a differential equation.
        n (int): size of the A matrix.
        epsilon_matrix_inversion (float): a desired precision in the matrix inversion
            problem.
        beta_contour_integral (float): radius of the contour integral. Upper bounds
            the matrix A eigenvalues.

    Steps in finding a quantum circuit for the given OLDE and
        running the resource estimation:
        1. Call 'optimize_chebyshev_coeff' function to find an a polynomial for the USVA
            procedure. If Exception is raised then the problem is not feasible.
            Adjusting time and/or accuracy of the Chebyshev expansion could help.
        2. Call 'qsp_solver' function passing the Chebyshev coefficients to solve
            for the phases in the USVA procedure.
        3. Call 'get_offset_tridagonal_block_encoding' function to block encode
            the matrix A. Note: the block-encoding of the matrix A contains a single
            time step. The etries in the block-encoding matrix can not be greater than
            certain threshold. For more details, see
            'get_offset_tridagonal_block_encoding'.
        4. Call 'long_time_integrator'. The result is a quantum circuit corresponding
            to the given OLDE. (Note: at the end of the circuit, there should be
            a standard amplitude amplification)
        5. Estimate the quantum resources required to execute the time-marching
            based quantum based solver.
    """

    delta_t = de_parameters["total_time"] / de_parameters["steps_number"]
    delta = 1 / de_parameters["steps_number"]
    n = de_parameters["matrix_size"]
    a_matrix = np.diag(de_parameters["a"] * delta_t * np.ones(2**n))
    b_matrix = np.diag(de_parameters["b"] * delta_t * np.ones(2**n - 2), k=-2)
    c_matrix = np.diag(de_parameters["c"] * delta_t * np.ones(2**n - 2), k=2)
    A_matrix = a_matrix + b_matrix + c_matrix
    A_matrix_norm = np.linalg.norm(A_matrix, "fro")
    # gamma_prime = np.sqrt(get_kappa(A_matrix_norm, delta_t))
    gamma_prime = 4.75

    try:
        chev_coeff, _, _ = optimize_chebyshev_coeff(
            error=de_parameters["error_cheb_expansion"],
            delta=delta,
            gamma_prime=gamma_prime,
        )
    except Exception:
        print("Not able to amplify singular values")
        exit()
    try:
        a = delta_t * de_parameters["a"]
        b = delta_t * de_parameters["b"]
        c = delta_t * de_parameters["c"]
        be_circuit = get_offset_tridagonal_block_encoding(n=n, a=a, b=b, c=c)
    except AssertionError:
        print("Not possible to construct a block encoding for the given entries")
        exit()
    phases, _ = qsp_solver(chev_coeff, parity=1, options={"criteria": 1e-3})
    # construct a time-marching circuit for the given parameters set
    time_marching_cir = long_time_propagator(
        phases,
        de_parameters["steps_number"],
        n,
        be_circuit,
        A_matrix_norm,
        delta_t,
        de_parameters["beta_contour_integral"],
        de_parameters["epsilon_matrix_inversion"],
    )

    # Save the time-marching circuit once it has been generated and load from file
    # to speed up the resource estimates.
    # save_circuit("time_marching_circuit.txt")
    # time_marching_cir = load_circuit("time_marching_circuit.txt")

    # Run resource estimates
    decomposed_cir = decompose_benchq_circuit(
        time_marching_cir, [Remove_Multicontrol()]
    )
    native_gates = transpile_to_native_gates(decomposed_cir)
    clifford_t = pyliqtr_transpile_to_clifford_t(native_gates, 1e-2)
    quantum_program = get_program_from_circuit(clifford_t)
    print(f"Number of T and T_dag gates: {quantum_program.n_t_gates}")
