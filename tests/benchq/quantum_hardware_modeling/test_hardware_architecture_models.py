from contextlib import suppress as do_not_raise

import pytest

from benchq.quantum_hardware_modeling import DetailedIonTrapModel
from benchq.resource_estimators.resource_info import (
    LogicalArchitectureResourceInfo,
    DetailedIonTrapArchitectureResourceInfo,
    ELUResourceInfo,
    MagicStateFactoryInfo,
    ResourceInfo,
)


@pytest.fixture(scope="function")
def dummy_resource_info():
    resource_info = ResourceInfo(
        code_distance=17,
        logical_error_rate=1,
        n_logical_qubits=30,
        n_physical_qubits=None,
        total_time_in_seconds=5,
        optimization="",
        decoder_info=None,
        magic_state_factory_name="",
        extra=None,
    )
    yield resource_info


class TestDetailedIonTrapModel:
    class TestConstructor:
        def test_default_constructor(self):
            model = DetailedIonTrapModel()

            assert model.physical_qubit_error_rate == 1e-4
            assert model.surface_code_cycle_time_in_seconds == 3e-3

        def test_parametrized_constructor(self):
            model = DetailedIonTrapModel(22, 36)

            assert model.physical_qubit_error_rate == 22
            assert model.surface_code_cycle_time_in_seconds == 36

    class TestPowerPerELU:
        def test_power_consumed_per_elu_in_kilowatts(self):
            model = DetailedIonTrapModel()
            assert model.power_consumed_per_ELU_in_kilowatts() == 5.0

    class TestFindMinimumCommIons:
        @pytest.mark.parametrize(
            "code_distance, attempts, expected_result",
            [
                (17, 1000, 1391),
                (19, 1000, 1524),
            ],
        )
        def test_find_minimum_comm_ions(self, code_distance, attempts, expected_result):
            model = DetailedIonTrapModel()
            result = model.find_minimum_comm_ions(code_distance, attempts)
            assert result == expected_result

    class TestHardwareResourceEstimates:
        @pytest.mark.parametrize(
            "code_distance, n_logical_qubits",
            [(13, 10), (21, 100)],
        )
        def test_hardware_resource_estimates(
            self,
            dummy_resource_info,
            code_distance,
            n_logical_qubits,
        ):
            # Given
            magic_state_factory_info = MagicStateFactoryInfo(
                "(15-to-1)_17,7,7", 4.5e-8, (72, 64), 4620, 42.6
            )

            n_bus_qubits = 9 * n_logical_qubits
            n_magic_state_factories = n_bus_qubits
            bus_architecture_resource_info = LogicalArchitectureResourceInfo(
                n_logical_qubits,
                n_bus_qubits,
                code_distance,
                n_magic_state_factories,
                magic_state_factory_info,
            )

            model = DetailedIonTrapModel()

            # When
            hw_resource_info = model.get_hardware_resource_estimates(
                bus_architecture_resource_info
            )

            # Then

            # Computational ions per ELU
            num_computational_ions_per_data_elu = (2 * code_distance - 1) ** 2
            num_computational_ions_per_bus_elu = (2 * code_distance - 1) ** 2 + (
                2 * code_distance - 1
            )
            num_computational_ions_per_distillation_elu = (
                magic_state_factory_info.qubits
            )

            # Memory ions per ELU
            num_memory_ions_per_data_elu = 4 * model.find_minimum_n_dist_pairs(
                code_distance
            ) + (2 * code_distance - 1)
            num_memory_ions_per_bus_elu = num_memory_ions_per_data_elu
            num_memory_ions_per_distillation_elu = num_memory_ions_per_data_elu

            # Communication ions per ELU
            num_communication_ions_per_data_elu = model.find_minimum_comm_ions(
                code_distance
            )
            num_communication_ions_per_bus_elu = num_communication_ions_per_data_elu
            num_communication_ions_per_distillation_elu = (
                num_communication_ions_per_data_elu
            )
            data_elu_resource_info = ELUResourceInfo(
                power_consumed_per_elu_in_kilowatts=5.0,
                num_communication_ports_per_elu=num_communication_ions_per_data_elu,
                second_switch_per_elu_necessary=True,
                num_communication_ions_per_elu=num_communication_ions_per_data_elu,
                num_memory_ions_per_elu=num_memory_ions_per_data_elu,
                num_computational_ions_per_elu=num_computational_ions_per_data_elu,
            )

            bus_elu_resource_info = ELUResourceInfo(
                power_consumed_per_elu_in_kilowatts=5.0,
                num_communication_ports_per_elu=num_communication_ions_per_bus_elu,
                second_switch_per_elu_necessary=True,
                num_communication_ions_per_elu=num_communication_ions_per_bus_elu,
                num_memory_ions_per_elu=num_memory_ions_per_bus_elu,
                num_computational_ions_per_elu=num_computational_ions_per_bus_elu,
            )
            distillation_elu_resource_info = ELUResourceInfo(
                power_consumed_per_elu_in_kilowatts=5.0,
                num_communication_ports_per_elu=(
                    num_communication_ions_per_distillation_elu
                ),
                second_switch_per_elu_necessary=True,
                num_communication_ions_per_elu=(
                    num_communication_ions_per_distillation_elu
                ),
                num_memory_ions_per_elu=num_memory_ions_per_distillation_elu,
                num_computational_ions_per_elu=(
                    num_computational_ions_per_distillation_elu
                ),
            )

            assert hw_resource_info == DetailedIonTrapArchitectureResourceInfo(
                num_data_elus=n_logical_qubits,
                data_elu_resource_info=data_elu_resource_info,
                num_bus_elus=n_bus_qubits,
                bus_elu_resource_info=bus_elu_resource_info,
                num_distillation_elus=n_magic_state_factories,
                distillation_elu_resource_info=distillation_elu_resource_info,
            )
