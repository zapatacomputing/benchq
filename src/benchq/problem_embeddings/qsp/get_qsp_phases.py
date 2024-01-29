# Copyright (c) 2020, University of California, Berkeley.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# (1) Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# (2) Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# (3) Neither the name of the University of California, Berkeley, nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Given the coefficients of the Chebyshev expansion, solve the optimization problem
# for gate phases.
#
# This is a Python translation of algorithm in QSPPACK
# (https://github.com/qsppack/QSPPACK/tree/master).
# The authors of the code are Yulong Dong and Lin Lin.
#
# The authors of the code translation are Bartu Bisgin, Erfan Abedi, Martin Mauser,
# Uzay. The original code translation is avaliable in
# (https://github.com/bartubisgin/QSVTinQiskit-2021-Europe-Hackathon-Winning-Project-)
import time
from typing import Callable, Dict, Tuple, Union

import numpy as np


def qsp_lbfgs(
    obj: Callable,
    grad: Callable,
    delta: np.ndarray,
    phi: np.ndarray,
    options: dict,
) -> Tuple[np.ndarray, float, Dict]:
    """Solving phase factors optimization via L-BFGS.

    Args:
        obj (Callable): Objective function L(phi) (Should also be given in grad).
        grad (Callable): Gradient of obj function.
        delta (np.ndarray): Samples.
        phi (np.ndarray): Initial value.
        options (dict): Options structure with fields
            maxiter: max iteration
            gamma: linesearch retraction rate
            accrate: linesearch accept ratio
            minstep: minimal stepsize
            criteria: stop criteria for obj value on Chevyshev points
            lmem: L-BFGS memory size
            print: whether to output
            itprint: print frequency
            parity: parity of polynomial (0 -- even, 1 -- odd)
            target: target polynomial

    Returns:
        phi (np.ndarray): Solution of phase factors optimization.
        obj_value (float): Objection value at optimal point L(phi^*).
        out (dict): Information about solving process.
    """

    if "maxiter" not in options:
        options["maxiter"] = 5e4
    if "gamma" not in options:
        options["gamma"] = 0.5
    if "accrate" not in options:
        options["accrate"] = 1e-3
    if "minstep" not in options:
        options["minstep"] = 1e-5
    if "criteria" not in options:
        options["criteria"] = 1e-12
    if "lmem" not in options:
        options["lmem"] = 200
    if "print" not in options:
        options["print"] = 1
    if "itprint" not in options:
        options["itprint"] = 1

    # stra1 = ['%4s','%13s','%10s','%10s','\n'];
    str_head = ["iter", "obj", "stepsize", "des_ratio"]
    str_num = "%4d %+5.4E %+3.2E %+3.2E \n"

    out = dict()

    # Copy values to parameters
    maxiter = options["maxiter"]
    gamma = options["gamma"]
    accrate = options["accrate"]
    lmem = options["lmem"]
    minstep = options["minstep"]
    pri = options["print"]
    itprint = options["itprint"]
    crit = options["criteria"]

    iter_ = 0
    d = len(phi)
    mem_size = 0
    mem_now = 0
    mem_grad = np.zeros((lmem, d))
    mem_obj = np.zeros((lmem, d))
    mem_dot = np.zeros((lmem,))
    [grad_s, obj_s] = grad(phi, delta, options)
    obj_value = np.mean(obj_s)
    GRAD = np.mean(grad_s, axis=0)

    # Start L-BFGS
    if pri:
        print("L-BFGS solver started")
    while True:
        iter_ += 1
        theta_d = GRAD.copy()
        alpha = np.zeros((mem_size, 1))
        for i in range(mem_size):
            subsc = np.mod(mem_now - i, lmem)
            alpha[i] = mem_dot[i] * (mem_obj[subsc, :] @ theta_d)
            theta_d -= alpha[i] * mem_grad[subsc, :].conj()
            # print(i, iter_)

        theta_d *= 0.5
        if options["parity"] == 0:
            theta_d[0] *= 2

            for i in range(mem_size):
                subsc = np.mod(mem_now - (mem_size - i) - 1, lmem)
                beta = mem_dot[subsc] * (mem_grad[subsc, :] @ theta_d)
                theta_d += (alpha[mem_size - i - 1] - beta) * mem_obj[subsc, :].conj()

        step = 1
        exp_des = GRAD.conj() @ theta_d
        while True:
            theta_new = phi - step * theta_d
            obj_snew = obj(theta_new, delta, options)
            obj_valuenew = np.mean(obj_snew)
            ad = obj_value - obj_valuenew
            if ad > exp_des * accrate * step or step < minstep:
                break
            step *= gamma

        phi = theta_new
        obj_value = obj_valuenew
        obj_max = np.max(obj_snew)
        [grad_s, _] = grad(phi, delta, options)
        GRAD_new = np.mean(grad_s, axis=0)
        mem_size = np.min([lmem, mem_size + 1])
        mem_now = np.mod(mem_now, lmem)
        mem_grad[mem_now, :] = GRAD_new - GRAD
        mem_obj[mem_now, :] = -step * theta_d
        mem_dot[mem_now] = 1 / (mem_grad[mem_now, :] @ mem_obj[mem_now, :].conj())
        GRAD = GRAD_new
        if pri and np.mod(iter_, itprint) == 0:
            if iter_ == 1 or np.mod(iter_ - itprint, itprint * 10) == 0:
                print(str_head)
            print(str_num % (iter_, obj_max, step, ad / (exp_des * step)))

        if iter_ >= maxiter:
            print("Max iteration reached")
            break

        if obj_max < crit**2:
            print("Stop criteria satisfied")
            break

    out["iter"] = iter_

    return phi, obj_value, out


def cheby_coeff_to_func(
    x: Union[np.ndarray, float],
    coeff: np.ndarray,
    parity: int,
    partialcoeff: bool,
) -> np.ndarray:
    """Evaluate function based on Chebyshev expansion coefficients.

    Args:
        x (float): an argument to evaluate function a, where function is the linear
            combination of Chebyshev polynomials.
        coeff (np.ndarray): coefficients in Chebyshev expantion.
        parity (int): 0 for even, 1 for odd.
        partialcoef (bool): true: only include even/odd coefficiennts.

    Return:
        result (np.ndarray): function evaluated at x.
    """
    if isinstance(x, np.float64):
        result = np.zeros((1, 1))
    elif isinstance(x, np.ndarray):
        result = np.zeros((len(x), 1))

    y = np.arccos(x)
    len_coeff = len(coeff)
    if partialcoeff:
        if parity == 0:
            for k in range(len_coeff):
                result += coeff[k] * np.cos(2 * k * y)
        else:
            for k in range(len_coeff):
                result += coeff[k] * np.cos((2 * (k + 1) - 1) * y)
    else:
        if parity == 0:
            for k in range(0, len_coeff, 2):
                result += coeff[k] * np.cos(k * y)
        else:
            for k in range(1, len_coeff, 2):
                result += coeff[k] * np.cos(k * y)

    return result


def qsp_get_unit_sym(phi: np.ndarray, x: float, parity: int) -> np.ndarray:
    """Get the QSP unitary matrix based on given phase vector and point x in [-1, 1].

    Args:
        phi (np.ndarray): The phase factors.
        x (float64): Point to be evaluated
       parity (int): Parity of phi (0 -- even, 1 -- odd)

    Return:
        qspmat (np.ndarray): The QSP unitary matrix.
    """
    Wx = np.array([[x, 1j * np.sqrt(1 - x**2)], [1j * np.sqrt(1 - x**2), x]])

    gate = np.array([[np.exp(1j * np.pi / 4), 0], [0, np.exp(-1j * np.pi / 4)]])

    exp_phi = np.exp(1j * phi)

    # Caused a problem here ?
    # sqrt(1-x^2) becomes a problem here because x = 0.99999 instead of 1
    if parity == 1:
        result = np.array([[exp_phi[0], 0], [0, exp_phi[0].conj()]])
        for k in range(1, len(exp_phi)):
            result = result @ Wx @ np.array([[exp_phi[k], 0], [0, exp_phi[k].conj()]])
        result = result @ gate
        qspmat = result.T @ Wx @ result
    else:
        result = np.eye(2)
        for k in range(1, len(exp_phi)):
            # @= is not yet supported (why?)
            result = result @ Wx * np.array([[exp_phi[k], 0], [0, exp_phi[k].conj()]])
        result = result @ gate
        qspmat = result.T @ np.array([[exp_phi[0], 0], [0, exp_phi[1].conj()]]) @ result

    return qspmat


def qsp_obj_sym(phi: np.ndarray, delta: np.ndarray, options: dict) -> np.ndarray:
    """Evalute the objective of QSP function, provided that phi is symmetric.

    Args:
        phi (np.ndarray): Variables.
        delta (np.ndarray): Samples.
        opts (dict): Options structure with fields
                target: target function
                parity: parity of phi (0 -- even, 1 -- odd)

    Return:
        obj (np.ndarray): Objective function value.
    """
    m = len(delta)
    obj = np.zeros((m, 1))

    for i in range(m):
        qspmat = qsp_get_unit_sym(phi, delta[i], options["parity"])
        obj[i] = 0.5 * (np.real(qspmat[0, 0]) - options["target"](delta[i])) ** 2

    return obj


def qsp_grad_sym(
    phi: np.ndarray, delta: np.ndarray, options: dict
) -> Tuple[object, object]:
    """Evalutes the gradient and objective of QSP function, provided that
    phi is symmetric.

    Args:
        phi (np.ndarray): Variables.
        delta (np.ndarray) Samples.
        opts (dict): Options structure with fields
            target: target function
            parity: parity of phi (0 -- even, 1 -- odd)

    Returns:
        grad (np.ndarray): Gradient of objective function.
        obj (np.ndarray): Objective function value.
    """
    m = len(delta)
    d = len(phi)
    obj = np.zeros((m, 1))
    grad = np.zeros((m, d))
    gate = np.array([[np.exp(1j * np.pi / 4), 0], [0, np.exp(-1j * np.pi / 4)]])

    exp_theta = np.exp(1j * phi)
    targetx = options["target"]
    parity = options["parity"]

    for i in range(m):
        x = delta[i]
        Wx = np.array([[x, 1j * np.sqrt(1 - x**2)], [1j * np.sqrt(1 - x**2), x]])
        temp_save_1 = np.zeros((2, 2, d), dtype=np.complex128)
        temp_save_2 = np.zeros((2, 2, d), dtype=np.complex128)

        temp_save_1[:, :, 0] = np.eye(2)
        # Remove the exp_theta[d-1 , ""0""]" s here ?
        temp_save_2[:, :, 0] = (
            np.array([[exp_theta[d - 1], 0], [0, exp_theta[d - 1].conj()]]) @ gate
        )

        for j in range(1, d):
            temp_save_1[:, :, j] = (
                temp_save_1[:, :, j - 1]
                * np.array([exp_theta[j - 1], exp_theta[j - 1].conj()])
                @ Wx
            )
            ## Here
            temp_save_2[:, :, j] = (
                np.array([[exp_theta[d - j - 1]], [exp_theta[d - j - 1].conj()]])
                * Wx
                @ temp_save_2[:, :, j - 1]
            )

        if parity == 1:
            qsp_mat = temp_save_2[:, :, d - 1].T @ Wx @ temp_save_2[:, :, d - 1]
            gap = np.real(qsp_mat[0, 0]) - targetx(x)
            leftmat = temp_save_2[:, :, d - 1].T @ Wx

            for j in range(d):
                grad_temp = (
                    leftmat
                    @ temp_save_1[:, :, j]
                    * np.array([1j, -1j])
                    @ temp_save_2[:, :, d - j - 1]
                )
                grad[i][j] = 2 * np.real(grad_temp[0, 0]) * gap

            obj[i] = 0.5 * (np.real(qsp_mat[0, 0]) - targetx(x)) ** 2
        else:
            qsp_mat = temp_save_2[:, :, d - 2].T @ Wx @ temp_save_2[:, :, d - 1]
            gap = np.real(qsp_mat[0, 0] - targetx(x))
            leftmat = temp_save_2[:, :, d - 2].T @ Wx
            for j in range(d):
                grad_temp = (
                    leftmat
                    @ temp_save_1[:, :, j]
                    * np.array([1j, -1j])
                    @ temp_save_2[:, :, d - j - 1]
                )
                # might be a bit shaky
                grad[i, j] = 2 * np.real(grad_temp[0, 0]) * gap

            grad[i, 0] /= 2
            obj[i] = 0.5 * np.real(qsp_mat[0, 0] - targetx(x)) ** 2

    return grad, obj


def get_qsp_phases(
    coeff: np.ndarray, parity: int, options: dict
) -> Tuple[object, object]:
    """Given coefficients of a polynomial P, yield corresponding phase factors.

    The reference chose the first half of the phase factors as the
    optimization variables, while in the code we used the second half of the
    phase factors. These two formulations are equivalent.

    To simplify the representation, a constant pi/4 is added to both sides of
    the phase factors when evaluating the objective and the gradient. In the
    output, the FULL phase factors with pi/4 are given.

    Args:
        coeff (Iterable): Coefficients of polynomial P under Chevyshev basis, P
            should be even/odd, only provide non-zero coefficients.
        parity (int): Parity of polynomial P (0 -- even, 1 -- odd).
        opts (dict): Options structure with fields. Criteria: stop criteria.

    Returns:
        phi_proc (Iterable): Solution of optimization problem, FULL phase factors.
        out (dict): Information of solving process.
    """
    if "criteria" not in options:
        options["criteria"] = 1e-12

    # out = ()
    tot_len = len(coeff)
    delta = np.cos(np.arange(1, 2 * tot_len, 2) * np.pi / 2 / (2 * tot_len)).conj()
    options["target"] = lambda x: cheby_coeff_to_func(x, coeff, parity, True)
    options["parity"] = parity
    options["print"] = 0
    obj = qsp_obj_sym
    grad = qsp_grad_sym

    start_time = time.time()
    # (tot_len, 1) or (tot_len, ) ?
    [phi, obj_value, out] = qsp_lbfgs(obj, grad, delta, np.zeros((tot_len,)), options)
    phi[-1] += np.pi / 4

    # The : indexes are 99# problematic, not sure how to convert them yet
    if parity == 0:
        phi_proc = np.zeros((2 * len(phi) - 1,))
        phi_proc[: len(phi) - 1] = phi[1:][::-1]
        phi_proc[len(phi) - 1 :] = phi
    else:
        phi_proc = np.zeros((2 * len(phi)))
        phi_proc[: len(phi)] = phi[::-1]
        phi_proc[len(phi) :] = phi

    lapsed_time = time.time() - start_time
    out["time"] = lapsed_time
    out["value"] = obj_value

    return phi_proc, out
