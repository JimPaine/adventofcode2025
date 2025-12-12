
import os
import pytest
import numpy as np

class Map:
    def __init__(self, raw):
        self.nodes = np.array([])
        self._parse(raw)


    def walk(self, start, end) -> int:
        s = [n for n in self.nodes if n.name == start][0]
        paths = s.walk(end)
        return paths


    def _parse(self, raw):
        # parents
        for row in raw:
            parts = row.split(' ')

            name = str(parts[0][:-1])
            _ = self._try_get(name)
        
        # links
        for row in raw:
            parts = row.split(' ')
            parent = self._try_get(parts[0][:-1])
            children = parts[1:]
            nodes = []
            for c in children:
                nodes = np.append(nodes, [self._try_get(c)])
  
            parent.add_children(nodes)


    def _try_get(self, name) -> object:
        if not any(n.name == name for n in self.nodes):
            n = Node(name)
            self.nodes = np.append(self.nodes, [n])
            return n
        return [o for o in self.nodes if o.name == name][0]
        

class Node:
    def __init__(self, name, children = None):
        self.name = name
        self.children = children if children != None else []
        self.exits = 0

    def add_children(self, children: list):
        self.children = np.append(self.children, children)


    def walk(self, end) -> int:
        if self.name == end:
            return 1

        if self.exits != 0:
            return self.exits

        for i, c in enumerate(self.children):
            self.exits += c.walk(end)

        return self.exits


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
    result = map.walk('svr', 'out')

    assert result == expected
