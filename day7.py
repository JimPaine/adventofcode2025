import os
import pytest
import numpy as np


def _read(path: str) -> list:
    rows = []
    with open(path, 'r') as file:
        for line in file:
            rows.append(list(line.rstrip('\n')))

    return rows


def fire_beam(path: str) -> tuple[int, int]:
    grid = _read(path)

    w = len(grid[0])
    beams = [ grid[0].index('S') ]
    paths = np.zeros(w, dtype=int)

    splits = 0
    paths[beams[0]] = 1
    for i in range(1, w):
        temp_beams = []
        temp_paths = np.zeros(w, dtype=int)

        for b in beams:
            if grid[i][b] == '^':
                temp_beams.extend([b - 1, b + 1])
                temp_paths[b-1] += paths[b]
                temp_paths[b+1] += paths[b]

                splits +=1
            else: 
                temp_beams.append(b)
                temp_paths[b] += paths[b]

        beams = list(set(temp_beams)) if len(temp_beams) > 0 else beams
        paths = temp_paths

    return splits, np.sum(paths)


@pytest.mark.parametrize("path, splits_expected, paths_expected", [
    ("examples/day7", 21, 40),
    ("inputs/day7", 1640, 40999072541589)
])
def test_optimize_forklift_part1(path: str, splits_expected: int, paths_expected: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    splits, paths = fire_beam(absolute_path)
    assert splits == splits_expected
    assert paths == paths_expected
