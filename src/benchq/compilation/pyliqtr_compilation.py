################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
from math import ceil, log10
from typing import Union

from cirq.circuits import Circuit as CirqCircuit
from orquestra.quantum.circuits import Circuit as OrquestraCircuit
from pyLIQTR.gate_decomp.cirq_transforms import clifford_plus_t_direct_transform
from qiskit.circuit import QuantumCircuit as QiskitCircuit

from ..conversions import export_circuit, import_circuit


def pyliqtr_transpile_to_clifford_t(
    circuit: Union[OrquestraCircuit, CirqCircuit, QiskitCircuit],
    synthesis_accuracy: float,
) -> OrquestraCircuit:
    """Compile a circuit into clifford + T using pyLIQTR. The only non-clifford + T
    gates that can be compiled are X, Y, and Z rotations.

    Args:
        circuit (Union[OrquestraCircuit, CirqCircuit, PyquilCircuit, QiskitCircuit]):
            Circuit to be compiled to clifford + T Gates.
        synthesis_accuracy (float): accuracy of each gate decomposition (not accuracy
            of total circuit decomposition). Accuracy must be converted into a number
            of significant figures. When this is done, the number of significant
            figures is always rounded up.

    Returns:
        OrquestraCircuit: circuit decomposed to Clifford + T using pyLIQTR.
    """
    cirq_circuit = export_circuit(CirqCircuit, import_circuit(circuit))
    precision = ceil(-log10(synthesis_accuracy))  # number accurate of digits
    compiled_cirq_circuit = clifford_plus_t_direct_transform(cirq_circuit, precision)

    return import_circuit(compiled_cirq_circuit)
