################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""Data structures describing estimated resources and related info."""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ResourceInfo:
    """Contains all resource estimated for a problem instance."""

    code_distance: int
    logical_error_rate: float
    n_logical_qubits: int
    n_nodes: int = field(repr=False)
    n_t_gates: int = field(repr=False)
    n_rotation_gates: int = field(repr=False)
    n_physical_qubits: int
    n_measurement_steps: int
    total_time_in_seconds: float
    max_decodable_distance: Optional[int] = field(repr=False)
    decoder_total_energy_consumption: Optional[float]
    decoder_power: Optional[float]
    decoder_area: Optional[float]
