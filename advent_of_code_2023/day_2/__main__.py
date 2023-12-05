import re
from dataclasses import dataclass, field
from typing import IO


@dataclass
class Extraction:
    num_red: int = 0
    num_green: int = 0
    num_blue: int = 0


@dataclass
class Game:
    id: int
    extractions: list[Extraction] = field(default_factory=list)

    def is_possible(self, num_red: int, num_green: int, num_blue: int) -> bool:
        return all([
            extraction.num_red <= num_red and extraction.num_green <= num_green and extraction.num_blue <= num_blue
            for extraction in self.extractions
        ])

    def get_max_num_red(self) -> int:
        return max([extraction.num_red for extraction in self.extractions])

    def get_max_num_green(self) -> int:
        return max([extraction.num_green for extraction in self.extractions])

    def get_max_num_blue(self) -> int:
        return max([extraction.num_blue for extraction in self.extractions])

    def get_power(self) -> int:
        return self.get_max_num_red() * self.get_max_num_green() * self.get_max_num_blue()


def get_game_id(raw_game: str) -> int:
    raw_game = raw_game.strip()
    pattern = r"Game (\d+):"
    first_match = re.match(pattern, raw_game)
    if first_match:
        return int(first_match.group(1))
    else:
        raise ValueError(f"Invalid game format: {raw_game}")


def get_extractions(raw_game: str) -> list[Extraction]:
    raw_game = raw_game.strip()
    raw_extractions = raw_game[raw_game.find(":") + 1:].strip()
    res = []
    for raw_extraction in raw_extractions.split(";"):
        res.append(Extraction(
            num_red=extract_color_num(raw_extraction, "red"),
            num_green=extract_color_num(raw_extraction, "green"),
            num_blue=extract_color_num(raw_extraction, "blue")
        ))
    return res


def extract_color_num(raw_extraction: str, color: str) -> int:
    raw_extraction = raw_extraction.strip()
    color_match = re.search(rf"(\d+) {color}", raw_extraction)
    return int(color_match.group(1)) if color_match else 0


def deserialize_games(raw_data: IO) -> list[Game]:
    return [
        Game(
            id=get_game_id(raw_game),
            extractions=get_extractions(raw_game))
        for raw_game in raw_data.readlines()
    ]


def result_1(games: list[Game]) -> int:
    return sum([game.id for game in games if game.is_possible(12, 13, 14)])


def result_2(games: list[Game]) -> int:
    return sum([game.get_power() for game in games])


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        print(f"first star solution: {result_1(deserialize_games(f))}")

    with open("input.txt", "r") as f:
        print(f"second star solution: {result_2(deserialize_games(f))}")
