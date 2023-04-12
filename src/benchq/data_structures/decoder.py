################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
from csv import reader

import numpy as np


class DecoderModel:
    """Class representing decoder model

    All the fields of the class represent some properties of the decoder model.
    """

    def __init__(
        self,
        power_d_26: float,
        power_ranks: np.ndarray,
        power_sqmat_inv: np.ndarray,
        area_d_26: float,
        area_ranks: np.ndarray,
        area_sqmat_inv: np.ndarray,
        delay_d_26: float,
        delay_ranks: np.ndarray,
        delay_sqmat_inv: np.ndarray,
        L2=10,
    ):
        self.power_d_26 = power_d_26
        self.power_ranks = power_ranks
        self.power_sqmat_inv = power_sqmat_inv
        self.area_d_26 = area_d_26
        self.area_ranks = area_ranks
        self.area_sqmat_inv = area_sqmat_inv
        self.delay_d_26 = delay_d_26
        self.delay_ranks = delay_ranks
        self.delay_sqmat_inv = delay_sqmat_inv
        self.L2 = L2

    def power(self, distance: int) -> float:
        """Calculates the power (in W) that it will take to decode the code
        of given distance.

        Args:
            distance: surface code distance.
        """
        return _get_estimate(
            distance, self.L2, self.power_d_26, self.power_ranks, self.power_sqmat_inv
        )

    def area(self, distance: int) -> float:
        """Calculates the area (in m^2) that it will take to have a decoder
        which allows to decode code of given distance.

        Args:
            distance: surface code distance.
        """
        return _get_estimate(
            distance, self.L2, self.area_d_26, self.area_ranks, self.area_sqmat_inv
        )

    def delay(self, distance: int) -> float:
        """Calculates the delay (in s) it will take to decode the code
        of given distance.

        Args:
            distance: surface code distance.
        """
        return _get_estimate(
            distance, self.L2, self.delay_d_26, self.delay_ranks, self.delay_sqmat_inv
        )

    def error_rate(self, distance: int) -> float:
        """Calculates the error rate of the decoder.

        Args:
            distance: surface code distance.
        """
        return 0

    @classmethod
    def from_csv(cls, file_path):
        """Creates DecoderModel object based on a csv file.
        The csv file should contain 3 rows, for data about power, area and delay.
        Each row should contain 8 values:
        - first corresponds to "d_26"
        - next three are "ranks"
        - last four are "sqmat_inv"

        Args:
            file_path: path of the file containing decoder data.
        """

        data = np.genfromtxt(file_path, delimiter=",")
        if data.shape != (3, 8):
            raise ValueError(
                "Data for creating DecoderModel don't comply to the required format."
            )
        power_d_26 = data[0][0]
        power_ranks = data[0][1:4]
        power_sqmat_inv = data[0][4:8]
        area_d_26 = data[1][0]
        area_ranks = data[1][1:4]
        area_sqmat_inv = data[1][4:8]
        delay_d_26 = data[2][0]
        delay_ranks = data[2][1:4]
        delay_sqmat_inv = data[2][4:8]

        return cls(
            power_d_26,
            power_ranks,
            power_sqmat_inv,
            area_d_26,
            area_ranks,
            area_sqmat_inv,
            delay_d_26,
            delay_ranks,
            delay_sqmat_inv,
        )


def _get_estimate(
    x: float, L2: float, d_26: float, ranks: np.ndarray, sqmat_inv: np.ndarray
) -> float:
    return (
        _d_26_term(x, d_26, L2) + _ranks_term(x, ranks) + _sqmat_inv_term(x, sqmat_inv)
    )


def _polynomial(x: float, coeffs: np.ndarray) -> float:
    return sum(x**i * coeff for i, coeff in enumerate(coeffs))


def _d_26_term(x: float, d_26: float, L2: float) -> float:
    return d_26 / (4 * (x**2 - 1)) * 4 * (x**2 - 1) * L2


def _ranks_term(x: float, ranks: np.ndarray):
    ranks_value = _polynomial(x**2, ranks)
    return (2 * (2 * x * (x - 1) + 1)) * ranks_value


def _sqmat_inv_term(x: float, sqmat_inv: np.ndarray):
    sqmat_inv_value = _polynomial(x**2, sqmat_inv)
    return sqmat_inv_value / 1000
