import os

import numpy as np
import pytest

from benchq.data_structures import DecoderModel


class TestDecoders:
    def file_path(self, file_name="decoder_test_data.csv"):
        curent_dir = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(curent_dir, file_name)

    def test_create_decoders_from_csv(self):
        decoder = DecoderModel.from_csv(self.file_path())
        assert decoder.power_d_26 == 0.3
        assert len(decoder.power_ranks) == 3
        assert len(decoder.power_sqmat_inv) == 4
        assert decoder.area_d_26 == 15000
        assert len(decoder.area_ranks) == 3
        assert len(decoder.area_sqmat_inv) == 4
        assert decoder.delay_d_26 == 15000
        assert len(decoder.delay_ranks) == 3
        assert len(decoder.delay_sqmat_inv) == 4

    def test_create_decoders_from_csv_throws_exception_for_invalid_data(self):
        file_name = "decoder_test_data_corrupted.csv"
        with pytest.raises(ValueError):
            _ = DecoderModel.from_csv(self.file_path(file_name))

    def test_properties_have_same_formulas(self):
        d_26 = 1
        ranks = np.array([1, 2, 3, 4])
        sqmat = np.array([4, -3, 2, -1])
        L2 = 100
        decoder = DecoderModel(
            d_26, ranks, sqmat, d_26, ranks, sqmat, d_26, ranks, sqmat, L2
        )
        distance = 10
        assert (
            decoder.power(distance) == decoder.area(distance) == decoder.delay(distance)
        )

    def test_decoder_estimates_didnt_change(self):
        decoder = DecoderModel.from_csv(self.file_path())
        distance = 10
        # These tests compare to hardcoded values for a particular set of params
        # at the time of writing these.
        # Their goal is to make sure that we have not accidentally changed the logic.
        # However, it might be that the logic was faulty from the beginning and
        # fixing the logic will make this test fail.
        # In such case it should be edited.
        assert decoder.power(distance) == 30966.8702
        assert decoder.area(distance) == 1126336933.5
        assert decoder.delay(distance) == 323571881.5
