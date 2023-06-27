################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
""" Tools for using mlflow to log benchq data """
from mlflow import log_param, log_metric

from benchq.data_structures.resource_info import ResourceInfo
from ..data_structures import (
    AlgorithmImplementation,
    BasicArchitectureModel,
    DecoderModel,
    ResourceInfo,
)
from typing import Optional
from icecream import ic
from dataclasses import asdict


def log_input_objects_to_mlflow(
    algorithm_description: AlgorithmImplementation,
    hardware_model: BasicArchitectureModel,
    decoder_model: Optional[DecoderModel] = None,
):
    """Ingests objects used to define a resource estimation and logs their parameters to mlflow"""
    ic(asdict(algorithm_description))
    ic(asdict(hardware_model))
    if decoder_model is not None:
        ic(decoder_model.__dict__)


def log_resource_info_to_mlflow(resource_info: ResourceInfo):
    """Ingests a ResourceInfo object and logs those values as metrics to mlflow"""
    ic(asdict(resource_info))
    # TODO: how should the dictionaries here be flattened? custom code? or use flatdict?
