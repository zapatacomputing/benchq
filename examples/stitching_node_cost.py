import matplotlib.pyplot as plt

# Data
nodes = [2, 3, 4, 5, 6, 7, 8, 9, 10]

without_buffer = [5656, 20737, 49320, 101983, 179172, 295073, 429318, 635647, 869966]
with_buffer = [5775, 21139, 50171, 103239, 181397, 298717, 434653, 643021, 879687]

percentage_used_for_buffer = [
    (with_buffer[i] - without_buffer[i]) / with_buffer[i] * 100
    for i in range(len(nodes))
]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(nodes, percentage_used_for_buffer, marker="o", label="Without buffer")

plt.title("Total Number of Nodes")
plt.ylabel("Percentage of Nodes Used for Buffer")
plt.xlabel("Ising model cubic lattice size")

plt.legend()
plt.grid(True)

plt.show()
