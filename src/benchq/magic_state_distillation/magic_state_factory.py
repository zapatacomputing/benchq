from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class MagicStateFactory:
    name: str
    distilled_magic_state_error_rate: float
    space: Tuple[int, int]
    qubits: int
    distillation_time_in_cycles: float
    t_gates_per_distillation: int = 1  # number of T-gates produced per distillation
