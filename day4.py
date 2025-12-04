import copy
import os


def _read_paper_layout(input_path: str) -> list:
    rows = []
    with open(input_path, 'r') as file:
        for line in file:
            rows.append(list(line.rstrip('\n')))

    return rows


def optimize_forklift(input_path: str, part2=False) -> int:
    temp_layout = _read_paper_layout(input_path)

    roll_count = 0
    flag = True

    while flag:
        temp_count = 0
        layout = copy.deepcopy(temp_layout)
        w = len(layout[0])
        h = len(layout)

        for x in range(0, w):
            for y in range(0, h):
                if layout[y][x] == '@':
                    x_slice = slice(x - 1 if x > 0 else 0, x + 2 if x < w - 1 else w)
                    y_slice = slice(y - 1 if y > 0 else 0, y + 2 if y < h - 1 else h)

                    area = layout[y_slice]
                    area = [row[x_slice] for row in area]
                    if _check_surrounding_area(area):
                        temp_count += 1
                        temp_layout[y][x] = '.'
        roll_count += temp_count
        flag = False if temp_count == 0 or not part2 else True

    return roll_count


def _check_surrounding_area(layout: list) -> bool:
    count = 0
    for y in range(len(layout)):
        for x in range(len(layout[y])):
            if layout[y][x] == '@':
                count += 1

    return count < 5  # including the center '@'


def test_optimize_forklift_example():
    example_path = os.path.join(os.path.dirname(__file__), 'examples/day4')
    roll_count = optimize_forklift(example_path)
    assert roll_count == 13


def test_optimize_forklift_part2_example():
    example_path = os.path.join(os.path.dirname(__file__), 'examples/day4')
    roll_count = optimize_forklift(example_path, part2=True)
    assert roll_count == 43


def test_optimize_forklift_input():
    input_path = os.path.join(os.path.dirname(__file__), 'inputs/day4')
    roll_count = optimize_forklift(input_path)
    assert roll_count == 1356


def test_optimize_forklift_part2_input():
    input_path = os.path.join(os.path.dirname(__file__), 'inputs/day4')
    roll_count = optimize_forklift(input_path, part2=True)
    assert roll_count == 1356
