################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
In this example, we compare the resource estimation results obtained using different
packages. We use the same circuit as in the previous example (2_time_evolution.py)
and compare the results obtained using the BenchQ's graph state compilation method and
the Azure QRE.
"""

from pathlib import Path
from pprint import pprint

from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.data_structures import BASIC_SC_ARCHITECTURE_MODEL, DecoderModel
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.resource_estimation.azure import AzureResourceEstimator
from benchq.resource_estimation.graph import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    run_custom_resource_estimation_pipeline,
    transpile_to_native_gates,
)
from benchq.timing import measure_time


def main():
    evolution_time = 5.0
    architecture_model = BASIC_SC_ARCHITECTURE_MODEL

    # Load some dummy decoder data for now. Replace with your own decoder data.
    decoder_file_path = str(Path(__file__).parent / "data" / "sample_decoder_data.csv")
    decoder_model = DecoderModel.from_csv(decoder_file_path)

    with measure_time() as t_info:
        N = 2  # Problem size
        operator = get_vlasov_hamiltonian(N=N, k=2.0, alpha=0.6, nu=0)

    print("Operator generation time:", t_info.total)

    with measure_time() as t_info:
        algorithm = qsp_time_evolution_algorithm(operator, evolution_time, 1e-3)

    print("Circuit generation time:", t_info.total)

    # We run the resource estimation pipeline using the graph state compilation method.
    # In this example we do not transpile to a clifford + T circuit, as this is more
    # similar to how Azure QRE works.
    with measure_time() as t_info:
        gsc_resource_estimates = run_custom_resource_estimation_pipeline(
            algorithm,
            estimator=GraphResourceEstimator(
                hw_model=architecture_model, decoder_model=decoder_model
            ),
            transformers=[
                transpile_to_native_gates,
                create_big_graph_from_subcircuits(),
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
        azure_resource_estimates = run_custom_resource_estimation_pipeline(
            algorithm,
            estimator=AzureResourceEstimator(),
            transformers=[],
        )

    print("Resource estimation time with Azure:", t_info.total)
    pprint(azure_resource_estimates)


if __name__ == "__main__":
    main()
