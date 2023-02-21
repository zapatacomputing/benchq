################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
# from juliacall import Main as jl
import json
import logging
import os
import pathlib
import subprocess
import time
import typing as t

import networkx as nx

LOGGER = logging.getLogger(__name__)


def load_algorithmic_graph(filename):
    t1 = time.time()
    graph = nx.read_adjlist(filename)
    LOGGER.info("nx.read_adjlist: ", time.time() - t1)
    return graph


def _run_quietly(cmd: t.Sequence[str]):
    """
    Runs ``cmd`` in a subprocess. Directs the child's stdout to a logger. Stderr is
    printed to the parent's process output.
    """
    LOGGER.info("Running command in a subprocess: %s", cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Based on: https://stackoverflow.com/a/21978778
    pipe: t.Any = proc.stdout
    for line in iter(pipe.readline, b""):
        line_str = line.decode().strip()
        LOGGER.info(line_str)

    proc.wait()

    assert proc.returncode == 0, f"Running {cmd} returned error code: {proc.returncode}"


def get_algorithmic_graph(circuit):
    n_qubits = circuit.n_qubits
    icm_input_circuit = translate_circuit_to_icm_input(circuit)
    icm_input_circuit.append(n_qubits)

    exec_path = pathlib.Path(__file__).parent.resolve()
    exec_name = "jabalizer_wrapper.jl"

    with open("icm_input_circuit.json", "w") as outfile:
        json.dump(icm_input_circuit, outfile)

    julia_file = os.path.join(exec_path, exec_name)
    # jl.evalfile(julia_file)
    _run_quietly(["julia", julia_file])

    return load_algorithmic_graph("adjacency_list.nxl")


def translate_circuit_to_icm_input(circuit):
    icm_input_circuit = []
    for op in circuit.operations:
        name = op.gate.name
        # TODO: THIS IS NOT CORRECT! TEMPORARY HACK!
        if name == "S_Dagger":
            name = "S"
        if name == "T_Dagger":
            name = "T"

        qubits = op.qubit_indices
        icm_gate = (name, [str(qubit) for qubit in qubits])
        icm_input_circuit.append(icm_gate)

    return icm_input_circuit
