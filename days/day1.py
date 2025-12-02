import logging


def decode_password(
        combination_path: str) -> tuple[int, int]:
    pos = 50
    zeros = 0
    clicks = 0

    logging.info("The dial starts by pointing at 50.")

    with open(combination_path, 'r') as file:
        for line in file:
            dir = line[0]
            moves = int(line[1:])
            pos, clicks = rotate(pos, moves, dir, clicks)
            logging.info(f"The dial is rotated {line} to point at {pos}.")
            if pos == 0:
                zeros += 1

    return zeros, clicks


def rotate(pos: int, moves: int, dir: str, clicks: int) -> tuple[int, int]:
    for _ in range(moves):
        if dir == 'R':
            pos = (pos + 1) % 100
        else:
            pos = (pos - 1) % 100

        if pos == 0:
            clicks += 1

    return pos, clicks
