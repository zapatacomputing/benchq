from benchq.visualization_tools.cycle_allocation import ResourceAllocation
import pandas as pd

# Create a ResourceAllocation object
cycle_allocation = ResourceAllocation()


def test_conversion_to_dataframe():
    # add some cycles to the given processes
    cycle_allocation.log(10, "Tstate-to-Tgate")
    cycle_allocation.log(20, "distillation")
    cycle_allocation.log(30, "entanglement")
    cycle_allocation.log(40, "Tstate-to-Tgate", "distillation")

    # test conversion to pandas DataFrame
    df = cycle_allocation.to_pandas_dataframe()

    # Create correct DataFrame
    row_1 = {
        "Tstate-to-Tgate": True,
        "distillation": False,
        "entanglement": False,
        "cycles": 10,
    }
    row_2 = {
        "Tstate-to-Tgate": False,
        "distillation": True,
        "entanglement": False,
        "cycles": 20,
    }
    row_3 = {
        "Tstate-to-Tgate": False,
        "distillation": False,
        "entanglement": True,
        "cycles": 30,
    }
    row_4 = {
        "Tstate-to-Tgate": True,
        "distillation": True,
        "entanglement": False,
        "cycles": 40,
    }
    target_df = pd.DataFrame([row_1, row_2, row_3, row_4])

    # Sort both DataFrames by all columns and then check if they are equal
    df = df[sorted(df.columns)]
    df = df.sort_values(by=list(df.columns)).reset_index(drop=True)

    target_df = target_df[sorted(target_df.columns)]
    target_df = target_df.sort_values(by=list(target_df.columns)).reset_index(drop=True)

    assert df.equals(target_df)


# add some cycles to the given processes
cycle_allocation.log(10, "Tstate-to-Tgate")
cycle_allocation.log(20, "distillation")
cycle_allocation.log(30, "entanglement")
cycle_allocation.log(40, "Tstate-to-Tgate", "distillation")
cycle_allocation.log(15, "entanglement", "distillation")
cycle_allocation.log(10, "Tstate-to-Tgate", "distillation", "entanglement")


from upsetplot import plot, UpSet, from_memberships
from matplotlib import pyplot as plt


# cycle_allocation.plot_upset_plot()
# cycle_allocation.plot_stacked_bar_chart()
cycle_allocation.plot()

# df = cycle_allocation.to_pandas_dataframe()


# # Prepare the dataset for the upset plot by summing up the "cycles" for each combination
# subset_data = df.groupby(["Tstate-to-Tgate", "distillation", "entanglement"])["cycles"].sum()

# # Generating the upset plot
# plot(subset_data, sort_by="cardinality")

# Visualizing with SuperVenn
# sets, labels = make_sets_from_chunk_sizes(df)
# supervenn(sets, labels)

plt.show()
# Visualizing with PyUpSet

# df.set_index(["Tstate-to-Tgate", "distillation", "entanglement"], inplace=True)
# print(df)

# df.index.names = ["Tstate-to-Tgate", "distillation", "entanglement"]


# # Now that the index names are strings, this should work
# plot_data = from_memberships(df.index)
# plot(plot_data)

# cycle_allocation.plot()
