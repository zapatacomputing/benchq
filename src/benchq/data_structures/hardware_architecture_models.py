################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
# WARNING! SIMPLE MODELING AHEAD! ABANDON NUANCE ALL YE WHO ENTER HERE!


class ABCArchitectureModel:
    def __init__(self):
        pass


class BasicArchitectureModel(ABCArchitectureModel):
    def __init__(
        self,
        physical_t_gate_error_rate,
        surface_code_cycle_time_in_seconds,
    ):
        self.physical_t_gate_error_rate = physical_t_gate_error_rate
        self.surface_code_cycle_time_in_seconds = surface_code_cycle_time_in_seconds


BASIC_ION_TRAP_ARCHITECTURE_MODEL = BasicArchitectureModel(1e-4, 1e-5)
BASIC_SC_ARCHITECTURE_MODEL = BasicArchitectureModel(1e-3, 1e-7)
