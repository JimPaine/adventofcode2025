import os
import pytest
import numpy as np
from collections import deque

MachineState = np.ndarray[tuple[int], np.dtype[np.signedinteger]]

class Machine:

    def __init__(self, raw: str):
        self._parse(raw)


    def _parse(self, raw: str):
        temp = raw.split(' ')
        self._target_state = np.array([0 if s == '.' else 1 for s in temp[0][1:-1]], dtype='int')
        self._target_joltage = np.array([int(j) for j in temp[-1:][0][1:-1].split(',')], dtype='int')

        raw_buttons = [s[1:-1].split(',') for s in temp[1:-1]]
        self._buttons = [Button(len(self._target_state), b) for b in raw_buttons]

        self._free_variables = []
        self._depends = []
        self._build_augmented_matrix()


    def _build_augmented_matrix(self):
        x = len(self._buttons)

        self._aug_matrix = [[0.0 for _ in range(x + 1)] for _ in range(len(self._target_joltage))]

        for i, button in enumerate(self._buttons):
            for j, switch in enumerate(button.flipped_switches):
                self._aug_matrix[j][i] = float(switch)

        for i, jolt in enumerate(self._target_joltage):
            self._aug_matrix[i][x] = float(jolt)


    def _key(self, array: MachineState) -> str:
        return f'{array}'

    def initialize(self) -> int:
        verticies = np.zeros(len(self._target_state), dtype='int')
        target = self._target_state
        queue = deque([verticies])
        start_key = self._key(verticies)
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
                if np.array_equal(next_state, target):
                    return clicks[self._key(next_state)]

                queue.append(next_state)
        return 0

    def configure_joltage(self) -> int:
        self._gaussian_elimination()
        return self._walk(0, np.zeros(len(self._free_variables), dtype=float))

    def _check(self, values: list[float]) -> int:
        total = sum(values)
        for r in range(len(self._depends)):
            v = self._aug_matrix[r][len(self._buttons)]
            for i, c in enumerate(self._free_variables):
                v -= self._aug_matrix[r][c] * values[i]

            r = round(v)
            if v < -1e-12 or abs(v - r) > 1e-12:
               return None

            total += int(r)
        return total

    def _walk(self, index: int, values, min=100000.0) -> int:
        if index == len(self._free_variables):
            r = self._check(values)
            return r if r != None and r < min else min 

        n = sum(values[:index])
        for v in range(np.max(self._target_joltage)):
            if n + v >= min:
                break
            values[index] = v
            min = self._walk(index + 1, values, min)
        values[index] = 0
        return min

    def _gaussian_elimination(self):
        pivot = 0
        cols = len(self._buttons)

        for c in range(cols):
            row = None
            val = -1
            for r in range(pivot, len(self._target_joltage)):
                v = abs(self._aug_matrix[r][c])
                if v > val:
                    row = r
                    val = v

            if val < 1e-12:
                self._free_variables.append(c)
                continue

            if row != pivot:
                self._aug_matrix[pivot], self._aug_matrix[row] = self._aug_matrix[row], self._aug_matrix[pivot]
            self._depends.append(c) 

            v = self._aug_matrix[pivot][c]
            for i in range(c, cols + 1):
                self._aug_matrix[pivot][i] /= v

            for r in range(len(self._target_joltage)):
                if r == pivot:
                    continue
                factor = self._aug_matrix[r][c]
                if abs(factor) > 1e-12:
                    for j in range(c, cols + 1):
                        self._aug_matrix[r][j] -= factor * self._aug_matrix[pivot][j]

            pivot += 1

        self._free_variables.extend([c for c in range(c, cols)])


class Button:

    def __init__(self, size: int, raw: list[str]):
        self._configure_button(size, raw)


    def _configure_button(self, size: int, switches: list[str]):
        flipped_switches = np.zeros(size, dtype='int')
        for s in switches:
            flipped_switches[int(s)] = 1
        self.flipped_switches = flipped_switches


    def click(self, current_state: MachineState) -> MachineState:
        return np.array(np.array(current_state, dtype='bool') ^ np.array(self.flipped_switches, dtype='bool'), dtype='int')


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
    ("inputs/day10", 486, 17820),
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

