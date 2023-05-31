################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
In this example we show how to deal with the case where the problem is too large to be
compiled to a graph. We use the extrapolation technique to estimate resources
for running time evolution for H2 molecule.
Number of block encodings needed to run the algorithm is too high, so we
estimate resources need for running similar circuit with 1, 2 and 3 block encodings
and then we extrapolate the results to estimate resources for full problem.
"""

from pathlib import Path
from pprint import pprint

from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.data_structures import (
    BASIC_SC_ARCHITECTURE_MODEL,
    DecoderModel,
    ErrorBudget,
)
from benchq.problem_ingestion import (
    generate_jw_qubit_hamiltonian_from_mol_data,
    get_vlasov_hamiltonian,
)
from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)
from benchq.resource_estimation.graph import (
    ExtrapolationResourceEstimator,
    create_big_graph_from_subcircuits,
    run_custom_extrapolation_pipeline,
    simplify_rotations,
)
from benchq.timing import measure_time


def main(use_hydrogen=True):
    evolution_time = 5.0
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL

    steps_to_extrapolate_from = [1, 2, 3]

    decoder_file_path = str(Path(__file__).parent / "data" / "sample_decoder_data.csv")
    decoder_model = DecoderModel.from_csv(decoder_file_path)

    with measure_time() as t_info:
        N = 2
        if use_hydrogen:
            application_instance = generate_hydrogen_chain_instance(N)
            operator = generate_jw_qubit_hamiltonian_from_mol_data(application_instance)
        else:
            operator = get_vlasov_hamiltonian(N=N, k=2.0, alpha=0.6, nu=0)

    print("Operator generation time:", t_info.total)

    with measure_time() as t_info:
        algorithm = qsp_time_evolution_algorithm(operator, evolution_time, 1e-3)
    print("Circuit generation time:", t_info.total)

    with measure_time() as t_info:
        extrapolated_resource_estimates = run_custom_extrapolation_pipeline(
            algorithm,
            estimator=ExtrapolationResourceEstimator(
                architecture_model,
                steps_to_extrapolate_from,
                decoder_model=decoder_model,
                n_measurement_steps_fit_type="linear",
            ),
            transformers=[
                simplify_rotations,
                create_big_graph_from_subcircuits(),
            ],
        )

    print("Resource estimation time with GSC:", t_info.total)
    pprint(extrapolated_resource_estimates)


if __name__ == "__main__":
    main()
