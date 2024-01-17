################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import os
import sys

import pytest
from orquestra.sdk.schema.workflow_run import State
from qiskit.circuit import QuantumCircuit

import examples.data.get_icm as icm
from benchq.compilation import (
    get_algorithmic_graph_from_Jabalizer,
    pyliqtr_transpile_to_clifford_t,
)
from benchq.conversions import import_circuit
from benchq.data_structures import (
    BASIC_SC_ARCHITECTURE_MODEL,
    AlgorithmImplementation,
    ErrorBudget,
    GraphPartition,
    QuantumProgram,
)
from benchq.resource_estimation.default_pipelines import run_precise_graph_estimate
from benchq.resource_estimation.graph import GraphResourceEstimator, graph_estimator
from benchq.resource_estimation.magic_state_distillation import Widget

MAIN_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(MAIN_DIR))
from examples.ex_1_from_qasm import main as from_qasm_main  # noqa: E402
from examples.ex_2_time_evolution import main as time_evolution_main  # noqa: E402
from examples.ex_3_packages_comparison import (  # noqa: E402
    main as packages_comparison_main,
)
from examples.ex_4_fast_graph_estimates import main as fast_graph  # noqa: E402
from examples.ex_11_utility_scale import main as utility_scale  # noqa: E402

SKIP_AZURE = pytest.mark.skipif(
    os.getenv("BENCHQ_TEST_AZURE") is None,
    reason="Azure tests can only run if BENCHQ_TEST_AZURE env variable is defined",
)


# def test_orquestra_example():
#     """
#     Tests that SDK workflow example works properly at least in process
#     """

#     wf = hydrogen_workflow()
#     wf_run = wf.run("in_process")

#     loops = 0

#     while True:
#         status = wf_run.get_status()
#         if status not in {State.WAITING, State.RUNNING}:
#             break
#         if loops > 180:  # 3 minutes should be enough to finish workflow.
#             pytest.fail("WF didn't finish in 150 secs.")

#         time.sleep(1)
#         loops += 1

#     wf_run.get_results()  # this will throw an exception on failed workflow


def test_from_qasm_example():
    file_path = os.path.join("examples", "data", "example_circuit.qasm")
    from_qasm_main(file_path)


def test_time_evolution_example():
    time_evolution_main()


@SKIP_AZURE
def test_packages_comparison_example():
    packages_comparison_main()


def test_extrapolation_example():
    fast_graph()


def test_utility_scale_example():
    decoder_data = os.path.join("examples", "data", "sample_decoder_data.csv")
    gsc, footprint = utility_scale(decoder_data, False, "triangular", 3)
    assert gsc
    assert footprint


def test_toy_example_notebook():
    """Test all of the lines in the toy model work."""
    file_path = os.path.join("examples", "data", "example_circuit.qasm")
    demo_circuit = QuantumCircuit.from_qasm_file(file_path)
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL

    clifford_t_circuit = pyliqtr_transpile_to_clifford_t(
        demo_circuit, circuit_precision=1e-6
    )

    circuit_graph = get_algorithmic_graph_from_Jabalizer(clifford_t_circuit)

    budget = ErrorBudget.from_even_split(
        1e-2
    )  # only allow a failure to occur 1% of the time
    program = GraphPartition(
        QuantumProgram.from_circuit(clifford_t_circuit), [circuit_graph]
    )
    implementation = AlgorithmImplementation(program, budget, 1)
    estimator = GraphResourceEstimator(architecture_model)

    estimator.estimate(implementation)

    budget = ErrorBudget.from_even_split(
        1e-2
    )  # only allow a failure to occur 1% of the time
    program = QuantumProgram.from_circuit(import_circuit(demo_circuit))

    implementation = AlgorithmImplementation(program, budget, 1)

    run_precise_graph_estimate(implementation, architecture_model)

    get_algorithmic_graph_from_Jabalizer(clifford_t_circuit)

    icm.get_icm(clifford_t_circuit)

    graph_partition = GraphPartition(program, [circuit_graph])

    graph_data = estimator._get_graph_data_for_single_graph(graph_partition)

    widget = Widget("(15-to-1)_11,5,5", 1.9e-11, (47, 44), 2070, 30)

    len(circuit_graph)

    n_total_t_gates = estimator.get_n_total_t_gates(
        graph_data.n_t_gates,
        graph_data.n_rotation_gates,
        budget.transpilation_failure_tolerance,
    )

    distance = estimator._minimize_code_distance(
        n_total_t_gates,
        graph_data,
        architecture_model.physical_qubit_error_rate,  # physical error
        widget,
    )
    estimator._get_n_physical_qubits(graph_data, distance, widget)
    estimator._get_time_per_circuit_in_seconds(
        graph_data, distance, n_total_t_gates, widget
    )

    from benchq.resource_estimation.graph.graph_estimator import substrate_scheduler

    compiler = substrate_scheduler(circuit_graph, "fast")
    [[node[0] for node in step] for step in compiler.measurement_steps]

    circuit = QuantumCircuit.from_qasm_file(file_path)

    clifford_t_circuit = pyliqtr_transpile_to_clifford_t(
        circuit, circuit_precision=1e-10
    )
    circuit_graph = get_algorithmic_graph_from_Jabalizer(clifford_t_circuit)
    substrate_scheduler(circuit_graph, "fast")
