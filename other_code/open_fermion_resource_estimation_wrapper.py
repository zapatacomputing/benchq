################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import matplotlib.pyplot as plt
from molecule_instance_generation import (
    generate_cyclic_ozone_hamiltonian,
    generate_cyclic_ozone_mean_field_object,
    generate_h2o_mean_field_object,
    generate_mean_field_object_from_molecule,
)
from openfermion.resource_estimates import sf
from openfermion.resource_estimates.surface_code_compilation.physical_costing import (
    cost_estimator,
)

from benchq.problem_ingestion.molecule_instance_generation import (
    generate_cyclic_ozone_hamiltonian,
    generate_cyclic_ozone_mean_field_object,
    generate_h2o_mean_field_object,
    generate_mean_field_object_from_molecule,
)
from benchq.resource_estimation import (
    model_toffoli_and_qubit_cost_from_single_factorized_mean_field_object,
)

# from openfermion.resource_estimates import df, thc


# def model_toffoli_and_qubit_cost_from_single_factorized_mean_field_object(
#     mean_field_object, rank, DE, CHI
# ):

#     num_orb = len(mean_field_object.mo_coeff)
#     num_spinorb = num_orb * 2

#     # First, up: lambda and CCSD(T)
#     eri_rr, LR = sf.factorize(mean_field_object._eri, rank)
#     lam = sf.compute_lambda(mean_field_object, LR)

#     # now do costing
#     stps1 = sf.compute_cost(num_spinorb, lam, DE, L=rank, chi=CHI, stps=20000)[0]

#     _, sf_total_toffoli_cost, sf_logical_qubits = sf.compute_cost(
#         num_spinorb, lam, DE, L=rank, chi=CHI, stps=stps1
#     )
#     return sf_total_toffoli_cost, sf_logical_qubits


def main():

    # mean_field_object = generate_h2o_mean_field_object()
    mean_field_object = generate_cyclic_ozone_mean_field_object()
    # molecule = gto.M(
    #     atom="""H    0.000000    0.000000    1.300000
    #             H   0.000000    0.000000    1.300000
    #         """,
    #     basis="6-31g",
    #     symmetry=False,
    #     charge=1,
    #     spin=1,
    # )

    # for n_hydrogens in [1, 2, 3]:  # , 5, 7, 10, 20, 50, 100]:
    #     # print("N qubits:", n_qubits)
    #     print("Number of hydrogen atoms:", n_hydrogens)
    #     # TA 1 part: specify the core computational capability
    #     # operator = all_terms_of_order_N(n_qubits, 2) + all_terms_of_order_N(n_qubits, 3)

    #     start = time.time()
    #     operator = generate_h_chain_jw_qubit_hamiltonian(n_hydrogens)
    #     end = time.time()
    #     print("Hamiltonian generation time:", end - start)
    #     print("Number of qubits:", operator.n_qubits)

    #     # TA 1.5 part:
    #     start = time.time()
    #     circuit = time_evolution(operator, time=1)
    #     end = time.time()
    #     print("Circuit generation time:", end - start)
    #     # circuit += Circuit([X(0), RZ(np.pi / 3)(1), CNOT(0, 1), RZ(np.pi / 7)(0)])
    #     # circuit = Circuit([RZ(np.pi / 3)(0)])
    #     # print(circuit)
    #     hardware_model = {"physical_gate_error_rate": 1e-3, "physical_gate_time": 1e-6}
    #     synthesis_accuracy = 1e-3
    #     start = time.time()
    #     resource_estimates = get_resource_estimations_for_circuit(
    #         circuit, hardware_model, synthesis_accuracy
    #     )
    #     end = time.time()
    #     print("Resource estimation time:", end - start)
    #     print(resource_estimates)

    # mean_field_object = generate_mean_field_object_from_molecule(
    #     molecule, ao_list
    # )
    # make pretty SF costing table

    # rank_range = [4 * (i + 1) for i in range(4)]
    # rank_range = [20, 25, 30, 35, 40, 45, 50]
    rank_range = [
        20,
        30,
        40,
        50,
        60,
        80,
        100,
        120,
    ]
    # rank_range = [
    #     160,
    #     200,
    #     240,
    #     # 200,
    #     # 300,
    #     # 400,
    #     # 400,
    #     # 500,
    #     # 600,
    #     # 700,
    # ]
    # Set phase estimation error tolerance
    DE = 0.001

    # Set number of bits of precision in ancilla state preparation
    CHI = 10
    toffoli_costs = []
    qubit_costs = []
    physical_qubit_counts = []
    runtimes_in_seconds = []

    for rank in rank_range:

        # Model logical costs
        (
            sf_total_toffoli_cost,
            sf_logical_qubits,
        ) = model_toffoli_and_qubit_cost_from_single_factorized_mean_field_object(
            mean_field_object, rank, DE, CHI
        )

        toffoli_costs += [sf_total_toffoli_cost]
        qubit_costs += [sf_logical_qubits]

        # Model physical costs
        best_cost, best_params = cost_estimator(
            sf_logical_qubits,
            sf_total_toffoli_cost,
            physical_error_rate=1.0e-3,
            portion_of_bounding_box=1.0,
        )

        physical_qubit_count = best_cost.physical_qubit_count
        duration = best_cost.duration

        physical_qubit_counts += [physical_qubit_count]
        runtimes_in_seconds += [duration.seconds / 3600]

    # plotting the points
    plt.plot(rank_range, runtimes_in_seconds, "o")

    # naming the x axis
    plt.xlabel("Rank (SVD truncation)")
    # naming the y axis
    # plt.ylabel("Runtime in Seconds")
    plt.ylabel("Runtime in Hours")

    # giving a title to my graph
    plt.title("Cyclic Ozone Resource Estimation")

    # function to show the plot
    plt.show()

    # plotting the points
    plt.plot(rank_range, physical_qubit_counts, "o")

    # naming the x axis
    plt.xlabel("Rank (SVD truncation)")
    # naming the y axis
    plt.ylabel("Physical qubits")

    # giving a title to my graph
    plt.title("Cyclic Ozone Resource Estimation")

    # function to show the plot
    plt.show()


if __name__ == "__main__":
    main()
