import itertools
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


@dataclass
class RangeMapper:
    source_range: range
    destination_range: range

    def map(self, range_to_map: range) -> list[range]:
        mappable_range = self.get_mappable_range(range_to_map)

        if not mappable_range:
            return [range_to_map]

        res = []
        start_delta = mappable_range.start - self.source_range.start
        end_delta = mappable_range.stop - self.source_range.start
        res.append(range(
            self.destination_range.start + start_delta,
            self.destination_range.start + end_delta
        ))

        not_mapped_ranges = range_difference(range_to_map, mappable_range)
        for not_mapped_range in not_mapped_ranges:
            res.append(not_mapped_range)

        return sorted(res, key=lambda x: x.start)

    def get_mappable_range(self, range_to_map: range) -> range | None:
        return range_intersect([range_to_map, self.source_range])


@dataclass
class RangeMultiMapper:
    mappers: list[RangeMapper]

    def map(self, range_to_map: range) -> list[range]:
        res = []
        mappable_ranges = []
        for mapper in self.mappers:
            mappable_range = mapper.get_mappable_range(range_to_map)
            if mappable_range:
                res += mapper.map(mappable_range)
                mappable_ranges.append(mappable_range)

        mappable_ranges = range_union(mappable_ranges)
        res += range_multiple_difference(range_to_map, mappable_ranges)

        return sorted(res, key=lambda x: (x.start, x.stop))


@dataclass
class RangeAlmanac:
    seeds: list[range]
    mappers: list[RangeMultiMapper]

    def map(self, starting_range_to_map: range) -> list[range]:
        mapped_ranges = [starting_range_to_map]
        for mapper in self.mappers:
            next_mapped_ranges = []
            while mapped_ranges:
                current_range_to_map = mapped_ranges.pop()
                next_mapped_ranges += mapper.map(current_range_to_map)
            mapped_ranges = next_mapped_ranges
        return mapped_ranges

    def get_lowest_location(self) -> int | None:
        location_ranges: list[range] = list(itertools.chain.from_iterable((self.map(seed) for seed in self.seeds)))
        if not location_ranges:
            return None
        return min(location_ranges, key=lambda x: x.start).start


def range_difference(range1: range, range2: range) -> list[range]:
    res = []
    if range1.start > range2.stop - 1 or range1.stop - 1 < range2.start:
        res = [range1]
    elif range1.start < range2.start and range1.stop > range2.stop:
        res = [
            range(range1.start, range2.start),
            range(range2.stop, range1.stop)
        ]
    elif range1.start < range2.start:
        res = [range(range1.start, range2.start)]
    elif range1.stop > range2.stop:
        res = [range(range2.stop, range1.stop)]
    return sorted(res, key=lambda x: x.start)


def range_multiple_difference(range1: range, ranges: list[range]) -> list[range]:
    res = [range1]
    for range_to_remove in ranges:
        idx = 0
        while idx < len(res):
            current_range = res[idx]
            diff = range_difference(current_range, range_to_remove)
            if diff != [current_range]:
                res.pop(idx)
                res = diff + res
            idx += 1
    return sorted(res, key=lambda x: x.start)


def range_intersect(ranges: list[range]) -> range | None:
    if len(ranges) == 0:
        return None
    intersection = ranges[0]
    for current_range in ranges[1:]:
        if intersection.start > current_range.stop - 1 or intersection.stop - 1 < current_range.start:
            return None
        intersection = range(max(intersection.start, current_range.start), min(intersection.stop, current_range.stop))
    return intersection


def range_union(ranges: list[range]) -> list[range]:
    res: list[range] = []
    for r in sorted(ranges, key=lambda x: (x.start, x.stop)):
        begin = r.start
        end = r.stop
        if res and res[-1].stop - 1 >= begin - 1:
            res[-1] = range(res[-1].start, max(res[-1].stop, end))
        else:
            res.append(range(begin, end))
    return sorted(res, key=lambda x: x.start)


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


def get_range_multimapper_from_file(rows: list[str], section_name: str) -> RangeMultiMapper:
    section_rows = get_file_section(rows, section_name)
    mappers: list[RangeMapper] = []
    for row in section_rows:
        destination_range_start, source_range_start, range_length = [int(x) for x in row.split(" ")]
        destination_range = range(destination_range_start, destination_range_start + range_length)
        source_range = range(source_range_start, source_range_start + range_length)
        mappers.append(RangeMapper(source_range, destination_range))
    return RangeMultiMapper(mappers)


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


def parse_input_range_almanac(input: IO) -> RangeAlmanac:
    rows = list(iterate_raw_rows(input))
    seeds: list[int] = [int(x) for x in rows[0][rows[0].find(":") + 1:].strip().split(" ")]
    range_seeds: list[range] = []
    for idx in range(0, len(seeds), 2):
        start = seeds[idx]
        length = seeds[idx + 1]
        range_seeds.append(range(start, start + length))

    return RangeAlmanac(
        range_seeds,
        [
            get_range_multimapper_from_file(rows, "seed-to-soil map"),
            get_range_multimapper_from_file(rows, "soil-to-fertilizer map"),
            get_range_multimapper_from_file(rows, "fertilizer-to-water map"),
            get_range_multimapper_from_file(rows, "water-to-light map"),
            get_range_multimapper_from_file(rows, "light-to-temperature map"),
            get_range_multimapper_from_file(rows, "temperature-to-humidity map"),
            get_range_multimapper_from_file(rows, "humidity-to-location map")
        ]
    )


def solve_1(input: IO) -> int:
    almanac = parse_input(input)
    return almanac.get_lowest_location()


def solve_2(input: IO) -> int:
    almanac = parse_input_range_almanac(input)
    return almanac.get_lowest_location()


if __name__ == "__main__":
    with open("input.txt") as f:
        print(f"Solution 1: {solve_1(f)}")
        f.seek(0)
        print(f"Solution 2: {solve_2(f)}")
