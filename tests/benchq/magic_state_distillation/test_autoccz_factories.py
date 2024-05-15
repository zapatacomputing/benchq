from benchq.magic_state_distillation.autoccz_factories import iter_auto_ccz_factories


def test_factory_properties_are_correct():
    for factory in iter_auto_ccz_factories(1e-4):
        assert factory.name[:7] == "AutoCCZ"
        assert factory.distilled_magic_state_error_rate < 1e-4
        assert factory.qubits > 0
        assert factory.distillation_time_in_cycles > 0
        assert factory.t_gates_per_distillation == 2
