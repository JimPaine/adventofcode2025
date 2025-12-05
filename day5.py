import os
import pytest


def _read_input(path: str) -> tuple[list, list]:
    fresh = []
    items = []
    flag = True

    with open(path, 'r') as file:
        for line in file:
            if line == '\n':
                flag = False
                continue
            if flag:
                low, high = line.rstrip('\n').split('-')
                fresh.append((int(low), int(high)))
            else:
                items.append(int(line.rstrip('\n')))

    return fresh, items


def get_fresh(path: str, part2: bool) -> int:
    fresh, items = _read_input(path)
    return _part1(items, fresh) if not part2 else _part2(fresh)


def _part1(item: list, fresh: list) -> int:
    fresh_items = []

    for i in item:
        for (l, h) in fresh:
            if int(l) <= i <= int(h):
                fresh_items.append(i)
                break

    return len(fresh_items)


def _part2(fresh: list) -> int:
    fresh.sort()
    low, high = fresh[0]
    count = 0
    for l, h, in fresh[1:]:
        if l > high + 1:
            count += high - low + 1
            low, high = l, h
        else:
            if h > high:
                high = h

    count += high - low + 1
    return count


@pytest.mark.parametrize("path, part2, expected", [
    ("examples/day5", False, 3),
    ("examples/day5", True, 14),
    ("inputs/day5", False, 611),
    ("inputs/day5", True, 345995423801866),
])
def test_day5(path: str, part2: bool, expected: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    roll_count = get_fresh(absolute_path, part2)
    assert roll_count == expected
