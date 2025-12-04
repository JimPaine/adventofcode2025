import logging
import os
import pytest


def decode_password(combination_path: str) -> tuple[int, int]:
    pos = 50
    zeros = 0
    clicks = 0

    logging.info("The dial starts by pointing at 50.")

    with open(combination_path, 'r') as file:
        for line in file:
            pos, clicks = rotate(pos, int(line[1:]), line[0], clicks)
            if pos == 0:
                zeros += 1

    return zeros, clicks


def rotate(pos: int, moves: int, dir: str, clicks: int) -> tuple[int, int]:
    for _ in range(moves):
        pos = (pos + 1) % 100 if dir == 'R' else (pos - 1) % 100

        if pos == 0:
            clicks += 1

    return pos, clicks


@pytest.mark.parametrize("path, expected_zeros, expected_clicks", [
    ("examples/day1", 3, 6),
    ("inputs/day1", 1120, 6554),
])
def test_decode_password(path: str, expected_zeros: int, expected_clicks: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    zeros, clicks = decode_password(absolute_path)
    assert zeros == expected_zeros
    assert clicks == expected_clicks
