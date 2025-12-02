import os
import pytest
from days.day1 import decode_password, rotate


def test_decode_password_example():
    example_path = os.path.join(os.path.dirname(__file__), 'examples/day1')
    zeros, clicks = decode_password(example_path)
    assert zeros == 3
    assert clicks == 6


def test_decode_password():
    input_path = os.path.join(os.path.dirname(__file__), 'inputs/day1')
    zero_count, zero_clicks = decode_password(input_path)
    assert zero_count == 1120
    assert zero_clicks == 6554


@pytest.mark.parametrize("pos, moves, dir, expected_pos, expected_clicks", [
    (50, 100, 'R', 50, 1),
    (50, 100, 'L', 50, 1),
    (0, 1, 'L', 99, 0),
    (0, 1, 'R', 1, 0),
    (99, 1, 'R', 0, 1),
    (99, 1, 'L', 98, 0),
    (1, 1, 'L', 0, 1),
    (50, 250, 'R', 0, 3),
    (50, 250, 'L', 0, 3),
    (50, 300, 'L', 50, 3),
    (0, 99, 'L', 1, 0),
    (0, 99, 'R', 99, 0),
    (0, 98, 'L', 2, 0),
    (99, 99, 'R', 98, 1),
    (99, 99, 'L', 0, 1),
    (50, 50, 'R', 0, 1),
    (50, 50, 'L', 0, 1)
])
def test_rotate(
    pos: int, moves: int, dir: str, expected_pos: int, expected_clicks: int
):
    pos, clicks = rotate(pos, moves, dir, 0)
    assert pos == expected_pos
    assert clicks == expected_clicks

@pytest.mark.parametrize("pos, rotations, expected_pos, expected_clicks", [
    (50, [('R', 50), ('L', 50)], 50, 1),
    (0, [('L', 1), ('R', 1)], 0, 1),
    (1, [('L', 99), ('L', 1)], 1, 1),
    (50, [('L', 50), ('L', 1)], 99, 1),
    (50, [('R', 50), ('R', 1)], 1, 1),
    (50, [('R', 50), ('R', 99), ('R', 1)], 0, 2),
])
def test_multiple_rotates(
    pos: int,
    rotations: list[tuple[str, int]],
    expected_pos: int,
    expected_clicks: int
):

    clicks = 0
    for dir, moves in rotations:
        pos, clicks = rotate(pos, moves, dir, clicks)
    assert pos == expected_pos
    assert clicks == expected_clicks
