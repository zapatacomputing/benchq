################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
In this example, we compare the resource estimation results obtained using different
packages. We use the same circuit as in the previous example (2_time_evolution.py)
and compare the results obtained using the BenchQ's graph state compilation method and
the Azure QRE.
WARNING: This example requires the pyscf extra. run `pip install benchq[pyscf]`
to install the extra.
"""

from pathlib import Path
from pprint import pprint

from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.compilation.graph_states import (
    get_implementation_compiler,
    get_ruby_slippers_circuit_compiler,
)
from benchq.decoder_modeling import DecoderModel
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.quantum_hardware_modeling import BASIC_SC_ARCHITECTURE_MODEL
from benchq.resource_estimators.azure_estimator import azure_estimator
from benchq.resource_estimators.graph_estimator import GraphResourceEstimator
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

    # We can adjust some of the parameters of the graph state compilation method.
    # Here I've included some of the most important ones as an example.
    circuit_compiler = get_ruby_slippers_circuit_compiler(
        optimal_dag_density=10,
        teleportation_threshold=60,
    )

    # We run the resource estimation pipeline using the graph state compilation method.
    # In this example we do not transpile to a clifford + T circuit, as this is more
    # similar to how Azure QRE works.
    with measure_time() as t_info:
        implementation_compiler = get_implementation_compiler(
            circuit_compiler=circuit_compiler, destination="single-thread"
        )
        gsc_estimator = GraphResourceEstimator(optimization="Time", verbose=True)
        gsc_resource_estimates = gsc_estimator.compile_and_estimate(
            algorithm,
            implementation_compiler,
            architecture_model,
            decoder_model=decoder_model,
        )

    print("Resource estimation time with GSC:", t_info.total)
    pprint(gsc_resource_estimates)

    # azure_estimator is a wrapper around Azure QRE. It takes the same arguments
    # as GraphResourceEstimator, but instead of running the graph state compilation
    # method, it runs the Azure QRE.
    # Azure QRE takes in quantum circuits as input and performs compilation internally,
    # so there's no need for using any transformers.
    with measure_time() as t_info:
        azure_resource_estimates = azure_estimator(
            algorithm,
            architecture_model=architecture_model,
        )

    print("Resource estimation time with Azure:", t_info.total)
    pprint(azure_resource_estimates)


if __name__ == "__main__":
    main()
