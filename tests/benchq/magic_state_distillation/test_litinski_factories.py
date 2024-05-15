import dataclasses
from dataclasses import replace

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
        DetailedIonTrapModel(),
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
        assert factory.t_gates_per_distillation >= 1


def test_factory_based_on_err_rate():
    ion = BASIC_ION_TRAP_ARCHITECTURE_MODEL
    cs = BASIC_SC_ARCHITECTURE_MODEL
    cs = replace(cs, physical_qubit_error_rate=1e-4)

    assert iter_litinski_factories(cs) == iter_litinski_factories(ion)
