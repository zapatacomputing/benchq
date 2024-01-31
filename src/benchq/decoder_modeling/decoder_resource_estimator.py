import warnings
from typing import Optional

from benchq.decoder_modeling.decoder import DecoderModel
from benchq.quantum_hardware_modeling.hardware_architecture_models import (
    BasicArchitectureModel,
)
from benchq.resource_estimators.resource_info import DecoderInfo


def get_decoder_info(
    hw_model,
    decoder_model: Optional[DecoderModel],
    code_distance: int,
    space_time_volume: float,
    n_logical_qubits: int,
) -> Optional[DecoderInfo]:
    if not decoder_model:
        return None
    else:
        speed_limit = get_decoder_distance_limit_due_to_speed(hw_model, decoder_model)
        if code_distance >= decoder_model.highest_calculated_distance:
            warnings.warn(
                f"Code distance {code_distance} is too high to get resource estimates "
                "because resource estimates have not been calculated for "
                f"distances beyond {decoder_model.highest_calculated_distance}.",
                RuntimeWarning,
            )
            return None
        elif code_distance > speed_limit:
            warnings.warn(
                f"Code distance {code_distance} is too high to be decoded "
                "because the decoder is too slow.",
                RuntimeWarning,
            )
            return None
        else:
            decoder_total_energy_in_joules = (
                space_time_volume
                * decoder_model.power_in_nanowatts(code_distance)
                * decoder_model.delay_in_nanoseconds(code_distance)
                * 1e-18
            )
            decoder_power_in_watts = (
                n_logical_qubits
                * decoder_model.power_in_nanowatts(code_distance)
                * 1e-9
            )
            decoder_area = n_logical_qubits * decoder_model.area_in_micrometers_squared(
                code_distance
            )
            max_decodable_distance = min(
                speed_limit,
                decoder_model.highest_calculated_distance,
            )

            return DecoderInfo(
                total_energy_in_joules=decoder_total_energy_in_joules,
                power_in_watts=decoder_power_in_watts,
                area_in_micrometers_squared=decoder_area,
                max_decodable_distance=max_decodable_distance,
            )


def get_decoder_distance_limit_due_to_speed(
    hw_model: BasicArchitectureModel, decoder_model: DecoderModel, min_d=4, max_d=100
) -> int:
    """Find the maximum distance that a decoder can decode before errors from logical
    correction start to build up.

    Args:
        hw_model (BasicArchitectureModel): Architecture model to calculate speed for.
        decoder_model (DecoderModel): Decoder model to calculate speed for.
        min_d (int, optional): Minimum distance to search. Defaults to 4.
        max_d (int, optional): Maximum distance to search. Defaults to 100.

    Returns:
        int: The highest distance that can be decoded with this hardware and decoder.
    """
    # ignore warnings coming from testing high distances
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="Code distance is too high to be decoded.",
            category=RuntimeWarning,
        )

        max_distance = 0
        for distance in range(min_d, max_d):
            time_for_logical_operation = (
                6 * hw_model.surface_code_cycle_time_in_seconds * distance
            )
            if (
                # compensate for delay being in ns
                decoder_model.delay_in_nanoseconds(distance) * 1e-9
                > time_for_logical_operation
            ):
                max_distance = distance - 1
                break

        return max_distance
