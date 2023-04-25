################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
TODO
"""

from pprint import pprint
from pathlib import Path

from benchq import BasicArchitectureModel
from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.data_structures import ErrorBudget
from benchq.problem_ingestion import generate_jw_qubit_hamiltonian_from_mol_data
from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)
from benchq.resource_estimation.graph import (
    ExtrapolationResourceEstimator,
    create_big_graph_from_subcircuits,
    run_extrapolation_pipeline,
    simplify_rotations,
)
from benchq.timing import measure_time
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.data_structures import DecoderModel


def main(use_hydrogen=True):
    evolution_time = 5.0
    error_budget = ErrorBudget(ultimate_failure_tolerance=1e-3)
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )

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
        algorithm = qsp_time_evolution_algorithm(
            operator, evolution_time, error_budget.circuit_generation_weight
        )
    print("Circuit generation time:", t_info.total)

    # We run the resource estimation pipeline using the graph state compilation method.
    # In this example we use delayed_gate_synthesis=True, as this is more similar to
    # how Azure QRE works.
    with measure_time() as t_info:
        extrapolated_resource_estimates = run_extrapolation_pipeline(
            algorithm.program,
            error_budget,
            estimator=ExtrapolationResourceEstimator(
                architecture_model,
                steps_to_extrapolate_from,
                decoder_model=decoder_model,
                n_measurement_steps_fit_type="linear",
            ),
            transformers=[
                simplify_rotations,
                create_big_graph_from_subcircuits(delayed_gate_synthesis=True),
            ],
        )

    print("Resource estimation time with GSC:", t_info.total)
    pprint(extrapolated_resource_estimates)


if __name__ == "__main__":
    main()
