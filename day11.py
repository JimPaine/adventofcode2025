
import os
import pytest
import numpy as np
import asyncio

class Map:
    def __init__(self, raw):
        self.nodes = np.array([])
        self._parse(raw)


    async def walk(self, start, end, visited_dac = True, visited_fft = True) -> int:
        s = [n for n in self.nodes if n.name == start][0]
        return await s.walk(end, visited_dac, visited_fft)


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
        self.parents = []
        self.visits_dac = False
        self.visits_fft = False
    

    def add_children(self, children: list):
        self.children = np.append(self.children, children)
        for c in children:
            if len([p for p in c.parents if p.name == self.name]) == 0:
                c.parents.append(self)
            if c.name == 'dac':
                c.set_dac()
            elif c.name == 'fft':
                c.set_fft()

    def set_dac(self):
        self.visits_dac = True
        for p in self.parents:
            p.set_dac()


    def set_fft(self):
        self.visits_fft = True
        for p in self.parents:
            p.set_fft()


    async def walk(self, end, visited_dac = False, visited_fft = False) -> int:
        if self.name == end and visited_dac and visited_fft:
            return 1
        elif self.name == end and end == 'dac':
            return 1
        elif self.name == end and end == 'fft':
            return 1
        elif self.name == end:
            return 0

        dac = True if self.name == 'dac' else visited_dac
        fft = True if self.name == 'fft' else visited_fft
        # if self.exits != 0 and visited_dac and visited_fft:
        #     return self.exits
        # else: 
        #     self.exits = 0

        tasks = []
        for c in self.children:
            if self.visits_dac and self.visits_fft:
                tasks.append(c.walk(end, dac, fft))
            elif visited_dac and visited_fft:
                tasks.append(c.walk(end, dac, fft))
            elif self.visits_dac and visited_fft:
                tasks.append(c.walk(end, dac, fft))
            elif visited_dac and self.visits_fft:
                tasks.append(c.walk(end, dac, fft))
        
        return np.sum(await asyncio.gather(*tasks))

def _read(path: str) -> list:
    rows = []
    with open(path, 'r') as file:
        for line in file:
            rows.append(line.rstrip('\n'))

    return rows


@pytest.mark.asyncio
@pytest.mark.parametrize("path, expected", [
    ("examples/day11", 5),
    ("inputs/day11", 652),
])
async def test_measure_part1(path: str, expected: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    raw = _read(absolute_path)
    map = Map(raw)
    paths = await map.walk('you', 'out')
    assert paths == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("path, expected", [
    ("examples/day11_2", 2),
    ("inputs/day11", 652),
])
async def test_measure_part2(path: str, expected: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    raw = _read(absolute_path)
    map = Map(raw)
    # result = map.walk('svr', 'out', False, False) 
    c = await map.walk('dac', 'out', True, True)
    b = await map.walk('fft', 'dac')
    a = await map.walk('svr', 'fft')
    z = await map.walk('fft', 'out', True, True)
    y = await map.walk('dac', 'fft') 
    x = await map.walk('svr', 'dac')

    assert (a * b * c) + (x * y * z) == expected
