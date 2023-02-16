################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
import pytest
from cirq import CNOT as CirqCNOT
from cirq import H as CirqH
from cirq import LineQubit
from cirq.circuits import Circuit as CirqCircuit
from orquestra.quantum.circuits import CNOT as OrquestraCNOT
from orquestra.quantum.circuits import Circuit as OrquestraCircuit
from orquestra.quantum.circuits import H as OrquestraH
from pyquil.gates import CNOT as PyquilCNOT
from pyquil.gates import H as PyquilH
from pyquil.quil import Program as PyquilCircuit
from qiskit.circuit import QuantumCircuit as QiskitCircuit

from benchq.conversions._circuit_translations import export_circuit, import_circuit


@pytest.mark.parametrize("circuit", [PyquilCircuit(), QiskitCircuit(), CirqCircuit()])
def test_import_empty_circuit_produces_correct_output(circuit):
    """Tests that import_circuit produces the correct output."""
    import_circuit(circuit) == OrquestraCircuit([])


single_qubit_qiskit_circuit = QiskitCircuit(1)
single_qubit_qiskit_circuit.h(0)


@pytest.mark.parametrize(
    "circuit",
    [
        PyquilCircuit(PyquilH(0)),
        single_qubit_qiskit_circuit,
        CirqCircuit([CirqH(LineQubit(0))]),
    ],
)
def test_import_single_qubit_circuit_produces_correct_output(circuit):
    """Tests that import_circuit produces the correct output."""
    import_circuit(circuit) == OrquestraCircuit([OrquestraH(0)])


two_qubit_qiskit_circuit = QiskitCircuit(2)
two_qubit_qiskit_circuit.cx(0, 1)


@pytest.mark.parametrize(
    "circuit",
    [
        PyquilCircuit(PyquilCNOT(0, 1)),
        two_qubit_qiskit_circuit,
        CirqCircuit([CirqCNOT(LineQubit(0), LineQubit(1))]),
    ],
)
def test_import_two_qubit_circuit_produces_correct_output(circuit):
    """Tests that import_circuit produces the correct output."""
    import_circuit(circuit) == OrquestraCircuit([OrquestraCNOT(0, 1)])


def test_wrong_type_to_import_circuit_gives_error():
    """Tests that import_circuit raises an error for an unsupported type."""
    with pytest.raises(NotImplementedError):
        import_circuit(1)


def test_export_empty_circuit_produces_correct_output():
    """Tests that export_circuit produces the correct output."""
    circuit = OrquestraCircuit([])
    assert export_circuit(PyquilCircuit, circuit) == PyquilCircuit()
    assert export_circuit(QiskitCircuit, circuit) == QiskitCircuit()
    assert export_circuit(CirqCircuit, circuit) == CirqCircuit()


def test_export_single_qubit_circuit_produces_correct_output():
    """Tests that export_circuit produces the correct output."""
    circuit = OrquestraCircuit([OrquestraH(0)])
    assert export_circuit(PyquilCircuit, circuit) == PyquilCircuit(PyquilH(0))
    assert export_circuit(QiskitCircuit, circuit) == single_qubit_qiskit_circuit
    assert export_circuit(CirqCircuit, circuit) == CirqCircuit([CirqH(LineQubit(0))])


def test_export_two_qubit_circuit_produces_correct_output():
    circuit = OrquestraCircuit([OrquestraCNOT(0, 1)])
    assert export_circuit(PyquilCircuit, circuit) == PyquilCircuit(PyquilCNOT(0, 1))
    assert export_circuit(QiskitCircuit, circuit) == two_qubit_qiskit_circuit
    assert export_circuit(CirqCircuit, circuit) == CirqCircuit(
        [CirqCNOT(LineQubit(0), LineQubit(1))]
    )


def test_wrong_type_to_export_circuit_gives_error():
    """Tests that import_circuit raises an error for an unsupported type."""
    with pytest.raises(NotImplementedError):
        export_circuit(1, 1)
