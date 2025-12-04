import os
import pytest


def high_joltage(input_path: str, batteries: int) -> int:
    joltage = 0
    with open(input_path, 'r') as file:
        for line in file:
            joltage += _process_bank(line.rstrip('\n'), batteries)
    return joltage


def _process_bank(line: str, batteries: int) -> int:
    idx = 0
    joltage = ''

    for b in range(batteries):
        v, p = _get_next_largest(line, idx, len(line) - (batteries - 1 - b))
        joltage = f'{joltage}{v}'
        idx = p + 1

    return int(joltage)


def _get_next_largest(line: str, s: int, e: int) -> tuple[int, int]:
    value = 0
    index = 0

    for i in range(s, e):
        if int(line[i]) > value:
            value = int(line[i])
            index = i

    return value, index


@pytest.mark.parametrize("path, batteries, expected", [
    ("examples/day3", 2, 357),
    ("inputs/day3", 2, 17493),
    ("examples/day3", 12, 3121910778619),
    ("inputs/day3", 12, 173685428989126),
])
def test_high_joltage(path: str, batteries: int, expected: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    joltage = high_joltage(absolute_path, batteries)
    assert joltage == expected
