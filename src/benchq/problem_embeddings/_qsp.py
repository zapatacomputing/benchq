################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
from typing import Any, Dict, Iterable, List, Optional, cast

import cirq
import numpy as np
import pyLIQTR.QSP as QSP
from orquestra.integrations.cirq.conversions import import_from_cirq, to_openfermion
from orquestra.quantum.circuits import Circuit
from orquestra.quantum.operators import PauliRepresentation
from pyLIQTR.QSP import gen_qsp

from ..conversions import openfermion_to_pyliqtr
from ..data_structures import QuantumProgram


def get_qsp_circuit(
    operator: PauliRepresentation,
    required_precision: float,
    dt: float,
    tmax: float,
    sclf: float,
    use_random_angles: bool = False,
) -> Circuit:
    pyliqtr_operator = openfermion_to_pyliqtr(to_openfermion(operator))

    # Ns = int(np.ceil(tmax / dt))  # Total number of timesteps
    timestep_vec = np.arange(0, tmax + dt, sclf * dt)  # Define array of timesteps

    occ_state = np.zeros(pyliqtr_operator.problem_size)
    occ_state[0] = 1

    pyliqtr_mode = "random" if use_random_angles else "legacy"
    tmp = [
        gen_qsp.compute_hamiltonian_angles(
            pyliqtr_operator, simtime=t, req_prec=required_precision, mode=pyliqtr_mode
        )
        for t in timestep_vec
    ]

    # tolerances = [a[1] for a in tmp]
    angles = [a[0] for a in tmp]
    angles = angles[1]

    qsp_generator = QSP.QSP.QSP(
        phis=angles,
        hamiltonian=pyliqtr_operator,
        target_size=pyliqtr_operator.problem_size,
    )

    qsp_circ = qsp_generator.circuit()

    return Circuit(
        [
            import_from_cirq(op) for op in _sanitize_cirq_circuit(qsp_circ)
        ]  # type: ignore
    )


def get_qsp_program(
    operator: PauliRepresentation,
    n_block_encodings: int,
):
    pyliqtr_operator = openfermion_to_pyliqtr(to_openfermion(operator))
    angles = np.random.random(3)

    qsp_generator = QSP.QSP.QSP(
        phis=angles,
        hamiltonian=pyliqtr_operator,
        target_size=pyliqtr_operator.problem_size,
    )
    rotation_circuit = qsp_generator.initialize_circuit()
    rotation_circuit = qsp_generator.add_phase_rotation(
        rotation_circuit, angles[0], rot_type="X"
    )
    select_v_circuit = qsp_generator.initialize_circuit()
    select_v_circuit = qsp_generator.add_select_v(select_v_circuit, angles[1])
    reflection_circuit = qsp_generator.initialize_circuit()
    reflection_circuit = qsp_generator.add_reflection(reflection_circuit, angles[2])
    circuits = [rotation_circuit, select_v_circuit, reflection_circuit]
    sanitized_circuits = cast(
        List[Circuit],
        [
            Circuit(
                [
                    import_from_cirq(op) for op in _sanitize_cirq_circuit(circuit)
                ]  # type: ignore
            )
            for circuit in circuits
        ],
    )

    # pad with identity so all subroutines have same number of qubits
    total_n_qubits = max(circuit.n_qubits for circuit in sanitized_circuits)
    padded_sanitized_circuits = [
        Circuit(
            [
                op.gate(
                    *[
                        total_n_qubits - circuit.n_qubits + index
                        for index in op.qubit_indices
                    ]
                )
                for op in circuit.operations
            ]
        )
        for circuit in sanitized_circuits
    ]

    def subroutine_sequence_for_qsp(n_block_encodings):
        my_subroutines = []
        my_subroutines.append(0)
        for _ in range(n_block_encodings):
            my_subroutines.append(1)
            my_subroutines.append(2)
        my_subroutines.append(1)
        my_subroutines.append(0)
        return my_subroutines

    return QuantumProgram(
        subroutines=padded_sanitized_circuits,
        steps=n_block_encodings,
        calculate_subroutine_sequence=subroutine_sequence_for_qsp,
    )


def _sanitize_cirq_circuit(circuit: cirq.Circuit) -> Iterable[cirq.Operation]:
    decomposed_ops = cirq.decompose(circuit)
    simplified_ops = _simplify_gates(decomposed_ops)
    return _replace_named_qubits(simplified_ops)


def _replace_named_qubits(ops: Iterable[cirq.Operation]) -> List[cirq.Operation]:
    all_qubits = set([qubit for op in ops for qubit in op.qubits])
    qubit_map: Dict[Any, cirq.LineQubit] = {}
    max_line_id = 0
    for qubit in all_qubits:
        if isinstance(qubit, cirq.LineQubit) and qubit.x > max_line_id:
            max_line_id = qubit.x

    current_qubit_id = max_line_id + 1
    for qubit in all_qubits:
        if isinstance(qubit, cirq.NamedQubit):
            qubit_map[qubit] = cirq.LineQubit(current_qubit_id)
            current_qubit_id += 1

    return [
        cast(cirq.Gate, op.gate).on(*[qubit_map.get(q, q) for q in op.qubits])
        for op in ops
    ]


XPOW_IDENTITY_1 = cirq.XPowGate(exponent=-1)
XPOW_IDENTITY_2 = cirq.XPowGate(global_shift=-0.25)
RESET_CHANNEL = cirq.ResetChannel()


def _is_identity(gate: cirq.Gate) -> bool:
    return (
        gate == cirq.I
        or (
            isinstance(gate, cirq.XPowGate)
            and (gate == XPOW_IDENTITY_1 or gate == XPOW_IDENTITY_2)
        )
        or gate == RESET_CHANNEL
    )


ZPOW_GATE_Z_EQUIVALENT = cirq.ZPowGate(exponent=-1)
CZPOW_GATE_CZ_EQUIVALENT = cirq.CZPowGate(exponent=-1)


def _replace_gate(op: cirq.Operation) -> Optional[cirq.Operation]:
    if isinstance(op.gate, cirq.YPowGate) and op.gate.exponent == 0.5:
        return cirq.Ry(rads=op.gate.exponent / np.pi).on(op.qubits[0])
    elif isinstance(op.gate, cirq.YPowGate) and op.gate.exponent == -0.5:
        return cirq.Ry(rads=-op.gate.exponent / np.pi).on(op.qubits[0])
    elif _is_identity(cast(cirq.Gate, op.gate)):
        return None
    elif op.gate == ZPOW_GATE_Z_EQUIVALENT:
        # TODO: requires verification!
        return cirq.Z.on(op.qubits[0])
    elif op.gate == CZPOW_GATE_CZ_EQUIVALENT:
        return cirq.CZ.on(op.qubits[0], op.qubits[1])
    else:
        return op


def _simplify_gates(ops: Iterable[cirq.Operation]) -> List[cirq.Operation]:
    return [new_op for op in ops if (new_op := _replace_gate(op)) is not None]
