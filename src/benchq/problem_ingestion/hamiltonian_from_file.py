################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################

import json
import os
from typing import List, Union

import h5py
import numpy as np
import openfermion as of
from openfermion import InteractionOperator, QubitOperator, jordan_wigner
from orquestra.integrations.cirq.conversions import from_openfermion
from orquestra.quantum.operators import PauliSum, PauliTerm
from orquestra.quantum.utils import ensure_open


def get_hamiltonian_from_file(
    file_name: str, allow_unsupported_files=True
) -> Union[PauliSum, None]:
    """Given a file with a hamiltonian, extract the hamiltonian from it. Currently
    supports json and hdf5 files.

    Args:
        file_name (str): The name of the file containing the hamiltonian in either
            json or hdf5 format
        allow_unsupported_files (bool): Whether to skip unsupported files
    Returns:
        Union[PauliSum, None]: The hamiltonian corresponding to the file. If the
            file is not supported and allow_unsupported_files is True, returns None.

    Raises:
        ValueError: If the file format is not supported and allow_unsupported_files
            is False
    """
    if file_name.endswith(".json"):
        return _get_hamiltonian_from_json(file_name)
    elif file_name.endswith(".hdf5"):
        return _get_hamiltonian_from_hdf5(file_name)
    else:
        if not allow_unsupported_files:
            file_extension = file_name.split(".")[-1]
            raise ValueError(
                f"Hamiltonian extraction failed for {file_name}. "
                f"File format {file_extension} is not supported."
            )
        else:
            return None


def get_all_hamiltonians_in_folder(
    folder_name: str, allow_unsupported_files=True
) -> List[PauliSum]:
    """Given a folder with hamiltonians in either json or hdf5 format, generate
    a list of all the hamiltonians.

    Args:
          folder_name (str): The name of the folder containing the hamiltonians
          allow_unsupported_files (bool): Whether to skip unsupported files
    Returns:
          List of hamiltonians for all of the files in the folder

    Raises:
        ValueError: If the a file with in the provided folder is not supported
            and allow_unsupported_files is False
    """
    hamiltonians = []
    for file_name in os.listdir(folder_name):
        full_file_name = folder_name + "/" + file_name
        hamiltonian = get_hamiltonian_from_file(full_file_name, allow_unsupported_files)
        if hamiltonian is not None:
            hamiltonians.append(hamiltonian)
    return hamiltonians


def _get_hamiltonian_from_json(file_name: str) -> PauliSum:
    """Given a file with a hamiltonian, generate QAOA circuit corresponding to it.

    Args:
          file_name (str): The name of the json file containing the hamiltonian
    Returns:
          the hamiltonian stored in the file
    """
    with ensure_open(file_name, "r") as f:
        data = json.load(f)

    full_operator = of.QubitOperator()
    for term_dict in data["terms"]:
        operator = []
        for pauli_op in term_dict["pauli_ops"]:
            operator.append((pauli_op["qubit"], pauli_op["op"]))
        coefficient = term_dict["coefficient"]["real"]
        if term_dict["coefficient"].get("imag"):
            coefficient += 1j * term_dict["coefficient"]["imag"]
        full_operator += of.QubitOperator(operator, coefficient)

    return from_openfermion(full_operator)


def _get_hamiltonian_from_hdf5(file_name: str) -> PauliSum:
    """Given a file with a hamiltonian, generate hamiltonian terms corresponding to it.
    This function only accepts hamiltonians in the format used by Guoming Wang's
    QAOA implementation and Alex Kunitsa's molecule implementation.

    Args:
          file_name (str): The name of the hdf5 file containing the hamiltonian
    Returns:
          the hamiltonian stored in the file

    Raises:
        ValueError: If the file format is not supported
    """
    data = h5py.File(file_name, "r")

    if "q_matrix" in data.keys():
        return _qaoa_hamiltonian_from_hdf5(data)
    elif "basis" in data.attrs:
        return from_openfermion(_molecule_hamiltonian_from_hdf5(data))
    else:
        raise ValueError(
            f"Hamiltonian extraction failed for {file_name}. "
            f"File format is not recognized. Please use formatting from either "
            f"Guoming Wang's QAOA implementation or Alex Kunitsa's molecule "
            f"implementation."
        )


def _qaoa_hamiltonian_from_hdf5(data: h5py.File) -> PauliSum:
    """Given a file with a hamiltonian, generate hamiltonian terms corresponding to it.
    This function only accepts hamiltonians in the format where the hamiltonian is
    stored as a q_matrix property of an hdf5 file   .

    Args:
        data (h5py.File): The hdf5 file containing the hamiltonian

    Returns:
        PauliSum: the hamiltonian stored in the file
    """
    q_matrix = np.array(data["q_matrix"][()])
    assert q_matrix.shape[0] == q_matrix.shape[1]

    N = q_matrix.shape[0]
    q_matrix = (q_matrix + q_matrix.T) / 2.0
    pauli_terms = []

    for i in range(N):
        # diagonal terms
        diag_pauli_term1 = PauliTerm("I0", q_matrix[i][i] / 2.0)
        diag_pauli_term2 = PauliTerm(f"Z{i}", -q_matrix[i][i] / 2.0)
        pauli_terms.append(diag_pauli_term1)
        pauli_terms.append(diag_pauli_term2)

        for j in range(i):
            # off-diagonal terms
            off_diag_pauli_term1 = PauliTerm("I0", q_matrix[i][j] / 2.0)
            off_diag_pauli_term2 = PauliTerm(f"Z{i}", -q_matrix[i][j] / 2.0)
            off_diag_pauli_term3 = PauliTerm(f"Z{j}", -q_matrix[i][j] / 2.0)
            off_diag_pauli_term4 = PauliTerm(f"Z{i} * Z{j}", q_matrix[i][j] / 2.0)
            pauli_terms.append(off_diag_pauli_term1)
            pauli_terms.append(off_diag_pauli_term2)
            pauli_terms.append(off_diag_pauli_term3)
            pauli_terms.append(off_diag_pauli_term4)

    hamiltonian = PauliSum(pauli_terms).simplify()
    return hamiltonian


def _molecule_hamiltonian_from_hdf5(data: h5py.File) -> QubitOperator:
    """Given a file with a hamiltonian, generate hamiltonian terms corresponding to it.
    This function only accepts hamiltonians in the format with one and two body terms as
    attributes of the hdf5 file.

    Args:
        data: A file with a hamiltonian described by one and two body terms.

    Returns:
        The Jordan-Wigner transformed Hamiltonian.
    """
    one_body_term = data["one_body_tensor"]
    two_body_term = data["two_body_tensor"]

    hamiltonian = InteractionOperator(
        constant=data.attrs["constant"],
        one_body_tensor=one_body_term,
        two_body_tensor=two_body_term,
    )
    return jordan_wigner(hamiltonian)
