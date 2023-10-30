from benchq.magic_state_distillation.autoccz_factories import iter_auto_ccz_factories


def test_factory_properties_are_correct():
    for factory in iter_auto_ccz_factories(1e-3):
        assert factory.name[:8] == "AutoCCZ"
        assert factory.distilled_magic_state_error_rate < 1e-3
        assert factory.qubits > 0
        assert factory.distillation_time_in_seconds > 0
        assert factory.n_t_gates_produced_per_distillation == 2
