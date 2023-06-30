################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
# WARNING! SIMPLE MODELING AHEAD! ABANDON NUANCE ALL YE WHO ENTER HERE!


from dataclasses import dataclass
from typing import Protocol


class BasicArchitectureModel(Protocol):
    """Basic Architecture model meant to serve as a base class for the
    other basic architecture models. WARNING! Running a resource estimate
    with this architecture model will fail as, you need to choose an ION
    based or SC based model in order to select a proper widget.

    Attributes:
        physical_qubit_error_rate (float): The probability that any given physical
            qubit incurs a pauli error during SPAM, entangling gates, or idling.
            For entangling gates and idles, each physical qubit involved in the
            operation is depolarized with probability 2p/3. For SPAM, a pauli that
            brings the state to an orthogonal state is applied with probability p.
        surface_code_cycle_time_in_seconds (float): The time it takes to run a
            surface code cycle.
    """
    physical_qubit_error_rate: float
    surface_code_cycle_time_in_seconds: float



@dataclass
class IONTrapModel:
    physical_qubit_error_rate: float
    surface_code_cycle_time_in_seconds: float


@dataclass
class SCModel(BasicArchitectureModel):
    physical_qubit_error_rate: float
    surface_code_cycle_time_in_seconds: float



BASIC_ION_TRAP_ARCHITECTURE_MODEL = IONTrapModel(1e-4, 1e-5)
BASIC_SC_ARCHITECTURE_MODEL = SCModel(1e-3, 1e-7)
