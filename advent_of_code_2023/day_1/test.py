from io import StringIO

from advent_of_code_2023.day_1.main import get_fixed_calibration_value, get_fixed_calibration_value_complete


def get_fixed_calibration_value():
    calibrations: str = """
    nine5fivecgfsbvbtsn57five7djxlclnfv
    2gzqrfldtlpeight3fivencmlmffivevqkhncfm
    7bbfbcvh6
    ffnrprtnine1tjznmckv5sixczv
    11
    01
    00
    a11a
    a123
    """
    assert get_fixed_calibration_value(StringIO(calibrations)) == 207

def test_get_fixed_calibration_value_complete():
    calibrations: str = """
    two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen
    """
    assert get_fixed_calibration_value_complete(StringIO(calibrations)) == 281

