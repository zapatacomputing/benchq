################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################

# This is experimental code! Use at your own risk!


from math import ceil

import numpy as np

INITIAL_SYNTHESIS_ACCURACY = 0.0001

data = [
    {
        "n_program_steps": 1,
        "logical_error_rate": 0.00033563750584339984,
        "total_time": 511340.6808,
        "physical_qubit_count": 58845096,
        "min_viable_distance": 37,
        "logical_st_volume": 265267928578248000,
        "n_measurement_steps": 67241,
        "n_logical_qubits": 1791,
        "n_nodes": 9597235,
    },
    {
        "n_program_steps": 2,
        "logical_error_rate": 0.00020540744783857707,
        "total_time": 788133.19968,
        "physical_qubit_count": 63004608,
        "min_viable_distance": 38,
        "logical_st_volume": 597447234185359680,
        "n_measurement_steps": 90419,
        "n_logical_qubits": 1818,
        "n_nodes": 14403019,
    },
    {
        "n_program_steps": 3,
        "logical_error_rate": 0.0003653494504228203,
        "total_time": 1051104.168,
        "physical_qubit_count": 62831328,
        "min_viable_distance": 38,
        "logical_st_volume": 1062653866561800000,
        "n_measurement_steps": 111739,
        "n_logical_qubits": 1813,
        "n_nodes": 19208775,
    },
    {
        "n_program_steps": 4,
        "logical_error_rate": 0.00015505562046075154,
        "total_time": 1348656.2855999998,
        "physical_qubit_count": 75088728,
        "min_viable_distance": 39,
        "logical_st_volume": 1660889926846728000,
        "n_measurement_steps": 128970,
        "n_logical_qubits": 2057,
        "n_nodes": 24014535,
    },
]

# don't linear fit to all the types of data yet
data_to_extrapolate = [
    "total_time",
    "min_viable_distance",
    "n_logical_qubits",
    "n_measurement_steps",
    "n_nodes",
]

linear_fit_data_types = [
    "total_time",
    "physical_qubit_count",
    "logical_st_volume",
    "n_measurement_steps",
    "n_logical_qubits",
    "n_nodes",
]

logarithmic_fit_data_types = ["min_viable_distance"]


def get_extrapolated_resource_estimates(data, steps_to_extrapolate_to):
    fits = {}
    x = np.array([d["n_program_steps"] for d in data])
    for data_type in data_to_extrapolate:
        y = np.array([d[data_type] for d in data])
        if data_type in linear_fit_data_types:
            fits[data_type] = get_linear_extrapolation(x, y, steps_to_extrapolate_to)
        elif data_type in logarithmic_fit_data_types:
            fits[data_type] = get_logarithmic_extrapolation(
                x, y, steps_to_extrapolate_to
            )
    return fits


def get_linear_extrapolation(x, y, steps_to_extrapolate_to):
    coeffs, sum_of_residuals, _, _, _ = np.polyfit(x, y, 1, full=True)
    r_squared = 1 - (sum_of_residuals[0] / (len(y) * np.var(y)))
    m, c = coeffs
    return {"value": ceil(m * steps_to_extrapolate_to + c), "R^2": r_squared}


# TODO figure out base of logarithm here (also power of logarithm)
def get_logarithmic_extrapolation(x, y, steps_to_extrapolate_to):
    coeffs, sum_of_residuals, _, _, _ = np.polyfit(np.log(x), y, 1, full=True)
    r_squared = 1 - (sum_of_residuals[0] / (len(y) * np.var(y)))
    m, c = coeffs
    return {
        "value": ceil(m * np.log(steps_to_extrapolate_to) + c),
        "R^2": r_squared,
    }


if __name__ == "__main__":
    print(get_extrapolated_resource_estimates(data, 550000))
