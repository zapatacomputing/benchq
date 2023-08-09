################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
"""Unit tests for benchq.mlflow.data_logging."""

from unittest.mock import patch

import pytest

from benchq.data_structures.algorithm_implementation import AlgorithmImplementation
from benchq.data_structures.decoder import DecoderModel
from benchq.data_structures.hardware_architecture_models import IONTrapModel
from benchq.data_structures.resource_info import ResourceInfo
from benchq.mlflow.data_logging import (
    _flatten_dict,
    log_input_objects_to_mlflow,
    log_resource_info_to_mlflow,
)


@pytest.mark.parametrize(
    "input_dict, expected",
    [
        ({"simple": {"a": 1}}, {"simple.a": 1}),
        (
            {"double_nest": {"middle": {"inner": 6.28}}},
            {"double_nest.middle.inner": 6.28},
        ),
        (
            {
                "code_distance": 19,
                "decoder_info": None,
                "extra": {
                    "max_graph_degree": 51,
                    "n_measurement_steps": 81,
                    "n_nodes": 1550,
                    "n_rotation_gates": 0,
                    "n_t_gates": 1546,
                },
                "logical_error_rate": 0.00026020397797732464,
                "n_logical_qubits": 51,
                "n_physical_qubits": 104344,
                "total_time_in_seconds": 950.748,
                "widget_name": "(15-to-1)^6_11,5,5 x (15-to-1)_25,11,11",
            },
            {
                "code_distance": 19,
                "decoder_info": None,
                "extra.max_graph_degree": 51,
                "extra.n_measurement_steps": 81,
                "extra.n_nodes": 1550,
                "extra.n_rotation_gates": 0,
                "extra.n_t_gates": 1546,
                "logical_error_rate": 0.00026020397797732464,
                "n_logical_qubits": 51,
                "n_physical_qubits": 104344,
                "total_time_in_seconds": 950.748,
                "widget_name": "(15-to-1)^6_11,5,5 x (15-to-1)_25,11,11",
            },
        ),
    ],
)
def test__flatten_dict(input_dict, expected):
    assert _flatten_dict(input_dict) == expected


@patch("benchq.mlflow.data_logging.mlflow", autospec=True)
def test_log_input_objects_to_mlflow(mock_mlflow):
    # Given
    test_algo_descrip = AlgorithmImplementation(None, None, 10)

    test_hardware_model = IONTrapModel(0.001, 0.1)

    test_decoder_model = DecoderModel({1: 1.5}, {2: 6.28}, {3: 0.0001}, 31)

    # When
    log_input_objects_to_mlflow(
        test_algo_descrip, "testing algo", test_hardware_model, test_decoder_model
    )

    # Then
    mock_mlflow.log_metric.assert_not_called()
    mock_mlflow.log_metrics.assert_not_called()

    mock_mlflow.log_param.assert_called()
    mock_mlflow.log_param.assert_any_call("n_calls", 10)  # from AlgorithmImplementation
    mock_mlflow.log_param.assert_any_call("algorithm_name", "testing algo")

    mock_mlflow.log_params.assert_called()
    mock_mlflow.log_params.assert_any_call(
        {"physical_qubit_error_rate": 0.001, "surface_code_cycle_time_in_seconds": 0.1}
    )  # from BasicArchitectureModel
    mock_mlflow.log_params.assert_any_call(
        {
            "power_table.1": 1.5,
            "area_table.2": 6.28,
            "delay_table.3": 0.0001,
            "distance_cap": 31,
        }
    )  # from DecoderModel


@patch("benchq.mlflow.data_logging.mlflow", autospec=True)
def test_log_resource_info_to_mlflow(mock_mlflow):
    # Given
    test_resource_info = ResourceInfo(
        code_distance=1,
        logical_error_rate=0.1,
        n_logical_qubits=1,
        n_physical_qubits=1,
        total_time_in_seconds=0.01,
        decoder_info=None,
        widget_name="tau",
        extra=None,
    )

    # When
    log_resource_info_to_mlflow(test_resource_info)

    # Then
    mock_mlflow.log_metric.assert_called()
    mock_mlflow.log_metrics.assert_not_called()
    mock_mlflow.log_param.assert_called()
    mock_mlflow.log_params.assert_not_called()

    mock_mlflow.log_metric.assert_any_call("code_distance", 1)
    mock_mlflow.log_metric.assert_any_call("logical_error_rate", 0.1)

    mock_mlflow.log_param.assert_any_call("decoder_info", "None")
    mock_mlflow.log_param.assert_any_call("widget_name", "tau")
