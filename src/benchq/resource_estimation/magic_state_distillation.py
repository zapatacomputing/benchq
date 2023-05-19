from dataclasses import dataclass
from typing import Tuple

from benchq.data_structures.hardware_architecture_models import (
    BASIC_ION_TRAP_ARCHITECTURE_MODEL,
    BASIC_SC_ARCHITECTURE_MODEL,
    BasicArchitectureModel,
)


@dataclass
class Widget:
    name: str
    p_out: float
    space: Tuple[int, int]
    qubits: int
    time: float


widget_lookup_table = {
    "ions": [
        Widget("(15-to-1)_7,3,3", 4.4e-8, (30, 27), 810, 18.1),
        Widget("(15-to-1)_9,3,3", 9.3e-10, (38, 30), 1150, 18.1),
        Widget("(15-to-1)_11,5,5", 1.9e-11, (47, 44), 2070, 30),
        Widget("(15-to-1)^4_9,3,3 x (20-to-4)_15,7,9", 2.4e-15, (221, 96), 16400, 90.3),
        Widget("(15-to-1)^4_9,3,3 x (15-to-1)_25,9,9", 6.3e-25, (193, 96), 18600, 67.8),
    ],
    "sc": [
        Widget("(15-to-1)_17,7,7", 4.5e-8, (72, 64), 4620, 42.6),
        Widget(
            "(15-to-1)^6_15,5,5 x (20-to-4)_23,11,13", 1.4e-10, (387, 155), 43300, 130
        ),
        Widget(
            "(15-to-1)^4_13,5,5 x (20-to-4)_27,13,15", 2.6e-11, (382, 142), 46800, 157
        ),
        Widget(
            "(15-to-1)^6_11,5,5 x (15-to-1)_25,11,11", 2.7e-12, (279, 117), 30700, 82.5
        ),
        Widget(
            "(15-to-1)^6_13,5,5 x (15-to-1)_29,11,13", 3.3e-14, (292, 138), 39100, 97.5
        ),
        Widget(
            "(15-to-1)^6_17,7,7 x (15-to-1)_41,17,17", 4.5e-20, (426, 181), 73400, 128
        ),
    ],
}


ions = [BASIC_ION_TRAP_ARCHITECTURE_MODEL]
sc = [BASIC_SC_ARCHITECTURE_MODEL]


def get_hardware_type(hardware_model: BasicArchitectureModel):
    if hardware_model in ions:
        return "ions"
    elif hardware_model in sc:
        return "sc"
    else:
        raise ValueError(
            f"Hardware type {hardware_model} not recognized. "
            f"Please choose from {ions} or {sc}."
        )


class WidgetIterator:
    def __init__(self, hardware_model: BasicArchitectureModel):
        self.hardware_type = get_hardware_type(hardware_model)
        self.data = widget_lookup_table[self.hardware_type]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            value = self.data[self.index]
            self.index += 1
            return value
        except IndexError:
            raise StopIteration("No Viable Widget Found!")


def get_specs_for_t_state_widget(
    widget_name: str, hardware_model: BasicArchitectureModel
):
    hardware_type = get_hardware_type(hardware_model)

    for widget in widget_lookup_table[hardware_type]:
        if widget.name == widget_name:
            widget_specs = widget
            break

    return widget_specs
