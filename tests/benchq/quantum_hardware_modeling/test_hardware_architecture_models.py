from contextlib import suppress as do_not_raise

import pytest

from benchq.quantum_hardware_modeling import (
    DetailedIonTrapModel,
)
from benchq.resource_estimators.resource_info import (
    ELUResourceInfo,
    DetailedIonTrapArchitectureResourceInfo,
    ResourceInfo,
    BusArchitectureResourceInfo,
    MagicStateFactoryInfo,
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
            assert model.surface_code_cycle_time_in_seconds == 1e-3

        def test_parametrized_constructor(self):
            model = DetailedIonTrapModel(22, 36)

            assert model.physical_qubit_error_rate == 22
            assert model.surface_code_cycle_time_in_seconds == 36

    class TestPowerPerELU:
        def test_power_consumed_per_elu_in_kilowatts(self):
            model = DetailedIonTrapModel()
            assert model.power_consumed_per_ELU_in_kilowatts() == 5.0

    # class TestNumCommunicationQubits:
    #     @pytest.mark.parametrize(
    #         "code_distance, qubits, throws",
    #         [
    #             (1, 0, True),
    #             (2, 0, True),
    #             (3, 72, False),
    #             (14, 392, False),
    #             (25, 800, False),
    #             (35, 1120, False),
    #             (36, 0, True),
    #             (1000, 0, True),
    #         ],
    #     )
    #     def test_num_communication_ions_per_elu(self, code_distance, qubits, throws):
    #         model = DetailedIonTrapModel()
    #         raises = pytest.raises(ValueError) if throws else do_not_raise()

    #         with raises:
    #             assert model.num_communication_ions_per_elu(code_distance) == qubits

    # class TestNumCommunicationPorts:
    #     @pytest.mark.parametrize(
    #         "code_distance, qubits, throws, second_switch_needed",
    #         [
    #             (1, 0, True, False),
    #             (2, 0, True, False),
    #             (3, 72, False, False),
    #             (14, 392, False, False),
    #             (25, 800, False, True),
    #             (35, 1120, False, True),
    #             (36, 0, True, False),
    #             (1000, 0, True, False),
    #         ],
    #     )
    #     def test_num_communication_ports(
    #         self, code_distance, qubits, throws, second_switch_needed
    #     ):
    #         model = DetailedIonTrapModel()
    #         raises = pytest.raises(ValueError) if throws else do_not_raise()

    #         with raises:
    #             assert model.num_communication_ports_per_ELU(code_distance) == (
    #                 qubits,
    #                 second_switch_needed,
    #             )

    # class TestFunctionDesignationOfChains:
    #     @pytest.mark.parametrize(
    #         "code_distance, computational_qubits, communication_qubits",
    #         [(10, 200, 280), (30, 1800, 960), (5, 50, 120)],
    #     )
    #     def test_functional_designation_of_chains_within_elu(
    #         self, code_distance, computational_qubits, communication_qubits
    #     ):
    #         model = DetailedIonTrapModel()

    #         assert model.functional_designation_of_chains_within_ELU(code_distance) == (
    #             code_distance,
    #             computational_qubits,
    #             communication_qubits,
    #         )

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
            # resource_info.n_logical_data_qubits = n_logical_data_qubits
            # resource_info.n_logical_bus_qubits = n_logical_bus_qubits
            # resource_info.n_magic_state_factories = n_magic_state_factories
            magic_state_factory_info = MagicStateFactoryInfo(
                "(15-to-1)_17,7,7", 4.5e-8, (72, 64), 4620, 42.6
            )

            n_bus_qubits = 9 * n_logical_qubits
            n_magic_state_factories = n_bus_qubits
            bus_architecture_resource_info = BusArchitectureResourceInfo(
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
                num_communication_ports_per_elu=num_communication_ions_per_distillation_elu,
                second_switch_per_elu_necessary=True,
                num_communication_ions_per_elu=num_communication_ions_per_distillation_elu,
                num_memory_ions_per_elu=num_memory_ions_per_distillation_elu,
                num_computational_ions_per_elu=num_computational_ions_per_distillation_elu,
            )

            assert hw_resource_info == DetailedIonTrapArchitectureResourceInfo(
                num_data_elus=n_logical_qubits,
                data_elu_resource_info=data_elu_resource_info,
                num_bus_elus=n_bus_qubits,
                bus_elu_resource_info=bus_elu_resource_info,
                num_distillation_elus=n_magic_state_factories,
                distillation_elu_resource_info=distillation_elu_resource_info,
            )
