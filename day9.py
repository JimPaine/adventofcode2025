import os
import pytest
import itertools
import numpy as np


def _read(path: str) -> list:
    rows = []
    with open(path, 'r') as file:
        for line in file:
            rows.append(list([int(c) for c in line.rstrip('\n').split(',')]))

    return rows


def map_floor(path: str) -> tuple[int, int]:
    floor = _read(path)
    distances = []
    max_x = 0
    max_y = 0
    for x, y in floor:
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    floor_map = [np.zeros(max_x + 1, dtype=bool) for i in range(max_y + 1)]

    for i in range(0, len(floor)):
        p1 = floor[i]
        p2 = floor[i + 1] if i + 1 < len(floor) else floor[0]
        if p1[1] == p2[1]:
            x1, x2 = (p1[0], p2[0]) if p1[0] < p2[0] else (p2[0], p1[0])
            floor_map[p1[1]][x1:x2+1] = 1 
        elif p1[0] == p2[0]:
            y1, y2 = (p1[1], p2[1]) if p1[1] < p2[1] else (p2[1], p1[1])
            for y in range(y1, y2 + 1):
                floor_map[y][p1[0]] = 1

    for y in range(len(floor)):
        for x in range(max_x):
            if floor_map[y][x] == 1:
                for temp_x in range(x + 1, max_x):
                    if floor_map[y][temp_x] == 1:
                        break
                    floor_map[y][temp_x] = 1

    for p1, p2 in itertools.combinations(floor, 2):
        x = (p1[0] - p2[0]) + 1 if p1[0] > p2[0] else (p2[0] - p1[0]) + 1
        y = (p1[1] - p2[1]) + 1 if p1[1] > p2[1] else (p2[1] - p1[1]) + 1 
        distances.append((p1, p2, x * y))

    arr = np.array(distances, dtype=object)
    sort_index = np.argsort([a[2] for a in arr])
    sorted = arr[sort_index]

    max_tiles = 0
    for i in range(len(sorted) - 1, -1, -1):
        p1, p2, d = sorted[i]

        x1, x2 = (p1[0], p2[0]) if p1[0] < p2[0] else (p2[0], p1[0])
        y1, y2 = (p1[1], p2[1]) if p1[1] < p2[1] else (p2[1], p1[1])

        area = floor_map[y1:y2 + 1]
        area = [row[x1:x2 + 1] for row in area]
        if not any(np.isin(0, r) for r in area):
           max_tiles = d
           break 
            
    _, _, d = sorted[-1:][0]
    return d, max_tiles

@pytest.mark.parametrize("path, part1, part2", [
    ("examples/day9", 50, 24),
    ("inputs/day9", 4748769124, 0),
])
def test_measure(path: str, part1: int, part2: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    p1, p2 = map_floor(absolute_path)
    assert p1 == part1
    assert p2 == part2
