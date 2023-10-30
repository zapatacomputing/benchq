from benchq.magic_state_distillation.litinski_factories import iter_litinski_factories
from benchq.data_structures.hardware_architecture_models import (
    DetailedIonTrapModel,
    SCModel,
    IONTrapModel,
)
import pytest


@pytest.mark.parametrize(
    "model",
    [DetailedIonTrapModel, SCModel, IONTrapModel],
)
def test_factory_properties_are_correct(architecture_model):
    for factory in iter_litinski_factories(architecture_model):
        assert (
            factory.distilled_magic_state_error_rate
            < architecture_model.physical_qubit_error_rate
        )
        assert factory.qubits > 0
        assert factory.distillation_time_in_seconds > 0
        assert factory.n_t_gates_produced_per_distillation >= 1
