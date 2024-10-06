import pytest

from orquestra.quantum.circuits import Circuit

from benchq.compilation.graph_states.compiled_data_structures import (
    CompiledQuantumProgram,
    GSCInfo,
)
from benchq.logical_architecture_modeling.graph_based_logical_architectures import (
    GraphBasedLogicalArchitectureModel,
    TwoRowBusArchitectureModel,
    AllToAllArchitectureModel,
    consume_t_measurements,
)

from benchq.problem_embeddings.quantum_program import QuantumProgram
from benchq.resource_estimators.resource_info import (
    LogicalArchitectureResourceInfo,
    MagicStateFactoryInfo,
)


@pytest.mark.parametrize(
    "gsc_info,optimization,expected_results,logical_architecture_model",
    [
        (
            GSCInfo(
                4,
                2,
                [3, 5],
                [0, 0],
                [0, 0],
            ),
            "Time",
            {
                "number_of_magic_state_factories": 0,
                "number_of_data_qubits": 4,
                "number_of_bus_qubits": 4,
            },
            TwoRowBusArchitectureModel(),
        ),
        (
            GSCInfo(
                5,
                2,
                [3, 5],
                [0, 7],
                [0, 1],
            ),
            "Time",
            {
                "number_of_magic_state_factories": 8,
                "number_of_data_qubits": 5,
                "number_of_bus_qubits": 13,
            },
            TwoRowBusArchitectureModel(),
        ),
        (
            GSCInfo(
                5,
                2,
                [3, 5],
                [0, 7],
                [0, 2],
            ),
            "Space",
            {
                "number_of_magic_state_factories": 1,
                "number_of_data_qubits": 5,
                "number_of_bus_qubits": 6,
            },
            TwoRowBusArchitectureModel(),
        ),
        (
            GSCInfo(
                5,
                2,
                [3, 5],
                [0, 7],
                [0, 2],
            ),
            "Space",
            {
                "number_of_magic_state_factories": 1,
                "number_of_data_qubits": 5,
                "number_of_bus_qubits": 0,
            },
            AllToAllArchitectureModel(),
        ),
    ],
)
def test_get_resource_estimations_for_program_accounts_for_spatial_resources(
    gsc_info, optimization, expected_results, logical_architecture_model
):

    dummy_circuit = Circuit()

    dummy_quantum_program = QuantumProgram(
        [dummy_circuit, dummy_circuit],
        steps=2,
        calculate_subroutine_sequence=lambda x: [0, 1],
    )

    compiled_program = CompiledQuantumProgram.from_program(
        dummy_quantum_program, [gsc_info, gsc_info]
    )

    magic_state_factory = MagicStateFactoryInfo(
        "dummy_msf",
        None,
        None,
        None,
        None,
        1,
    )
    data_and_bus_code_distance = None

    logical_architecture_resource_info = (
        logical_architecture_model.generate_spatial_resource_breakdown(
            compiled_program,
            optimization,
            data_and_bus_code_distance,
            magic_state_factory,
        )
    )

    number_of_magic_state_factories = (
        logical_architecture_resource_info.num_magic_state_factories
    )

    number_of_data_qubits = logical_architecture_resource_info.num_logical_data_qubits

    number_of_bus_qubits = logical_architecture_resource_info.num_logical_bus_qubits

    # Check that the number of magic state factories is correct
    assert (
        number_of_magic_state_factories
        == expected_results["number_of_magic_state_factories"]
    )
    assert number_of_data_qubits == expected_results["number_of_data_qubits"]

    assert number_of_bus_qubits == expected_results["number_of_bus_qubits"]


# Test for the time optimal cycle allocation functionality
@pytest.mark.parametrize(
    "gsc_info,optimization,cycles_per_layer",
    [
        (
            GSCInfo(
                4,
                3,
                [3, 5, 1],
                [0, 7, 1],
                [0, 0, 1],
            ),
            "Time",
            [9 * 3, 9 * 5 + 9 * 2, 27 + 9 * 2 + (27 + 9 * 2) * (30 - 1)],
        ),
        (
            GSCInfo(
                4,
                3,
                [3, 5, 1],
                [0, 7, 1],
                [0, 0, 1],
            ),
            "Space",
            [
                9 * 3,
                9 * 5
                + 9 * 2 * 2 / 2
                + (27 + 9 * 2)
                * ((7 - 2) / 2 + 0.5),  # rounding up due to discrete number of T states
                27
                + 9 * 2 * 2 / 2
                + (27 + 9 * 2)
                * (30 - 1),  # sequential T states for rotations can be parallelized
            ],
        ),
    ],
)
def test_get_qec_cycle_allocation(gsc_info, optimization, cycles_per_layer):

    distillation_time_in_cycles = 27
    t_gates_per_distillation = 2
    n_t_gates_per_rotation = 30
    data_and_bus_code_distance = 9

    dummy_circuit = Circuit()

    def calculate_subroutine_sequence(x):
        return [0, 1]

    dummy_quantum_program = QuantumProgram(
        [dummy_circuit, dummy_circuit],
        steps=2,
        calculate_subroutine_sequence=calculate_subroutine_sequence,
    )

    compiled_program = CompiledQuantumProgram.from_program(
        dummy_quantum_program, [gsc_info, gsc_info]
    )

    magic_state_factory = MagicStateFactoryInfo(
        "dummy_msf",
        None,
        None,
        None,
        distillation_time_in_cycles,
        t_gates_per_distillation,
    )
    logical_architecture_model = GraphBasedLogicalArchitectureModel()
    logical_architecture_resource_info = LogicalArchitectureResourceInfo(
        num_logical_data_qubits=None,
        num_logical_bus_qubits=None,
        data_and_bus_code_distance=data_and_bus_code_distance,
        num_magic_state_factories=1,
        magic_state_factory=magic_state_factory,
    )

    time_allocation = logical_architecture_model.get_qec_cycle_allocation(
        compiled_program,
        optimization,
        logical_architecture_resource_info,
        n_t_gates_per_rotation,
    )

    # Check that the number of cycles is correct
    assert time_allocation.total == sum(cycles_per_layer) * len(
        calculate_subroutine_sequence(0)
    )


@pytest.mark.parametrize(
    "remaining_t_measurements_per_node,n_parallel_t_measurements,expected_output",
    [
        ([3, 2, 1], 1, [2, 2, 1]),
        ([3, 2, 1], 2, [2, 1, 1]),
    ],
)
def test_consume_t_measurements(
    remaining_t_measurements_per_node,
    n_parallel_t_measurements,
    expected_output,
):
    assert (
        consume_t_measurements(
            remaining_t_measurements_per_node, n_parallel_t_measurements
        )
        == expected_output
    )
