################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import pyLIQTR.model_simulators.vlasovsim as vs  # Cannot find this in pyLIQTR_v1
from orquestra.integrations.cirq.conversions import from_openfermion
from orquestra.quantum.operators import PauliRepresentation

from pyLIQTR.utils.Hamiltonian import Hamiltonian as pyH


from ...conversions import pyliqtr_to_openfermion


def get_vlasov_hamiltonian(
    k: float, alpha: float, nu: float, N: int
) -> PauliRepresentation:
    ham_strings = vs.hamiltonian_wfn_vlasov_hermite_linear_sym_string(k, alpha, nu, N)
    qsp_H = pyH(ham_strings)
    pauli_sum = from_openfermion(pyliqtr_to_openfermion(qsp_H))
    for term in pauli_sum.terms:
        term.coefficient = term.coefficient.real
    return pauli_sum
