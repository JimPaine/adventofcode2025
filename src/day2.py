import re
import os


def sum_invalid_ids(ids_path: str, part=1) -> int:
    ranges = []
    with open(ids_path, 'r') as file:
        ranges = file.readline().split(',')
    invalid = []

    for r in ranges:
        min = int(r.split('-')[0])
        max = int(r.split('-')[1])

        pattern = r'^(\d+)\1$'
        if part == 2:
            pattern = r'^(\d{1,})\1+$'

        for id in range(min, max + 1):
            match = re.match(pattern, str(id))
            if match:
                invalid.append(id)

    return sum(invalid)


def test_sum_invalid_ids_example():
    example_path = os.path.join(os.path.dirname(__file__), 'examples/day2')
    invalid_sum = sum_invalid_ids(example_path, part=1)
    assert invalid_sum == 1227775554
    invalid_sum = sum_invalid_ids(example_path, part=2)
    assert invalid_sum == 4174379265


def test_sum_invalid_ids_input():
    input_path = os.path.join(os.path.dirname(__file__), 'inputs/day2')
    invalid_sum = sum_invalid_ids(input_path, part=1)
    assert invalid_sum == 34826702005
    invalid_sum = sum_invalid_ids(input_path, part=2)
    assert invalid_sum == 43287141963
