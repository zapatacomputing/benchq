################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
from decimal import Decimal, getcontext

from . import BasicArchitectureModel

getcontext().prec = 100


def logical_cell_error_rate(physical_qubit_error_rate: float, distance: int) -> float:
    precise_physical_qubit_error_rate = Decimal(physical_qubit_error_rate)
    precise_distance = Decimal(distance)
    precise_coefficent = Decimal(0.3)
    return float(
        1
        - (
            1
            - precise_coefficent
            * (70 * precise_physical_qubit_error_rate) ** ((precise_distance + 1) / 2)
        )
        ** precise_distance
    )


def get_total_logical_failure_rate(
    hw_model: BasicArchitectureModel,
    logical_st_volume: float,
    code_distance: int,
) -> float:
    precise_logical_cell_failure_rate = Decimal(
        logical_cell_error_rate(hw_model.physical_qubit_error_rate, code_distance)
    )
    precise_logical_st_volume = Decimal(logical_st_volume)

    return float(
        1 - (1 - precise_logical_cell_failure_rate) ** precise_logical_st_volume
    )


def physical_qubits_per_logical_qubit(code_distance: int) -> int:
    return (code_distance) ** 2 * 2
