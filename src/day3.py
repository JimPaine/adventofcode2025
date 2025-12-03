import logging
import os
import pytest


def high_joltage(input_path: str) -> int:
    joltage = 0
    with open(input_path, 'r') as file:
        for line in file:
            joltage += process_bank(line)
    return joltage


def process_bank(line: str) -> int:
    largest_value = 0
    largest_index = 0
    line = line.rstrip('\n')

    for i in range(0, len(line) - 1):
        if int(line[i]) > largest_value:
            largest_value = int(line[i])
            largest_index = i

    next_largest = 0

    for i in range(largest_index + 1, len(line)):
        if int(line[i]) > next_largest:
            next_largest = int(line[i])

    return int(f'{largest_value}{next_largest}')


@pytest.mark.parametrize("line, expected", [
    ("123456", 56),
    ("123456\n", 56),
])
def test_process_bank(line: str, expected: int):
    assert process_bank(line) == expected


def test_high_joltage_example():
    example_path = os.path.join(os.path.dirname(__file__), 'examples/day3')
    joltage = high_joltage(example_path)
    assert joltage == 357


def test_high_joltage_input():
    input_path = os.path.join(os.path.dirname(__file__), 'inputs/day3')
    joltage = high_joltage(input_path)
    assert joltage == 357
