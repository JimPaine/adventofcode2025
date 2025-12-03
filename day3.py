import os
import pytest


def high_joltage(input_path: str, batteries: int) -> int:
    joltage = 0
    with open(input_path, 'r') as file:
        for line in file:
            joltage += process_bank(line.rstrip('\n'), batteries)
    return joltage


def process_bank(line: str, batteries: int) -> int:
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


@pytest.mark.parametrize("line, batteries, expected", [
    ("987654321111111", 2, 98),
    ("811111111111119", 2, 89),
    ("234234234234278", 2, 78),
    ("818181911112111", 2, 92),
])
def test_process_bank(line: str, batteries: int, expected: int):
    assert process_bank(line, batteries) == expected


def test_high_joltage_example():
    example_path = os.path.join(os.path.dirname(__file__), 'examples/day3')
    joltage = high_joltage(example_path, 2)
    assert joltage == 357


def test_high_joltage_part2_example():
    example_path = os.path.join(os.path.dirname(__file__), 'examples/day3')
    joltage = high_joltage(example_path, 12)
    assert joltage == 3121910778619


def test_high_joltage_input():
    input_path = os.path.join(os.path.dirname(__file__), 'inputs/day3')
    joltage = high_joltage(input_path, 2)
    assert joltage == 17493


def test_high_joltage_part2_input():
    input_path = os.path.join(os.path.dirname(__file__), 'inputs/day3')
    joltage = high_joltage(input_path, 12)
    assert joltage == 173685428989126
