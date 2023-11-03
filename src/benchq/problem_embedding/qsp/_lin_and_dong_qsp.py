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
# The code in this Python file is a modified version for the QSP circuit
# construction as profided in the QSPPACK GitHub repository.
# The code source is available in the following path:
# https://github.com/qsppack/RACBEM/blob/master/racbem.py
#
# The work is based on the research paper by Yulong Dong and Lin Lin.
# "Random circuit block-encoded matrix and a proposal of quantum
# LINPACK benchmark."
# https://arxiv.org/abs/2006.04010
#
# The authors of the code are Yulong Dong and Lin Lin.
#
# Be aware that Qiskit uses the column-major ordering of tensors (1st
# qubit goes first), instead of the standard row-major ordering of tensors
# (last qubit goes first).
# There is a global phase factor that could be missing.

import numpy as np
import numpy.typing as npt
from qiskit import QuantumCircuit, QuantumRegister


def build_control_rotation(num_qubits: int, phi: float) -> QuantumCircuit:
    """Build the controlled rotation gate.

    Args:
        num_qubits (int): total number of qubits of the QSP circuit.
        phi (float): a phase angle.

    Returns:
        qc_crot (QuantumCircuit): a qiskit quantum circuit
            for control rotations.
    """

    qr = QuantumRegister(num_qubits)
    qc_crot = QuantumCircuit(qr)

    control_qubits = list(range(1, num_qubits))
    qc_crot.x(qr[control_qubits])
    qc_crot.mcx(qr[control_qubits], qr[0])
    qc_crot.rz(phi * 2.0, qr[0])
    qc_crot.mcx(qr[control_qubits], qr[0])
    qc_crot.x(qr[control_qubits])

    return qc_crot


def build_qsp_circuit(
    num_qubits: int,
    be_qc: QuantumCircuit,
    phi_seq: npt.NDArray[np.float64],
    realpart=True,
) -> QuantumCircuit:
    """Build a QSP circuit.

    Build a circuit for quantum signal processing, given a
    block-encoding matrix.

    Args:
        num_qubits (int): total number of qubits of the QSP circuit.
        be_qc (QuantumCircuit): an instance of the qiskit.QuantumCircuit
            representing the block encoding of a matrix.
        phi_seq (Iterable[float]): a sequence of phase factors defined in
            the QSP circuit.
        realpart: if True, returns the real part of the polynomial
            encoded by QSP. This is implemented without the need of
            an extra ancilla qubit.

    Returns:
        qsp_circuit (QuantumCircuit): an instance of qiskit.QuantumCircuit
            representing the circuit for the QSP.
    """

    qr = QuantumRegister(num_qubits)
    qsp_circuit = QuantumCircuit(qr)

    dag = False
    if realpart:
        # Add Hadamard gate as prepare oracle
        qsp_circuit.h(qr[0])

    be_qc_dag = be_qc.inverse()

    # The for loop starts from the last phase factor, starting from
    # UA instead of UA_dag
    qc_crot = build_control_rotation(num_qubits, phi_seq[-1])
    qsp_circuit.compose(qc_crot, inplace=True)

    for phi in reversed(phi_seq[:-1]):
        if not dag:
            qsp_circuit.compose(be_qc, qr[1:], inplace=True)
        else:
            qsp_circuit.compose(be_qc_dag, qr[1:], inplace=True)

        if realpart:
            # Add a Z gate before the control.
            qsp_circuit.z(qr[0])

        qc_crot = build_control_rotation(num_qubits, phi)
        qsp_circuit.compose(qc_crot, qr[0:num_qubits], inplace=True)

        dag = not dag

    if realpart:
        # Add Hadamard gate as prepare oracle
        qsp_circuit.h(qr[0])

    # neglecting the global phase for now
    return qsp_circuit
