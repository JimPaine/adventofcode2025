import copy
import os
import pytest


def _read(path: str) -> list:
    rows = []
    with open(path, 'r') as file:
        for line in file:
            rows.append(list(line.rstrip('\n')))

    return rows


def fire_beam(path: str, part2: bool) -> int:
    grid = _read(path)

    beams = []

    for i in range(len(grid[0])):
        if grid[0][i] == 'S':
            beams = [i]

    splits = 0
    for i in range(1, len(grid)):
        temp_beams = []
        for b in beams:
            if grid[i][b] == '^':
                temp_beams.extend([b - 1, b + 1])
                splits +=1
            else: 
                temp_beams.append(b)

        beams = list(set(temp_beams)) if len(temp_beams) > 0 else beams

    return splits


@pytest.mark.parametrize("path, part2, expected", [
    ("examples/day7", False, 21),
    ("inputs/day7", False, 1640)
])
def test_optimize_forklift_part1(path: str, part2: bool, expected: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    result = fire_beam(absolute_path, part2)
    assert result == expected