import os
import pytest
import numpy as np

class Map:
    def __init__(self, raw):
        self.nodes = np.array([])
        self._parse(raw)


    def walk(self, start, end) -> int:
        s = [n for n in self.nodes if n.name == start][0]
        return s.walk(end)


    def _parse(self, raw):
        for row in raw:
            parts = row.split(' ')
            
            children = parts[1:]
            nodes = []
            for c in children:
                nodes = np.append(nodes, [self._try_add(c)])
 
            name = str(parts[0][:-1])
            parent = self._try_add(name)
            parent.add_children(nodes)

            x = 1

    
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
        self.exits = -1

    def add_children(self, children: list):
        self.children = np.append(self.children, children)

    def walk(self, end) -> int:
        if self.name == end:
            return 1

        if self.exits != -1:
            return self.exits

        exits = 0
        for c in self.children:
            exits += c.walk(end)

        self.exits = exits
        return self.exits


def _read(path: str) -> list:
    rows = []
    with open(path, 'r') as file:
        for line in file:
            rows.append(line.rstrip('\n'))

    return rows


@pytest.mark.parametrize("path, part1", [
    ("examples/day11", 5),
    ("inputs/day11", 652),
])
def test_measure(path: str, part1):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    raw = _read(absolute_path)
    map = Map(raw)
    count = map.walk('you', 'out')
    assert count == part1
