import re
from typing import IO


def iterate_raw_rows(input: IO) -> list[str]:
    for row in input.readlines():
        if row.strip() != "":
            yield row.strip()


def extract_numbers(current_row: str) -> tuple[set[int], set[int]]:
    colon_position = current_row.find(":")
    if colon_position == -1:
        raise ValueError("Invalid input. Expected a colon.")
    current_row = current_row[colon_position + 1:].strip()
    splitted_row = [x.strip() for x in current_row.split("|")]
    if len(splitted_row) != 2:
        raise ValueError("Invalid input. Expected exactly one pipe.")
    winning_numbers: set[int] = {int(x) for x in re.split(r'\s+', splitted_row[0])}
    given_numbers: set[int] = {int(x) for x in re.split(r'\s+', splitted_row[1])}
    return winning_numbers, given_numbers


def get_card_points(winning_numbers: set[int], given_numbers: set[int]) -> int:
    matches = len(winning_numbers & given_numbers)
    return 2 ** (matches - 1) if matches > 0 else 0


def solve_1(input: IO) -> int:
    points = 0
    for current_row in iterate_raw_rows(input):
        winning_numbers, given_numbers = extract_numbers(current_row)
        points += get_card_points(winning_numbers, given_numbers)
    return points


def solve_2(input: IO) -> int:
    pass


if __name__ == "__main__":
    with open("input.txt") as f:
        print(f"Solution 1: {solve_1(f)}")
