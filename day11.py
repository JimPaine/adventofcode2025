import os
import pytest
import numpy as np

class Map:
    def __init__(self, raw):
        self.nodes = np.array([])
        self._parse(raw)


    def walk(self, start, end) -> int:
        if start == end:
            return 1

        node = [n for n in self.nodes if n.name == start][0]

        paths = 0
        for child in node.children:
            paths += self.walk(child, end)
 
        return paths


    def _parse(self, raw):
        for row in raw:
            parts = row.split(' ')

            name = str(parts[0][:-1])
            parent = self._try_add(name)

            children = parts[1:]
            parent.add_children(children)

    def _try_add(self, name) -> object:
        if not any(n.name == name for n in self.nodes):
            n = Node(name)
            self.nodes = np.append(self.nodes, [n])
            return n
        return [o for o in self.nodes if o.name == name][0]
        

class Node:
    def __init__(self, name, children = None):
        self.name = name
        self.children = children if children != None else []


    def add_children(self, children: list[str]):
        self.children = np.append(self.children, children)

def _read(path: str) -> list:
    rows = []
    with open(path, 'r') as file:
        for line in file:
            rows.append(line.rstrip('\n'))

    return rows


@pytest.mark.parametrize("path, expected", [
    ("examples/day11", 5),
    ("inputs/day11", 652),
])
def test_measure_part1(path: str, expected: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    raw = _read(absolute_path)
    map = Map(raw)
    paths = map.walk('you', 'out')
    assert paths == expected


@pytest.mark.parametrize("path, expected", [
    ("examples/day11_2", 2),
    ("inputs/day11", 652),
])
def test_measure_part2(path: str, expected: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    raw = _read(absolute_path)
    map = Map(raw)
    paths = map.walk('svr', 'out', ['dac', 'fft'])
    assert paths == expected