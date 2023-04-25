################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
In this example, we compare the resource estimation results obtained using different
packages. We use the same circuit as in the previous example (2_time_evolution.py)
and compare the results obtained using the BenchQ's graph state compilation method and 
the Azure QRE.
"""

from pprint import pprint
import os
from pathlib import Path

from benchq import BasicArchitectureModel
from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.data_structures import ErrorBudget
from benchq.problem_ingestion import generate_jw_qubit_hamiltonian_from_mol_data
from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)
from benchq.resource_estimation.azure import AzureResourceEstimator
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_resource_estimation_pipeline,
    simplify_rotations,
    synthesize_clifford_t,
)
from benchq.timing import measure_time
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.data_structures import DecoderModel


def main():
    evolution_time = 5.0
    error_budget = ErrorBudget(ultimate_failure_tolerance=1e-3)
    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )

    decoder_file_path = str(Path(__file__).parent / "data" / "sample_decoder_data.csv")
    decoder_model = DecoderModel.from_csv(decoder_file_path)

    with measure_time() as t_info:
        N = 2  # Problem size
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
        gsc_resource_estimates = run_resource_estimation_pipeline(
            algorithm.program,
            error_budget,
            estimator=GraphResourceEstimator(
                hw_model=architecture_model, decoder_model=decoder_model
            ),
            transformers=[
                simplify_rotations,
                create_big_graph_from_subcircuits(delayed_gate_synthesis=True),
            ],
        )

    print("Resource estimation time with GSC:", t_info.total)
    pprint(gsc_resource_estimates)

    # AzureResourceEstimator is a wrapper around Azure QRE. It takes the same arguments
    # as GraphResourceEstimator, but instead of running the graph state compilation
    # method, it runs the Azure QRE.
    # Azure QRE takes in quantum circuits as input and performs compilation internally,
    # so there's no need for using any transformers.
    with measure_time() as t_info:
        azure_resource_estimates = run_resource_estimation_pipeline(
            algorithm.program,
            error_budget,
            estimator=AzureResourceEstimator(),
            transformers=[],
        )

    print("Resource estimation time with Azure:", t_info.total)
    pprint(azure_resource_estimates)


if __name__ == "__main__":
    main()
