################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
# WARNING! SIMPLE MODELING AHEAD! ABANDON NUANCE ALL YE WHO ENTER HERE!


import warnings
from dataclasses import dataclass
from typing import Protocol

from .resource_info import ResourceInfo


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

    @property
    def physical_qubit_error_rate(self) -> float:
        pass

    @property
    def surface_code_cycle_time_in_seconds(self) -> float:
        pass


@dataclass(frozen=True)
class IONTrapModel:
    physical_qubit_error_rate: float = 1e-4
    surface_code_cycle_time_in_seconds: float = 1e-3


@dataclass(frozen=True)
class SCModel:
    physical_qubit_error_rate: float = 1e-3
    surface_code_cycle_time_in_seconds: float = 1e-7


BASIC_ION_TRAP_ARCHITECTURE_MODEL = IONTrapModel()
BASIC_SC_ARCHITECTURE_MODEL = SCModel()


@dataclass
class DetailedIonTrapResourceInfo:
    """Info relating to detailed ion trap architecture model resources."""

    power_consumed_per_elu_in_kW: float
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
    total_elu_power_consumed_in_kW: float
    total_elu_energy_consumed_in_kJ: float


class DetailedIonTrapModel:
    def __init__(
        self,
        physical_qubit_error_rate: float = 1e-4,
        surface_code_cycle_time_in_seconds: float = 1e-3,
    ):
        self.physical_qubit_error_rate = 1e-4
        # TODO: PJ check with Simon about this number
        self.surface_code_cycle_time_in_seconds = 1e-3

    def get_hardware_resource_estimates(self, resource_info: ResourceInfo):
        code_distance = resource_info.code_distance

        # Compute per-elu values
        (
            memory_qubits,
            computational_qubits,
            communication_qubits,
        ) = self.functional_designation_of_chains_within_ELU(code_distance)

        (
            num_communication_ports_per_elu,
            second_switch_per_elu_necessary,
        ) = self.num_communication_ports_per_ELU(code_distance)

        # Compute totals

        # Number of logical qubits can't exceed 1 per ELU
        # Protocol requires 1 logical qubit per ELU
        num_elus = resource_info.n_logical_qubits

        # Multiply quantities by number of ELUs
        total_num_memory_qubits = num_elus * memory_qubits
        total_num_computational_qubits = num_elus * computational_qubits
        total_num_communication_qubits = num_elus * communication_qubits
        total_num_ions = (
            total_num_memory_qubits
            + total_num_computational_qubits
            + total_num_communication_qubits
        )
        total_num_communication_ports = num_elus * num_communication_ports_per_elu
        total_elu_power_consumed_in_kW = num_elus * self.power_consumed_per_ELU_in_kW()
        total_elu_energy_consumed_in_kJ = (
            num_elus
            * self.power_consumed_per_ELU_in_kW()
            * resource_info.total_time_in_seconds
        )

        hardware_resource_estimates = DetailedIonTrapResourceInfo(
            power_consumed_per_elu_in_kW=self.power_consumed_per_ELU_in_kW(),
            num_communication_ports_per_elu=num_communication_ports_per_elu,
            second_switch_per_elu_necessary=second_switch_per_elu_necessary,
            num_communication_qubits_per_elu=communication_qubits,
            num_memory_qubits_per_elu=memory_qubits,
            num_computational_qubits_per_elu=computational_qubits,
            num_optical_cross_connect_layers=self.num_optical_cross_connect_layers(
                num_elus,
                communication_qubits,
                num_communication_ports_per_elu,
            ),
            num_ELUs_per_optical_cross_connect=self.num_ELUs_per_optical_cross_connect(
                code_distance, communication_qubits
            ),
            total_num_ions=total_num_ions,
            total_num_communication_qubits=total_num_communication_qubits,
            total_num_memory_qubits=total_num_memory_qubits,
            total_num_computational_qubits=total_num_computational_qubits,
            total_num_communication_ports=total_num_communication_ports,
            num_elus=num_elus,
            total_elu_power_consumed_in_kW=total_elu_power_consumed_in_kW,
            total_elu_energy_consumed_in_kJ=total_elu_energy_consumed_in_kJ,
        )

        return hardware_resource_estimates

    def power_consumed_per_ELU_in_kW(
        self,
    ):
        # Value reported by IonQ
        return 5.0

    def num_communication_qubits_per_ELU(self, code_distance):
        # Lookup table generated from simulations of the 3-3-9s protocol by
        # Hudson Leone of UTS
        qubit_count_lookup_table = {
            3: 72,
            4: 96,
            5: 120,
            6: 168,
            7: 196,
            8: 224,
            9: 252,
            10: 280,
            11: 308,
            12: 336,
            13: 364,
            14: 392,
            15: 420,
            16: 448,
            17: 476,
            18: 504,
            19: 532,
            20: 560,
            21: 588,
            22: 704,
            23: 736,
            24: 768,
            25: 800,
            26: 832,
            27: 864,
            28: 896,
            29: 928,
            30: 960,
            31: 992,
            32: 1024,
            33: 1056,
            34: 1088,
            35: 1120,
        }

        # Check if input is an integer
        if not isinstance(code_distance, int):
            raise ValueError("Input should be an integer.")

        # Check if the integer is between 3 and 35
        if 3 <= code_distance <= 35:
            return qubit_count_lookup_table[code_distance]
        else:
            raise ValueError(
                f"Distance should be between 3 and 35. Got {code_distance}"
            )

    def num_communication_ports_per_ELU(self, code_distance):
        # Computes the number of physical ports (optical fibers) going from the
        # ELU to the quantum switch.
        num_communication_ions_per_elu = self.num_communication_qubits_per_ELU(
            code_distance
        )

        num_ports = num_communication_ions_per_elu

        # Check and flag if an extra switch is necessary for each ELU
        second_switch_per_elu_necessary = False
        if num_ports > 500:
            second_switch_per_elu_necessary = True

        return num_ports, second_switch_per_elu_necessary

    def functional_designation_of_chains_within_ELU(self, code_distance):
        # Functional designation of chains within the ELU
        memory_qubits = code_distance
        computational_qubits = 2 * code_distance**2
        communication_qubits = self.num_communication_qubits_per_ELU(code_distance)
        return memory_qubits, computational_qubits, communication_qubits

    def num_optical_cross_connect_layers(
        self,
        num_elus,
        num_communication_qubits_per_elu,
        num_communication_ports_per_elu,
    ):
        # Description of accounting of optical cross-connect and switch architecture:
        # Need to ensure that each ELU can be connected with its nearest neighbor in
        # the two rows of the bus architecture:
        # B - A - D - ... - X
        # |   |   |         |
        # X - C - X - ... - X
        # Each group of ELU + neighbors needs to be serviced by a single switch
        # (e.g. A, B, C, D) Switches with common ELUs need to be connected by other
        # switches For switches that need to be connected, XXX many of their switches
        # must be used for connecting to connector switches
        # Each switch has 1000 ports
        # Each group of ELU + neighbor has at most 4 ELUs
        warnings.warn("This output parameter has yet to be implemented.")

        num_OXC_layers = None

        return num_OXC_layers

    def num_ELUs_per_optical_cross_connect(
        self, code_distance, num_communication_qubits
    ):
        warnings.warn("This output parameter has yet to be implemented.")
        num_ELUs_per_OXC = None
        return num_ELUs_per_OXC


DETAILED_ION_TRAP_ARCHITECTURE_MODEL = DetailedIonTrapModel()
