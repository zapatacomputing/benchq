################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""Data structures describing estimated resources and related info."""

from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar

from benchq.compilation.graph_states.compiled_data_structures import (
    CompiledAlgorithmImplementation,
)

from ..visualization_tools.resource_allocation import CycleAllocation, QubitAllocation

TExtra = TypeVar("TExtra")


@dataclass
class DecoderInfo:
    """Information relating the decoder."""

    total_energy_in_joules: float
    power_in_watts: float
    area_in_micrometers_squared: float
    max_decodable_distance: int = field(repr=False)


@dataclass
class DetailedIonTrapResourceInfo:
    """Info relating to detailed ion trap architecture model resources."""

    power_consumed_per_elu_in_kilowatts: float
    num_communication_ports_per_elu: int
    second_switch_per_elu_necessary: bool
    num_communication_qubits_per_elu: int
    num_memory_qubits_per_elu: int
    num_computational_qubits_per_elu: int
    num_optical_cross_connect_layers: int
    num_ELUs_per_optical_cross_connect: int

    total_num_ions: int
    total_num_communication_qubits: int
    total_num_memory_qubits: int
    total_num_computational_qubits: int
    total_num_communication_ports: int
    num_elus: int
    total_elu_power_consumed_in_kilowatts: float
    total_elu_energy_consumed_in_kilojoules: float


@dataclass
class ResourceInfo(Generic[TExtra]):
    """Generic information about estimated resources with possible extras.

    The generic parameter of this class is a type of extra information stored
    in the extra field. This information should relate to the specific
    compilation method or algorithm used for estimating resources.

    Other fields are common between estimation methods that we currently have.

    There are several variants of this class aliased below.
    """

    n_physical_qubits: int
    total_time_in_seconds: float
    optimization: str
    code_distance: int
    logical_error_rate: float
    n_logical_qubits: int
    decoder_info: Optional[DecoderInfo]
    magic_state_factory_name: str
    extra: TExtra
    hardware_resource_info: Optional[DetailedIonTrapResourceInfo] = None


@dataclass
class GraphExtra:
    """Extra info relating to resource estimation using Graph State Compilation."""

    implementation: CompiledAlgorithmImplementation
    time_allocation: Optional[CycleAllocation]
    qubit_allocation: Optional[QubitAllocation]


# Alias for type of resource info returned by GraphResourceEstimator
GraphResourceInfo = ResourceInfo[GraphExtra]


@dataclass
class AzureExtra:
    """Extra info relating to resource estimation on Azure."""

    depth: int
    cycle_time: float
    raw_data: dict


# Alias for type of resource info returned by azure_estimator
AzureResourceInfo = ResourceInfo[AzureExtra]


@dataclass
class OpenFermionExtra:
    """Extra info relating to resource estimation using OpenFermion."""

    fail_rate_msFactory: float
    rounds_magicstateFactory: float
    scc_time: float
    physical_qubit_error_rate: float


# Alias for type of resource info returned by OpenFermion
OpenFermionResourceInfo = ResourceInfo[OpenFermionExtra]
