from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class MagicStateFactory:
    name: str
    distilled_magic_state_error_rate: float
    space: Tuple[int, int]
    qubits: int
    distillation_time_in_cycles: float
    n_t_gates_produced_per_distillation: int = 1
