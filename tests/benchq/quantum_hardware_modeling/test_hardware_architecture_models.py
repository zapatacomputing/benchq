from contextlib import suppress as do_not_raise

import pytest

from benchq.quantum_hardware_modeling import DetailedIonTrapModel
from benchq.resource_estimators.resource_info import (
    DetailedIonTrapResourceInfo,
    ResourceInfo,
)


@pytest.fixture(scope="function")
def dummy_resource_info():
    resource_info = ResourceInfo(
        code_distance=90,
        logical_error_rate=1,
        n_logical_qubits=30,
        n_physical_qubits=300,
        total_time_in_seconds=5,
        decoder_info=None,
        magic_state_factory_name="",
        routing_to_measurement_volume_ratio=1,
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

    class TestNumCommunicationQubits:
        @pytest.mark.parametrize(
            "code_distance, qubits, throws",
            [
                (1, 0, True),
                (2, 0, True),
                (3, 72, False),
                (14, 392, False),
                (25, 800, False),
                (35, 1120, False),
                (36, 0, True),
                (1000, 0, True),
            ],
        )
        def test_num_communication_qubits_per_elu(self, code_distance, qubits, throws):
            model = DetailedIonTrapModel()
            raises = pytest.raises(ValueError) if throws else do_not_raise()

            with raises:
                assert model.num_communication_qubits_per_ELU(code_distance) == qubits

    class TestNumCommunicationPorts:
        @pytest.mark.parametrize(
            "code_distance, qubits, throws, second_switch_needed",
            [
                (1, 0, True, False),
                (2, 0, True, False),
                (3, 72, False, False),
                (14, 392, False, False),
                (25, 800, False, True),
                (35, 1120, False, True),
                (36, 0, True, False),
                (1000, 0, True, False),
            ],
        )
        def test_num_communication_ports(
            self, code_distance, qubits, throws, second_switch_needed
        ):
            model = DetailedIonTrapModel()
            raises = pytest.raises(ValueError) if throws else do_not_raise()

            with raises:
                assert model.num_communication_ports_per_ELU(code_distance) == (
                    qubits,
                    second_switch_needed,
                )

    class TestFunctionDesignationOfChains:
        @pytest.mark.parametrize(
            "code_distance, computational_qubits, communication_qubits",
            [(10, 200, 280), (30, 1800, 960), (5, 50, 120)],
        )
        def test_functional_designation_of_chains_within_elu(
            self, code_distance, computational_qubits, communication_qubits
        ):
            model = DetailedIonTrapModel()

            assert model.functional_designation_of_chains_within_ELU(code_distance) == (
                code_distance,
                computational_qubits,
                communication_qubits,
            )

    class TestHardwareResourceEstimates:
        @pytest.mark.parametrize(
            "code_distance, qubits, n_logical_qubits, total_time_in_seconds",
            [(5, 120, 10, 15), (10, 280, 1, 1)],
        )
        def test_hardware_resource_estimates(
            self,
            dummy_resource_info,
            qubits,
            code_distance,
            n_logical_qubits,
            total_time_in_seconds,
        ):
            # Given
            resource_info = dummy_resource_info
            resource_info.code_distance = code_distance
            resource_info.n_logical_qubits = n_logical_qubits
            resource_info.total_time_in_seconds = total_time_in_seconds
            model = DetailedIonTrapModel()

            # When
            hw_resource_info = model.get_hardware_resource_estimates(resource_info)

            # Then
            num_computational_qubits_per_elu = 2 * code_distance**2

            assert hw_resource_info == DetailedIonTrapResourceInfo(
                power_consumed_per_elu_in_kilowatts=5,
                num_communication_ports_per_elu=qubits,
                second_switch_per_elu_necessary=False,
                num_communication_qubits_per_elu=qubits,
                num_memory_qubits_per_elu=code_distance,
                num_computational_qubits_per_elu=num_computational_qubits_per_elu,
                num_optical_cross_connect_layers=None,
                num_ELUs_per_optical_cross_connect=None,
                total_num_ions=n_logical_qubits
                * (num_computational_qubits_per_elu + code_distance + qubits),
                total_num_communication_qubits=n_logical_qubits * qubits,
                total_num_memory_qubits=n_logical_qubits * code_distance,
                total_num_computational_qubits=num_computational_qubits_per_elu
                * n_logical_qubits,
                total_num_communication_ports=n_logical_qubits * qubits,
                num_elus=n_logical_qubits,
                total_elu_power_consumed_in_kilowatts=5 * n_logical_qubits,
                total_elu_energy_consumed_in_kilojoules=5
                * n_logical_qubits
                * total_time_in_seconds,
            )
