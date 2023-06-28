################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
"""Unit tests for benchq.mlflow.data_logging."""

import pytest
from benchq.mlflow.data_logging import _flatten_dict

@pytest.mark.parametrize("input_dict, expected",
    [
    ({"simple": {"a": 1}}, {"simple.a": 1}), 
    ({"double_nest": {"middle": {"inner": 6.28}}}, {"double_nest.middle.inner": 6.28}),
    ({'code_distance': 19,
        'decoder_info': None,
        'extra': {'max_graph_degree': 51,
                    'n_measurement_steps': 81,
                    'n_nodes': 1550,
                    'n_rotation_gates': 0,
                    'n_t_gates': 1546},
        'logical_error_rate': 0.00026020397797732464,
        'n_logical_qubits': 51,
        'n_physical_qubits': 104344,
        'total_time_in_seconds': 950.748,
        'widget_name': '(15-to-1)^6_11,5,5 x (15-to-1)_25,11,11'}, {'code_distance': 19,
        'decoder_info': None,
        'extra.max_graph_degree': 51,
        'extra.n_measurement_steps': 81,
        'extra.n_nodes': 1550,
        'extra.n_rotation_gates': 0,
        'extra.n_t_gates': 1546,
        'logical_error_rate': 0.00026020397797732464,
        'n_logical_qubits': 51,
        'n_physical_qubits': 104344,
        'total_time_in_seconds': 950.748,
        'widget_name': '(15-to-1)^6_11,5,5 x (15-to-1)_25,11,11'})
    ]
)
def test__flatten_dict(input_dict, expected):
    assert _flatten_dict(input_dict) == expected

