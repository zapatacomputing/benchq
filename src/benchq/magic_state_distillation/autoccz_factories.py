import math
from typing import Iterator, Tuple

from ..quantum_hardware_modeling.fowler_surface_code import (  # noqa: E501
    get_total_logical_failure_rate,
    physical_qubits_per_logical_qubit,
)
from ..resource_estimators.resource_info import MagicStateFactoryInfo


def iter_auto_ccz_factories(
    physical_qubit_error_rate: float,
) -> Iterator[MagicStateFactoryInfo]:
    for l1_distance in range(5, 25, 2):
        for l2_distance in range(l1_distance + 2, 41, 2):
            w, h, d = _autoccz_or_t_factory_dimensions(
                l1_distance=l1_distance, l2_distance=l2_distance
            )
            f_ccz = _compute_autoccz_distillation_error(
                l1_distance=l1_distance,
                l2_distance=l2_distance,
                physical_qubit_error_rate=physical_qubit_error_rate,
            )

            yield MagicStateFactoryInfo(
                name=f"AutoCCZ({physical_qubit_error_rate},"
                f"{l1_distance}, {l2_distance})",
                distilled_magic_state_error_rate=float(f_ccz),
                space=(w, h),
                qubits=w * h * physical_qubits_per_logical_qubit(l2_distance),
                distillation_time_in_cycles=int(d * l2_distance),
                t_gates_per_distillation=2,
            )


def _autoccz_or_t_factory_dimensions(
    l1_distance: int, l2_distance: int
) -> Tuple[int, int, float]:
    """Determine the width, height, depth of the magic state factory."""
    t1_height = 4 * l1_distance / l2_distance
    t1_width = 8 * l1_distance / l2_distance
    t1_depth = 5.75 * l1_distance / l2_distance

    ccz_depth = 5
    ccz_height = 6
    ccz_width = 3
    storage_width = 2 * l1_distance / l2_distance

    ccz_rate = 1 / ccz_depth
    t1_rate = 1 / t1_depth
    t1_factories = int(math.ceil((ccz_rate * 8) / t1_rate))
    t1_factory_column_height = t1_height * math.ceil(t1_factories / 2)

    width = int(math.ceil(t1_width * 2 + ccz_width + storage_width))
    height = int(math.ceil(max(ccz_height, t1_factory_column_height)))
    depth = max(ccz_depth, t1_depth)

    return width, height, depth


def _compute_autoccz_distillation_error(
    l1_distance: int, l2_distance: int, physical_qubit_error_rate: float
) -> float:
    # Level 0
    L0_distance = l1_distance // 2
    L0_distillation_error = physical_qubit_error_rate
    L0_topological_error = get_total_logical_failure_rate(
        logical_st_volume=100,  # Estimated 100 for T injection.
        code_distance=L0_distance,
        physical_qubit_error_rate=physical_qubit_error_rate,
    )
    L0_total_T_error = L0_distillation_error + L0_topological_error

    # Level 1
    L1_topological_error = get_total_logical_failure_rate(
        logical_st_volume=1100,  # Estimated 1000 for factory, 100 for T injection.
        code_distance=l1_distance,
        physical_qubit_error_rate=physical_qubit_error_rate,
    )
    L1_distillation_error = 35 * L0_total_T_error**3
    L1_total_T_error = L1_distillation_error + L1_topological_error

    # Level 2
    L2_topological_error = get_total_logical_failure_rate(
        logical_st_volume=1000,  # Estimated 1000 for factory.
        code_distance=l2_distance,
        physical_qubit_error_rate=physical_qubit_error_rate,
    )
    L2_distillation_error = 28 * L1_total_T_error**2
    L2_total_CCZ_or_2T_error = L2_topological_error + L2_distillation_error

    return L2_total_CCZ_or_2T_error


def _two_level_t_state_factory_1p1000(
    physical_qubit_error_rate: float,
) -> MagicStateFactoryInfo:
    assert physical_qubit_error_rate == 0.001
    return MagicStateFactoryInfo(
        name="SC Qubit AutoCCZ Factory",
        distilled_magic_state_error_rate=4 * 9 * 1e-17,
        space=(12 * 8, 4),
        qubits=(12 * 8) * (4) * physical_qubits_per_logical_qubit(31),
        distillation_time_in_cycles=6 * 31,
        t_gates_per_distillation=2,
    )


def iter_all_openfermion_factories(
    physical_qubit_error_rate: float,
) -> Iterator[MagicStateFactoryInfo]:
    if physical_qubit_error_rate == 0.001:
        yield _two_level_t_state_factory_1p1000(
            physical_qubit_error_rate=physical_qubit_error_rate
        )
    yield from iter_auto_ccz_factories(physical_qubit_error_rate)
