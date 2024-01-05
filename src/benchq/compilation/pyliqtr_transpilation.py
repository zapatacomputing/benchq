################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
import warnings
from typing import Optional, Union

from cirq.circuits import Circuit as CirqCircuit
from orquestra.quantum.circuits import Circuit as OrquestraCircuit
from orquestra.quantum.circuits import GateOperation
from pyLIQTR.gate_decomp.cirq_transforms import clifford_plus_t_direct_transform
from qiskit.circuit import QuantumCircuit as QiskitCircuit

from ..conversions import export_circuit, import_circuit


def pyliqtr_transpile_to_clifford_t(
    circuit: Union[OrquestraCircuit, CirqCircuit, QiskitCircuit],
    gate_precision: Optional[float] = None,
    circuit_precision: Optional[float] = None,
    n_rotation_gates: Optional[int] = None,
) -> OrquestraCircuit:
    """Compile a circuit into clifford + T using pyLIQTR. The only non-clifford + T
    gates that can be compiled are X, Y, and Z rotations.

    Args:
        circuit (Union[OrquestraCircuit, CirqCircuit, PyquilCircuit, QiskitCircuit]):
            Circuit to be compiled to clifford + T Gates.
        gate_precision (float): precision of each gate decomposition (not precision
            of total circuit decomposition). Precision must be converted into a number
            of significant figures. When this is done, the number of significant
            figures is always rounded up.
        circuit_precision (float): Precision required for a whole circuit
            Each gate will be bounded by either `circuit_precision` divided by
            the number of rotation gates (if given a float),
            or 10^{-circuit_precision} (if given an int)
        n_rotation_gates (int): Number of rotation gates to use in the decomposition.
            If not given, pyliqtr will send erroneous warnings saying that the
            provided gates cannot be decomposed.

    Returns:
        OrquestraCircuit: circuit decomposed to Clifford + T using pyLIQTR.
    """
    has_rotations = False
    orquestra_circuit = import_circuit(circuit)
    for op in orquestra_circuit.operations:
        if isinstance(op, GateOperation) and op.gate.name in ["RX", "RY", "RZ"]:
            has_rotations = True
            break
    if not has_rotations:
        return orquestra_circuit

    if circuit_precision is None and gate_precision is None:
        raise ValueError(
            "Please supply precision either for the gates or for the circuit"
        )
    if circuit_precision is not None and gate_precision is not None:
        raise ValueError("Please supply gate or circuit precision not both")

    cirq_circuit = export_circuit(CirqCircuit, orquestra_circuit)
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", message=r".* is not a rotation gate, cannot decompose."
        )
        compiled_cirq_circuit = clifford_plus_t_direct_transform(
            cirq_circuit,
            precision=gate_precision,
            circuit_precision=circuit_precision,
            use_random_decomp=False,
            num_rotation_gates=n_rotation_gates,
        )

    return import_circuit(compiled_cirq_circuit, orquestra_circuit.n_qubits)
