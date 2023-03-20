################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
from math import ceil, log10
from typing import Union

from cirq.circuits import Circuit as CirqCircuit
from orquestra.quantum.circuits import Circuit as OrquestraCircuit
from pyLIQTR.gate_decomp.cirq_transforms import clifford_plus_t_direct_transform
from pyquil.quil import Program as PyquilCircuit
from qiskit.circuit import QuantumCircuit as QiskitCircuit

from ..conversions import export_circuit, import_circuit


def pyliqtr_transpile_to_clifford_t(
    circuit: Union[OrquestraCircuit, CirqCircuit, PyquilCircuit, QiskitCircuit],
    gate_accuracy: Union[float, None] = None,
    circuit_accuracy: Union[float, None] = None,
) -> OrquestraCircuit:
    """Compile a circuit into clifford + T using pyLIQTR. The only non-clifford + T
    gates that can be compiled are X, Y, and Z rotations. 
    Note that while we are using accuracy pyLIQTR requires specifying precision

    Args:
        circuit (Union[OrquestraCircuit, CirqCircuit, PyquilCircuit, QiskitCircuit]):
            Circuit to be compiled to clifford + T Gates.
        gate_accuracy (float): accuracy of each gate decomposition (not accuracy
            of total circuit decomposition). Accuracy must be converted into a number
            of significant figures. When this is done, the number of significant
            figures is always rounded up.
        circuit_accuracy (float): Accuracy required for a whole circuit
            Each gate will be bounded by either `circuit_precision` divided by 
            the number of rotation gates (if given a float),
            or 10^{-circuit_precision} (if given an int)


    Returns:
        OrquestraCircuit: circuit decomposed to Clifford + T using pyLIQTR.
    """
    cirq_circuit = export_circuit(CirqCircuit, import_circuit(circuit))
    gate_precision, circuit_precision = None, None
    if gate_accuracy is not None and circuit_accuracy is None:
        gate_precision = ceil(-log10(gate_accuracy))  # number accurate of digits
    elif circuit_accuracy is not None and gate_accuracy is None:
        circuit_precision = ceil(-log10(circuit_accuracy))
    elif circuit_accuracy and gate_accuracy is None:
        raise ValueError("Please supply accuracy either for the gates or for the circuit")
    else:
        raise ValueError("Please supply gate or circuit accuracy not both")


    compiled_cirq_circuit = clifford_plus_t_direct_transform(cirq_circuit, precision=gate_precision, 
                            circuit_precision=circuit_precision
                            )

    return import_circuit(compiled_cirq_circuit)
