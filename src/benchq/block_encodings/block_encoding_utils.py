from typing import Iterable, List, Optional

from orquestra.quantum.circuits import Circuit, GateOperation, X


def controlled_clock(
    size: int,
    targets: Optional[List[int]] = None,
    controls: Optional[List[int]] = None,
    control_states: Optional[List[int]] = None,
    direction: str = "forward",
) -> Circuit:
    """Constructs a clock circuit which is controlled by the qubits
    given in the controls input. The result is the following matrix
    M when direction is "forward":

        [ 0            1]
        [ 1  0          ]
    M = [ 0  1   .   .  ]
        [ 0  0   1   .  ]
        [ 0  0   0   1 0]

    "backward" will return the inverse of the matrix given above.

    This is a translation of the MATLAB code provided by Daan Camps at
    https://github.com/QuantumComputingLab/explicit-block-encodings.

    Args:
        size (int): number of qubits with which to make the clock. Thus, the number of
            tocks is 2^n.
        targets (Optional[List[int]], optional): The qubits to which the clock is
            applied. Defaults to None, which means all qubits.
        controls (Optional[List[int]], optional): The qubits that control the clock.
            Defaults to None, which means no controls.
        control_states (Optional[List[int]], optional): The states of the control
            qubits that activate the clock. Defaults to None, which means all control
            qubits must be in the state 1.

    Returns:
        Circuit: The clock circuit.
    """
    if targets is None:
        targets = list(range(size))
    if controls is None:
        controls = []
    if control_states is None:
        control_states = [1 for _ in controls]

    assert size > 0
    assert not set(targets).intersection(controls)
    assert len(targets) == size
    assert len(control_states) == len(controls)
    assert all([s in [0, 1] for s in control_states])
    assert direction in ["forward", "backward"]

    circuit = Circuit()
    ctrl_states = get_x_for_control(controls, control_states)
    for i in range(1, len(targets)):
        ctrl = controls + targets[i:]
        targ = targets[i - 1]
        if direction == "backward":
            ctrl_states += targets[i:]
        circuit += x_conj_gate(ctrl_states, X.controlled(len(ctrl))(*ctrl, targ))
        # reset ctrl_states
        ctrl_states = get_x_for_control(controls, control_states)
    if controls:
        circuit += x_conj_gate(
            ctrl_states, X.controlled(len(controls))(*controls, targets[-1])
        )
    else:
        circuit += X(targets[-1])
    return circuit


def get_x_for_control(controls: List[int], control_states: List[int]) -> List[int]:
    """Given a set of qubits used to control and the states which you want those qubits
    to enact their control, this function returns the qubits that should be X'd to
    enact the control.

    Args:
        controls (List[int]): control qubits
        control_states (List[int]): control qubit states. List of either 0 or 1.

    Returns:
        List[int]: qubits that should be X'd to enact the control.
    """
    assert len(controls) == len(control_states)
    assert all([s in [0, 1] for s in control_states])

    return [qubit for qubit, state in zip(controls, control_states) if state == 0]


def x_conj_gate(targets: Iterable[int], gate: GateOperation) -> Circuit:
    """Constructs a circuit that applies X to the targets, applies the gate,
    and then applies X to the targets again.

    Args:
        targets (Iterable[int]): The qubits to which X is applied.
        gate (GateOperation): The gate to apply between the X gates.

    Returns:
        Circuit: The circuit that applies X to the targets, applies the gate,
            and then applies X to the targets again.
    """
    circuit = Circuit()
    for i in targets:
        circuit += X(i)
    circuit += gate
    for i in targets:
        circuit += X(i)
    return circuit
