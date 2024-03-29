from functools import singledispatch
from typing import Iterable

from benchq.quantum_hardware_modeling.hardware_architecture_models import (
    BasicArchitectureModel,
)

from .magic_state_factory import MagicStateFactory

_ALLOWED_PHYSICAL_ERROR_RATES = (1e-3, 1e-4)

_ERROR_RATE_FACTORY_MAPPING = {
    1e-3: (
        MagicStateFactory("(15-to-1)_17,7,7", 4.5e-8, (72, 64), 4620, 42.6),
        MagicStateFactory(
            "(15-to-1)^6_15,5,5 x (20-to-4)_23,11,13",
            1.4e-10,
            (387, 155),
            43300,
            130,
        ),
        MagicStateFactory(
            "(15-to-1)^4_13,5,5 x (20-to-4)_27,13,15",
            2.6e-11,
            (382, 142),
            46800,
            157,
            n_t_gates_produced_per_distillation=1,
        ),
        MagicStateFactory(
            "(15-to-1)^6_11,5,5 x (15-to-1)_25,11,11",
            2.7e-12,
            (279, 117),
            30700,
            82.5,
        ),
        MagicStateFactory(
            "(15-to-1)^6_13,5,5 x (15-to-1)_29,11,13",
            3.3e-14,
            (292, 138),
            39100,
            97.5,
        ),
        MagicStateFactory(
            "(15-to-1)^6_17,7,7 x (15-to-1)_41,17,17",
            4.5e-20,
            (426, 181),
            73400,
            128,
        ),
    ),
    1e-4: (
        MagicStateFactory("(15-to-1)_7,3,3", 4.4e-8, (30, 27), 810, 18.1),
        MagicStateFactory("(15-to-1)_9,3,3", 9.3e-10, (38, 30), 1150, 18.1),
        MagicStateFactory("(15-to-1)_11,5,5", 1.9e-11, (47, 44), 2070, 30),
        MagicStateFactory(
            "(15-to-1)^4_9,3,3 x (20-to-4)_15,7,9",
            2.4e-15,
            (221, 96),
            16400,
            90.3,
            n_t_gates_produced_per_distillation=4,
        ),
        MagicStateFactory(
            "(15-to-1)^4_9,3,3 x (15-to-1)_25,9,9", 6.3e-25, (193, 96), 18600, 67.8
        ),
    ),
}


def iter_litinski_factories(
    architecture_model: BasicArchitectureModel,
) -> Iterable[MagicStateFactory]:
    assert architecture_model.physical_qubit_error_rate in _ALLOWED_PHYSICAL_ERROR_RATES

    return _ERROR_RATE_FACTORY_MAPPING[architecture_model.physical_qubit_error_rate]
