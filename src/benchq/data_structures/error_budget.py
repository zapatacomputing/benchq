from dataclasses import dataclass


@dataclass
class ErrorBudget:
    """_summary_

    Returns:
        _description_
    """

    ultimate_failure_tolerance: float
    circuit_generation_weight: float = 1
    synthesis_weight: float = 1
    ec_weight: float = 1

    @property
    def total_weights(self):
        return self.circuit_generation_weight + self.synthesis_weight + self.ec_weight

    @property
    def circuit_generation_failure_tolerance(self):
        return (
            self.ultimate_failure_tolerance
            * self.circuit_generation_weight
            / self.total_weights
        )

    @property
    def synthesis_failure_tolerance(self):
        return (
            self.ultimate_failure_tolerance * self.synthesis_weight / self.total_weights
        )

    @property
    def ec_failure_tolerance(self):
        return self.ultimate_failure_tolerance * self.ec_weight / self.total_weights
