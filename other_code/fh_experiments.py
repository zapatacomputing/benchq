################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import matplotlib.pyplot as plt
import numpy as np
from hamiltonian_generation import generate_fermi_hubbard_jw_qubit_hamiltonian
from orquestra.quantum.evolution import time_evolution

from examples.h_chain_trotter import get_resource_estimations_for_circuit


def make_plot(results, y_key, x_label, y_label, file_name):
    x_values = []
    y_values = []
    for x, estimates in results.items():
        x_values.append(x)
        y_values.append(estimates[y_key])
    # Fit linear regression via least squares with numpy.polyfit
    # It returns an slope (b) and intercept (a)
    # deg=1 means linear fit (i.e. polynomial of degree 1)
    b, a = np.polyfit(x_values, y_values, deg=1)

    # Create sequence of 100 numbers from 0 to 100
    xseq = np.linspace(0, 20, num=100)

    # Plot regression line
    plt.plot(xseq, a + b * xseq, color="k", lw=2.5)
    print("COEFFICIENTS", file_name, a, b)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot(x_values, y_values, linestyle="", marker="o")
    plt.savefig(file_name + ".png")
    plt.clf()


def plot_time_vs_y(results):
    make_plot(results, x_label="FH dimension")


def plot_time_vs_trotter(results):
    make_plot(results, x_label="Trotter steps")


def time_vs_y_experiment():
    results = {}
    for y_dimension in [1, 2, 3, 4, 5, 6, 7, 8]:
        print("Y dimension:", y_dimension)
        operator = generate_fermi_hubbard_jw_qubit_hamiltonian(
            x_dimension=1,
            y_dimension=y_dimension,
            tunneling=1,
            coulomb=4,
            chemical_potential=0.5,
        )
        print("operator", operator)
        # TA 1.5 part:
        circuit = time_evolution(operator, time=1, trotter_order=5)
        # circuit += Circuit([X(0), RZ(np.pi / 3)(1), CNOT(0, 1), RZ(np.pi / 7)(0)])
        # circuit = Circuit([RZ(np.pi / 3)(0)])
        # print(circuit)
        hardware_model = {"physical_gate_error_rate": 1e-3, "physical_gate_time": 1e-6}
        synthesis_accuracy = 1e-3
        resource_estimates = get_resource_estimations_for_circuit(
            circuit, hardware_model, synthesis_accuracy
        )
        results[y_dimension] = resource_estimates
        for k, v in resource_estimates.items():
            print(f"{k}: {v}")
    make_plot(
        results,
        y_key="total_time",
        x_label="FH dimension",
        y_label="Wall time [s]",
        file_name="fh_time",
    )
    make_plot(
        results,
        y_key="total_number_of_qubits",
        x_label="FH dimension",
        y_label="Number of physical qubits",
        file_name="fh_nq",
    )


def time_vs_trotter_experiment():
    results = {}
    for trotter_steps in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        y_dimension = 4
        print("Trotter steps:", trotter_steps)
        operator = generate_fermi_hubbard_jw_qubit_hamiltonian(
            x_dimension=1,
            y_dimension=y_dimension,
            tunneling=1,
            coulomb=4,
            chemical_potential=0.5,
        )
        print("operator", operator)
        # TA 1.5 part:
        circuit = time_evolution(operator, time=1, trotter_order=trotter_steps)
        # circuit += Circuit([X(0), RZ(np.pi / 3)(1), CNOT(0, 1), RZ(np.pi / 7)(0)])
        # circuit = Circuit([RZ(np.pi / 3)(0)])
        # print(circuit)
        hardware_model = {"physical_gate_error_rate": 1e-3, "physical_gate_time": 1e-6}
        synthesis_accuracy = 1e-3
        resource_estimates = get_resource_estimations_for_circuit(
            circuit, hardware_model, synthesis_accuracy
        )
        results[trotter_steps] = resource_estimates
        for k, v in resource_estimates.items():
            print(f"{k}: {v}")
    make_plot(
        results,
        y_key="total_time",
        x_label="Trotter steps",
        y_label="Wall time [s]",
        file_name="trotter_time",
    )
    make_plot(
        results,
        y_key="total_number_of_qubits",
        x_label="Trotter steps",
        y_label="Number of physical qubits",
        file_name="trotter_nq",
    )


if __name__ == "__main__":
    time_vs_y_experiment()
    time_vs_trotter_experiment()
