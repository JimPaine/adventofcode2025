import os
import pytest
import itertools
import numpy as np
from shapely import make_valid
from shapely.geometry import Polygon


def _read(path: str) -> list:
    rows = []
    with open(path, 'r') as file:
        for line in file:
            rows.append(list([int(c) for c in line.rstrip('\n').split(',')]))

    return rows


def map_floor(path: str) -> tuple[int, int]:
    floor = _read(path)
    distances = []

    for p1, p2 in itertools.combinations(floor, 2):
        x = (p1[0] - p2[0]) + 1 if p1[0] > p2[0] else (p2[0] - p1[0]) + 1
        y = (p1[1] - p2[1]) + 1 if p1[1] > p2[1] else (p2[1] - p1[1]) + 1 
        distances.append((p1, p2, x * y))

    arr = np.array(distances, dtype=object)
    sort_index = np.argsort([a[2] for a in arr])
    sorted = arr[sort_index]

    max_tiles = 0
    points = [(x,y) for x, y in floor]
    poly = Polygon(points)
    for i in range(len(sorted) - 1, -1, -1):
        p1, p2, d = sorted[i]
        coords = [(p1[0], p1[1]), (p2[0], p2[1]),(p2[0], p1[1]), (p1[0], p2[1])]
        p = Polygon(coords)
        p.buffer(0)
        valid_p = make_valid(p)
        if poly.covers(valid_p):
            max_tiles = d
            break 
            
    _, _, d = sorted[-1:][0]
    return d, max_tiles

@pytest.mark.parametrize("path, part1, part2", [
    ("examples/day9", 50, 24),
    ("inputs/day9", 4748769124, 1525991432),
])
def test_measure(path: str, part1: int, part2: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    p1, p2 = map_floor(absolute_path)
    assert p1 == part1
    assert p2 == part2
