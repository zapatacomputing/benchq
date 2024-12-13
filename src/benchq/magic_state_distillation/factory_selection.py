from decimal import Decimal
from typing import Iterable, Union

from ..resource_estimators.resource_info import MagicStateFactoryInfo


def find_optimal_factory(
    per_t_gate_failure_tolerance: Union[float, Decimal],
    magic_state_factory_iterator: Iterable[MagicStateFactoryInfo],
    optimization: str = "Time",
) -> Union[MagicStateFactoryInfo, None]:
    """Find the optimal factory from a given iterator of factories based on
        the optimization criteria.
    Args:
        per_t_gate_failure_tolerance (float): The maximum error rate per
            T-gate that is acceptable.
        magic_state_factory_iterator (Iterable[MagicStateFactoryInfo]):
            An iterator of MagicStateFactoryInfo objects.
        optimization (str): The optimization criteria. Either "Time" or "Space".
    Returns:
        MagicStateFactoryInfo: The optimal factory based on the optimization
            criteria.
    """
    best_found_factory = None
    min_resource = float("inf")
    for factory in magic_state_factory_iterator:
        if factory.distilled_magic_state_error_rate <= per_t_gate_failure_tolerance:
            if optimization == "Space":
                qubits_per_t_gtate = factory.qubits / factory.t_gates_per_distillation
                if qubits_per_t_gtate < min_resource:
                    best_found_factory = factory
                    min_resource = qubits_per_t_gtate
            elif optimization == "Time":
                cycles_per_t_state = (
                    factory.distillation_time_in_cycles
                    / factory.t_gates_per_distillation
                )
                if cycles_per_t_state < min_resource:
                    best_found_factory = factory
                    min_resource = cycles_per_t_state
            else:
                raise ValueError(
                    f"Unknown optimization: {optimization}. "
                    f"Should be either 'Time' or 'Space'."
                )
    return best_found_factory
