################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
""" Tools for using mlflow to log benchq data """
from dataclasses import asdict
from logging import getLogger
from numbers import Number
from typing import Any, Callable, Dict, Optional

import mlflow  # type: ignore

from ..algorithms.data_structures import AlgorithmImplementation
from ..decoder_modeling import DecoderModel
from ..quantum_hardware_modeling import BasicArchitectureModel
from ..resource_estimators.resource_info import ResourceInfo


def log_input_objects_to_mlflow(
    algorithm_implementation: AlgorithmImplementation,
    algorithm_name: str,
    hardware_model: BasicArchitectureModel,
    decoder_model: Optional[DecoderModel] = None,
) -> None:
    """Ingests objects used to define a resource estimation
    and logs their parameters to mlflow
    """
    # Sometimes the algorithm implementation has a None as a value,
    #   which causes problem if we try to log it
    for algo_key, algo_value in _flatten_dict(asdict(algorithm_implementation)).items():
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


def log_resource_info_to_mlflow(resource_info: ResourceInfo) -> None:
    """Ingests a ResourceInfo object and logs those values as metrics to mlflow"""
    flat_resource_dict = _flatten_dict(asdict(resource_info))
    for key, value in flat_resource_dict.items():
        if isinstance(value, Number):
            mlflow.log_metric(key, value)
        elif value is not None:
            mlflow.log_param(key, value)
        elif value is None:
            mlflow.log_param(key, "None")


def create_mlflow_scf_callback(
    mlflow_client: mlflow.client.MlflowClient,
    run_id: str,
) -> Callable[[Any], None]:
    """
    Callback function for pySCF calculations that also logs to mlflow

    In order to make logging to mlflow in parallel work (for instance, parallel
    Orquestra tasks), we need to have started an mlflow Client and a run associated
    with that client that can be passed in.
    For an example of creating the mlflow_client and run_id, see _run_pyscf()
    in MolecularHamiltonianGenerator
    """

    def scf_callback(vars):
        logger = getLogger(__name__)
        data = {
            "last_hf_e": vars.get("last_hf_e"),
            "norm_gorb": vars.get("norm_gorb"),
            "norm_ddm": vars.get("norm_ddm"),
            "cond": vars.get("cond"),
            "cput0_0": vars.get("cput0")[0],
            "cput0_1": vars.get("cput0")[1],
        }
        logger.info(str(data))
        for key, val in data.items():
            mlflow_client.log_metric(run_id, key, val)

    return scf_callback


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
