import matplotlib.pyplot as plt
from upsetplot import UpSet
import pandas as pd

# Example data
data = {"A": {1, 2, 3, 5, 7, 8}, "B": {3, 5, 7}, "C": {2, 3, 8, 9}, "D": {10}}

# Convert data to form suitable for upsetplot
from itertools import combinations


def make_upset_data(sets):
    import pandas as pd

    all_elements = set().union(*sets.values())
    data = []
    for k in range(1, len(sets) + 1):
        for combo in combinations(sets.keys(), k):
            intersection = set.intersection(*(sets[key] for key in combo))
            for element in intersection:
                row = {key: key in combo for key in sets.keys()}
                data.append(row)
    return pd.DataFrame(data).astype(int).groupby(list(sets.keys())).size()


upset_data = make_upset_data(data)

# Create UpSet plot but without the totals plot
upset = UpSet(upset_data, show_counts="%d")
axes = upset.plot()
axes["intersections"].set_title("Intersections Size")

# Replace totals plot with a custom rotated plot
axes["totals"].cla()  # Clear the totals axis
# Rotated line plot (swap x and y)
x = ["A", "B", "C"]
y = [4, 5, 6]
axes["totals"].plot(y, x)  # Notice the swap here
axes["totals"].set_title("Inclusive Cycles")
axes["totals"].set_xlabel("Cycles")  # Label appropriately as it's rotated

plt.show()
