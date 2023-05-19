import matplotlib.pyplot as plt

# First dataset
qubits_dataset_1 = [499, 1215, 1256, 1464]
code_distance_dataset_1 = [23, 25, 26, 26]
time_dataset_1 = [0.07376429999999999, 0.1887318, 0.40407, 0.40475639999999996]
gsc_results_dataset_1 = [3, 4, 5, 6]

# Second dataset
qubits_dataset_2 = [35, 46, 63, 57]
code_distance_dataset_2 = [19, 20, 21, 21]
time_dataset_2 = [0.0101841, 0.0190215, 0.0386271, 0.0318735]
gsc_results_dataset_2 = [3, 4, 5, 6]

# Plotting
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))

# Number of Qubits vs Number of Stocks
ax1.plot(
    gsc_results_dataset_1,
    qubits_dataset_1,
    marker="o",
    linestyle="-",
    label="Dataset 1",
)
ax1.plot(
    gsc_results_dataset_2,
    qubits_dataset_2,
    marker="o",
    linestyle="-",
    label="Dataset 2",
)
ax1.set_ylabel("Number of Qubits")
ax1.set_xlabel("")
ax1.legend()
ax1.grid(True)

# Code Distance vs Number of Stocks
ax2.plot(
    gsc_results_dataset_1,
    code_distance_dataset_1,
    marker="o",
    linestyle="-",
    label="Dataset 1",
)
ax2.plot(
    gsc_results_dataset_2,
    code_distance_dataset_2,
    marker="o",
    linestyle="-",
    label="Dataset 2",
)
ax2.set_ylabel("Code Distance")
ax2.set_xlabel("")
ax2.legend()
ax2.grid(True)

# Time vs Number of Stocks
ax3.plot(
    gsc_results_dataset_1, time_dataset_1, marker="o", linestyle="-", label="Dataset 1"
)
ax3.plot(
    gsc_results_dataset_2, time_dataset_2, marker="o", linestyle="-", label="Dataset 2"
)
ax3.set_ylabel("Time (seconds)")
ax3.set_xlabel("Number of Stocks")
ax3.legend()
ax3.grid(True)

plt.tight_layout()
plt.show()
