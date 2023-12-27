import re
from typing import IO
from dataclasses import dataclass


@dataclass
class Mapper:
    destination_range_start: int
    source_range_start: int
    range_length: int

    def destination_range(self) -> range:
        return range(self.destination_range_start, self.destination_range_start + self.range_length)

    def source_range(self) -> range:
        return range(self.source_range_start, self.source_range_start + self.range_length)

    def map(self, source: int) -> int | None:
        if source not in self.source_range():
            return None
        return self.destination_range_start + (source - self.source_range_start)


@dataclass
class MultiMapper:
    mappers: list[Mapper]

    def map(self, category: int) -> int | None:
        for mapper in self.mappers:
            mapped_category = mapper.map(category)
            if mapped_category is not None:
                return mapped_category
        return None


@dataclass
class Almanac:
    seeds: list[int]
    category_mappers: list[MultiMapper]

    def map(self, category: int) -> int:
        for mapper in self.category_mappers:
            mapped_category = mapper.map(category)
            if mapped_category is not None:
                category = mapped_category
        return category

    def get_lowest_location(self) -> int:
        return min(self.map(seed) for seed in self.seeds)


def iterate_raw_rows(input: IO) -> list[str]:
    for row in input.readlines():
        if row.strip() != "":
            yield row.strip()


def get_file_section(rows: list[str], section_name: str) -> list[str]:
    section_start_row_index = -1
    section_end_row_index = -1
    for row_index in range(len(rows)):
        row = rows[row_index]
        if section_name in row:
            section_start_row_index = row_index + 1
        elif section_start_row_index != -1 and re.match(r'\D', row):
            section_end_row_index = row_index
            break
    if section_start_row_index == -1:
        raise Exception(f"Section {section_name} not found")
    if section_end_row_index == -1:
        section_end_row_index = len(rows)
    return rows[section_start_row_index:section_end_row_index]


def get_multimapper_from_file(rows: list[str], section_name: str) -> MultiMapper:
    section_rows = get_file_section(rows, section_name)
    mappers: list[Mapper] = []
    for row in section_rows:
        destination_range_start, source_range_start, range_length = [int(x) for x in row.split(" ")]
        mappers.append(Mapper(destination_range_start, source_range_start, range_length))
    return MultiMapper(mappers)


def parse_input(input: IO) -> Almanac:
    rows = list(iterate_raw_rows(input))
    seeds: list[int] = [int(x) for x in rows[0][rows[0].find(":") + 1:].strip().split(" ")]
    return Almanac(
        seeds,
        [
            get_multimapper_from_file(rows, "seed-to-soil map"),
            get_multimapper_from_file(rows, "soil-to-fertilizer map"),
            get_multimapper_from_file(rows, "fertilizer-to-water map"),
            get_multimapper_from_file(rows, "water-to-light map"),
            get_multimapper_from_file(rows, "light-to-temperature map"),
            get_multimapper_from_file(rows, "temperature-to-humidity map"),
            get_multimapper_from_file(rows, "humidity-to-location map")
        ]
    )


def solve_1(input: IO) -> int:
    almanac = parse_input(input)
    return almanac.get_lowest_location()


if __name__ == "__main__":
    with open("input.txt") as f:
        print(f"Solution 1: {solve_1(f)}")
