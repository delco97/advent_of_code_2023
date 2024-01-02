from io import StringIO

from advent_of_code_2023.day_5.__main__ import solve_1, Mapper, parse_input, Almanac, MultiMapper, solve_2, RangeMapper, \
    range_intersect, RangeMultiMapper, RangeAlmanac, parse_input_range_almanac, range_difference, range_union, \
    range_multiple_difference


def test_mapper_destination_range():
    mapper = Mapper(destination_range_start=50, source_range_start=98, range_length=2)
    assert mapper.destination_range() == range(50, 52)

    mapper = Mapper(destination_range_start=52, source_range_start=50, range_length=48)
    assert mapper.destination_range() == range(52, 100)


def test_mapper_source_range():
    mapper = Mapper(destination_range_start=50, source_range_start=98, range_length=2)
    assert mapper.source_range() == range(98, 100)

    mapper = Mapper(destination_range_start=52, source_range_start=50, range_length=48)
    assert mapper.source_range() == range(50, 98)


def test_mapper_map_in_range():
    mapper = Mapper(destination_range_start=50, source_range_start=98, range_length=2)
    assert mapper.map(98) == 50
    assert mapper.map(99) == 51

    mapper = Mapper(destination_range_start=52, source_range_start=50, range_length=48)
    assert mapper.map(53) == 55
    assert mapper.map(70) == 72


def test_mapper_map_out_of_range():
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


def test_range_mapper_map():
    mapper = RangeMapper(source_range=range(10, 21), destination_range=range(30, 41))

    assert mapper.map(range(8, 10)) == [range(8, 10)]
    assert mapper.map(range(21, 23)) == [range(21, 23)]
    assert mapper.map(range(9, 11)) == [range(9, 10), range(30, 31)]
    assert mapper.map(range(9, 11)) == [range(9, 10), range(30, 31)]
    assert mapper.map(range(20, 22)) == [range(21, 22), range(40, 41)]
    assert mapper.map(range(9, 15)) == [range(9, 10), range(30, 35)]
    assert mapper.map(range(15, 22)) == [range(21, 22), range(35, 41)]
    assert mapper.map(range(11, 20)) == [range(31, 40)]
    assert mapper.map(range(10, 21)) == [range(30, 41)]
    assert mapper.map(range(9, 22)) == [range(9, 10), range(21, 22), range(30, 41)]


def test_range_multi_mapper():
    multi_mapper = RangeMultiMapper([
        RangeMapper(source_range=range(10, 21), destination_range=range(40, 51)),
        RangeMapper(source_range=range(30, 41), destination_range=range(60, 71)),
    ])

    assert multi_mapper.map(range(8, 10)) == [range(8, 10)]
    assert multi_mapper.map(range(9, 11)) == [range(9, 10), range(40, 41)]
    assert multi_mapper.map(range(9, 12)) == [range(9, 10), range(40, 42)]
    assert multi_mapper.map(range(10, 12)) == [range(40, 42)]
    assert multi_mapper.map(range(11, 20)) == [range(41, 50)]
    assert multi_mapper.map(range(19, 21)) == [range(49, 51)]
    assert multi_mapper.map(range(19, 22)) == [range(21, 22), range(49, 51)]
    assert multi_mapper.map(range(20, 22)) == [range(21, 22), range(50, 51)]
    assert multi_mapper.map(range(21, 30)) == [range(21, 30)]
    assert multi_mapper.map(range(19, 32)) == [range(21, 30), range(49, 51), range(60, 62)]
    assert multi_mapper.map(range(9, 42)) == [range(9, 10), range(21, 30), range(40, 51), range(41, 42), range(60, 71)]


def test_intersect_ranges():
    assert range_intersect([range(10, 21), range(8, 10)]) is None
    assert range_intersect([range(10, 21), range(21, 23)]) is None
    assert range_intersect([range(10, 21), range(9, 11)]) == range(10, 11)
    assert range_intersect([range(10, 21), range(20, 22)]) == range(20, 21)
    assert range_intersect([range(10, 21), range(9, 16)]) == range(10, 16)
    assert range_intersect([range(10, 21), range(15, 22)]) == range(15, 21)
    assert range_intersect([range(10, 21), range(11, 20)]) == range(11, 20)
    assert range_intersect([range(10, 21), range(10, 21)]) == range(10, 21)
    assert range_intersect([range(10, 21), range(9, 22)]) == range(10, 21)


def test_union_ranges():
    assert range_union([range(10, 21), range(5, 10)]) == [range(5, 21)]
    assert range_union([range(10, 21), range(8, 10)]) == [range(8, 21)]
    assert range_union([range(10, 21), range(21, 23)]) == [range(10, 23)]
    assert range_union([range(10, 21), range(9, 11)]) == [range(9, 21)]
    assert range_union([range(10, 21), range(20, 22)]) == [range(10, 22)]
    assert range_union([range(10, 21), range(9, 16)]) == [range(9, 21)]
    assert range_union([range(10, 21), range(15, 22)]) == [range(10, 22)]
    assert range_union([range(10, 21), range(11, 20)]) == [range(10, 21)]
    assert range_union([range(10, 21), range(10, 21)]) == [range(10, 21)]
    assert range_union([range(10, 21), range(9, 22)]) == [range(9, 22)]


def test_range_almanac_parse_input_range_almanac():
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
    assert parse_input_range_almanac(StringIO(input)) == RangeAlmanac(
        seeds=[range(79, 93), range(55, 68)],
        mappers=[
            RangeMultiMapper([
                RangeMapper(source_range=range(98, 100), destination_range=range(50, 52)),
                RangeMapper(source_range=range(50, 98), destination_range=range(52, 100))
            ]),
            RangeMultiMapper([
                RangeMapper(source_range=range(15, 52), destination_range=range(0, 37)),
                RangeMapper(source_range=range(52, 54), destination_range=range(37, 39)),
                RangeMapper(source_range=range(0, 15), destination_range=range(39, 54))
            ]),
            RangeMultiMapper([
                RangeMapper(source_range=range(53, 61), destination_range=range(49, 57)),
                RangeMapper(source_range=range(11, 53), destination_range=range(0, 42)),
                RangeMapper(source_range=range(0, 7), destination_range=range(42, 49)),
                RangeMapper(source_range=range(7, 11), destination_range=range(57, 61))
            ]),
            RangeMultiMapper([
                RangeMapper(source_range=range(18, 25), destination_range=range(88, 95)),
                RangeMapper(source_range=range(25, 95), destination_range=range(18, 88))
            ]),
            RangeMultiMapper([
                RangeMapper(source_range=range(77, 100), destination_range=range(45, 68)),
                RangeMapper(source_range=range(45, 64), destination_range=range(81, 100)),
                RangeMapper(source_range=range(64, 77), destination_range=range(68, 81)),
            ]),
            RangeMultiMapper([
                RangeMapper(source_range=range(69, 70), destination_range=range(0, 1)),
                RangeMapper(source_range=range(0, 69), destination_range=range(1, 70))
            ]),
            RangeMultiMapper([
                RangeMapper(source_range=range(56, 93), destination_range=range(60, 97)),
                RangeMapper(source_range=range(93, 97), destination_range=range(56, 60))
            ])
        ]
    )


def test_range_almanac():
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
    range_almanac: RangeAlmanac = parse_input_range_almanac(StringIO(input))
    almanac: Almanac = parse_input(StringIO(input))

    # Always out of range
    assert range_almanac.map(range(-10, -5)) == [range(-10, -5)]
    assert almanac.map(-1) == -1

    assert almanac.map(79) == range_almanac.map(range(79, 80))[0].start


def test_range_difference():
    assert range_difference(range(10, 21), range(8, 10)) == [range(10, 21)]
    assert range_difference(range(10, 21), range(21, 23)) == [range(10, 21)]
    assert range_difference(range(10, 21), range(9, 11)) == [range(11, 21)]
    assert range_difference(range(10, 21), range(20, 22)) == [range(10, 20)]
    assert range_difference(range(10, 21), range(9, 16)) == [range(16, 21)]
    assert range_difference(range(10, 21), range(15, 22)) == [range(10, 15)]
    assert range_difference(range(10, 21), range(11, 20)) == [range(10, 11), range(20, 21)]
    assert range_difference(range(10, 21), range(10, 21)) == []
    assert range_difference(range(10, 21), range(9, 22)) == []


def test_range_multiple_difference():
    range1 = range(1, 5)
    range2 = range(6, 10)
    result = range_difference(range1, range2)
    assert result == [range1]

    range1 = range(1, 8)
    range2 = range(5, 10)
    result = range_difference(range1, range2)
    assert result == [range(1, 5)]

    range1 = range(1, 10)
    range2 = range(3, 7)
    result = range_difference(range1, range2)
    assert result == [range(1, 3), range(7, 10)]

    range1 = range(1, 5)
    ranges_to_remove = [range(6, 10), range(12, 15)]
    result = range_multiple_difference(range1, ranges_to_remove)
    assert result == [range1]

    range1 = range(1, 10)
    ranges_to_remove = [range(5, 15), range(18, 20)]
    result = range_multiple_difference(range1, ranges_to_remove)
    assert result == [range(1, 5)]

    range1 = range(1, 10)
    ranges_to_remove = [range(3, 7), range(2, 8)]
    result = range_multiple_difference(range1, ranges_to_remove)
    assert result == [range(1, 2), range(8, 10)]


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


def test_example_part_2():
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
    assert solve_2(StringIO(input)) == 46
