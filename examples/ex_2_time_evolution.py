################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
Example showing how to estimate the resources required to run a time evolution
algorithm. It shows two different ways of estimating the resources: one with gate
synthesis performed at the circuit level, while the other one does it during the
measurement phase. The first is more accurate and leads to lower resources,
but is also more expensive in terms of runtime and memory usage.

Most of the objects has been described in the `1_from_qasm.py` examples, here
we only explain new concepts.

WARNING: This example requires the pyscf extra as well as the sdk extra.
run `pip install benchq[pyscf]` then `pip install benchq[sdk]` from the
main to install the extras. Then run `orq start` to start local ray.
"""
from pprint import pprint
from time import time


from pyLIQTR.BlockEncodings.getEncoding import getEncoding, VALID_ENCODINGS
from pyLIQTR.clam.lattice_definitions import (
    CubicLattice,
    SquareLattice,
    TriangularLattice,
)
from pyLIQTR.ProblemInstances.getInstance import getInstance


from benchq.algorithms.time_evolution import (
    qsp_time_evolution_algorithm_from_block_encoding,
)


# Requires jabalizer install. See README.
# from benchq.compilation.graph_states import get_jabalizer_circuit_compiler
from benchq.compilation.graph_states import get_ruby_slippers_circuit_compiler
from benchq.compilation.graph_states.implementation_compiler import (
    get_implementation_compiler,
)

from benchq.quantum_hardware_modeling import BASIC_SC_ARCHITECTURE_MODEL
from benchq.resource_estimators.graph_estimator import GraphResourceEstimator
from benchq.timing import measure_time


def main():

    # Here we generate the AlgorithmImplementation structure, which contains
    # information such as what subroutine needs to be executed and how many times.
    # In this example we perform time evolution using the QSP algorithm.

    start_time = time()

    # Fermi-Hubbard model parameters
    J = -1.0
    N = 2
    U = 4.0
    shape = (N, N)

    # Generate the Fermi-Hubbard model instance
    model = getInstance("FermiHubbard", shape=shape, J=J, U=U, cell=SquareLattice)

    # Get the block encoding for the Fermi-Hubbard model
    encoding = getEncoding(VALID_ENCODINGS.FermiHubbardSquare)
    block_encoding = encoding(model)

    evolution_time = 5.0 * block_encoding.alpha
    failure_tolerance = 1e-4

    with measure_time() as t_info:
        algorithm = qsp_time_evolution_algorithm_from_block_encoding(
            block_encoding, evolution_time, failure_tolerance
        )

    print("Circuit generation time:", t_info.total)
    print("n qubits in circuit:", algorithm.program.subroutines[0].n_qubits)

    # Allows for parallelized compilation. Uses ruby slippers compiler by default.
    # The single-thread setting is simplest to use. You can parallelize on a local
    # machine by setting the destination to "local" and running `orq up` in the
    # terminal. Additional settings as well as using a remote cluster can be
    # configured by using other settings available in the get_implementation_compiler
    implementation_compiler = get_implementation_compiler(
        circuit_compiler=get_ruby_slippers_circuit_compiler(),
        destination="single-thread",
    )
    estimator = GraphResourceEstimator(optimization="Time", verbose=True)

    with measure_time() as t_info:
        resource_estimate = estimator.compile_and_estimate(
            algorithm,
            implementation_compiler,
            BASIC_SC_ARCHITECTURE_MODEL,
        )

    print("Resource estimation time without synthesis:", t_info.total)
    pprint(resource_estimate)

    print("Total time to estimate resources:", time() - start_time)


if __name__ == "__main__":
    main()
