################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
# WARNING! SIMPLE MODELING AHEAD! ABANDON NUANCE ALL YE WHO ENTER HERE!


from dataclasses import dataclass
from typing import Protocol
from .resource_info import (
    ResourceInfo,
)


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
    surface_code_cycle_time_in_seconds: float = 1e-5


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
    number_of_qubits_per_chain: int
    number_of_communication_qubits_per_elu: int
    number_of_memory_qubits_per_elu: int
    number_of_computational_qubits_per_elu: int
    number_of_optical_cross_connect_layers: int
    number_of_ELUs_per_optical_cross_connect: int


class DetailedIonTrapModel:
    def __init__(
        self,
        physical_qubit_error_rate: float = 1e-4,
        surface_code_cycle_time_in_seconds: float = 1e-5,
    ):
        self.physical_qubit_error_rate = 1e-4
        self.surface_code_cycle_time_in_seconds = 1e-5

    def get_hardware_resource_estimates(self, resource_info: ResourceInfo):
        code_distance = resource_info.code_distance
        n_physical_qubits = resource_info.n_physical_qubits

        # TODO: check this!
        number_of_elus = int(n_physical_qubits / 1000)

        (
            memory_qubits,
            computational_qubits,
            communication_qubits,
        ) = self.functional_designation_of_chains_within_ELU(code_distance)

        hardware_resource_estimates = DetailedIonTrapResourceInfo(
            power_consumed_per_elu_in_kW=self.power_consumed_per_ELU_in_kW(),
            number_of_qubits_per_chain=self.compute_number_of_qubits_per_chain(
                code_distance
            ),
            number_of_communication_qubits_per_elu=communication_qubits,
            number_of_memory_qubits_per_elu=memory_qubits,
            number_of_computational_qubits_per_elu=computational_qubits,
            number_of_optical_cross_connect_layers=self.number_of_optical_cross_connect_layers(
                number_of_elus, communication_qubits
            ),
            number_of_ELUs_per_optical_cross_connect=self.number_of_ELUs_per_optical_cross_connect(
                code_distance, communication_qubits
            ),
        )

        return hardware_resource_estimates

    def compute_number_of_qubits_per_chain(self, code_distance):
        # Simon can give this function
        # lookup table
        # lookup_table_num_qubits = upload_lookup_table()
        # number_of_qubits = lookup_table_num_qubits[code_distance]
        number_of_qubits = 100

        if number_of_qubits > 1000:
            Warning(
                "Number of qubits per chain greater than 1000 cannot be supported by the architecture."
            )
        return number_of_qubits

    # Output to dict
    def power_consumed_per_ELU_in_kW(
        self,
    ):
        # As reported by Ilia
        return 5.0

    def number_of_communication_qubits_per_ELU(self, code_distance):
        # Simon can give
        number_of_qubits = 42
        return number_of_qubits

    def number_of_communication_ports_per_ELU(self, code_distance):
        # Question 2: is this meaningfully different from communication qubit/communication ions?
        number_of_ports = 42
        return number_of_ports

    # Communication ports is the number of physical port (optical fibers) going from the ELU to the quantum switch.

    def functional_designation_of_chains_within_ELU(self, code_distance):
        # Check with Simon
        # Functional designation of chains within the ELU (such as computational function,
        # memory function, etc.)
        memory_qubits = code_distance
        computational_qubits = code_distance**2
        communication_qubits = 42
        return memory_qubits, computational_qubits, communication_qubits

    # Doesn't differ from above
    # def number_of_functional_units_within_ELU(code_distance):
    #   # Number of different functional units within and across ELUs
    #   # in the system (how many computational and memory units do we need?) This would also
    #   # be protocol and d-dependent. However, the computational zone would be the largest to
    #   # support having a “local” error-correct qubit, the rest would support lattice surgery operations.
    #   return number_of_functional_units

    def number_of_optical_cross_connect_layers(
        self, number_of_elus, number_of_communication_qubits_per_elu
    ):
        # Question 4: Simon wasn't sure what this was. Are OXC the same as "optical switches?
        # And are you suggesting we just set this value to 2?
        # This is an optical cross connect, it’s not a switch per se, more like a network mesh.
        # So this number depends on the amount of ports we need. If we need more than 1000 ports, then we need more then a single layer.
        # We believe that a (quantum) switch can have around 1000 ports.
        # Assuming we leave some overhead for intra and inter-layer connectivity,
        # this would probably not require more than 2 layers at most (again, this
        # really depends on requirements from d, and both Ns). We can probably improve
        # the resource ask by multiplexing but this assessment would have to delayed.

        # Ilia: Depends on how many
        number_of_OXC_layers = 42
        return number_of_OXC_layers

    def number_of_ELUs_per_optical_cross_connect(
        self, code_distance, number_of_communication_qubits
    ):
        # Question 5: Shold we reverse this so that we use the number of ELUs to compute the
        # number of optical cross connects?
        return 42
