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
WARNING: This example requires the pyscf extra. run `pip install benchq[pyscf]`
to install the extra.
"""

from pprint import pprint

from benchq.algorithms.time_evolution import qsp_time_evolution_algorithm
from benchq.decoder_modeling import DecoderModel
from benchq.logical_architecture_modeling.graph_based_logical_architectures import (
    TwoRowBusArchitectureModel,
)
from benchq.problem_ingestion.solid_state_hamiltonians.ising import (
    generate_ising_hamiltonian_on_triangular_lattice,
)
from benchq.quantum_hardware_modeling import DETAILED_ION_TRAP_ARCHITECTURE_MODEL
from benchq.resource_estimators.default_estimators import get_fast_graph_estimate
from benchq.timing import measure_time


def main() -> None:
    hardware_architecture_model = DETAILED_ION_TRAP_ARCHITECTURE_MODEL
    logical_architecture_model = TwoRowBusArchitectureModel()

    with measure_time() as t_info:
        lattice_size = 3
        operator = generate_ising_hamiltonian_on_triangular_lattice(lattice_size)

    print("Operator generation time:", t_info.total)

    with measure_time() as t_info:
        evolution_time: float = 1.0
        failure_tolerance: float = 1e-3
        algorithm = qsp_time_evolution_algorithm(
            operator,
            evolution_time,
            failure_tolerance,
        )

    print("Circuit generation time:", t_info.total)

    with measure_time() as t_info:
        fast_gsc_resources = get_fast_graph_estimate(
            algorithm,
            logical_architecture_model,
            hardware_architecture_model,
            optimization="Time",
        )

    print("Resource estimation time with GSC:", t_info.total)
    pprint(fast_gsc_resources)


if __name__ == "__main__":
    main()
