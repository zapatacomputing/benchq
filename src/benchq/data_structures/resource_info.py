################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""Data structures describing estimated resources and related info."""

from dataclasses import dataclass, field
from typing import Generic, List, Optional, TypeVar

TExtra = TypeVar("TExtra")


@dataclass
class DecoderInfo:
    """Information relating the deceoder."""

    total_energy_consumption: float
    power: float
    area: float
    max_decodable_distance: int = field(repr=False)


@dataclass
class ResourceInfo(Generic[TExtra]):
    """Generic information about estimated resources with possible extras.

    The generic parameter of this class is a type of extra information stored
    in the extra field. This information should relate to the specific
    compilation method or algorithm used for estimating resources.

    Other fields are common between estimation methods that we currently have.

    There are several variants of this class aliased below.
    """

    code_distance: int
    logical_error_rate: float
    n_logical_qubits: int
    n_physical_qubits: int
    total_time_in_seconds: float
    decoder_info: Optional[DecoderInfo]
    widget_name: str
    extra: TExtra


@dataclass
class GraphData:
    """Minimal set of graph-related data needed for resource estimation."""

    max_graph_degree: int
    n_nodes: int
    n_t_gates: int
    n_rotation_gates: int
    n_measurement_steps: int


@dataclass
class GraphDataResourceInfo(GraphData):
    graph_measure_ratio: float


# Alias for type of resource info returned by GraphResourceEstimator
GraphResourceInfo = ResourceInfo[GraphDataResourceInfo]


@dataclass
class ExtrapolatedGraphData(GraphData):
    """GraphData extended with extrapolation-related info."""

    n_logical_qubits_r_squared: float
    n_measurement_steps_r_squared: float
    data_used_to_extrapolate: List[GraphData] = field(repr=False)
    steps_to_extrapolate_to: int = field(repr=False)

    @property
    def max_graph_degree_r_squared(self) -> float:
        return self.n_logical_qubits_r_squared


# Alias for type of resource info returned by ExtrapolationResourceEstimator
ExtrapolatedGraphResourceInfo = ResourceInfo[ExtrapolatedGraphData]


@dataclass
class AzureExtra:
    """Extra info relating to resource estimation on Azure."""

    depth: int
    cycle_time: float
    raw_data: dict


# Alias for type of resource info returned by AzureResourceEstimator
AzureResourceInfo = ResourceInfo[AzureExtra]


@dataclass
class OpenFermionExtra:
    """Extra info relating to resource estimation using OpenFermion."""

    fail_rate_msFactory: float
    rounds_magicstateFactory: int
    scc_time: float
    physical_qubit_error_rate: float


# Alias for type of resource info returned by OpenFermion
OpenFermionResourceInfo = ResourceInfo[OpenFermionExtra]
