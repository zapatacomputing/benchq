from dataclasses import dataclass


@dataclass
class ErrorBudget:
    circuit_generation_failure_tolerance: float
    synthesis_failure_tolerance: float
    ec_failure_tolerance: float

    @property
    def total_failure_tolerance(self):
        return (
            self.circuit_generation_failure_tolerance
            + self.synthesis_failure_tolerance
            + self.ec_failure_tolerance
        )

    @staticmethod
    def from_weights(
        total_failure_tolerance: float,
        circuit_generation_weight: int = 1,
        ec_weight: int = 1,
        synthesis_weight: int = 1,
    ) -> "ErrorBudget":
        """Split the error budget between the three types of errors according to the
        weights.

        Args:
            total_tolerance (float): The total error budget.
            circuit_generation_weight (int): The weight of the circuit generation error.
            ec_weight (int): The weight of the error correction error.
            synthesis_weight (int): The weight of the synthesis error.

        Returns:
            ErrorBudget: The error budget split according to the weights.
        """

        total_weights = circuit_generation_weight + ec_weight + synthesis_weight

        circuit_generation_failure_tolerance = (
            total_failure_tolerance * circuit_generation_weight / total_weights
        )
        synthesis_failure_tolerance = (
            total_failure_tolerance * synthesis_weight / total_weights
        )
        ec_failure_tolerance = total_failure_tolerance * ec_weight / total_weights
        return ErrorBudget(
            circuit_generation_failure_tolerance,
            synthesis_failure_tolerance,
            ec_failure_tolerance,
        )

    @staticmethod
    def from_even_split(total_failure_tolerance: float) -> "ErrorBudget":
        """Evenly split the error budget between the three types of errors.

        Args:
            total_tolerance (float): The total error budget

        Returns:
            ErrorBudget: The error budget split evenly between the three types of errors
        """
        return ErrorBudget.from_weights(total_failure_tolerance, 1, 1, 1)
