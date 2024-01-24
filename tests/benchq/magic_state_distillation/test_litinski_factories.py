import pytest

from benchq.magic_state_distillation.litinski_factories import iter_litinski_factories
from benchq.quantum_hardware_modeling.hardware_architecture_models import (
    BASIC_ION_TRAP_ARCHITECTURE_MODEL,
    BASIC_SC_ARCHITECTURE_MODEL,
    DetailedIonTrapModel,
)


@pytest.mark.parametrize(
    "architecture_model",
    [
        BASIC_ION_TRAP_ARCHITECTURE_MODEL,
        BASIC_SC_ARCHITECTURE_MODEL,
    ],
)
def test_factory_properties_are_correct(architecture_model):
    for factory in iter_litinski_factories(architecture_model):
        assert (
            factory.distilled_magic_state_error_rate
            < architecture_model.physical_qubit_error_rate
        )
        assert factory.qubits > 0
        assert factory.distillation_time_in_cycles > 0
        assert factory.n_t_gates_produced_per_distillation >= 1
