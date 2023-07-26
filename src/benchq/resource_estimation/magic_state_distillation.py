from dataclasses import dataclass
from functools import singledispatch
from typing import Iterable, Tuple

from benchq.data_structures.hardware_architecture_models import (
    BasicArchitectureModel,
    IONTrapModel,
    SCModel,
)

from benchq.data_structures import SubroutineModel

from openfermion.resource_estimates.surface_code_compilation.physical_costing import (
    _autoccz_factory_dimensions,
    _compute_autoccz_distillation_error,
    _physical_qubits_per_logical_qubit,
)


@dataclass(frozen=True)
class Widget:
    name: str
    distilled_magic_state_error_rate: float
    space: Tuple[int, int]
    qubits: int
    time_in_tocks: float
    n_t_gates_produced_per_cycle: int = 1


@singledispatch
def default_widget_list(architecture_model: BasicArchitectureModel) -> Iterable[Widget]:
    raise NotImplementedError(f"No widgets known for type model {architecture_model}")


@default_widget_list.register
def default_widget_list_for_ion_traps(
    _architecture_model: IONTrapModel,
) -> Iterable[Widget]:
    return [
        Widget("(15-to-1)_7,3,3", 4.4e-8, (30, 27), 810, 18.1),
        Widget("(15-to-1)_9,3,3", 9.3e-10, (38, 30), 1150, 18.1),
        Widget("(15-to-1)_11,5,5", 1.9e-11, (47, 44), 2070, 30),
        Widget(
            "(15-to-1)^4_9,3,3 x (20-to-4)_15,7,9",
            2.4e-15,
            (221, 96),
            16400,
            90.3,
            n_t_gates_produced_per_cycle=4,
        ),
        Widget("(15-to-1)^4_9,3,3 x (15-to-1)_25,9,9", 6.3e-25, (193, 96), 18600, 67.8),
    ]


@default_widget_list.register
def default_widget_list_for_sc(_architecture_model: SCModel) -> Iterable[Widget]:
    return [
        Widget("(15-to-1)_17,7,7", 4.5e-8, (72, 64), 4620, 42.6),
        Widget(
            "(15-to-1)^6_15,5,5 x (20-to-4)_23,11,13",
            1.4e-10,
            (387, 155),
            43300,
            130,
        ),
        Widget(
            "(15-to-1)^4_13,5,5 x (20-to-4)_27,13,15",
            2.6e-11,
            (382, 142),
            46800,
            157,
            n_t_gates_produced_per_cycle=1,
        ),
        Widget(
            "(15-to-1)^6_11,5,5 x (15-to-1)_25,11,11",
            2.7e-12,
            (279, 117),
            30700,
            82.5,
        ),
        Widget(
            "(15-to-1)^6_13,5,5 x (15-to-1)_29,11,13",
            3.3e-14,
            (292, 138),
            39100,
            97.5,
        ),
        Widget(
            "(15-to-1)^6_17,7,7 x (15-to-1)_41,17,17",
            4.5e-20,
            (426, 181),
            73400,
            128,
        ),
    ]


class AutoCCZDistillation(SubroutineModel):
    def __init__(
        self,
        task_name="toffoli_gate",
        requirements=None,
        hardware_architecture_model=SubroutineModel("hardware_architecture_model"),
    ):
        super().__init__(
            task_name,
            requirements,
            hardware_architecture_model=hardware_architecture_model,
        )

    def set_requirements(self, failure_tolerance):
        args = locals()
        # Clean up the args dictionary before setting requirements
        args.pop("self")
        args = {k: v for k, v in args.items() if not k.startswith("__")}
        super().set_requirements(**args)

    def populate_requirements_for_subroutines(self):
        t_state_physical_error_rate = (
            self.hardware_architecture_model.get_physical_error_rate()
        )
        surface_code_cycle_time_in_seconds = (
            self.hardware_architecture_model.get_cycle_time()
        )

        ### Find the smallest-volume factory that meets the allotted failure tolerance
        distillation_failure_tolerance = self.requirements["failure_tolerance"]
        width, height, depth, l1_distance, l2_distance = self.find_smallest_factory(
            t_state_physical_error_rate, distillation_failure_tolerance
        )

        number_of_surface_code_cycles = depth * l2_distance
        self.hardware_architecture_model.number_of_times_called = (
            number_of_surface_code_cycles
        )
        self.hardware_architecture_model.requirements["qubits"] = (
            width * height * _physical_qubits_per_logical_qubit(l2_distance)
        )
        self.hardware_architecture_model.requirements["runtime_in_seconds"] = (
            number_of_surface_code_cycles * surface_code_cycle_time_in_seconds
        )

    def find_smallest_factory(
        self, t_state_physical_error_rate, distillation_failure_tolerance
    ):
        best_volume = None
        for l1_distance in range(5, 25, 2):
            for l2_distance in range(l1_distance + 2, 41, 2):
                width, height, depth = _autoccz_factory_dimensions(
                    l1_distance=l1_distance, l2_distance=l2_distance
                )
                current_distillation_volume = width * height * depth
                failure_rate = _compute_autoccz_distillation_error(
                    l1_distance=l1_distance,
                    l2_distance=l2_distance,
                    physical_error_rate=t_state_physical_error_rate,
                )

                if failure_rate > distillation_failure_tolerance:
                    continue
                if best_volume is None or current_distillation_volume < best_volume:
                    best_volume = current_distillation_volume

            return width, height, depth, l1_distance, l2_distance
