import os
import pytest
import numpy as np
import itertools
from collections import defaultdict


def _read(path: str) -> list:
    rows = []
    with open(path, 'r') as file:
        for line in file:
            rows.append(list([int(c) for c in line.rstrip('\n').split(',')]))

    return rows


def measure(path: str, cables: int, part2: bool) -> int:
    points = _read(path)
    distances = []

    for p1, p2 in itertools.combinations(points, 2):
        # Euclidean Distance
        distance = np.sum((np.array(p1)-np.array(p2))**2)
        distances.append((p1, p2, distance))
    
    arr = np.array(distances, dtype=object)
    sort_index = np.argsort([a[2] for a in arr])
    sorted = arr[sort_index]

    pairs = [[tuple(o[0]), tuple(o[1])] for o in sorted]
    nodes = {tuple(p):tuple(p) for p in points}

    circuits = defaultdict(int) 
    patches = range(cables) if not part2 else range(len(pairs))
    keep_patching = True
    while keep_patching:
        keep_patching = part2
        for c in patches:
            p1, p2 = pairs[c]

            if get_root(nodes, p1) == get_root(nodes, p2):
                continue

            set_parent(nodes, p1, p2)

            if part2 and all(get_root(nodes, tuple(points[0])) == get_root(nodes, tuple(p)) for p in points):
                keep_patching = False
                x1, _, _ = p1
                x2, _, _ = p2
                return x1 * x2

    for node in nodes.values():
        root = get_root(nodes, node)
        circuits[root] += 1

    sorted_sizes = list(circuits.values())
    sorted_sizes.sort()
    result = 1
    for s in sorted_sizes[-3:]:
        result *= s 
    return result


def get_root(nodes: dict[tuple, tuple], p: tuple):
    if nodes[p] == p:
        return p

    nodes[p] = get_root(nodes, nodes[p])
    return nodes[p]


def set_parent(nodes: dict[tuple, tuple], p1: tuple, p2: tuple):
    parent = get_root(nodes, p1)
    child = get_root(nodes, p2)
    nodes[parent] = child


@pytest.mark.parametrize("path, cables, part2, expected", [
    ("examples/day8", 10, False, 40),
    ("inputs/day8", 1000, False, 26400),
    ("examples/day8", -1, True, 25272),
    ("inputs/day8", -1, True, 8199963486),

])
def test_measure(path: str, cables: int, part2: bool, expected: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    result = measure(absolute_path, cables, part2)
    assert result == expected
