################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
"""
Surface code model based on the numbers used in openfermion:
https://github.com/quantumlib/OpenFermion/tree/master/src/openfermion/resource_estimates
"""


def logical_cell_error_rate(
    code_distance: int, physical_qubit_error_rate: float
) -> float:
    return 0.1 * (100 * physical_qubit_error_rate) ** ((code_distance + 1) / 2)


def get_total_logical_failure_rate(
    code_distance: int, physical_qubit_error_rate: float, logical_st_volume: int
) -> float:
    return logical_st_volume * logical_cell_error_rate(
        code_distance, physical_qubit_error_rate
    )


def physical_qubits_per_logical_qubit(code_distance: int) -> int:
    return (code_distance + 1) ** 2 * 2
