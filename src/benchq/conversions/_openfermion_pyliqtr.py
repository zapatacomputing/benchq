################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
from openfermion import QubitOperator, count_qubits
from pyLIQTR.QSP.Hamiltonian import Hamiltonian


def pyliqtr_to_openfermion(hamiltonian: Hamiltonian) -> QubitOperator:
    """Converts a Hamiltonian from pyLIQTR form into Openfermion.

    Args:
        hamiltonian: Hamiltonian to be converted
    """
    qubit_op = QubitOperator()
    for term in hamiltonian.terms:
        ops = [f"{op}{i}" for i, op in enumerate(term[0]) if op != "I"]
        qubit_op += term[1] * QubitOperator("[" + " ".join(ops) + "]")
    return qubit_op


def openfermion_to_pyliqtr(qubit_operator: QubitOperator) -> Hamiltonian:
    """Converts a QubitOperator from Openfermion into pyLIQTR

    Args:
        qubit_operator: qubit operator to be converted
    """
    n_qubits = count_qubits(qubit_operator)
    new_terms = []
    for term, coeff in qubit_operator.terms.items():
        new_term_list = ["I"] * n_qubits
        for op in term:
            new_term_list[op[0]] = op[1]
        new_terms.append(("".join(new_term_list), coeff))
    return Hamiltonian(new_terms)
