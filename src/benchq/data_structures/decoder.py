################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
import numpy as np
from csv import reader


class DecoderModel:
    def __init__(
        self,
        power_d_26: float,
        power_ranks: np.ndarray,
        power_sqmat: np.ndarray,
        area_d_26: float,
        area_ranks: np.ndarray,
        area_sqmat: np.ndarray,
        delay_d_26: float,
        delay_ranks: np.ndarray,
        delay_sqmat: np.ndarray,
        L2=10,
    ):
        self.power_d_26 = power_d_26
        self.power_ranks = power_ranks
        self.power_sqmat = power_sqmat
        self.area_d_26 = area_d_26
        self.area_ranks = area_ranks
        self.area_sqmat = area_sqmat
        self.delay_d_26 = delay_d_26
        self.delay_ranks = delay_ranks
        self.delay_sqmat = delay_sqmat
        self.L2 = L2

    def power(self, distance: int):
        return _get_estimate(
            distance, self.L2, self.power_d_26, self.power_ranks, self.power_sqmat
        )

    def area(self, distance: int):
        return _get_estimate(
            distance, self.L2, self.area_d_26, self.area_ranks, self.area_sqmat
        )

    def delay(self, distance: int):
        return _get_estimate(
            distance, self.L2, self.delay_d_26, self.delay_ranks, self.delay_sqmat
        )

    @classmethod
    def from_csv(cls, file_name):
        data = np.genfromtxt(file_name, delimiter=",")
        power_d_26 = data[0][0]
        power_ranks = data[0][1:4]
        power_sqmat = data[0][4:8]
        area_d_26 = data[1][0]
        area_ranks = data[1][1:4]
        area_sqmat = data[1][4:8]
        delay_d_26 = data[2][0]
        delay_ranks = data[2][1:4]
        delay_sqmat = data[2][4:8]

        return cls(
            power_d_26,
            power_ranks,
            power_sqmat,
            area_d_26,
            area_ranks,
            area_sqmat,
            delay_d_26,
            delay_ranks,
            delay_sqmat,
        )


def _get_estimate(
    x: float, L2: float, d_26: float, ranks: np.ndarray, sqmat: np.ndarray
) -> float:
    return _d_26_term(x, d_26, L2) + _ranks_term(x, ranks) + _sqmat_term(x, sqmat)


def _polynomial(x: float, coeffs: np.ndarray) -> float:
    return sum(x**i * coeff for i, coeff in enumerate(coeffs))


def _d_26_term(x: float, d_26: float, L2: float) -> float:
    return d_26 / (4 * (x**2 - 1)) * 4 * (x**2 - 1) * L2


def _ranks_term(x: float, ranks: np.ndarray):
    ranks_value = _polynomial(x**2, ranks)
    return (2 * (2 * x * (x - 1) + 1)) * ranks_value


def _sqmat_term(x: float, sqmat: np.ndarray):
    sqmat_value = _polynomial(x**2, sqmat)
    return sqmat_value / 1000
