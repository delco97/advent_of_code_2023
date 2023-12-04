from io import StringIO

from advent_of_code_2023.day_2.__main__ import Game, deserialize_games

from advent_of_code_2023.day_2.__main__ import Extraction as E


def test_deserialize():
    content = """
    Game 1: 1 red, 10 blue, 5 green; 11 blue, 6 green; 6 green; 1 green, 1 red, 12 blue; 3 blue; 3 blue, 4 green, 1 red
    """.strip()

    res = deserialize_games(StringIO(content))
    assert res == [
        Game(1, [
            E(num_red=1, num_green=5, num_blue=10),
            E(num_red=0, num_green=6, num_blue=11),
            E(num_red=0, num_green=6, num_blue=0),
            E(num_red=1, num_green=1, num_blue=12),
            E(num_red=0, num_green=0, num_blue=3),
            E(num_red=1, num_green=4, num_blue=3)
        ])
    ]
