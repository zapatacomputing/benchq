################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
import warnings
from dataclasses import dataclass
from typing import Dict

import numpy as np


@dataclass
class DecoderModel:
    """Class representing decoder model for belief-propagation decoder.

    Most parameters don't have physical interpretations, they are just numerical
    coefficients coming from the fit of the simulation data. Their names come from
    numberical methods used for their calculation.
    The exception is L2, which corresponds to the number of interations of
    belief-propagation.
    """

    power_table: Dict[int, float]
    area_table: Dict[int, float]
    delay_table: Dict[int, float]
    highest_calculated_distance: int = 31

    def power_in_nanowatts(self, distance: int) -> float:
        """Calculates the power (in nW) that it will take to decode the code
        of given distance. Returns infinity if the decoder is not available for
        given distance.

        Args:
            distance: surface code distance.
        """
        return self.power_table.get(distance, invalid_code_distance())

    def area_in_micrometers_squared(self, distance: int) -> float:
        """Calculates the area (in μm^2) that it will take to have a decoder
        which allows to decode code of given distance. Returns infinity if the decoder
        is not available for given distance.

        Args:
            distance: surface code distance.
        """
        return self.area_table.get(distance, invalid_code_distance())

    def delay_in_nanoseconds(self, distance: int) -> float:
        """Calculates the delay (in ns) it will take to decode the code of given
        distance. Returns infinity if the decoder is not available for given distance.

        Args:
            distance: surface code distance.
        """
        return self.delay_table.get(distance, invalid_code_distance())

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
        if data.shape[1] != 4:
            raise ValueError(
                "Data for creating DecoderModel doesn't comply to the required format."
            )
        distances = data[1:, 0]
        delay_table = data[1:, 1]
        area_table = data[1:, 2]
        power_table = data[1:, 3]

        distances = list(distances)
        highest_distance = int(max(distances))

        completed_power_table = {}
        completed_area_table = {}
        completed_delay_table = {}

        for d in range(highest_distance + 1):
            if d not in distances:
                new_d_index = find_next_highest_distance(distances, d)
                completed_power_table[d] = power_table[new_d_index]
                completed_area_table[d] = area_table[new_d_index]
                completed_delay_table[d] = delay_table[new_d_index]
            else:
                d_index = distances.index(d)
                completed_power_table[d] = power_table[d_index]
                completed_area_table[d] = area_table[d_index]
                completed_delay_table[d] = delay_table[d_index]

        return cls(
            completed_power_table,
            completed_area_table,
            completed_delay_table,
            highest_calculated_distance=highest_distance,
        )


def find_next_highest_distance(distances, d):
    """Finds the next highest distance in the list of distances.

    Args:
        distances: list of distances.
        d: distance to compare to.
    """
    for new_d in range(d, int(max(distances)) + 1):
        if new_d in distances:
            return distances.index(new_d)
    raise ValueError("No higher distance found.")


def invalid_code_distance():
    """Returns the delay for invalid code distance."""
    return np.infty
