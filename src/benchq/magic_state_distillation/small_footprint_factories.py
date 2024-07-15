from typing import Iterable

from benchq.quantum_hardware_modeling.hardware_architecture_models import (
    BasicArchitectureModel,
)

from ..resource_estimators.resource_info import MagicStateFactoryInfo

_ALLOWED_PHYSICAL_ERROR_RATES = {1e-5}

_ERROR_RATE_FACTORY_MAPPING = {
    1e-5: (
        MagicStateFactoryInfo(
            "small footprint (15-to-1)_3,1,1", 1.8e-06, (6, 7), 86, 12.1
        ),
        MagicStateFactoryInfo(
            "small footprint (15-to-1)_5,1,3", 7.8e-09, (10, 9), 186, 37.3
        ),
        MagicStateFactoryInfo(
            "small footprint (15-to-1)_7,3,3", 5.5e-12, (14, 19), 538, 36.0
        ),
        MagicStateFactoryInfo(
            "small footprint (15-to-1)_9,3,3", 3.2e-14, (18, 21), 762, 36.0
        ),
        MagicStateFactoryInfo(
            "small footprint (15-to-1)_5,1,1 x (20-to-4)_11,3,5",
            6.7e-15,
            (37, 22),
            1462,
            150.0,
        ),
        MagicStateFactoryInfo(
            "small footprint (15-to-1)_5,1,3 x (20-to-4)_11,3,5",
            1.4e-16,
            (43, 22),
            1614,
            275.1,
        ),
        MagicStateFactoryInfo(
            "small footprint (15-to-1)_5,1,1 x (20-to-4)_11,5,5",
            1.3e-17,
            (51, 22),
            1958,
            150.0,
        ),
        MagicStateFactoryInfo(
            "small footprint (15-to-1)_5,1,1 x (20-to-4)_13,5,5",
            1.8e-20,
            (51, 22),
            2350,
            150.0,
        ),
        MagicStateFactoryInfo(
            "small footprint (15-to-1)_5,1,3 x (20-to-4)_15,5,5",
            2.7e-22,
            (55, 30),
            2782,
            275.0,
        ),
        MagicStateFactoryInfo(
            "small footprint (15-to-1)_5,1,3 x (20-to-4)_15,5,5",
            3.8e-23,
            (63, 30),
            3190,
            276.8,
        ),
    ),
}


def iter_small_footprint_factories(
    architecture_model: BasicArchitectureModel,
) -> Iterable[MagicStateFactoryInfo]:
    """
    An iterator which yields magic state factories which are optimized in order
    to minimize the number of physical qubits.
    """

    assert architecture_model.physical_qubit_error_rate in _ALLOWED_PHYSICAL_ERROR_RATES

    return _ERROR_RATE_FACTORY_MAPPING[architecture_model.physical_qubit_error_rate]
