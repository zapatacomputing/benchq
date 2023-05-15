################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""Data structures describing estimated resources and related info."""
from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar

TExtra = TypeVar("TExtra")


@dataclass
class DecoderInfo:
    total_energy_consumption: float
    power: float
    area: float
    max_decodable_distance: int = field(repr=False)


@dataclass
class GraphData:
    """Contains minimal set of data to get a resource estimate for a graph."""

    max_graph_degree: int
    n_nodes: int
    n_t_gates: int
    n_rotation_gates: int
    n_measurement_steps: int


@dataclass
class ResourceInfo(Generic[TExtra]):
    """Contains all resource estimated for a problem instance."""

    code_distance: int
    logical_error_rate: float
    n_logical_qubits: int
    n_physical_qubits: int
    total_time_in_seconds: float
    decoder_info: Optional[DecoderInfo]
    extra: TExtra


GraphCompilationResourceInfo = ResourceInfo[GraphData]
