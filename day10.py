import os
import pytest
import numpy as np
from collections import deque

MachineState = np.ndarray[tuple[int], np.dtype[np.signedinteger]]

class Machine:

    def __init__(self, raw: str):
        self._parse(raw)
        return None


    def _parse(self, raw: str):
        temp = raw.split(' ')
        self._target_state = np.array([0 if s == '.' else 1 for s in temp[0][1:-1]], dtype='int')
        self._target_joltage = np.array([int(j) for j in temp[-1:][0][1:-1].split(',')], dtype='int')

        raw_buttons = [s[1:-1].split(',') for s in temp[1:-1]]
        self._buttons = [Button(len(self._target_state), b) for b in raw_buttons]


    def _key(self, array: MachineState) -> str:
        return f'{array}'


    def initialize(self) -> int:
        return self._walk(np.zeros(len(self._target_state), dtype='int'), self._target_state)


    def configure_joltage(self) -> int:
        return self._walk(np.zeros(len(self._target_joltage), dtype='int'), self._target_joltage, False)


    def _walk(self, verticies: MachineState, target: MachineState, toggle=True) -> int:
        queue = deque([verticies])
        start_key = self._key(verticies)
        visited = {start_key}

        clicks = {start_key: 0}

        while queue:
            current_state = queue.popleft()
            current_key = self._key(current_state)

            for b in self._buttons:
                next_state = b.click(current_state, toggle)
                next_key = self._key(next_state)

                if next_key in visited:
                    continue

                visited.add(next_key)

                clicks[next_key] = clicks[current_key] + 1
                if np.array_equal(next_state, target):
                    return clicks[self._key(next_state)]

                queue.append(next_state)
        return 0


class Button:

    def __init__(self, size: int, raw: list[str]):
        self._configure_button(size, raw)
        self.known_states = {}


    def _configure_button(self, size: int, switches: list[str]):
        button = np.zeros(size, dtype='int')
        for s in switches:
            button[int(s)] = 1
        self._button = button


    def click(self, current_state: MachineState, toggle: bool) -> MachineState:
        if toggle:
            return np.array(np.array(current_state, dtype='bool') ^ np.array(self._button, dtype='bool'), dtype='int')
        return np.array(current_state, dtype='int') + np.array(self._button, dtype='int')


class Factory:

    def __init__(self, raw: list[str]):
        self.machines = [Machine(m) for m in raw]


    def initialize_machines(self) -> int:
        clicks = 0
        for m in self.machines:
            clicks += m.initialize()
        return clicks


    def configure_joltage(self) -> int:
        clicks = 0
        for m in self.machines:
            clicks += m.configure_joltage()
        return clicks


@pytest.mark.parametrize("path, part1, part2", [
    ("examples/day10", 7, 33),
    ("inputs/day10", 486, 0),
])
def test_initialize_machines(path: str, part1: int, part2: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    raw = _read(absolute_path)
    factory = Factory(raw)
    init_clicks = factory.initialize_machines()
    jolt_clicks = factory.configure_joltage()
    assert init_clicks == part1
    assert jolt_clicks == part2


def _read(path: str) -> list:
    rows = []
    with open(path, 'r') as file:
        for line in file:
            rows.append(line.rstrip('\n'))

    return rows

