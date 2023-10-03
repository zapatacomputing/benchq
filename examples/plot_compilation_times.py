import matplotlib.pyplot as plt

# Data for GraphSim Mini
graphsim_mini = {
    2: 4.316492080688477,
    3: 5.233307838439941,
    4: 13.580762147903442,
    5: 53.78805112838745,
    6: 291.41524505615234,
}

# Data for Jabalizer
jabalizer = {
    2: 11.379709959030151,
    3: 136.9883210659027,
    4: 769.641072034835,
}

# Data for Ruby Slippers
ruby_slippers = {
    2: 7.898834228515625,
    3: 9.44984793663,
    4: 12.287305831909,
    5: 18.02216911315918,
    6: 27.38937091827392,
    7: 40.324304819107,
    8: 47.6569011211395,
    9: 64.32893705368042,
    10: 114.1283948421478,
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
plt.plot(sizes_graphsim_mini, times_graphsim_mini, marker="o", label="GraphSim Mini")
plt.plot(sizes_jabalizer, times_jabalizer, marker="o", label="Jabalizer")
plt.plot(sizes_ruby_slippers, times_ruby_slippers, marker="o", label="Ruby Slippers")

# Add labels and title
plt.xlabel("Size")
plt.ylabel("Time (s)")
plt.title("Performance of Compilation Methods")

# Add a note to the plot
plt.text(5.2, 540, "Excluded runtimes > 3000 seconds", fontsize=12, color="red")

# Add legend
plt.legend()

# Show the plot
plt.grid(True)
# plt.show()

# Save the plot
plt.savefig("plot_compilation_times.png")
