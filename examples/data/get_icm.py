from orquestra.quantum.circuits import CNOT, Circuit


def get_icm(
    circuit: Circuit, gates_to_decompose=["T", "T_Dagger", "RX", "RY", "RZ"]
) -> Circuit:
    """Convert a circuit to the ICM form.

    Args:
        circuit (Circuit): the circuit to convert to ICM form
        gates_to_decompose (list, optional): list of gates to decompose into CNOT
        and adding ancilla qubits. Defaults to ["T", "T_Dagger"].

    Returns:
        Circuit: the circuit in ICM form
    """
    compiled_qubit_index = {i: i for i in range(circuit.n_qubits)}
    icm_circuit = []
    icm_circuit_n_qubits = circuit.n_qubits - 1
    for op in circuit.operations:
        compiled_qubits = [
            compiled_qubit_index.get(qubit, qubit) for qubit in op.qubit_indices
        ]

        if op.gate.name in gates_to_decompose:
            for original_qubit, compiled_qubit in zip(
                op.qubit_indices, compiled_qubits
            ):
                icm_circuit_n_qubits += 1
                compiled_qubit_index[original_qubit] = icm_circuit_n_qubits
                icm_circuit += [CNOT(compiled_qubit, icm_circuit_n_qubits)]
        else:
            icm_circuit += [
                op.gate(*[compiled_qubit_index[i] for i in op.qubit_indices])
            ]

    return Circuit(icm_circuit)
