################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""Data structures describing estimated resources and related info."""

from dataclasses import dataclass, field
from typing import Generic, Optional, Tuple, TypeVar

from benchq.compilation.graph_states.compiled_data_structures import (
    CompiledAlgorithmImplementation,
)

from ..visualization_tools.resource_allocation import QECCycleAllocation

TExtra = TypeVar("TExtra")


@dataclass
class DecoderInfo:
    """Information relating the decoder."""

    total_energy_in_joules: float
    power_in_watts: float
    area_in_micrometers_squared: float
    max_decodable_distance: int = field(repr=False)


@dataclass
class MagicStateFactoryInfo:
    name: str
    distilled_magic_state_error_rate: float
    space: Tuple[int, int]
    qubits: int
    distillation_time_in_cycles: float
    t_gates_per_distillation: int = 1  # number of T-gates produced per distillation


@dataclass
class ELUResourceInfo:
    """Info relating to elementary logic unit (ELU) resources."""

    power_consumed_per_elu_in_kilowatts: Optional[float] = None
    num_communication_ports_per_elu: Optional[int] = None
    second_switch_per_elu_necessary: Optional[bool] = None
    num_communication_ions_per_elu: Optional[int] = None
    num_memory_ions_per_elu: Optional[int] = None
    num_computational_ions_per_elu: Optional[int] = None
    num_optical_cross_connect_layers: Optional[int] = None
    num_ELUs_per_optical_cross_connect: Optional[int] = None


@dataclass
class DetailedIonTrapArchitectureResourceInfo:
    """Info relating to detailed ion trap architecture model resources."""

    num_data_elus: int
    data_elu_resource_info: ELUResourceInfo
    num_bus_elus: int
    bus_elu_resource_info: ELUResourceInfo
    num_distillation_elus: int
    distillation_elu_resource_info: ELUResourceInfo

@dataclass
class LogicalFailureRates:
    """Logical failure rates for various processes."""

    total_circuit_failure_rate: float
    total_rotation_failure_rate: float
    total_distillation_failure_rate: float
    total_qec_failure_rate: float
    per_rotation_synthesi_failure_rate: float
    per_t_gate_failure_rate: float
    per_qec_failure_rate: float

@dataclass
class LogicalArchitectureResourceInfo:
    """Info logical architecture model resources."""

    num_logical_data_qubits: int
    num_logical_bus_qubits: int
    data_and_bus_code_distance: int
    num_magic_state_factories: int
    magic_state_factory: Optional[MagicStateFactoryInfo] = None
    qec_cycle_allocation: Optional[QECCycleAllocation] = None
    logical_failure_rates: LogicalFailureRates = None
    
    @property
    def num_logical_qubits(self) -> int:
        return self.num_logical_data_qubits + self.num_logical_bus_qubits

    @property
    def spacetime_volume_in_logical_qubit_tocks(self) -> float:
        st_volume_in_logical_qubit_tocks = self.qec_cycle_allocation.total*self.num_logical_qubits / self.data_and_bus_code_distance
        return st_volume_in_logical_qubit_tocks

@dataclass
class AbstractLogicalResourceInfo:
    """Info relating to abstract logical resources."""

    n_abstract_logical_qubits: int
    n_t_gates: int

@dataclass
class ResourceInfo(Generic[TExtra]):
    """Generic information about estimated resources with possible extras.

    The generic parameter of this class is a type of extra information stored
    in the extra field. This information should relate to the specific
    compilation method or algorithm used for estimating resources.

    Other fields are common between estimation methods that we currently have.

    There are several variants of this class aliased below.
    """

    n_abstract_logical_qubits: Optional[int] = None
    n_physical_qubits: Optional[int] = None
    n_t_gates: Optional[int] = None
    total_time_in_seconds: Optional[float] = None
    abstract_logical_resource_info: Optional[AbstractLogicalResourceInfo] = None
    logical_architecture_resource_info: Optional[LogicalArchitectureResourceInfo] = None
    hardware_resource_info: Optional[DetailedIonTrapArchitectureResourceInfo] = None
    decoder_info: Optional[DecoderInfo] = None
    optimization: Optional[str] = None
    extra: Optional[TExtra] = None


@dataclass
class GraphExtra:
    """Extra info relating to resource estimation using Graph State Compilation."""

    implementation: CompiledAlgorithmImplementation


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
