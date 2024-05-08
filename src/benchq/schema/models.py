################################################################################
# © Copyright 2024 Zapata Computing Inc.
################################################################################
""""This file defines pydantic models to help with serializing logical and physical
resource estimates. They are inspired by but slightly different from the JSON schemas
defined in the QB-Estimate-Reporting repository."""

from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field


class TaskType(StrEnum):
    GROUND_STATE_ENERGY_ESTIMATION = "ground_state_energy_estimation"
    TIME_INDEPENDENT_DYNAMICS = "time_independent_dynamics"
    TIME_DEPENDENT_DYNAMICS = "time_dependent_dynamics"
    LINEAR_SYSTEMS = "linear_system"
    NONLINEAR_DIFFERENTIAL_EQUATION = "nonlinear_differential_equation"


class InstanceCategory(StrEnum):
    SCIENTIFIC = "scientific"
    INDUSTRIAL = "industrial"


class Code(StrEnum):
    SURFACE = "surface"
    OTHER = "other"


class LogicalAbstractResourceEstimate(BaseModel):
    num_qubits: int
    t_count: int
    clifford_count: Optional[int] = None
    gate_count: Optional[int] = None
    circuit_depth: Optional[int] = None
    t_depth: Optional[int] = None


class PhysicalResourceEstimate(BaseModel):
    physical_architecture_description: str
    code_name: Code
    code_distance: int
    runtime: float
    num_qubits: int
    t_count: Optional[int] = None
    num_t_factories: Optional[int] = None
    num_factory_qubits: Optional[int] = None
    gate_count: Optional[int] = None
    circuit_depth: Optional[int] = None
    t_depth: Optional[int] = None
    clifford_count: Optional[int] = None


class Task(BaseModel):
    id: str = Field(description="Unique identifier")
    size: str = Field("Description of instance size (problem specific)")
    task: TaskType = Field("Computational task")
    implementation: str = Field(
        description="Description of implementation, e.g. algorithm / encoding"
    )
    repetitions: int
    logical_abstract: LogicalAbstractResourceEstimate = Field(
        serialization_alias="logical-abstract", description="Abstract logical estimates"
    )
    physical: PhysicalResourceEstimate = Field(
        description="Physical resource estimates"
    )


class ApplicationInstance(BaseModel):
    id: str = Field(description="Unique identifier")
    name: str = Field(description="Application name")
    category: InstanceCategory
    value: float = Field(description="Financial value (dollars)")
    tasks: list[Task]
