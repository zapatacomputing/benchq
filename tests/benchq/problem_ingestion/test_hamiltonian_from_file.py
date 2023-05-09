################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import pathlib

import pytest

from benchq.problem_ingestion import (
    get_all_hamiltonians_in_folder,
    get_hamiltonian_from_file,
)


@pytest.mark.parametrize(
    "file_name",
    [
        "test_hamiltonian.json",
        "test_guoming_hamiltonian.hdf5",
        "test_alex_hamiltonian.hdf5",
    ],
)
def test_get_hamiltonian_from_file(file_name):
    curr_dir = str(pathlib.Path(__file__).parent.resolve())
    full_file_name = curr_dir + "/test_hamiltonian_folder/" + file_name
    hamiltonian = get_hamiltonian_from_file(full_file_name)

    assert hamiltonian is not None
    assert hamiltonian.terms is not []


def test_get_hamiltonian_from_unsupported_file_returns_none_by_default():
    curr_dir = str(pathlib.Path(__file__).parent.resolve())
    full_file_name = curr_dir + "/test_hamiltonian_folder/test_hamiltonian.txt"
    hamiltonian = get_hamiltonian_from_file(full_file_name)

    assert hamiltonian is None


def test_get_hamiltonian_from_file_raises_error_for_improperly_formatted_files():
    curr_dir = str(pathlib.Path(__file__).parent.resolve())
    full_file_name = curr_dir + "/test_hamiltonian_folder/test_hamiltonian.txt"
    with pytest.raises(ValueError):
        get_hamiltonian_from_file(full_file_name, allow_unsupported_files=False)


def test_get_all_hamiltonians_in_folder():
    curr_dir = str(pathlib.Path(__file__).parent.resolve())
    full_file_name = curr_dir + "/test_hamiltonian_folder"
    hamiltonians = get_all_hamiltonians_in_folder(full_file_name)

    assert len(hamiltonians) == 3
    for hamiltonian in hamiltonians:
        assert hamiltonian is not None
        assert hamiltonian.terms is not []


def test_get_all_hamiltonians_in_folder_raises_error_for_improperly_formatted_files():
    curr_dir = str(pathlib.Path(__file__).parent.resolve())
    full_file_name = curr_dir + "/test_hamiltonian_folder"
    with pytest.raises(ValueError):
        get_all_hamiltonians_in_folder(full_file_name, allow_unsupported_files=False)
