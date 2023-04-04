################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
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

    circuit = _sanitize_cirq_circuit(qsp_circ)

    return import_from_cirq(circuit)


# TODO: This logic is copied from pyLIQTR, perhaps we want to change it to our own?
def _get_steps(tau, req_prec):
    # have tau and epsilon, backtrack in order to get steps
    steps, closeval = QSP.get_steps_from_logeps(np.log(req_prec), tau, 1)
    # print(':------------------------------------------')
    # print(f': Steps = {steps}')
    while QSP.getlogepsilon(tau, steps) > np.log(req_prec):
        steps += 4
    return steps


def get_qsp_program(
    operator: PauliRepresentation,
    required_precision: float,
    dt: float,
    tmax: float,
    sclf: float,
    mode: str = "gse",
    gse_accuracy: float = 1e-3,
) -> QuantumProgram:
    pyliqtr_operator = openfermion_to_pyliqtr(to_openfermion(operator))

    # TODO: I dont know why we have `gse_accuracy` and `required_precision` separately.
    if mode == "gse":
        n_block_encodings = int(
            np.ceil(np.pi * (pyliqtr_operator.alpha) / (gse_accuracy))
        )
        # *2 for each layer consisting of 2 blocks,
        # +2 for rotation layers,
        # #+1 for extra select-V
        steps = n_block_encodings * 2 + 3

    elif mode == "time_evolution":
        timestep_vec = np.arange(0, tmax + dt, sclf * dt)  # Define array of timesteps

        occ_state = np.zeros(pyliqtr_operator.problem_size)
        occ_state[0] = 1

        # TODO: I think the way we calculate it is incorrect.
        tau = timestep_vec[1] * pyliqtr_operator.alpha
        steps = _get_steps(tau, required_precision)

    # number of steps needs to be odd for QSP
    if not (steps % 2):
        steps += 1

        n_block_encodings = int((steps - 3) / 2)

    angles = np.random.random(steps)

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
    sanitized_circuits = [
        import_from_cirq(_sanitize_cirq_circuit(circuit)) for circuit in circuits
    ]

    # pad with identity so all subroutines have same number of qubits
    total_n_qubits = max(circuit.n_qubits for circuit in sanitized_circuits)
    padded_sanitized_circuits = []
    for circuit in sanitized_circuits:
        new_circuit = Circuit()
        n_qubits = circuit.n_qubits
        shift = total_n_qubits - n_qubits
        # in this case we know qubits only need to be moved up.
        for op in circuit.operations:
            new_circuit += op.gate(*[shift + index for index in op.qubit_indices])
        padded_sanitized_circuits.append(new_circuit)

    def subroutine_sequence_for_qsp(n_block_encodings):
        my_subroutines = []
        my_subroutines.append(0)
        for i in range(n_block_encodings):
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


def _sanitize_cirq_circuit(circuit: cirq.Circuit) -> cirq.Circuit:
    decomposed_circuit = cirq.Circuit(cirq.decompose(circuit))
    circuit_without_resets = _replace_resets(decomposed_circuit)
    simplified_circuit = _simplify_gates(circuit_without_resets)
    circuit_with_line_qubits = _replace_named_qubit(simplified_circuit)
    return circuit_with_line_qubits


def _replace_named_qubit(circuit: cirq.Circuit) -> cirq.Circuit:
    all_qubits = circuit.all_qubits()
    qubit_map = {}
    max_line_id = 0
    for qubit in all_qubits:
        if isinstance(qubit, cirq.LineQubit) and qubit.x > max_line_id:
            max_line_id = qubit.x

    current_qubit_id = max_line_id + 1
    for qubit in all_qubits:
        if isinstance(qubit, cirq.NamedQubit):
            qubit_map[qubit] = cirq.LineQubit(current_qubit_id)
            current_qubit_id += 1

    return circuit.transform_qubits(qubit_map)  # type: ignore


def _replace_resets(circuit: cirq.Circuit) -> cirq.Circuit:
    def replace_resets_with_I(op: cirq.Operation, _: int) -> cirq.OP_TREE:
        if op.gate == cirq.ResetChannel():
            yield cirq.I(op.qubits[0])
        else:
            yield op

    return cirq.map_operations_and_unroll(circuit, replace_resets_with_I)


def _simplify_gates(circuit: cirq.Circuit) -> cirq.Circuit:
    def _replace_gates(op: cirq.Operation, _: int) -> cirq.OP_TREE:
        # TODO: account for special cases - i.e. close to pi, close to 0, etc.
        # This is basically just dropping a global phase, needed for
        # interframework compatibility reasons.

        if isinstance(op.gate, cirq.YPowGate):
            if op.gate.exponent == 0.5:
                yield cirq.Ry(rads=op.gate.exponent / np.pi).on(op.qubits[0])
            if op.gate.exponent == -0.5:
                yield cirq.Ry(rads=-op.gate.exponent / np.pi).on(op.qubits[0])
        elif op.gate == cirq.XPowGate(global_shift=-0.25):
            # No need to include identity gates
            # yield cirq.I.on(op.qubits[0])
            pass
        elif op.gate == cirq.XPowGate(exponent=-1):
            # No need to include identity gates
            # yield cirq.I.on(op.qubits[0])
            pass
        elif op.gate == cirq.ZPowGate(exponent=-1):
            # TODO: requires verification!
            yield cirq.Z.on(op.qubits[0])
        elif op.gate == cirq.CZPowGate(exponent=-1):
            yield cirq.CZ.on(op.qubits[0], op.qubits[1])
        elif op.gate == cirq.I:
            # No need to include identity gates
            pass
        else:
            yield op

    return cirq.map_operations_and_unroll(circuit, _replace_gates)
