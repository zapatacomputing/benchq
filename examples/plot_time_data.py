import numpy as np
import matplotlib.pyplot as plt


def plot_log_log_with_fit(times, problem_sizes):
    # Convert lists to numpy arrays for mathematical operations
    log_times = np.log(times)
    log_sizes = np.log(problem_sizes)

    # Fit a line to the logarithmic values
    coefficients = np.polyfit(log_sizes, log_times, 1)
    poly = np.poly1d(coefficients)

    # Create an extended range of problem sizes up to 20
    extended_sizes = np.linspace(min(problem_sizes), 20, 100)

    # Calculate fitted values over the extended range
    fit_values = np.exp(poly(np.log(extended_sizes)))

    # Plotting the original data
    plt.scatter(problem_sizes, times, color="blue", label="Original data")

    # Plotting the fit over the extended range
    plt.plot(
        extended_sizes,
        fit_values,
        color="red",
        label=f"Fit: y = {coefficients[0]:.2f}x + {np.exp(coefficients[1]):.2f}",
    )

    # Setting the scale to log-log
    plt.xscale("log")
    plt.yscale("log")

    # Labels and legend
    plt.xlabel("Lattice Size")
    plt.ylabel("Time")
    plt.title("Log-Log Plot with Linear Fit Extended to Lattice Size 20")
    plt.legend()

    # Display the plot
    plt.show()


# Example usage
problem_sizes = [6, 8, 10, 12]
times = [
    73.17189908027649,
    118.44559001922607,
    175.57360100746155,
    236.62325501441956,
]
plot_log_log_with_fit(times, problem_sizes)
