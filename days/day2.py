import re


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
