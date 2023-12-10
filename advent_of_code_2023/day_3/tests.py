from io import StringIO

from advent_of_code_2023.day_3.__main__ import solve_1, get_symbols, get_numbers, get_dots, \
    MatchedPart


def test_get_symbols():
    input: str = "467..114..%&...23._"
    assert get_symbols(input) == [
        MatchedPart("%", 10, 10),
        MatchedPart("&", 11, 11),
        MatchedPart("_", 18, 18),
    ]


def test_get_numbers():
    input: str = "467..114..%&...23._"
    assert get_numbers(input) == [
        MatchedPart("467", 0, 2),
        MatchedPart("114", 5, 7),
        MatchedPart("23", 15, 16),
    ]


def test_get_dots():
    input: str = "467..114..%&...23._"
    assert get_dots(input) == [
        MatchedPart(".", 3, 3),
        MatchedPart(".", 4, 4),
        MatchedPart(".", 8, 8),
        MatchedPart(".", 9, 9),
        MatchedPart(".", 12, 12),
        MatchedPart(".", 13, 13),
        MatchedPart(".", 14, 14),
        MatchedPart(".", 17, 17),
    ]


def test_solve_1():
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
    assert solve_1(StringIO(input)) == 4361
