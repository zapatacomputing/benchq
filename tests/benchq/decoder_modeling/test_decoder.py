import os

import pytest

from benchq.decoder_modeling import DecoderModel


class TestDecoders:
    def file_path(self, file_name="decoder_test_data.csv"):
        curent_dir = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(curent_dir, file_name)

    def test_create_decoders_from_csv_throws_exception_for_invalid_data(self):
        file_name = "decoder_test_data_corrupted.csv"
        with pytest.raises(ValueError):
            _ = DecoderModel.from_csv(self.file_path(file_name))

    def test_decoder_estimates_didnt_change(self):
        decoder = DecoderModel.from_csv(self.file_path())
        distance = 10
        # These tests compare to hardcoded values for a particular set of params
        # at the time of writing these.
        # Their goal is to make sure that we have not accidentally changed the logic.
        # However, it might be that the logic was faulty from the beginning and
        # fixing the logic will make this test fail.
        # In such case it should be edited.
        assert decoder.delay_in_nanoseconds(distance) == 5.0
        assert decoder.area_in_micrometers_squared(distance) == 500.0
        assert decoder.power_in_nanowatts(distance) == 50000.0
