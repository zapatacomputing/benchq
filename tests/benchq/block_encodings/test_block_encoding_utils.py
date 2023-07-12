import numpy as np
import pytest

from benchq.block_encodings.block_encoding_utils import controlled_clock


@pytest.mark.parametrize(
    "size, direction, target_unitary",
    [
        (1, "forward", np.array([[0, 1], [1, 0]])),
        (1, "backward", np.array([[0, 1], [1, 0]])),
        (
            2,
            "forward",
            np.array([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0]]),
        ),
        (
            2,
            "backward",
            np.array([[0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]),
        ),
        (
            3,
            "forward",
            np.array(
                [
                    [0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0],
                ]
            ),
        ),
    ],
)
def test_bare_clock_produces_correct_output(size, direction, target_unitary):
    circuit = controlled_clock(size, direction=direction)
    test_unitary = circuit.to_unitary()

    assert np.allclose(test_unitary, target_unitary)


@pytest.mark.parametrize(
    "size, targets, controls, target_unitary",
    [
        (
            1,
            [1],
            [0],
            np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]),
        ),
        (
            1,
            [0],
            [1],
            np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]]),
        ),
        (
            1,
            [2],
            [0, 1],
            np.array(
                [
                    [1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 1, 0],
                ]
            ),
        ),
        (
            2,
            [1, 2],
            [0],
            np.array(
                [
                    [1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 1, 0, 0, 0],
                ]
            ),
        ),
        (
            2,
            [0, 1],
            [2],
            np.array(
                [
                    [1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 1, 0, 0, 0, 0, 0, 0],
                ]
            ),
        ),
    ],
)
def test_clock_with_controls_produces_correct_output(
    size, targets, controls, target_unitary
):
    circuit = controlled_clock(size, targets=targets, controls=controls)
    test_unitary = circuit.to_unitary()

    assert np.allclose(test_unitary, target_unitary)
