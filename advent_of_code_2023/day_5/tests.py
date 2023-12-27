from io import StringIO

from advent_of_code_2023.day_5.__main__ import solve_1, Mapper, parse_input, Almanac, MultiMapper


def test_category_mapper_destination_range():
    mapper = Mapper(destination_range_start=50, source_range_start=98, range_length=2)
    assert mapper.destination_range() == range(50, 52)

    mapper = Mapper(destination_range_start=52, source_range_start=50, range_length=48)
    assert mapper.destination_range() == range(52, 100)


def test_category_mapper_source_range():
    mapper = Mapper(destination_range_start=50, source_range_start=98, range_length=2)
    assert mapper.source_range() == range(98, 100)

    mapper = Mapper(destination_range_start=52, source_range_start=50, range_length=48)
    assert mapper.source_range() == range(50, 98)


def test_category_mapper_map_in_range():
    mapper = Mapper(destination_range_start=50, source_range_start=98, range_length=2)
    assert mapper.map(98) == 50
    assert mapper.map(99) == 51

    mapper = Mapper(destination_range_start=52, source_range_start=50, range_length=48)
    assert mapper.map(53) == 55
    assert mapper.map(70) == 72


def test_category_mapper_map_out_of_range():
    mapper = Mapper(destination_range_start=50, source_range_start=98, range_length=2)
    assert mapper.map(97) is None
    assert mapper.map(100) is None
    assert mapper.map(1) is None

    mapper = Mapper(destination_range_start=52, source_range_start=50, range_length=48)
    assert mapper.map(49) is None
    assert mapper.map(98) is None


def test_parse_input():
    input = """
    seeds: 79 14 55 13

    seed-to-soil map:
    50 98 2
    52 50 48

    soil-to-fertilizer map:
    0 15 37
    37 52 2
    39 0 15

    fertilizer-to-water map:
    49 53 8
    0 11 42
    42 0 7
    57 7 4

    water-to-light map:
    88 18 7
    18 25 70

    light-to-temperature map:
    45 77 23
    81 45 19
    68 64 13

    temperature-to-humidity map:
    0 69 1
    1 0 69

    humidity-to-location map:
    60 56 37
    56 93 4
    """
    assert parse_input(StringIO(input)) == Almanac(
        seeds=[79, 14, 55, 13],
        category_mappers=[
            MultiMapper([
                Mapper(destination_range_start=50, source_range_start=98, range_length=2),
                Mapper(destination_range_start=52, source_range_start=50, range_length=48)
            ]),
            MultiMapper([
                Mapper(destination_range_start=0, source_range_start=15, range_length=37),
                Mapper(destination_range_start=37, source_range_start=52, range_length=2),
                Mapper(destination_range_start=39, source_range_start=0, range_length=15)
            ]),
            MultiMapper([
                Mapper(destination_range_start=49, source_range_start=53, range_length=8),
                Mapper(destination_range_start=0, source_range_start=11, range_length=42),
                Mapper(destination_range_start=42, source_range_start=0, range_length=7),
                Mapper(destination_range_start=57, source_range_start=7, range_length=4)
            ]),
            MultiMapper([
                Mapper(destination_range_start=88, source_range_start=18, range_length=7),
                Mapper(destination_range_start=18, source_range_start=25, range_length=70)
            ]),
            MultiMapper([
                Mapper(destination_range_start=45, source_range_start=77, range_length=23),
                Mapper(destination_range_start=81, source_range_start=45, range_length=19),
                Mapper(destination_range_start=68, source_range_start=64, range_length=13)
            ]),
            MultiMapper([
                Mapper(destination_range_start=0, source_range_start=69, range_length=1),
                Mapper(destination_range_start=1, source_range_start=0, range_length=69)
            ]),
            MultiMapper([
                Mapper(destination_range_start=60, source_range_start=56, range_length=37),
                Mapper(destination_range_start=56, source_range_start=93, range_length=4)
            ])
        ]
    )


def test_example_part_1():
    input: str = """
    seeds: 79 14 55 13
    
    seed-to-soil map:
    50 98 2
    52 50 48
    
    soil-to-fertilizer map:
    0 15 37
    37 52 2
    39 0 15
    
    fertilizer-to-water map:
    49 53 8
    0 11 42
    42 0 7
    57 7 4
    
    water-to-light map:
    88 18 7
    18 25 70
    
    light-to-temperature map:
    45 77 23
    81 45 19
    68 64 13
    
    temperature-to-humidity map:
    0 69 1
    1 0 69
    
    humidity-to-location map:
    60 56 37
    56 93 4
    """
    assert solve_1(StringIO(input)) == 35
