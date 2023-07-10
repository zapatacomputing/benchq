################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
""" Tools for using mlflow to log benchq data """
import mlflow
from benchq.data_structures.resource_info import ResourceInfo
from ..data_structures import (
    AlgorithmImplementation,
    BasicArchitectureModel,
    DecoderModel,
    ResourceInfo,
)
from typing import Optional, Dict, Any
from dataclasses import asdict
from numbers import Number


def log_input_objects_to_mlflow(
    algorithm_description: AlgorithmImplementation,
    algorithm_name: str,
    hardware_model: BasicArchitectureModel,
    decoder_model: Optional[DecoderModel] = None,
):
    """Ingests objects used to define a resource estimation and logs their parameters to mlflow"""
    # Sometimes the algorithm description has a None as a value, which causes problem if we try to log it
    for algo_key, algo_value in _flatten_dict(asdict(algorithm_description)).items():
        if algo_value is not None:
            mlflow.log_param(algo_key, algo_value)
        else:
            mlflow.log_param(algo_key, "None")

    mlflow.log_param("algorithm_name", algorithm_name)

    mlflow.log_params(_flatten_dict(asdict(hardware_model)))

    # because decoder model is optional, check to make sure it exists
    if decoder_model is not None:
        mlflow.log_params(_flatten_dict(asdict(decoder_model)))
    else:
        mlflow.log_param("decoder_model", "None")


def log_resource_info_to_mlflow(resource_info: ResourceInfo):
    """Ingests a ResourceInfo object and logs those values as metrics to mlflow"""
    flat_resource_dict = _flatten_dict(asdict(resource_info))
    for key, value in flat_resource_dict.items():
        if isinstance(value, Number):
            mlflow.log_metric(key, value)
        elif value is not None:
            mlflow.log_param(key, value)
        elif value is None:
            mlflow.log_param(key, "None")


def _flatten_dict(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Function to take in a dictionary and flatten it, separating with `:`s"""
    result = {}
    for key, value in input_dict.items():
        if isinstance(value, dict):
            for new_key, new_value in _flatten_dict(value).items():
                result[f"{key}.{new_key}"] = new_value
        else:
            result[key] = value
    return result
