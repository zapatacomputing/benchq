################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
# WARNING! SIMPLE MODELING AHEAD! ABANDON NUANCE ALL YE WHO ENTER HERE!


class ABCArchitectureModel:
    def __init__(self):
        pass


class BasicArchitectureModel(ABCArchitectureModel):
    """A basic architecture model used for getting a rough estimate of the
    performance of a quantum computer.

    Attributes:
        physical_t_gate_error_rate (float): The error rate of a physical T-gate,
            stemming from the error in magic state preparation.
        surface_code_cycle_time_in_seconds (float): The time it takes to run a
            surface code cycle.
    """
    def __init__(
        self,
        physical_t_gate_error_rate,
        surface_code_cycle_time_in_seconds,
    ):
        self.physical_t_gate_error_rate = physical_t_gate_error_rate
        self.surface_code_cycle_time_in_seconds = surface_code_cycle_time_in_seconds


BASIC_ION_TRAP_ARCHITECTURE_MODEL = BasicArchitectureModel(1e-4, 1e-5)
BASIC_SC_ARCHITECTURE_MODEL = BasicArchitectureModel(1e-3, 1e-7)
