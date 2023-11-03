from dataclasses import dataclass


@dataclass
class ErrorBudget:
    """A class that manages the sources of error for the resource estimation.

    Attributes:
        algorithm_failure_tolerance (float): A Failure tolerance which is
            inherent to the algorithm itself. i.e. even if the circuit
            was implemented perfectly, the algorithm would still have a
            probability of failure. Example: grover's algorithm can still
            fail due to limited application of grover diffusion operator,
            even if the operator is implemented without error.
        transpilation_failure_tolerance (float): A failure tolerance which is
            stems from imperfect decomposition of the gates used in the
            algorithm to native gates. Example: decomposing arbitrary
            rotations into Clifford + T.
        hardware_failure_tolerance (float): The failure tolerance
            due to imperfections in the gate implementation which persist
            after error correction. Example: imperfect implementation of
            a circuit at the physical level is 1e-2, but after error
            correction, the failure rate drops to 1e-8. This refers to
            the 1e-8 quantity.
    """

    algorithm_failure_tolerance: float
    transpilation_failure_tolerance: float
    hardware_failure_tolerance: float

    @property
    def total_failure_tolerance(self):
        return (
            self.algorithm_failure_tolerance
            + self.transpilation_failure_tolerance
            + self.hardware_failure_tolerance
        )

    @staticmethod
    def from_weights(
        total_failure_tolerance: float,
        algorithm_failure_weight: int = 1,
        transpilation_failure_weight: int = 1,
        hardware_failure_weight: int = 1,
    ) -> "ErrorBudget":
        """Split the error budget between the three types of errors according to the
        weights.

        Args:
            total_tolerance (float): The total error budget.
            algorithm_failure_weight (int): The weight of the circuit generation error.
            hardware_failure_weight (int): The weight of the error correction error.
            transpilation_failure_weight (int): The weight of the synthesis error.

        Returns:
            ErrorBudget: The error budget split according to the weights.
        """

        total_weights = (
            algorithm_failure_weight
            + hardware_failure_weight
            + transpilation_failure_weight
        )

        algorithm_failure_tolerance = (
            total_failure_tolerance * algorithm_failure_weight / total_weights
        )
        transpilation_failure_tolerance = (
            total_failure_tolerance * transpilation_failure_weight / total_weights
        )
        hardware_failure_tolerance = (
            total_failure_tolerance * hardware_failure_weight / total_weights
        )
        return ErrorBudget(
            algorithm_failure_tolerance,
            transpilation_failure_tolerance,
            hardware_failure_tolerance,
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
