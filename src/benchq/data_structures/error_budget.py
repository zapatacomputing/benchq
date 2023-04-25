from dataclasses import dataclass


@dataclass
class ErrorBudget:
    """Data structure which holds the error budget that should be used for
    a resource estimation.

    Attributes:
        ultimate_failure_tolerance: The total budget for the resource estimation
            - i.e. what is the maximum error rate that is allowed for running
            the all the calculations.
        circuit_generation_weight: The weight of the failure tolerance associated
            with circuit generation.
        synthesis_weight: The weight of the failure tolerance associated
            with gate synthesis.
        ec_weight: The weight of the failure tolerance associated
            with error correction.
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
