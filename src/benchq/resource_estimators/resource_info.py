################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""Data structures describing estimated resources and related info."""

from dataclasses import dataclass, field
from typing import Generic, Optional, Tuple, TypeVar, Union
from decimal import Decimal


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

    num_data_elus: Optional[int] = None
    data_elu_resource_info: Optional[ELUResourceInfo] = None
    num_bus_elus: Optional[int] = None
    bus_elu_resource_info: Optional[ELUResourceInfo] = None
    num_distillation_elus: Optional[int] = None
    distillation_elu_resource_info: Optional[ELUResourceInfo] = None


@dataclass
class LogicalFailureRateInfo:
    """Logical failure rates for various processes."""

    total_rotation_failure_rate: Union[None, float, Decimal] = None
    total_distillation_failure_rate: Union[None, float, Decimal] = None
    total_qec_failure_rate: Union[None, float, Decimal] = None
    per_rotation_failure_rate: Union[None, float, Decimal] = None
    per_t_gate_failure_rate: Union[None, float, Decimal] = None
    per_qec_failure_rate: Union[None, float, Decimal] = None

    @property
    def total_circuit_failure_rate(self) -> float:
        """Dynamically calculate total circuit failure rate."""
        return (
            (
                float(self.total_rotation_failure_rate)
                if self.total_rotation_failure_rate is not None
                else 0
            )
            + (
                float(self.total_distillation_failure_rate)
                if self.total_distillation_failure_rate is not None
                else 0
            )
            + (
                float(self.total_qec_failure_rate)
                if self.total_qec_failure_rate is not None
                else 0
            )
        )


@dataclass
class LogicalArchitectureResourceInfo:
    """Info logical architecture model resources."""

    num_logical_data_qubits: Optional[int] = None
    num_logical_bus_qubits: Optional[int] = None
    data_and_bus_code_distance: Optional[int] = None
    num_magic_state_factories: Optional[int] = None
    magic_state_factory: Optional[MagicStateFactoryInfo] = None
    qec_cycle_allocation: Optional[QECCycleAllocation] = None
    logical_failure_rate_info: Optional[LogicalFailureRateInfo] = None

    @property
    def num_logical_qubits(self) -> int:
        if (
            not isinstance(self.num_logical_data_qubits, int)
            and self.num_logical_data_qubits is not None
        ):
            raise TypeError("num_logical_data_qubits must be an integer")
        if (
            not isinstance(self.num_logical_bus_qubits, int)
            and self.num_logical_bus_qubits is not None
        ):
            raise TypeError("num_logical_bus_qubits must be an integer")
        return (self.num_logical_data_qubits or 0) + (self.num_logical_bus_qubits or 0)

    @property
    def spacetime_volume_in_logical_qubit_tocks(self) -> float:
        if self.qec_cycle_allocation is None:
            raise ValueError("qec_cycle_allocation must not be None")
        if self.data_and_bus_code_distance is None:
            raise ValueError("data_and_bus_code_distance must not be None")
        st_volume_in_logical_qubit_tocks = (
            self.qec_cycle_allocation.total
            * self.num_logical_qubits
            / self.data_and_bus_code_distance
        )
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
    total_circuit_failure_rate: Optional[float] = None
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
class OpenFermionExtra:
    """Extra info relating to resource estimation using OpenFermion."""

    fail_rate_msFactory: float
    rounds_magicstateFactory: float
    scc_time: float
    physical_qubit_error_rate: float
    code_distance: int
    logical_error_rate: float
    magic_state_factory_name: str


# Alias for type of resource info returned by OpenFermion
OpenFermionResourceInfo = ResourceInfo[OpenFermionExtra]
