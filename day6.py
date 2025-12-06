import os
import pytest


def _read_input(path: str) -> list:
    lines = []
    with open(path, 'r') as file:
        for line in file:
            lines.append(line.rstrip('\n').split())

    return lines


def maths(path: str, part2: bool) -> int:
    lines = _read_input(path)
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



@pytest.mark.parametrize("path, part2, expected", [
    ("examples/day6", False, 4277556),
    ("examples/day6", True, 3263827),
    ("inputs/day6", False, 4878670269096),
    # ("inputs/day6", True, 0),
])
def test_optimize_forklift_example(path: str, part2: bool, expected: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    result = maths(absolute_path, part2)
    assert result == expected
