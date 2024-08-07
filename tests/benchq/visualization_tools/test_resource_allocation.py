import pandas as pd
import pytest

from benchq.visualization_tools.resource_allocation import ResourceAllocation


@pytest.fixture
def time_allocation():
    return ResourceAllocation("cycles")


@pytest.fixture
def possible_processes():
    return ["T measurement", "distillation", "graph state prep"]


@pytest.mark.parametrize(
    "processes_list, time_per_process",
    [
        (
            [
                ["T measurement"],
                ["T measurement"],
            ],
            [10, 20],
        ),
        (
            [
                ["T measurement", "distillation"],
                ["T measurement", "distillation"],
            ],
            [30, 40],
        ),
    ],
)
def test_logg_adds_correctly(time_allocation, processes_list, time_per_process):
    for processes, cycles in zip(processes_list, time_per_process):
        time_allocation.log(cycles, *processes)

    assert time_allocation.exclusive(*processes_list[0]) == sum(time_per_process)
    assert time_allocation.inclusive(*processes_list[0]) == sum(time_per_process)


@pytest.mark.parametrize(
    "processes_list, time_per_process",
    [
        (
            [
                "T measurement",
                "distillation",
            ],
            [10, 20],
        ),
        (
            [
                "T measurement",
                "distillation",
                "graph state prep",
            ],
            [10, 20, 30],
        ),
    ],
)
def test_parallel_logging(time_allocation, processes_list, time_per_process):
    time_allocation.log_parallelized(time_per_process, processes_list)

    for process_num in range(len(processes_list)):
        assert time_allocation.exclusive(*processes_list[process_num:]) == 10


def test_parallel_and_single_logging_non_constructive(time_allocation):
    time_allocation.log(10, "T measurement")
    time_allocation.log_parallelized([30, 50], ["T measurement", "distillation"])

    assert time_allocation.exclusive("T measurement") == 10
    assert time_allocation.exclusive("distillation") == 20
    assert time_allocation.exclusive("T measurement", "distillation") == 30

    assert time_allocation.inclusive("T measurement") == 40
    assert time_allocation.inclusive("distillation") == 50


def test_parallel_and_single_logging_constructive(time_allocation):
    time_allocation.log(10, "T measurement")
    time_allocation.log_parallelized([30, 40], ["distillation", "T measurement"])

    assert time_allocation.exclusive("T measurement") == 20
    assert time_allocation.exclusive("T measurement", "distillation") == 30

    assert time_allocation.inclusive("T measurement") == 50
    assert time_allocation.inclusive("distillation") == 30


@pytest.mark.parametrize(
    "processes_list, time_per_process",
    [
        (
            [
                ["T measurement"],
            ],
            [10],
        ),
        (
            [
                ["T measurement"],
                ["distillation"],
            ],
            [10],
        ),
        (
            [
                ["T measurement", "distillation"],
            ],
            [10],
        ),
        (
            [
                ["T measurement"],
                ["distillation"],
                ["graph state prep"],
                ["T measurement", "distillation"],
            ],
            [10, 20, 30, 40],
        ),
    ],
)
def test_conversion_to_dataframe(
    time_allocation, possible_processes, processes_list, time_per_process
):
    # add some cycles to the given processes
    for processes, cycles in zip(processes_list, time_per_process):
        time_allocation.log(cycles, *processes)
    df = time_allocation.to_pandas_dataframe()

    # create a target DataFrame
    dataframe_rows = []
    for processes, cycles in zip(processes_list, time_per_process):
        dataframe_rows.append(
            {process: process in processes for process in possible_processes}
        )
        dataframe_rows[-1][time_allocation.resource_name] = cycles
    target_df = pd.DataFrame(dataframe_rows)

    # Sort both DataFrames by all columns and then check if they are equal
    df = df[sorted(df.columns)]
    df = df.sort_values(by=list(df.columns)).reset_index(drop=True)

    target_df = target_df[sorted(target_df.columns)]
    target_df = target_df.sort_values(by=list(target_df.columns)).reset_index(drop=True)

    assert df.equals(target_df)
