import os
from days.day2 import sum_invalid_ids


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
