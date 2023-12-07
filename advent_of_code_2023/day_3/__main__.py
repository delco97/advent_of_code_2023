from io import StringIO
from typing import IO
import re

def get_symbols_positions(row: str) -> list[int]:
    return [m.start() for m in re.finditer(r"[^\d\.]", row)]

def solve_1(input: IO) -> int:
    rows = [row.strip() for row in input.readlines() if row.strip() != ""]
    prev_row: str = ""
    next_row: str = ""
    num_rows: int = len(rows)

    for idx, current_row in enumerate(rows):
        prev_row = rows[idx - 1] if idx - 1 >= 0 else ""
        next_row = rows[idx + 1] if idx + 1 < num_rows else ""
        symbols_positions = get_symbols_positions(current_row)
        for symbol_position in symbols_positions:
            





if __name__ == "__main__":
    input: str = """
    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..
    """
    solve_1(StringIO(input))