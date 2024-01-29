################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
from dataclasses import dataclass
from typing import Dict, Generic, Iterable, List, Optional, Sequence, TypeVar, cast

import cirq
import numpy as np
import pyLIQTR.QSP as QSP
from orquestra.integrations.cirq.conversions import import_from_cirq, to_openfermion
from orquestra.quantum.circuits import Circuit, GateOperation
from orquestra.quantum.operators import PauliRepresentation
from pyLIQTR.QSP import gen_qsp
from pyLIQTR.QSP.qsp_helpers import qsp_decompose_once

from ...conversions import openfermion_to_pyliqtr
from ..quantum_program import QuantumProgram

TCircuit = TypeVar("TCircuit")


@dataclass
class QSPComponents(Generic[TCircuit]):
    """Structure to store QSP program components.

    The select_v field is stored as a sequence, because depending on if you use
    decomposition or not it might contain more than one circuit.
    """

    rotation: TCircuit
    reflection: TCircuit
    select_v: Sequence[TCircuit]


@dataclass
class _Indices:
    """Structure for storing indices of QSP components.

    Indices are needed because our QSP QuantumProgram requires
    them (or at least function that computes them).

    Rotation and reflection comprise a single subroutine, but the
    select_v comprises several subroutines, that's why it's a list.
    """

    rotation: int
    reflection: int
    select_v: List[int]


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
            import_from_cirq(op)
            for op in _sanitize_cirq_circuit(
                qsp_circ, _map_named_qubits_to_line_qubits([qsp_circ])
            )
        ]  # type: ignore
    )


def get_qsp_program(
    operator: PauliRepresentation,
    n_block_encodings: int,
    decompose_select_v: bool = True,
) -> QuantumProgram:
    pyliqtr_operator = openfermion_to_pyliqtr(to_openfermion(operator))
    angles = np.random.random(3)

    qsp_generator = QSP.QSP.QSP(
        phis=angles,
        hamiltonian=pyliqtr_operator,
        target_size=pyliqtr_operator.problem_size,
    )

    components = _preprocess_qsp_cirq_components(
        _create_qsp_components(qsp_generator, angles, decompose_select_v)
    )

    if decompose_select_v:
        # We are done preprocessing the circuits, so we might now explode the list
        # of circuits to actually include daggers of select_v components.
        # We are not using builtin circuit.inverse() because it creates Dagger
        # objects for RY gates.
        all_circuits = [
            components.rotation,
            components.select_v[0],
            components.select_v[1],
            components.select_v[2],
            components.select_v[3],
            _invert_without_ry_dagger(components.select_v[2]),
            _invert_without_ry_dagger(components.select_v[1]),
            _invert_without_ry_dagger(components.select_v[0]),
            components.reflection,
        ]
        indices = _Indices(rotation=0, reflection=8, select_v=list(range(1, 8)))
    else:
        all_circuits = [
            components.rotation,
            components.select_v[0],
            components.reflection,
        ]
        indices = _Indices(rotation=0, reflection=2, select_v=[1])

    def subroutine_sequence_for_qsp(n_block_encodings):
        my_subroutines = []
        my_subroutines.append(indices.rotation)
        for _ in range(n_block_encodings):
            my_subroutines += indices.select_v
            my_subroutines.append(indices.reflection)
        my_subroutines += indices.select_v
        my_subroutines.append(indices.rotation)
        return my_subroutines

    return QuantumProgram(
        subroutines=all_circuits,
        steps=n_block_encodings,
        calculate_subroutine_sequence=subroutine_sequence_for_qsp,
    )


def _create_qsp_components(
    qsp_generator: QSP.QSP.QSP, angles: np.ndarray, decompose_select_v: bool
) -> QSPComponents[cirq.Circuit]:
    rotation_circuit = qsp_generator.initialize_circuit()
    rotation_circuit = qsp_generator.add_phase_rotation(
        rotation_circuit, angles[0], rot_type="X"
    )

    select_v_circuits = _generate_select_v_circuits(
        qsp_generator, angles[1], decompose_select_v
    )

    reflection_circuit = qsp_generator.initialize_circuit()
    reflection_circuit = qsp_generator.add_reflection(reflection_circuit, angles[2])

    return QSPComponents(
        rotation=rotation_circuit,
        reflection=reflection_circuit,
        select_v=select_v_circuits,
    )


def _dagger(operation: GateOperation) -> GateOperation:
    if isinstance(operation, GateOperation):
        return (
            operation.replace_params((-operation.params[0],))  # type: ignore
            if operation.gate.name == "RY"
            else operation.gate.dagger(*operation.qubit_indices)
        )
    else:
        return operation


def _invert_without_ry_dagger(circuit: Circuit):
    return Circuit(
        list(map(_dagger, reversed(circuit.operations))), n_qubits=circuit.n_qubits
    )


# Explanation of indices:
# 0 - Prepare subcircuit
# 1 - A single reset
# 2 - SelVBase subcircuit
# 3 - Rotation subcircuit
# 4 - Dagger of SelVBase subcircuit
# 5 - A single reset
# 6 - Dagger of Prepare subcircuit
# And hence, we only need circuits 0, 1, 2, and 3, because the rest can
# be constructed by taking circuit.inverse() or are duplicates.
SELECT_V_DECOMPOSITION_INDICES = (0, 1, 2, 3)


def _generate_select_v_circuits(
    generator: QSP.QSP.QSP, angle: float, decompose: bool
) -> List[cirq.Circuit]:
    select_v_circuit = generator.initialize_circuit()
    select_v_circuit = generator.add_select_v(select_v_circuit, angle)
    if decompose:
        components = qsp_decompose_once(select_v_circuit)
        return [cirq.Circuit(components[i]) for i in SELECT_V_DECOMPOSITION_INDICES]
    else:
        return [select_v_circuit]


def _preprocess_qsp_cirq_components(
    components: QSPComponents[cirq.Circuit],
) -> QSPComponents[Circuit]:
    base_circuits = [components.rotation, *components.select_v, components.reflection]

    qubit_map = _map_named_qubits_to_line_qubits(
        [components.rotation, *components.select_v, components.reflection]
    )

    sanitized_circuits = [
        Circuit(
            [
                import_from_cirq(op)
                for op in _sanitize_cirq_circuit(circuit, qubit_map)
            ]  # type: ignore
        )
        for circuit in base_circuits
    ]

    total_n_qubits = max(circuit.n_qubits for circuit in sanitized_circuits)
    padded_circuits = [
        Circuit(circuit.operations, n_qubits=total_n_qubits)
        for circuit in sanitized_circuits
    ]

    return QSPComponents(
        rotation=padded_circuits[0],
        reflection=padded_circuits[-1],
        select_v=padded_circuits[1:-1],
    )


def _sanitize_cirq_circuit(
    circuit: cirq.Circuit,
    named_qubits_to_line_qubits_map: Dict[cirq.Qid, cirq.LineQubit],
) -> Iterable[cirq.Operation]:
    decomposed_ops = cirq.decompose(circuit)
    simplified_ops = _simplify_gates(decomposed_ops)
    return _replace_named_qubits(simplified_ops, named_qubits_to_line_qubits_map)


def _map_named_qubits_to_line_qubits(
    circuits: Iterable[cirq.Circuit],
) -> Dict[cirq.Qid, cirq.LineQubit]:
    all_qubits = set(
        [
            qubit
            for circuit in circuits
            for op in circuit.all_operations()
            for qubit in op.qubits
        ]
    )

    line_qubits = [qubit for qubit in all_qubits if isinstance(qubit, cirq.LineQubit)]

    named_qubits = [qubit for qubit in all_qubits if isinstance(qubit, cirq.NamedQubit)]

    max_line_id = max(qubit.x for qubit in line_qubits) if len(line_qubits) != 0 else -1

    return {
        qubit: cirq.LineQubit(i)
        for i, qubit in enumerate(named_qubits, max_line_id + 1)
    }


def _replace_named_qubits(
    ops: Iterable[cirq.Operation],
    named_qubits_to_line_qubits_map: Dict[cirq.Qid, cirq.LineQubit],
) -> List[cirq.Operation]:
    return [
        cast(cirq.Gate, op.gate).on(
            *[named_qubits_to_line_qubits_map.get(q, q) for q in op.qubits]
        )
        for op in ops
    ]


XPOW_X_1 = cirq.XPowGate(exponent=-1)
XPOW_X_2 = cirq.XPowGate(global_shift=-0.25)


ZPOW_GATE_Z_EQUIVALENT = cirq.ZPowGate(exponent=-1)
CZPOW_GATE_CZ_EQUIVALENT = cirq.CZPowGate(exponent=-1)


def _replace_gate(op: cirq.Operation) -> Optional[cirq.Operation]:
    if isinstance(op.gate, cirq.YPowGate) and abs(op.gate.exponent) == 0.5:
        return cirq.Ry(rads=op.gate.exponent / np.pi).on(op.qubits[0])
    elif isinstance(op.gate, cirq.XPowGate) and op.gate == XPOW_X_1:
        return cirq.X(op.qubits[0])
    elif isinstance(op.gate, cirq.XPowGate) and op.gate == XPOW_X_2:
        return cirq.X(op.qubits[0])
    elif op.gate == cirq.I:
        return None
    elif op.gate == ZPOW_GATE_Z_EQUIVALENT:
        return cirq.Z.on(op.qubits[0])
    elif op.gate == CZPOW_GATE_CZ_EQUIVALENT:
        return cirq.CZ.on(op.qubits[0], op.qubits[1])
    else:
        return op


def _simplify_gates(ops: Iterable[cirq.Operation]) -> List[cirq.Operation]:
    return [new_op for op in ops if (new_op := _replace_gate(op)) is not None]
