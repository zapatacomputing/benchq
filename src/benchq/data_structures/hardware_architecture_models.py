################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
# WARNING! SIMPLE MODELING AHEAD! ABANDON NUANCE ALL YE WHO ENTER HERE!


class ABCArchitectureModel:
    def __init__(self):
        return self


class BasicArchitectureModel(ABCArchitectureModel):
    def __init__(
        self,
        physical_gate_error_rate,
        physical_gate_time_in_seconds,
    ):
        self.physical_gate_error_rate = physical_gate_error_rate
        self.physical_gate_time_in_seconds = physical_gate_time_in_seconds


BasicIonTrapArchitectureModel = BasicArchitectureModel(1e-4, 1e-5)
BasicSCArchitectureModel = BasicArchitectureModel(1e-3, 1e-7)
