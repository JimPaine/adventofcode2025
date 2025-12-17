import os
import pytest
import numpy as np
from collections import deque

class Machine:
    
    def __init__(self, raw: str):
        self._parse(raw)
        return None


    def _parse(self, raw: str):
        temp = raw.split(' ')
        self._target_state = np.array([False if s == '.' else True for s in temp[0][1:-1]])
        self.indicator_lights = np.array([False for _ in range(len(self._target_state))])

        raw_buttons = [s[1:-1].split(',') for s in temp[1:-1]]
        self._buttons = [Button(len(self._target_state), b) for b in raw_buttons]

    def _key(self, array: np.array) -> tuple:
        return (array.dtype.str, array.shape, f'{array}')

    def initialize(self) -> int:
        queue = deque([self.indicator_lights])
        start_key = self._key(self.indicator_lights)
        visited = {start_key}

        clicks = {start_key: 0}

        while queue:
            current_state = queue.popleft()
            current_key = self._key(current_state)

            for b in self._buttons:
                next_state = b.click(current_state)
                next_key = self._key(next_state)

                if next_key in visited:
                    continue

                visited.add(next_key)

                clicks[next_key] = clicks[current_key] + 1
                if np.array_equal(next_state, self._target_state):
                    return clicks[self._key(next_state)]

                queue.append(next_state)
        return 0


class Button:

    def __init__(self, size: int, raw: str):
        self._configure_button(size, raw)
        self.known_states = {}


    def _configure_button(self, size: int, switches: list):
        button = [False for _ in range(size)]
        for s in switches:
            button[int(s)] = True # can I use 0s and 1s and still do bit ops
        self._button = button


    def click(self, current_state: list) -> list:
        return np.array(current_state) ^ np.array(self._button)


class Factory:
    
    def __init__(self, raw: str):
        self.machines = [Machine(m) for m in raw]


    def initialize_machines(self) -> int:
        clicks = 0
        for m in self.machines:
            clicks += m.initialize()
        return clicks 


@pytest.mark.parametrize("path, expected", [
    ("examples/day10", 7),
    ("inputs/day10", 486),
])
def test_initialize_machines(path: str, expected: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    raw = _read(absolute_path)
    factory = Factory(raw)
    result = factory.initialize_machines()
    assert result == expected


def _read(path: str) -> list:
    rows = []
    with open(path, 'r') as file:
        for line in file:
            rows.append(line.rstrip('\n'))

    return rows

