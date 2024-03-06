import json
import typing
import warnings
from typing import Literal

from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.decoder_modeling import DecoderModel
from benchq.problem_ingestion.solid_state_hamiltonians.ising import (
    generate_ising_hamiltonian_on_cubic_lattice,
    generate_ising_hamiltonian_on_kitaev_lattice,
    generate_ising_hamiltonian_on_triangular_lattice,
)
from benchq.quantum_hardware_modeling import (
    DETAILED_ION_TRAP_ARCHITECTURE_MODEL,
    BASIC_SC_ARCHITECTURE_MODEL,
)
from benchq.resource_estimators.graph_estimator import (
    GraphResourceEstimator,
)
from benchq.compilation.graph_states.implementation_compiler import (
    get_implementation_compiler,
)
from benchq.compilation.graph_states.circuit_compilers import (
    get_ruby_slippers_circuit_compiler,
)
from benchq.compilation.circuits.pyliqtr_transpilation import (
    get_total_t_gates_after_transpilation,
)
from benchq.resource_estimators.openfermion_estimator import (
    openfermion_estimator,
)


def get_resources(lattice_type: str, size: int, decoder_data_file: str):
    print(f"Getting operator for size {size} {lattice_type} lattice...")
    if lattice_type == "triangular":
        operator = generate_ising_hamiltonian_on_triangular_lattice(size)
    elif lattice_type == "kitaev":
        operator = generate_ising_hamiltonian_on_kitaev_lattice(size)
    elif lattice_type == "cubic":
        operator = generate_ising_hamiltonian_on_cubic_lattice(size)
    else:
        raise ValueError(f"Lattice type {lattice_type} not supported")

    architecture_model = BASIC_SC_ARCHITECTURE_MODEL

    print("Getting algorithm implementation...")
    evolution_time = 1
    failure_tolerance = 1e-4
    algorithm_implementation = qsp_time_evolution_algorithm(
        operator, evolution_time, failure_tolerance
    )

    print("Setting resource estimation parameters...")
    decoder_model = DecoderModel.from_csv(decoder_data_file)
    circuit_compiler = get_ruby_slippers_circuit_compiler(
        teleportation_threshold=80, optimal_dag_density=10
    )
    implementation_compiler = get_implementation_compiler(
        circuit_compiler, destination="single-thread"
    )
    estimator = GraphResourceEstimator(optimization="Time", verbose=True)

    print("Estimating resources via graph state compilation...")
    gsc_resources = estimator.compile_and_estimate(
        algorithm_implementation,
        implementation_compiler,
        architecture_model,
        decoder_model,
    )

    total_t_gates = get_total_t_gates_after_transpilation(algorithm_implementation)
    hw_tolerance = algorithm_implementation.error_budget.hardware_failure_tolerance

    footprint_resources = openfermion_estimator(
        algorithm_implementation.program.num_data_qubits,
        num_t=total_t_gates,
        architecture_model=architecture_model,
        hardware_failure_tolerance=hw_tolerance,
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
