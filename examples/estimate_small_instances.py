################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
Basic example of how to perform resource estimation of a circuit from a QASM file.
"""

from copy import copy

from orquestra.integrations.qiskit.conversions import import_from_qiskit

from benchq import BASIC_SC_ARCHITECTURE_MODEL
from benchq.algorithms.qaoa import get_qaoa_program
from benchq.compilation import get_algorithmic_graph_from_Jabalizer
from benchq.data_structures import AlgorithmImplementation, DecoderModel, ErrorBudget
from benchq.problem_ingestion.hamiltonian_from_file import (
    get_all_hamiltonians_in_folder,
    get_hamiltonian_from_file,
)
from benchq.resource_estimation.graph import (
    ExtrapolationResourceEstimator,
    FootprintResourceEstimator,
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_custom_extrapolation_pipeline,
    run_custom_resource_estimation_pipeline,
    simplify_rotations,
    synthesize_clifford_t,
)


def main(file_name):
    # Uncomment to see extra debug output
    # logging.getLogger().setLevel(logging.INFO)

    # We can load a circuit from a QASM file using qiskit
    # hamiltonians = get_all_hamiltonians_in_folder("hamiltonians")
    # programs = [get_qaoa_program(ham) for ham in hamiltonians]

    # In order to perform resource estimation we need to translate it to a
    # benchq program.
    hamiltonians = get_all_hamiltonians_in_folder(file_name)
    # set number of layers!!
    programs = [get_qaoa_program(ham, n_layers=1) for ham in hamiltonians]

    for i, quantum_program in enumerate(programs):
        if i == 0:
            quantum_program.steps = 3
        if i == 1:
            quantum_program.steps = 4
        if i == 2:
            quantum_program.steps = 5
        if i == 3:
            quantum_program.steps = 6

        # Error budget is used to define what should be the failure rate of running
        # the whole calculation. It also allows to set relative weights for different
        # parts of the calculation, such as gate synthesis or circuit generation.
        error_budget = ErrorBudget.from_even_split(total_failure_tolerance=1e-3)

        # algorithm implementation encapsulates the how the algorithm is implemented
        # including the program, the number of times the program must be repeated,
        # and the error budget which will be used in the circuit.
        algorithm_description = AlgorithmImplementation(
            quantum_program, error_budget, 1
        )

        decoder_model = DecoderModel.from_csv("real_decoder_data.csv")

        # Use this for just a single layer
        gsc_resource_estimator = GraphResourceEstimator(
            BASIC_SC_ARCHITECTURE_MODEL,
            decoder_model=decoder_model,
            optimization="time",  # change this to "space" when you need to
        )

        # extrapolated_resource_estimator = ExtrapolationResourceEstimator(
        #     BASIC_SC_ARCHITECTURE_MODEL,
        #     decoder_model=decoder_model,
        #     steps_to_extrapolate_from=[1, 2, 3],
        #     optimization="time",  # change this to "space" when you need to
        # )

        # footprint_resource_estimator = FootprintResourceEstimator(
        #     BASIC_SC_ARCHITECTURE_MODEL,
        #     decoder_model=decoder_model,
        #     optimization="time",  # change this to "space" when you need to
        # )

        # Here we run the resource estimation pipeline.
        # In this case before performing estimation we use the following transformers:
        # 1. Simplify rotations – it is a simple transpilation that removes redundant
        # rotations from the circuit, such as RZ(0) or RZ(2pi) and replaces RX and RY
        # gates with RZs
        # 2. Gate synthesis – replaces all RZ gates with Clifford+T gates
        # 3. Create big graph from subcircuits – this transformer is used to create
        # a graph from subcircuits. It is needed to perform resource estimation using
        # the graph resource estimator. In this case we use delayed gate synthesis, as
        # we have already performed gate synthesis in the previous step.

        gsc_resource_estimates = run_custom_resource_estimation_pipeline(
            algorithm_description,
            estimator=gsc_resource_estimator,
            transformers=[
                simplify_rotations,
                synthesize_clifford_t(error_budget),
                create_big_graph_from_subcircuits(
                    # graph_production_method=get_algorithmic_graph_from_Jabalizer
                ),
            ],
        )

        print(f"\nGSC Resource estimates results for {quantum_program.steps}:")
        print(gsc_resource_estimates)

        # footprint_resource_estimates = run_custom_resource_estimation_pipeline(
        #     algorithm_description,
        #     estimator=footprint_resource_estimator,
        #     transformers=[
        #         simplify_rotations,
        #     ],
        # )

        # print(f"\nFootprint Resource estimation results for {quantum_program.steps}:")
        # print(footprint_resource_estimates)

        # print("\n\n")

    # for i, quantum_program in enumerate(programs):
    #     if i == 0:
    #         quantum_program.steps = 3
    #     elif i == 1:
    #         quantum_program.steps = 4
    #     elif i == 2:
    #         quantum_program.steps = 5
    #     elif i == 3:
    #         quantum_program.steps = 6

    #     # Error budget is used to define what should be the failure rate of running
    #     # the whole calculation. It also allows to set relative weights for different
    #     # parts of the calculation, such as gate synthesis or circuit generation.
    #     error_budget = ErrorBudget.from_even_split(total_failure_tolerance=1e-1)

    #     # algorithm implementation encapsulates the how the algorithm is implemented
    #     # including the program, the number of times the program must be repeated,
    #     # and the error budget which will be used in the circuit.
    #     algorithm_description = AlgorithmImplementation(
    #         quantum_program, error_budget, 1
    #     )

    #     decoder_model = DecoderModel.from_csv("real_decoder_data.csv")

    #     # Use this for just a single layer
    #     gsc_resource_estimator = GraphResourceEstimator(
    #         BASIC_SC_ARCHITECTURE_MODEL,
    #         decoder_model=decoder_model,
    #         optimization="time",  # change this to "space" when you need to
    #     )

    #     extrapolated_resource_estimator = ExtrapolationResourceEstimator(
    #         BASIC_SC_ARCHITECTURE_MODEL,
    #         decoder_model=decoder_model,
    #         steps_to_extrapolate_from=[1, 2, 3],
    #         optimization="time",  # change this to "space" when you need to
    #     )

    #     footprint_resource_estimator = FootprintResourceEstimator(
    #         BASIC_SC_ARCHITECTURE_MODEL,
    #         decoder_model=decoder_model,
    #         optimization="time",  # change this to "space" when you need to
    #     )

    #     # Here we run the resource estimation pipeline.
    #     # In this case before performing estimation we use the following transformers:
    #     # 1. Simplify rotations – it is a simple transpilation that removes redundant
    #     # rotations from the circuit, such as RZ(0) or RZ(2pi) and replaces RX and RY
    #     # gates with RZs
    #     # 2. Gate synthesis – replaces all RZ gates with Clifford+T gates
    #     # 3. Create big graph from subcircuits – this transformer is used to create
    #     # a graph from subcircuits. It is needed to perform resource estimation using
    #     # the graph resource estimator. In this case we use delayed gate synthesis, as
    #     # we have already performed gate synthesis in the previous step.
    #     gsc_resource_estimates = run_custom_resource_estimation_pipeline(
    #         algorithm_description,
    #         estimator=gsc_resource_estimator,
    #         transformers=[
    #             simplify_rotations,
    #             create_big_graph_from_subcircuits(
    #                 graph_production_method=get_algorithmic_graph_from_Jabalizer
    #             ),
    #         ],
    #     )

    #     print(f"\nGSC Resource estimates results for {quantum_program.steps}:")
    #     print(gsc_resource_estimates)

    #     extrapolated_resource_estimates = run_custom_extrapolation_pipeline(
    #         copy(algorithm_description),
    #         estimator=extrapolated_resource_estimator,
    #         transformers=[
    #             simplify_rotations,
    #             create_big_graph_from_subcircuits(
    #                 graph_production_method=get_algorithmic_graph_from_Jabalizer
    #             ),
    #         ],
    #     )

    #     print(
    #         f"\nExtrapolated Resource estimation results for {quantum_program.steps}:"
    #     )
    #     print(extrapolated_resource_estimates)

    #     print("\n\n")


if __name__ == "__main__":
    main("small_qubo_instances")
