import os
import pytest
import numpy as np


def part1(path: str) -> int:
    lines = []
    with open(path, 'r') as file:
        for line in file:
            lines.append(line.rstrip('\n').split())

    problem_count = len(lines[0])
    op_pos = len(lines) - 1
    total = 0

    for x in range(problem_count):
        sub_total = 0
        for y in range(len(lines) - 1):
            if lines[op_pos][x] == '+':
                sub_total += int(lines[y][x])
            else:
                if sub_total == 0:
                    sub_total = 1
                sub_total *= int(lines[y][x])
        total += sub_total
    return total


def part2(path: str) -> int:
    lines = []
    with open(path, 'r') as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    total = 0
    arr = list(zip(*lines))

    sub_total = 0
    op = ''
    for y in range(len(arr)):
       
        n_str = ''.join(arr[y][0:len(arr[y]) - 1]).strip()
        n = 0
        if n_str == '':
            total += sub_total
            sub_total = 0
            op = ''
            continue
        else:
            n = int(n_str)

        if op == '':
            op = arr[y][len(arr[y]) - 1]

        if op == '*':
            if sub_total == 0:
                sub_total = 1
            sub_total *= n
        else:
            sub_total += n

    return total + sub_total


@pytest.mark.parametrize("path, expected", [
    ("examples/day6", 4277556),
    ("inputs/day6", 4878670269096),
])
def test_optimize_forklift_part1(path: str, expected: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    result = part1(absolute_path)
    assert result == expected


@pytest.mark.parametrize("path, expected", [
    ("examples/day6", 3263827),
    ("inputs/day6", 8674740488592),
])
def test_optimize_forklift_part2(path: str, expected: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    result = part2(absolute_path)
    assert result == expected
