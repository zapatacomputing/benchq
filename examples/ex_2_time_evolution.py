################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
Example showing how to estimate the resources required to run a time evolution
algorithm. It shows two different ways of estimating the resources: one with gate
synthesis performed at the circuit level, while the other one does it during the
measurement phase. The first is more accurate and leads to lower resources,
but is also more expensive in terms of runtime and memory usage.

Most of the objects has been described in the `1_from_qasm.py` examples, here
we only explain new concepts.
"""
from pprint import pprint

from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.data_structures import BASIC_SC_ARCHITECTURE_MODEL
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.problem_ingestion.hamiltonian_generation import (
    generate_1d_heisenberg_hamiltonian,
    generate_cubic_hamiltonian,
)
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_custom_resource_estimation_pipeline,
    synthesize_clifford_t,
    transpile_to_native_gates,
)
from benchq.timing import measure_time

from benchq.compilation.julia_utils import (
    get_ruby_slippers_compiler,
    get_algorithmic_graph_from_Jabalizer,
    get_algorithmic_graph_from_graphsim_mini,
)


def main():
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL

    # Utility scale numbers:
    # evolution_time = 100
    # N = 10
    # these are out of reach for GraphResourceEstimator but you can at least see
    # what the progress looks like.
    evolution_time = 100
    N = 10

    operator = generate_cubic_hamiltonian(N)
    algorithm = qsp_time_evolution_algorithm(operator, evolution_time, 1e-3)
    algorithm.program.steps = 1

    run_custom_resource_estimation_pipeline(
        algorithm,
        estimator=GraphResourceEstimator(architecture_model),
        transformers=[
            transpile_to_native_gates,
            # Pick your compiler!
            # 1. Ruby Slippers
            create_big_graph_from_subcircuits(  # default teleportation threshold is 40
                graph_production_method=get_ruby_slippers_compiler()
            ),
            # 2. Graph Sim mini
            # create_big_graph_from_subcircuits(
            #     graph_production_method=get_algorithmic_graph_from_graphsim_mini
            # ),
            # 3. Jabalizer
            create_big_graph_from_subcircuits(
                graph_production_method=get_algorithmic_graph_from_Jabalizer
            ),
        ],
    )


if __name__ == "__main__":
    main()
