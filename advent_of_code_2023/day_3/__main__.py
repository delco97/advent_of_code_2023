from dataclasses import dataclass
from typing import IO
import re


@dataclass(frozen=True)
class MatchedPart:
    value: str
    start: int
    end: int


@dataclass(frozen=True)
class PartNumber:
    value: int
    row: int
    start: int
    end: int


@dataclass(frozen=True)
class Row:
    index: int
    value: str


def get_start_end_positions_of_matches(row: str, pattern: str) -> list[MatchedPart]:
    return [MatchedPart(m.group(), m.start(), m.end() - 1) for m in re.finditer(pattern, row)]


def get_symbols(row: str) -> list[MatchedPart]:
    return get_start_end_positions_of_matches(row, r"[^\d\.]")


def get_numbers(row: str) -> list[MatchedPart]:
    return get_start_end_positions_of_matches(row, r"\d+")


def get_dots(row: str) -> list[MatchedPart]:
    return get_start_end_positions_of_matches(row, r"\.")


def is_symbol(value: str) -> bool:
    return re.match(r"[^\d\.]", value) is not None


def is_part_number(number_match: MatchedPart, candidate_positions: list[int]) -> bool:
    return any(number_match.start <= pos <= number_match.end for pos in candidate_positions)


def get_part_numbers(row: Row, candidate_positions: [int, int]) -> list[PartNumber]:
    return [
        PartNumber(int(number_match.value), row.index, number_match.start, number_match.end)
        for number_match in get_numbers(row.value)
        if is_part_number(number_match, candidate_positions)
    ]


def get_nearby_part_numbers(
        symbol_index: int,
        current_row: Row, previous_row: Row | None,
        next_row: Row | None) -> set[PartNumber]:
    nearby_part_numbers: set[PartNumber] = set()
    for row in [previous_row, current_row, next_row]:
        if row is not None:
            candidate_part_numbers_positions = [
                x for x in [symbol_index - 1, symbol_index, symbol_index + 1]
                if x >= 0 and x < len(row.value)
            ]
            row_part_numbers = get_part_numbers(row, candidate_part_numbers_positions)
            nearby_part_numbers.update(row_part_numbers)
    return nearby_part_numbers


def solve_1(input: IO) -> int:
    raw_rows = [row.strip() for row in input.readlines() if row.strip() != ""]
    rows = [Row(row_index, row.strip()) for row_index, row in enumerate(raw_rows)]
    part_numbers: set[PartNumber] = set()
    for current_row in rows:
        next_row = rows[current_row.index + 1] if current_row.index + 1 < len(rows) else None
        previous_row = rows[current_row.index - 1] if current_row.index - 1 >= 0 else None
        for symbol in get_symbols(current_row.value):
            nearby_part_numbers = get_nearby_part_numbers(symbol.start, current_row, previous_row, next_row)
            part_numbers.update(nearby_part_numbers)
    part_numbers_sum = sum([part_number.value for part_number in part_numbers])
    return part_numbers_sum


if __name__ == "__main__":
    with open("input.txt") as f:
        print(solve_1(f))
