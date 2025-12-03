import logging
import os


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
