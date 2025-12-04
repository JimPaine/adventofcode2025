import re
import os
import pytest


def sum_invalid_ids(ids_path: str, part2: bool) -> int:
    ranges = []
    with open(ids_path, 'r') as file:
        ranges = file.readline().split(',')
    invalid = []

    for r in ranges:
        min = int(r.split('-')[0])
        max = int(r.split('-')[1])

        pattern = r'^(\d+)\1$' if not part2 else r'^(\d+)\1+$'

        for id in range(min, max + 1):
            match = re.match(pattern, str(id))
            if match:
                invalid.append(id)

    return sum(invalid)


@pytest.mark.parametrize("path, part2, expected", [
    ("examples/day2", False, 1227775554),
    ("examples/day2", True, 4174379265),
    ("inputs/day2", False, 34826702005),
    ("inputs/day2", True, 43287141963),
])
def test_sum_invalid_ids(path: str, part2: bool, expected: int):
    absolute_path = os.path.join(os.path.dirname(__file__), path)
    invalid_sum = sum_invalid_ids(absolute_path, part2)
    assert invalid_sum == expected
