################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
# WARNING! SIMPLE MODELING AHEAD! ABANDON NUANCE ALL YE WHO ENTER HERE!


class ABCArchitectureModel:
    def __init__(self):
        pass


class BasicArchitectureModel(ABCArchitectureModel):
    """Basic Architecture model meant to serve as a base class for the
    other basic architecture models. WARNING! Running a resource estimate
    with this architecture model will fail as, you need to choose an ION
    based or SC based model in order to select a proper widget.
    """

    def __init__(
        self,
        physical_gate_error_rate,
        physical_gate_time_in_seconds,
    ):
        self.physical_gate_error_rate = physical_gate_error_rate
        self.physical_gate_time_in_seconds = physical_gate_time_in_seconds


BASIC_ION_TRAP_ARCHITECTURE_MODEL = BasicArchitectureModel(1e-4, 1e-5)
BASIC_SC_ARCHITECTURE_MODEL = BasicArchitectureModel(1e-3, 1e-7)
