import datetime
import json
import os
from dataclasses import dataclass
from pathlib import Path

from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.compilation import get_ruby_slippers_compiler
from benchq.data_structures import (
    BASIC_ION_TRAP_ARCHITECTURE_MODEL,
    BASIC_SC_ARCHITECTURE_MODEL,
    DecoderModel,
)
from benchq.data_structures.hardware_architecture_models import DetailedIonTrapModel
from benchq.problem_ingestion.hamiltonian_generation import (
    generate_cubic_hamiltonian,
    generate_kitaev_hamiltonian,
    generate_triangular_hamiltonian,
)
from benchq.resource_estimation.graph import (
    ExtrapolationResourceEstimator,
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    remove_isolated_nodes,
    run_custom_extrapolation_pipeline,
    run_custom_resource_estimation_pipeline,
    transpile_to_native_gates,
)
from benchq.resource_estimation.openfermion_re import get_physical_cost


def get_resources(lattice_type: str, size: int, architecture_model):
    print(f"Getting operator for size {size} {lattice_type} lattice...")
    if lattice_type == "triangular":
        operator = generate_triangular_hamiltonian(size)
    elif lattice_type == "kitaev":
        operator = generate_kitaev_hamiltonian(size)
    elif lattice_type == "cubic":
        operator = generate_cubic_hamiltonian(size)
    else:
        raise ValueError(f"Lattice type {lattice_type} not supported")

    print("Getting algorithm implementation...")
    evolution_time = 1
    failure_tolerance = 1e-4
    algorithm_implementation = qsp_time_evolution_algorithm(
        operator, evolution_time, failure_tolerance
    )

    print("Setting resource estimation parameters...")
    decoder_model = DecoderModel.from_csv("stochastic_re_realistic.csv")
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

    if architecture_model == BASIC_ION_TRAP_ARCHITECTURE_MODEL:
        gsc_detailed_ion_trap_resource_info = (
            DetailedIonTrapModel().get_hardware_resource_estimates(gsc_resources)
        )

    print("Estimating resources via footprint analysis...")
    total_t_gates = my_estimator.get_n_total_t_gates(
        gsc_resources.extra.n_t_gates,
        gsc_resources.extra.n_rotation_gates,
        algorithm_implementation.error_budget.transpilation_failure_tolerance,
    )

    footprint_resources = get_physical_cost(
        algorithm_implementation.program.num_data_qubits,
        num_t=total_t_gates,
        architecture_model=my_estimator.hw_model,
        hardware_failure_tolerance=algorithm_implementation.error_budget.hardware_failure_tolerance,
        decoder_model=decoder_model,
    )

    if architecture_model == BASIC_ION_TRAP_ARCHITECTURE_MODEL:
        footprint_detailed_ion_trap_resource_info = (
            DetailedIonTrapModel().get_hardware_resource_estimates(footprint_resources)
        )

    print("Saving results...")
    cwd = os.getcwd()
    results_folder = get_new_directory(
        lattice_type, save_base_path=cwd + "/new_results/"
    )

    if architecture_model == BASIC_ION_TRAP_ARCHITECTURE_MODEL:
        gsc_resource_data = [gsc_resources, gsc_detailed_ion_trap_resource_info]
        footprint_resource_data = [
            footprint_resources,
            footprint_detailed_ion_trap_resource_info,
        ]
    else:
        gsc_resource_data = [gsc_resources]
        footprint_resource_data = [footprint_resources]

    with open(results_folder + lattice_type + "_gsc_re_data.json", "w") as outfile:
        json.dump(gsc_resource_data, outfile, indent=4, sort_keys=True, default=str)
    with open(
        results_folder + lattice_type + "_footprint_re_data.json", "w"
    ) as outfile:
        json.dump(
            footprint_resource_data, outfile, indent=4, sort_keys=True, default=str
        )


def get_new_directory(lattice_type, save_base_path=None):
    if save_base_path is None:
        return datetime.datetime.now().strftime(lattice_type + "-%Y-%m-%d_%H-%M-%S/")
    else:
        Path(
            save_base_path
            + datetime.datetime.now().strftime(lattice_type + "-%Y-%m-%d_%H-%M-%S/")
        ).mkdir(parents=True, exist_ok=True)
        return save_base_path + datetime.datetime.now().strftime(
            lattice_type + "-%Y-%m-%d_%H-%M-%S/"
        )


if __name__ == "__main__":
    architecture_model = BASIC_ION_TRAP_ARCHITECTURE_MODEL

    # size 30 has 900 nodes
    get_resources("triangular", 30, architecture_model)
    # size 22 has 1056 nodes
    # get_resources("kitaev", 22, architecture_model)
    # size 10 has 1000 nodes
    # get_resources("cubic", 10, architecture_model)
