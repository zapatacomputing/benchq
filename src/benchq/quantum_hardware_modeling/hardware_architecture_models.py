################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
import math
from dataclasses import dataclass
from typing import Optional, Protocol, runtime_checkable

from ..resource_estimators.resource_info import (
    BusArchitectureResourceInfo,
    DetailedIonTrapArchitectureResourceInfo,
    ELUResourceInfo,
    MagicStateFactoryInfo,
    ResourceInfo,
)


class BasicArchitectureModel(Protocol):
    """Basic Architecture model meant to serve as a base class for the
    other basic architecture models. WARNING! Running a resource estimate
    with this architecture model will fail as, you need to choose an ION
    based or SC based model in order to select a proper factory.

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
        raise NotImplementedError("This method should be overridden by subclasses")

    @property
    def surface_code_cycle_time_in_seconds(self) -> float:
        raise NotImplementedError("This method should be overridden by subclasses")


@runtime_checkable
class DetailedArchitectureModel(BasicArchitectureModel, Protocol):
    """DetailedArchitectureModel extends basic one, with the ability to
    calculate detailed hardware estimates."""

    def get_hardware_resource_estimates(
        self, bus_architecture_resource_info: BusArchitectureResourceInfo
    ):
        pass


@dataclass(frozen=True)
class IONTrapModel:
    physical_qubit_error_rate: float = 1e-4
    surface_code_cycle_time_in_seconds: float = 1e-3


@dataclass(frozen=True)
class SCModel:
    physical_qubit_error_rate: float = 1e-3
    surface_code_cycle_time_in_seconds: float = 1e-6


BASIC_ION_TRAP_ARCHITECTURE_MODEL = IONTrapModel()
BASIC_SC_ARCHITECTURE_MODEL = SCModel()


class DetailedIonTrapModel:
    def __init__(
        self,
        physical_qubit_error_rate: float = 1e-4,
        # A single inter-ELU lattice surgery operation requires 1ms.
        # Each inter-ELU lattice surgery operation for a single ELU
        # happens sequentially and each bus interacts with at most 3 neighbors
        # so the total time for a single surface code cycle is 3ms.
        surface_code_cycle_time_in_seconds: float = 3e-3,
    ):
        self.physical_qubit_error_rate = physical_qubit_error_rate
        self.surface_code_cycle_time_in_seconds = surface_code_cycle_time_in_seconds

    def get_hardware_resource_estimates(
        self, bus_architecture_resource_info: BusArchitectureResourceInfo
    ):
        code_distance = bus_architecture_resource_info.data_and_bus_code_distance

        # Check that the resource_info.logical_architecture_resource_info
        # is BusArchitectureResourceInfo
        if not isinstance(
            bus_architecture_resource_info,
            BusArchitectureResourceInfo,
        ):
            raise ValueError(
                "bus_architecture_resource_info should be BusArchitectureResourceInfo"
            )

        n_logical_data_qubits = bus_architecture_resource_info.num_logical_data_qubits
        n_logical_bus_qubits = bus_architecture_resource_info.num_logical_bus_qubits
        n_magic_state_factories = (
            bus_architecture_resource_info.num_magic_state_factories
        )

        # Populate info for logical data qubit ELUs
        data_elu_resource_info = self.model_data_elu_resource_info(code_distance)

        # Populate info for logical bus qubit ELUs
        bus_elu_resource_info = self.model_bus_elu_resource_info(code_distance)

        # Populate info for distillation ELUs
        distillation_elu_resource_info = self.model_distillation_elu_resource_info(
            code_distance, bus_architecture_resource_info.magic_state_factory
        )

        hardware_resource_estimates = DetailedIonTrapArchitectureResourceInfo(
            num_data_elus=n_logical_data_qubits,
            data_elu_resource_info=data_elu_resource_info,
            num_bus_elus=n_logical_bus_qubits,
            bus_elu_resource_info=bus_elu_resource_info,
            num_distillation_elus=n_magic_state_factories,
            distillation_elu_resource_info=distillation_elu_resource_info,
        )

        # TODO: Implement the following
        # hardware_resource_estimates = self.model_switch_network(
        #     hardware_resource_estimates
        # )

        return hardware_resource_estimates

    def model_switch_network(
        self,
        detailed_ion_trap_resource_info: DetailedIonTrapArchitectureResourceInfo,
    ):
        # # Optical cross-connect resources
        # detailed_ion_trap_resource_info.num_optical_cross_connect_layers = (
        #     self.num_optical_cross_connect_layers(
        #         num_elus,
        #         num_communication_ions_per_elu,
        #         num_communication_ports_per_elu,
        #     )
        # )
        # detailed_ion_trap_resource_info.num_ELUs_per_optical_cross_connect = None

        raise NotImplementedError("model_switch_network is not implemented yet")
        # return detailed_ion_trap_resource_info

    def model_comm_and_memory_unit(
        self, elu_resource_info: ELUResourceInfo, code_distance: int
    ):

        # Communication resources
        (
            num_communication_ports_per_elu,
            second_switch_per_elu_necessary,
        ) = self.num_communication_ports_per_ELU(code_distance)
        elu_resource_info.num_communication_ports_per_elu = (
            num_communication_ports_per_elu
        )
        elu_resource_info.num_communication_ions_per_elu = (
            num_communication_ports_per_elu
        )

        elu_resource_info.second_switch_per_elu_necessary = (
            second_switch_per_elu_necessary
        )

        # Memory resources
        num_memory_ions_per_elu = (
            4 * self.find_minimum_n_dist_pairs(code_distance) + 2 * code_distance - 1
        )
        elu_resource_info.num_memory_ions_per_elu = num_memory_ions_per_elu

        return elu_resource_info

    def model_data_elu_resource_info(self, code_distance: int):
        elu_resource_info = ELUResourceInfo()
        elu_resource_info = self.model_comm_and_memory_unit(
            elu_resource_info, code_distance
        )
        elu_resource_info.power_consumed_per_elu_in_kilowatts = (
            self.power_consumed_per_ELU_in_kilowatts()
        )
        elu_resource_info.num_computational_ions_per_elu = (2 * code_distance - 1) ** 2

        return elu_resource_info

    def model_bus_elu_resource_info(self, code_distance: int):
        elu_resource_info = ELUResourceInfo()
        elu_resource_info = self.model_comm_and_memory_unit(
            elu_resource_info, code_distance
        )
        elu_resource_info.power_consumed_per_elu_in_kilowatts = (
            self.power_consumed_per_ELU_in_kilowatts()
        )
        elu_resource_info.num_computational_ions_per_elu = (
            2 * code_distance - 1
        ) ** 2 + (2 * code_distance - 1)

        return elu_resource_info

    def model_distillation_elu_resource_info(
        self,
        code_distance: int,
        magic_state_factory: Optional[MagicStateFactoryInfo] = None,
    ):
        if magic_state_factory is None:
            print(
                "Warning: magic_state_factory is None. "
                "Returning empty ELUResourceInfo object."
            )
            return ELUResourceInfo()

        elu_resource_info = ELUResourceInfo()
        elu_resource_info = self.model_comm_and_memory_unit(
            elu_resource_info, code_distance
        )
        elu_resource_info.power_consumed_per_elu_in_kilowatts = (
            self.power_consumed_per_ELU_in_kilowatts()
        )
        elu_resource_info.num_computational_ions_per_elu = magic_state_factory.qubits

        return elu_resource_info

    def power_consumed_per_ELU_in_kilowatts(
        self,
    ):
        # Value reported by IonQ
        return 5.0

    def num_communication_ports_per_ELU(self, code_distance: int):
        # Computes the number of physical ports (optical fibers) going from the
        # ELU to the quantum switch.
        num_communication_ions_per_elu = self.find_minimum_comm_ions(code_distance)

        num_ports = num_communication_ions_per_elu

        # Check and flag if an extra switch is necessary for each ELU
        second_switch_per_elu_necessary = False
        if num_ports > 500:
            second_switch_per_elu_necessary = True

        return num_ports, second_switch_per_elu_necessary

    def num_optical_cross_connect_layers(
        self,
        num_elus: int,
        num_communication_ions_per_elu: int,
        num_communication_ports_per_elu: int,
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

        # Not yet implemented
        return -1

    def num_ELUs_per_optical_cross_connect(
        self, code_distance: int, num_communication_qubits: int
    ):
        # Not yet implemented
        return -1

    def find_minimum_n_dist_pairs(self, code_distance):
        """Finds the minimum number of pairs required to achieve a given fidelity."""
        p_dist = 0.76  # 4->1 distillation success probability
        required_fidelity = 0.999  # required distilled fidelity
        required_number_of_pairs = 2 * code_distance - 1

        targetNum = required_number_of_pairs
        cdf = 1 - stable_binom_cdf(required_number_of_pairs - 1, targetNum, p_dist)

        while cdf < required_fidelity:
            targetNum += 1
            cdf = 1 - stable_binom_cdf(required_number_of_pairs - 1, targetNum, p_dist)

        return targetNum

    # TODO: determine how to handle attempts
    def find_minimum_comm_ions(self, code_distance, attempts=1000):
        ion_to_ion_entanglement_success_probability = (
            0.000218  # ion-ion entanglement success probability
        )
        required_number_of_pairs = 4 * self.find_minimum_n_dist_pairs(code_distance)
        required_fidelity = 0.999  # required distilled fidelity

        targetNum = required_number_of_pairs
        curSuccProb = 1 - (1 - ion_to_ion_entanglement_success_probability) ** attempts
        cdf = 1 - stable_binom_cdf(required_number_of_pairs - 1, targetNum, curSuccProb)

        while cdf < required_fidelity:
            targetNum += 1
            cdf = 1 - stable_binom_cdf(
                required_number_of_pairs - 1, targetNum, curSuccProb
            )

        return targetNum


# Helper functions to compute the number of distillation pairs and communication ions


def log_binomial_coefficient(n, k):
    """Compute the logarithm of the binomial coefficient
    for the purpose of numerical stability."""
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def stable_binom_cdf(x, n, p):
    log_p = math.log(p)
    log_q = math.log(1 - p)
    cdf = 0
    cdf_exp = []

    # Calculate the log of the CDF using a sum of exponentials
    for k in range(x + 1):
        log_prob = log_binomial_coefficient(n, k) + k * log_p + (n - k) * log_q
        cdf_exp.append(log_prob)

    # Compute the maximum log-probability to scale the other terms to prevent underflow
    max_log_prob = max(cdf_exp)
    cdf = sum(math.exp(log_prob - max_log_prob) for log_prob in cdf_exp)

    return math.exp(max_log_prob) * cdf


DETAILED_ION_TRAP_ARCHITECTURE_MODEL = DetailedIonTrapModel()
