import warnings
from typing import Optional

from benchq.data_structures.decoder import DecoderModel
from benchq.data_structures.resource_info import DecoderInfo


def get_decoder_info(
    hw_model,
    decoder_model: Optional[DecoderModel],
    code_distance: int,
    space_time_volume: float,
    n_logical_qubits: int,
):
    # get decoder requirements
    if decoder_model and decoder_model.distance_cap >= code_distance:
        decoder_total_energy_consumption = (
            space_time_volume
            * decoder_model.power(code_distance)
            * decoder_model.delay(code_distance)
        )
        decoder_power = 2 * n_logical_qubits * decoder_model.power(code_distance)
        decoder_area = n_logical_qubits * decoder_model.area(code_distance)
        max_decodable_distance = find_max_decodable_distance(hw_model, decoder_model)
        decoder_info = DecoderInfo(
            total_energy_consumption=decoder_total_energy_consumption,
            power=decoder_power,
            area=decoder_area,
            max_decodable_distance=max_decodable_distance,
        )
    else:
        if decoder_model and decoder_model.distance_cap < code_distance:
            warnings.warn(
                f"Code distance {code_distance} is too high to be decoded. "
                f"Using decoder data with max distance {decoder_model.distance_cap}."
            )
        decoder_info = None

    return decoder_info


def find_max_decodable_distance(hw_model, decoder_model, min_d=4, max_d=100):
    max_distance = 0
    for distance in range(min_d, max_d):
        time_for_logical_operation = (
            6 * hw_model.surface_code_cycle_time_in_seconds * distance
        )
        # compensate for delay being in ns
        if decoder_model.delay(distance) * 1e-9 < time_for_logical_operation:
            max_distance = distance

    return max_distance
