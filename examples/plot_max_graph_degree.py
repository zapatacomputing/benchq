import matplotlib.pyplot as plt

# Data for GraphSim Mini
graphsim_mini = {
    2: 153,
    3: 679,
    4: 1197.0,
    5: 4967,
    6: 10317,
}

# Data for Jabalizer
jabalizer = {
    2: 59,
    3: 119,
    4: 257,
}

# Data for Ruby Slippers
ruby_slippers = {
    2: 217,
    3: 212,
    4: 294,
    5: 352,
    6: 323,
    7: 289,
    8: 373,
    9: 316,
    10: 357,
}

# Extract the x and y values for each dataset
sizes_graphsim_mini = list(graphsim_mini.keys())
times_graphsim_mini = list(graphsim_mini.values())

sizes_jabalizer = list(jabalizer.keys())
times_jabalizer = list(jabalizer.values())

sizes_ruby_slippers = list(ruby_slippers.keys())
times_ruby_slippers = list(ruby_slippers.values())

# Create the plot
plt.figure(figsize=(10, 6))
plt.loglog(sizes_graphsim_mini, times_graphsim_mini, marker="o", label="GraphSim Mini")
plt.loglog(sizes_jabalizer, times_jabalizer, marker="o", label="Jabalizer")
plt.loglog(sizes_ruby_slippers, times_ruby_slippers, marker="o", label="Ruby Slippers")

# Add labels and title
plt.xlabel("Size")
plt.ylabel("Max Graph Degree")
plt.title("Max Graph Degree by Compilation Method")

# Add legend
plt.legend()

# Show the plot
plt.grid(True)
# plt.show()

# Save the plot
plt.savefig("plot_max_graph_degree.png")
