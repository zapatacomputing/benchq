from benchq.data_structures import DecoderModel
import os
import numpy as np


class TestDecoders:
    def file_path(self):
        curent_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = "decoders_data_test.csv"
        return os.path.join(curent_dir, file_name)

    def test_create_decoders_from_csv(self):
        decoder = DecoderModel.from_csv(self.file_path())
        assert decoder.power_d_26 == 0.3
        assert len(decoder.power_ranks) == 3
        assert len(decoder.power_sqmat) == 4
        assert decoder.area_d_26 == 15000
        assert len(decoder.area_ranks) == 3
        assert len(decoder.area_sqmat) == 4
        assert decoder.delay_d_26 == 15000
        assert len(decoder.delay_ranks) == 3
        assert len(decoder.delay_sqmat) == 4

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
