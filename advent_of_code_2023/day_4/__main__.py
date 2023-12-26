import re
from typing import IO
from dataclasses import dataclass


@dataclass
class Card:
    number: int
    winning_numbers: set[int]
    given_numbers: set[int]
    instances: int

    def get_points(self) -> int:
        matches = len(self.winning_numbers & self.given_numbers)
        return 2 ** (matches - 1) if matches > 0 else 0


def iterate_raw_rows(input: IO) -> list[str]:
    for row in input.readlines():
        if row.strip() != "":
            yield row.strip()


def get_card_points(winning_numbers: set[int], given_numbers: set[int]) -> int:
    matches = len(winning_numbers & given_numbers)
    return 2 ** (matches - 1) if matches > 0 else 0


def parse_card(raw: str) -> Card:
    colon_position = raw.find(":")
    if colon_position == -1:
        raise ValueError("Invalid input. Expected a colon.")
    card_number = int(raw[:colon_position].strip().split(" ")[1])
    raw_numbers = raw[colon_position + 1:].strip()
    splitted_row = [x.strip() for x in raw_numbers.split("|")]
    if len(splitted_row) != 2:
        raise ValueError("Invalid input. Expected exactly one pipe.")
    winning_numbers: set[int] = {int(x) for x in re.split(r'\s+', splitted_row[0])}
    given_numbers: set[int] = {int(x) for x in re.split(r'\s+', splitted_row[1])}
    return Card(card_number, winning_numbers, given_numbers, 1)


def solve_1(input: IO) -> int:
    cards_pile: list[Card] = [
        parse_card(current_row) for current_row in iterate_raw_rows(input)
    ]
    return sum([card.get_points() for card in cards_pile])


def solve_2(input: IO) -> int:
    pass


if __name__ == "__main__":
    with open("input.txt") as f:
        print(f"Solution 1: {solve_1(f)}")
