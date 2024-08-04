################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
from typing import Dict, Iterable, List, Optional, TypeVar, cast

import cirq
import numpy as np

from pyLIQTR.qubitization.qubitized_gates import QubitizedReflection


from orquestra.quantum.circuits import Circuit
from orquestra.integrations.cirq.conversions import import_from_cirq

from qualtran.bloqs.arithmetic.addition import AddConstantMod

from cirq.circuits import Circuit as CirqCircuit


# # TODO: remove these imports as they relies on unsupported pyLIQTR v0 functions
# import pyLIQTR.QSP as QSP  # Cannot find this in pyLIQTR_v1
# as qsp_generator = pQSP.QSP, I cannot find where this is imported from
# from pyLIQTR.QSP import gen_qsp  # Cannot find this in pyLIQTR_v1
# from pyLIQTR.QSP.qsp_helpers import qsp_decompose_once  # Cannot find this in pyLIQTR_v1

from pyLIQTR.BlockEncodings.BlockEncoding import BlockEncoding
from pyLIQTR.qubitization.qubitized_gates import QubitizedReflection
from pyLIQTR.qubitization.qsvt import QSP_fourier_response


from ...conversions import export_circuit, import_circuit

from ..quantum_program import QuantumProgram

TCircuit = TypeVar("TCircuit")


def get_qsp_program_from_block_encoding(
    block_encoding: BlockEncoding,
    evolution_time: float,
    qsp_failure_tolerance: float,
) -> QuantumProgram:

    alpha = block_encoding.alpha
    renormalized_time = evolution_time * alpha

    from pyLIQTR.phase_factors.optimization.expander import Expander

    # TODO: rather than computing this number of coefficients here, we
    # may want to be be more integrated with the pyLIQTR software that
    # generates them. However, we need to understand if there is a
    # way to get the count of the number of coefficients from pyLIQTR
    # without actually generating the coefficients (which can be costly
    # for large numbers of coefficients).
    expdr = Expander()
    max_order, num_coeffs = expdr._ja_get_trig_order(
        renormalized_time, qsp_failure_tolerance
    )

    num_phases = num_coeffs

    qsp_cirq_subroutines = get_qsp_cirq_subroutines(block_encoding)

    preprocessed_qsp_circuits = _preprocess_qsp_cirq_components(qsp_cirq_subroutines)

    return QuantumProgram(
        preprocessed_qsp_circuits, num_phases, calculate_qsp_subroutine_sequence
    )


# TODO: (DTA2-495) consider leveraging how the decompose_from_registers method contains the
# same logic as the subroutine_sequence creation below.
# Currently we are choosing to re-implement this logic in a bespoke way.
# But, eventually we may want to import this logic from the qualtran object.
def get_qsp_cirq_subroutines(block_encoding: BlockEncoding) -> List[CirqCircuit]:
    # Grab block encoding quregs
    block_encoding_quregs = {}
    for register in block_encoding.signature:
        block_encoding_quregs[register.name] = np.array(
            [cirq.NamedQubit(f"{register.name}{i}") for i in range(register.bitsize)]
        )

    # Add phase rotation qureg
    phase_rotation_qureg = {
        "phase": np.array([cirq.NamedQubit("phase")]),
    }
    quregs = {**block_encoding_quregs, **phase_rotation_qureg}
    # Define registers for block reflection
    selection_qubits = []
    junk_qubits = []

    kw_block_regs = {"target": quregs["target"]}
    kw_rotation_regs = {"target": quregs["phase"]}

    for reg in block_encoding.selection_registers:
        selection_qubits += quregs[reg.name].tolist()

    for reg in block_encoding.junk_registers:
        junk_qubits += quregs[reg.name].tolist()
        kw_block_regs[reg.name] = quregs[reg.name]

    kw_rotation_args = {
        "control_val": None,
        "rotation_gate": cirq.Rx,
        "multi_control_val": 1,
        "multi_target_gate": cirq.Z,
        "multi_target_val": 1,
    }
    kw_rotation_regs["control"] = selection_qubits + junk_qubits

    kw_block_regs["control"] = kw_rotation_regs["target"]

    # Create single qubit rotation circuit
    # Inputting a random phi value for now
    phi = 1.0
    single_qubit_rotation = cirq.Circuit(
        [cirq.Ry(rads=phi).on(kw_rotation_regs["target"][0])]
    )

    # Create block reflection circuit
    block_reflection_circuit = cirq.Circuit(
        cirq.decompose(
            QubitizedReflection(
                len(kw_rotation_regs["control"]),
                target_gate=kw_rotation_args["multi_target_gate"],
                control_val=kw_rotation_args["multi_target_val"],
                multi_control_val=kw_rotation_args["multi_control_val"],
            ).on_registers(
                controls=kw_rotation_regs["control"], target=kw_rotation_regs["target"]
            )
        )
    )
    # Create block encoding circuit
    context = cirq.DecompositionContext(cirq.SimpleQubitManager())
    block_encoding_circuit = cirq.Circuit(
        cirq.decompose(
            block_encoding.circuit,
            context=context,
        ),
    )

    qsp_cirq_subroutines = [
        single_qubit_rotation,
        block_encoding_circuit,
        block_reflection_circuit,
    ]
    return qsp_cirq_subroutines


# TODO: (DTA2-494) update this after the new subroutine_sequence interface is built
def calculate_qsp_subroutine_sequence(num_phases: int) -> List[int]:
    subroutine_sequence = []
    subroutine_sequence.append(0)

    for n in range(0, int((num_phases - 3) / 2)):

        subroutine_sequence.append(1)
        subroutine_sequence.append(0)
        subroutine_sequence.append(1)
        subroutine_sequence.append(2)
        subroutine_sequence.append(0)
        subroutine_sequence.append(2)

    subroutine_sequence.append(1)
    subroutine_sequence.append(0)
    subroutine_sequence.append(1)
    subroutine_sequence.append(0)

    return subroutine_sequence


def _preprocess_qsp_cirq_components(
    qsp_cirq_subroutines: List[cirq.Circuit],
) -> List[Circuit]:

    qubit_map = _map_all_qubits_to_line_qubits(qsp_cirq_subroutines)

    sanitized_circuits = [
        Circuit(
            [import_from_cirq(op) for op in _sanitize_cirq_circuit(circuit, qubit_map)]
        )
        for circuit in qsp_cirq_subroutines
    ]

    total_n_qubits = max(circuit.n_qubits for circuit in sanitized_circuits)
    # Pad circuits to have the same number of qubits
    preprocessed_qsp_subroutines = [
        Circuit(circuit.operations, n_qubits=total_n_qubits)
        for circuit in sanitized_circuits
    ]
    return preprocessed_qsp_subroutines


def _sanitize_cirq_circuit(
    circuit: cirq.Circuit,
    all_qubits_to_line_qubits_map: Dict[cirq.Qid, cirq.LineQubit],
) -> Iterable[cirq.Operation]:
    decomposed_ops = cirq.decompose(circuit)
    # TODO: decide how to handle classical controls in the subroutine circuits rather than removing them
    ops_without_classical_controls = [
        decomposed_op.without_classical_controls() for decomposed_op in decomposed_ops
    ]
    simplified_ops = _simplify_gates(ops_without_classical_controls)
    return _replace_all_qubits_with_line_qubits(
        simplified_ops, all_qubits_to_line_qubits_map
    )


def _map_all_qubits_to_line_qubits(
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

    clean_qubits = [
        qubit for qubit in all_qubits if isinstance(qubit, cirq.ops.CleanQubit)
    ]

    max_line_id = max(qubit.x for qubit in line_qubits) if line_qubits else -1

    map_from_qubits_to_line_qubits = {
        qubit: cirq.LineQubit(i)
        for i, qubit in enumerate(named_qubits + clean_qubits, max_line_id + 1)
    }
    return map_from_qubits_to_line_qubits


def _replace_all_qubits_with_line_qubits(
    ops: Iterable[cirq.Operation],
    all_qubits_to_line_qubits_map: Dict[cirq.Qid, cirq.LineQubit],
) -> List[cirq.Operation]:

    ops_with_qubits_switched_to_line_qubits = [
        cast(cirq.Gate, op.gate).on(
            *[all_qubits_to_line_qubits_map.get(q, q) for q in op.qubits]
        )
        for op in ops
    ]

    return ops_with_qubits_switched_to_line_qubits


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
    # Replace measurement gate cirq.MeasurementGate
    # TODO: decide how to handle measurements
    elif isinstance(op.gate, cirq.MeasurementGate):
        return cirq.Z.on(op.qubits[0])
    # Replace the cirq.X/Y/ZPowGate with an cirq.Rx/y/z
    elif isinstance(op.gate, cirq.XPowGate):
        return cirq.Rx(rads=op.gate.exponent).on(op.qubits[0])
    elif isinstance(op.gate, cirq.YPowGate):
        return cirq.Ry(rads=op.gate.exponent).on(op.qubits[0])
    elif isinstance(op.gate, cirq.ZPowGate):
        return cirq.Rz(rads=op.gate.exponent).on(op.qubits[0])
    # Remove the ops.GlobalPhaseGate gate
    elif isinstance(op.gate, cirq.GlobalPhaseGate):
        return None
    # Remove the AddConstantMod gate
    # TODO: decide how to handle the AddConstantMod gate
    elif isinstance(op.gate, AddConstantMod):
        return None
    else:
        return op


def _simplify_gates(ops: Iterable[cirq.Operation]) -> List[cirq.Operation]:
    return [new_op for op in ops if (new_op := _replace_gate(op)) is not None]
