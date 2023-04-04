################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
Objectives:

1. Have a "benchq" script, which takes in a circuit and outputs a resource estimate
    - Prototype, but needs to make sense in principle.
    - Well defined I/Os


2. Have a "darpa-1.5" script, which creates a circuit from an application instance.
    - This is mostly for completeness and illustratory purposes
    - Software can be quite crappy
"""
from pprint import pprint

from benchq import BasicArchitectureModel
from benchq.algorithms import get_qsp_program
from benchq.timing import measure_time
from benchq.problem_ingestion import get_vlasov_hamiltonian
from benchq.resource_estimation.v2 import (
    GraphResourceEstimator,
    run_resource_estimation_pipeline,
)

# This examples shows three ways of performing resource estimation:
# 1. Generating the whole circuit, creating a graph out of it and performing
#   estimation on it
# 2. Using Quantum Program, performing estimation on the subcircuits
#   and then combining them together
# 3. Using Quantum Program, recreating the full graph from it, and then
#   performing resource estimation on it
#
# The first method is a reference, as it does not involve any simplification,
# it represents the exact result. However, given the size of the target circuits
# it's not scalable.
#
# The second method does not explicitly create the whole circuit, but uses the quantum
# program and subcircuits. For each subcircuit it creats a graph and then joins all
# the graphs together to recreate the graph of the full circuit. Ideally,
# the recreated graph should exactly match the ful graph from the previous
# example (up to local clifford transformations). However, at this point the method
# for recreating graph is imperfect, so it might introduce some approximations.

# The third method creates only the subgraphs for each subroutine in a quantum program,
# and the creates resource estimation based on them, without explicitly recreating
# the full graph. It is the least accurate from all threee, as it introduces
# certain assumptions, so should be treated as an upper bound on the resources needed.
# However, it is also the fastest and the least resource intensive.

# At this stage of development we are aware that there are some issues with methods
# 2 and 3 and they do not necessarily yield correct results.


def main():
    # Uncomment to see Jabalizer output
    # logging.getLogger().setLevel(logging.INFO)

    k = 2.0
    alpha = 0.6
    nu = 0.0

    dt = 0.1  # Integration timestep
    tmax = 5  # Maximal timestep
    sclf = 1

    tolerable_logical_error_rate = 1e-3
    qsp_required_precision = (
        tolerable_logical_error_rate / 3
    )  # Allocate half the error budget to trotter precision

    error_budget = {
        "qsp_required_precision": qsp_required_precision,
        "tolerable_circuit_error_rate": tolerable_logical_error_rate,
        "total_error": 1e-2,
        "synthesis_error_rate": 0.5,
        "ec_error_rate": 0.5,
    }

    architecture_model = BasicArchitectureModel(
        physical_gate_error_rate=1e-3,
        physical_gate_time_in_seconds=1e-6,
    )

    for N in [2]:
        # TA 1 part: specify the core computational capability
        with measure_time() as t_info:
            operator = get_vlasov_hamiltonian(k, alpha, nu, N)

        print("Operator generation time:", t_info.total)

        ### METHOD 2: Estimation from quantum program, without recreating full graph
        # TA 1.5 part: model algorithmic circuit
        with measure_time() as t_info:
            program = get_qsp_program(
                operator, qsp_required_precision, dt, tmax, sclf, mode="time_evolution"
            )

        print("Circuit generation time:", t_info.total)
        # TA 2 part: model hardware resources

        with measure_time() as t_info:
            gsc_resource_estimates = run_resource_estimation_pipeline(
                program,
                error_budget,
                estimator=GraphResourceEstimator(architecture_model)
            )

        print("Resource estimation time:", t_info.total)
        pprint(gsc_resource_estimates)


if __name__ == "__main__":
    main()
