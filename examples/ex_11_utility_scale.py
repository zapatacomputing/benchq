import datetime
import json
import os
import typing
import warnings
from pathlib import Path
from typing import Literal

from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.compilation import get_ruby_slippers_compiler
from benchq.quantum_hardware_modeling import DETAILED_ION_TRAP_ARCHITECTURE_MODEL
from benchq.decoder_modeling import DecoderModel
from benchq.problem_ingestion.hamiltonians.ising_hamiltonians import (
    generate_cubic_hamiltonian,
    generate_kitaev_hamiltonian,
    generate_triangular_hamiltonian,
)
from benchq.resource_estimators.graph_estimators import (
    ExtrapolationResourceEstimator,
    create_big_graph_from_subcircuits,
    remove_isolated_nodes,
    run_custom_extrapolation_pipeline,
    transpile_to_native_gates,
)
from benchq.resource_estimators.footprint_estimators.openfermion_estimator import (
    footprint_estimator,
)


def get_resources(lattice_type: str, size: int, decoder_data_file: str):
    print(f"Getting operator for size {size} {lattice_type} lattice...")
    if lattice_type == "triangular":
        operator = generate_triangular_hamiltonian(size)
    elif lattice_type == "kitaev":
        operator = generate_kitaev_hamiltonian(size)
    elif lattice_type == "cubic":
        operator = generate_cubic_hamiltonian(size)
    else:
        raise ValueError(f"Lattice type {lattice_type} not supported")

    architecture_model = DETAILED_ION_TRAP_ARCHITECTURE_MODEL

    print("Getting algorithm implementation...")
    evolution_time = 1
    failure_tolerance = 1e-4
    algorithm_implementation = qsp_time_evolution_algorithm(
        operator, evolution_time, failure_tolerance
    )

    print("Setting resource estimation parameters...")
    decoder_model = DecoderModel.from_csv(decoder_data_file)
    my_estimator = ExtrapolationResourceEstimator(
        architecture_model,
        [2, 4, 6, 8, 10],
        n_measurement_steps_fit_type="logarithmic",
        optimization="space",
        decoder_model=decoder_model,
    )

    # select teleportation threshold to tune number of logical qubits
    if lattice_type == "triangular":
        gpm = get_ruby_slippers_compiler(teleportation_threshold=70)
    elif lattice_type == "kitaev":
        gpm = get_ruby_slippers_compiler(teleportation_threshold=60)
    elif lattice_type == "cubic":
        gpm = get_ruby_slippers_compiler(teleportation_threshold=70)
    else:
        raise ValueError(f"Lattice type {lattice_type} not supported")

    print("Estimating resources via graph state compilation...")
    gsc_resources = run_custom_extrapolation_pipeline(
        algorithm_implementation,
        my_estimator,
        transformers=[
            transpile_to_native_gates,
            create_big_graph_from_subcircuits(gpm),
            remove_isolated_nodes,
        ],
    )

    total_t_gates = my_estimator.get_n_total_t_gates(
        gsc_resources.extra.n_t_gates,
        gsc_resources.extra.n_rotation_gates,
        algorithm_implementation.error_budget.transpilation_failure_tolerance,
    )

    footprint_resources = footprint_estimator(
        algorithm_implementation.program.num_data_qubits,
        num_t=total_t_gates,
        architecture_model=my_estimator.hw_model,
        hardware_failure_tolerance=algorithm_implementation.error_budget.hardware_failure_tolerance,
        decoder_model=decoder_model,
    )
    return gsc_resources, footprint_resources


def save_to_file(gsc_resources, footprint_resources, lattice_type, path: str):
    results_folder = path

    with open(results_folder + lattice_type + "_gsc_re_data.json", "w") as outfile:
        json.dump(gsc_resources, outfile, indent=4, sort_keys=True, default=str)
    with open(
        results_folder + lattice_type + "_footprint_re_data.json", "w"
    ) as outfile:
        json.dump(footprint_resources, outfile, indent=4, sort_keys=True, default=str)


def main(
    decoder_data_file: str,
    save_results: bool,
    lattice_type: Literal["triangular", "kitaev", "cubic"],
    size: int,
    path_to_save_results: typing.Optional[str] = None,
):
    gsc_estimates, footprint_estimates = get_resources(
        lattice_type, size, decoder_data_file
    )

    if save_results:
        if path_to_save_results is None:
            warnings.warn("Path is required to save the results.")
        else:
            save_to_file(
                gsc_estimates, footprint_estimates, lattice_type, path_to_save_results
            )

    return gsc_estimates, footprint_estimates


if __name__ == "__main__":
    warnings.warn(
        "These utility scale estimates take a lot of time to calculate."
        "It can take up to a day for single example to finish calculation."
    )

    decoder_data = "data/sample_decoder_data.csv"
    save_results = False
    path_to_save_results = "."

    utiliy_scale_problems: typing.Dict[
        Literal["triangular", "kitaev", "cubic"], int
    ] = {"triangular": 30, "kitaev": 22, "cubic": 10}

    lattice_type: Literal["triangular", "kitaev", "cubic"]

    lattice_type = "triangular"
    # lattice_type = "kitaev"
    # lattice_type = "cubic"

    gsc_estimates, footprint_estimates = main(
        decoder_data,
        save_results,
        lattice_type,
        utiliy_scale_problems[lattice_type],
        path_to_save_results,
    )

    print(gsc_estimates)
    print(footprint_estimates)
