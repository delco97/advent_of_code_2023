from io import StringIO

from advent_of_code_2023.day_3.__main__ import solve_1


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


