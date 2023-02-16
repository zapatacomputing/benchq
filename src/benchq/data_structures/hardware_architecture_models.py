################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
class ABCArchitectureModel:
    def __init__(self):
        return self


class BasicArchitectureModel(ABCArchitectureModel):
    def __init__(
        self,
        physical_gate_error_rate: float = 1e-3,
        physical_gate_time_in_seconds: float = 1e-6,
    ):
        self.physical_gate_error_rate = physical_gate_error_rate
        self.physical_gate_time_in_seconds = physical_gate_time_in_seconds
