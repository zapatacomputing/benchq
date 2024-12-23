################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import os
import sys

import pytest
from orquestra.sdk.schema.workflow_run import State
from qiskit.circuit import QuantumCircuit

from benchq.algorithms.data_structures import AlgorithmImplementation, ErrorBudget
from benchq.compilation.circuits import pyliqtr_transpile_to_clifford_t
from benchq.compilation.graph_states import (
    get_implementation_compiler,
    get_jabalizer_circuit_compiler,
    jl,
)
from benchq.compilation.graph_states.substrate_scheduler.python_substrate_scheduler import (  # noqa: E501
    python_substrate_scheduler,
)
from benchq.conversions import import_circuit
from benchq.logical_architecture_modeling.graph_based_logical_architectures import (
    TwoRowBusArchitectureModel,
)
from benchq.quantum_hardware_modeling import BASIC_SC_ARCHITECTURE_MODEL
from benchq.resource_estimators.default_estimators import get_precise_graph_estimate
from benchq.resource_estimators.graph_estimator import GraphResourceEstimator

MAIN_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(MAIN_DIR))
from examples.data.get_icm import get_icm  # noqa: E402
from examples.ex_1_from_qasm import main as from_qasm_main  # noqa: E402
from examples.ex_2_time_evolution import main as time_evolution_main  # noqa: E402
from examples.ex_4_fast_graph_estimates import main as fast_graph  # noqa: E402
from examples.ex_10_utility_scale import main as utility_scale  # noqa: E402


def test_from_qasm_example():
    file_path = os.path.join("examples", "data", "example_circuit.qasm")
    from_qasm_main(file_path)


def test_time_evolution_example():
    time_evolution_main()


def test_fast_graph_example():
    fast_graph()


def test_utility_scale_example():
    decoder_data = os.path.join("examples", "data", "sample_decoder_data.csv")
    gsc, footprint = utility_scale(decoder_data, False, "triangular", 2)
    assert gsc
    assert footprint


def test_toy_example_notebook():
    """Test all of the lines in the toy model work."""
    file_path = os.path.join("examples", "data", "single_rotation.qasm")
    demo_circuit = QuantumCircuit.from_qasm_file(file_path)
    hardware_architecture_model = BASIC_SC_ARCHITECTURE_MODEL
    logical_architecture_model = TwoRowBusArchitectureModel()
    logical_architecture_name = logical_architecture_model.name

    clifford_t_circuit = pyliqtr_transpile_to_clifford_t(
        demo_circuit, circuit_precision=1e-2
    )

    compiler = get_jabalizer_circuit_compiler()
    optimization = "Time"  # or "Space"
    verbose = False
    compiler(
        clifford_t_circuit,
        logical_architecture_name,
        optimization,
        verbose,
    )

    asg, pauli_tracker, _ = jl.get_rbs_graph_state_data(
        clifford_t_circuit,
        takes_graph_input=False,
        gives_graph_output=False,
        verbose=verbose,
        optimization=optimization,
    )
    asg = jl.python_asg(asg)
    pauli_tracker = jl.python_pauli_tracker(pauli_tracker)

    # 1% error margin split evenly between all sources of error
    budget = ErrorBudget.from_even_split(1e-2)
    # Specify the circuit and the margins of error we allow in the results
    implementation = AlgorithmImplementation.from_circuit(
        clifford_t_circuit, budget, n_shots=1
    )

    # Specify how to run the circuit
    estimator = GraphResourceEstimator(optimization, verbose)

    # Modify our compiler to compile AlgorithmImplementation objects rather than
    # just circuits
    implementation_compiler = get_implementation_compiler(compiler)

    # run the estimator
    estimator.compile_and_estimate(
        implementation,
        implementation_compiler,
        logical_architecture_model,
        hardware_architecture_model,
    )

    # only allow a failure to occur 1% of the time
    budget = ErrorBudget.from_even_split(1e-2)
    implementation = AlgorithmImplementation.from_circuit(demo_circuit, budget, 1)
    optimization = "Time"
    get_precise_graph_estimate(
        implementation,
        logical_architecture_model,
        hardware_architecture_model,
        optimization,
    )

    compiler(
        clifford_t_circuit,
        logical_architecture_name,
        "Time",
        True,
    )

    get_icm(clifford_t_circuit)

    asg, _, __ = jl.get_rbs_graph_state_data(
        clifford_t_circuit,
        takes_graph_input=False,
        gives_graph_output=False,
        verbose=False,
    )
    asg = jl.python_asg(asg)

    if logical_architecture_name == "Time":
        print("shallow")
        breakpoint()

    compiled_implementation = implementation_compiler(
        implementation,
        logical_architecture_name=logical_architecture_name,
        optimization=optimization,
    )
    compiled_implementation.program.subroutines[0]

    estimator.estimate_resources_from_compiled_implementation(
        compiled_implementation,
        logical_architecture_model,
        hardware_architecture_model,
    )

    schedule = python_substrate_scheduler(asg, "fast")

    [[node[0] for node in step] for step in schedule.measurement_steps]

    file_path = os.path.join("examples", "data", "ghz_circuit.qasm")
    ghz_circuit = import_circuit(QuantumCircuit.from_qasm_file(file_path))

    asg, _, __ = jl.get_rbs_graph_state_data(
        ghz_circuit, takes_graph_input=False, gives_graph_output=False, verbose=False
    )
    asg = jl.python_asg(asg)

    schedule = python_substrate_scheduler(asg, "fast")

    file_path = os.path.join("examples", "data", "h_chain_circuit.qasm")
    h_chain_circuit = import_circuit(QuantumCircuit.from_qasm_file(file_path))

    asg, _, __ = jl.get_rbs_graph_state_data(
        h_chain_circuit,
        takes_graph_input=False,
        gives_graph_output=False,
        verbose=False,
    )
    asg = jl.python_asg(asg)

    schedule = python_substrate_scheduler(asg, "fast")
