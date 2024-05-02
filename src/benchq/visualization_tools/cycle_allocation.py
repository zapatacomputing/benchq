import itertools
import pandas as pd
from copy import copy
from typing import Tuple

import matplotlib.pyplot as plt

from upsetplot import UpSet

from matplotlib.colors import LinearSegmentedColormap
import numpy as np

default_process_types = {"distillation", "Tstate-to-Tgate", "entanglement"}


class ResourceAllocation:

    def __init__(self, resource_name, process_types=default_process_types):
        """Initialize the ResourceAllocation object. We use the object to track
        the number of resources used by different combinations of processes.

        Attributes:
            allocation_data (dict): a dictionary that maps a frozenset of process
                types to the number of resources that are used by that combination of
                processes exclusively.
        """
        self.resource_name = resource_name
        self.process_types = process_types
        self.allocation_data = {}
        for combo in all_combinations(self.process_types):
            self.allocation_data[frozenset(combo)] = 0

    def log(self, resources: float, *processes):
        """Add resources to the given processes."""
        assert resources >= 0
        self.allocation_data[frozenset(processes)] += resources

    def log_parallelized(self, resource_tuple, processes_tuple):
        """Add the resources used by processes that start at the same time.

        Args:
            resource_tuple (tuple): a tuple of the number of resources used by each process.
            processes_tuple (tuple): a tuple of the processes that start at the same time.
        """
        assert len(resource_tuple) == len(processes_tuple)
        for resources in resource_tuple:
            assert resources >= 0

        combined_tuple = list(zip(resource_tuple, processes_tuple))
        combined_tuple.sort(key=lambda x: x[0])
        combined_tuple.reverse()

        for i in range(len(combined_tuple) - 1):
            self.log(
                combined_tuple[i][0] - combined_tuple[i + 1][0],
                *tuple(tup[1] for tup in combined_tuple[: i + 1]),
            )
        self.log(
            combined_tuple[-1][0],
            *processes_tuple,
        )

    @property
    def total(self):
        return sum(self.allocation_data.values())

    def exclusive(self, *processes):
        """Return the number of resources that are exclusive to the given processes.

        Returns:
            float: number of resources
        """
        return self.allocation_data[frozenset(processes)]

    def inclusive(self, *processes):
        """Return the total number of resources that include the given processes.
        This includes resources that are shared with other processes.

        Returns:
            float: number of resources
        """
        return sum(
            [
                self.allocation_data[combo]
                for combo in self.allocation_data
                if processes in combo
            ]
        )

    def __repr__(self):
        return (
            str(self.allocation_data)
            .replace("frozenset", "")
            .replace("(", "")
            .replace(")", "")
            .replace("'", "")
        )

    def to_pandas_dataframe(self):
        data = []
        for processes, resources in self.allocation_data.items():
            if resources != 0:
                row = {process: process in processes for process in self.process_types}
                row["resources"] = resources
                data.append(row)
        df = pd.DataFrame(data)
        df.fillna(False, inplace=True)
        return df

    def plot(self):
        upset = self.plot_upset_plot(show_immediately=False)
        self.plot_stacked_bar_chart(show_immediately=False, ax=upset["totals"])
        plt.show()

    def plot_upset_plot(self, show_immediately=True):
        """Plot a bar chart showing the time used by each process type."""
        df = self.to_pandas_dataframe()
        # Prepare the dataset for the upset plot by
        # summing up the resources for each combination
        subset_data = df.groupby(list(self.process_types))["resources"].sum()
        # Generating the upset plot
        upset = UpSet(
            subset_data,
            sort_by="cardinality",
            orientation="vertical",
            show_percentages=True,
        )

        axes_dict = upset.plot()

        # Changing the labels
        # axes_dict["totals"].set_ylabel("Total Cycles for\n each Process Type")
        axes_dict["intersections"].set_xlabel(self.resource_name)

        plt.title("Parallelization Breakdown")

        # Show the plot
        if show_immediately:
            plt.show()

        # plt.close()

        return axes_dict

    def plot_stacked_bar_chart(self, show_immediately=True, ax=None):
        if ax is None:
            ax = plt
            process_types = self.process_types
        else:
            process_types = [tick.get_text() for tick in ax.get_xticklabels()]

        init_resources = [0] * len(process_types)
        data = {i + 1: copy(init_resources) for i in range(len(process_types))}
        for combo in all_combinations(process_types):
            for process_index, process in enumerate(process_types):
                if process in combo:
                    data[len(combo)][process_index] += self.exclusive(*combo)

        # Number of categories and subcategories
        n_categories = len(process_types)
        sub_categories = list(data.keys())
        n_sub_categories = len(sub_categories)

        # Define the positions for the categories
        ind = np.arange(n_categories)

        # Define a color map from red to green
        color_map = LinearSegmentedColormap.from_list(
            "gr", ["green", "yellow", "red"], N=n_sub_categories
        )

        # Base height for the stacked bars
        height_cumulative = np.zeros(n_categories)

        # Labeling and legend
        if show_immediately:
            ax.ylabel(self.resource_name)
            ax.title("Total " + self.resource_name + " for each Process")
            ax.xticks(ind, process_types)
            ax.xlabel("Process Types")
        else:
            ax.cla()
            ax.set_ylabel(self.resource_name)
            ax.set_title("Total " + self.resource_name + " \nfor each Process")
            ax.set_xticks(ind)
            ax.set_xticklabels(process_types)
            ax.set_xlabel("Process Types")

        # Plot each sub-category
        for i, (sub_category, values) in reversed(list(enumerate(data.items()))):
            ax.bar(
                ind,
                values,
                color=color_map(i / (n_sub_categories - 1)),
                edgecolor="black",
                label=sub_category,
                bottom=height_cumulative,
            )
            height_cumulative += np.array(values)

        ax.legend(
            title="Number of\nParallel Processes",
            bbox_to_anchor=(1.05, 1),
            loc="upper left",
        )

        if show_immediately:
            ax.tight_layout()
            plt.show()

        fig, axes = plt.subplots()
        # plt.close()

        return axes


def all_combinations(iterable):
    # Loop over all lengths from 1 to max_length (inclusive)
    max_length = len(iterable)
    for r in range(1, max_length + 1):
        # Generate and yield combinations of the current length
        for combo in itertools.combinations(iterable, r):
            yield combo


class CycleAllocation(ResourceAllocation):
    def __init__(self, process_types=default_process_types):
        super().__init__("cycles", process_types)

    def __add__(self, other, safe=False):
        new_data = CycleAllocation(self.process_types)
        for combo in self.allocation_data:
            new_data.allocation_data[combo] = self.allocation_data[combo]
        for combo in other.allocation_data:
            new_data.allocation_data[combo] += other.allocation_data[combo]
        return new_data


class QubitAllocation(ResourceAllocation):
    def __init__(
        self, physical_qubits_per_logical_qubit, process_types=default_process_types
    ):
        super().__init__("qubits", process_types)

    def get_num_logical_qubits(self, physical_qubits_per_logical_qubit):
        """Return the number of logical qubits that are being used by the computation.
        Assumes that all qubits not being used for distillation are being used for
        computation."""
        physical_qubits_not_used_for_distillation = 0
        for combo in all_combinations(self.process_types):
            if not "distillation" in combo:
                physical_qubits_not_used_for_distillation += self.exclusive(*combo)

        return (
            physical_qubits_not_used_for_distillation
            / physical_qubits_per_logical_qubit
        )
