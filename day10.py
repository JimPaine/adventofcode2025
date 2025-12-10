import os
import itertools
import pytest
import numpy as np

def _read(path: str) -> list:
    rows = []
    with open(path, 'r') as file:
        for line in file:
            rows.append(line.rstrip('\n'))

    return rows

def toggler(path: str) -> tuple[int, int]:
    raw = _read(path)

    click_total = 0
    
    for machine in raw:
        temp = machine.split(' ')
        target_state = np.array([False if s == '.' else True for s in temp[0][1:-1]])

        # joltage = np.array([int(j) for j in temp[-1:][0][1:-1].split(',')])
        raw_buttons = [s[1:-1].split(',') for s in temp[1:-1]]
        buttons = np.array([get_button(r, len(target_state)) for r in raw_buttons])
        clicks = 1
        counter = 0
        current_clicks = 0 
        while True:
            
            for bs in itertools.combinations_with_replacement(buttons, clicks):
                current_state = np.array([False for _ in range(len(target_state))])
                for b in bs:
                    current_state = click(current_state, b)

                if all(current_state == target_state):
                    current_clicks = clicks if current_clicks == 0 or clicks < current_clicks else current_clicks
                    counter += 1

            if counter >= 20: # hack to make sure we check lots of combos
                click_total += current_clicks
                break
            clicks += 1

    return click_total, 0

def get_button(switches: list, expected: int) -> list:
    button = np.zeros(expected, dtype=bool)
    for s in switches:
        button[int(s)] = True
    return button


def click(current_state: list, button: list) -> list:
    return current_state ^ button

@pytest.mark.parametrize("path, part1, part2", [
    ("examples/day10", 7, 0),
    ("inputs/day10", 486, 0),
])
def test_measure(path: str, part1: int, part2: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    p1, p2 = toggler(absolute_path)
    assert p1 == part1
    assert p2 == part2
