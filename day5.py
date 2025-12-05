import logging
import os
import pytest


def _read_paper_layout(input_path: str) -> tuple[list, list]:
    fresh = []
    items = []
    flag = True

    with open(input_path, 'r') as file:
        for line in file:
            if line == '\n':
                flag = False
                continue
            if flag:
                fresh.append(line.rstrip('\n'))
            else:
                items.append(line.rstrip('\n'))

    return fresh, items


def get_fresh(path: str, part2: bool) -> int:
    fresh, items = _read_paper_layout(path)
    fresh_items = []
    fresh_ranges = []
    usable_ranges = []

    for i in items:
        for f in fresh:
            min = int(f.split('-')[0])
            max = int(f.split('-')[1])
            if int(i) >= min and int(i) <= max:
                fresh_items.append(int(i))
                if f not in usable_ranges:
                    usable_ranges.append(f)
                if not part2:
                    break

    if part2:
        for u in usable_ranges:
            fresh_ranges.sort()
            logging.warn(f'process {u}')
            min = int(u.split('-')[0])
            max = int(u.split('-')[1]) + 1
            for x in range(min, max):
                if x not in fresh_ranges:
                    fresh_ranges.append(x)

    return len(fresh_items) if not part2 else len(fresh_ranges)


@pytest.mark.parametrize("path, part2, expected", [
    ("examples/day5", False, 3),
    ("examples/day5", True, 14),
    ("inputs/day5", False, 611),
    ("inputs/day5", True, 1),
])
def test_day5(path: str, part2: bool, expected: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    roll_count = get_fresh(absolute_path, part2)
    assert roll_count == expected
