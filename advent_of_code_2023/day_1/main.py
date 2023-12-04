from typing import IO


def get_calibration_value(calibration: str) -> int:
    if not isinstance(calibration, str):
        raise ValueError("calibration must be a string")
    if len(calibration) == 0:
        raise ValueError("calibration can't be an empty string")

    head = 0
    tail = len(calibration) - 1
    n = len(calibration)
    value: str = ""
    digit_found_head = False
    digit_found_tail = False
    while ((not digit_found_head or not digit_found_tail) and head <= tail):
        if not digit_found_head and calibration[head].isdigit():
            value = calibration[head] + value
            digit_found_head = True

        if not digit_found_tail and calibration[tail].isdigit():
            value = value + calibration[tail]
            digit_found_tail = True

        if not digit_found_head and head < n - 1:
            head += 1

        if not digit_found_tail and tail > 0:
            tail -= 1

    try:
        return int(value)
    except ValueError:
        return 0


def get_spelled_digit(value: str) -> str | None:
    if not isinstance(value, str):
        raise ValueError("param must be a string")
    if len(value) == 0:
        raise ValueError("param can't be an empty string")

    map_spelled_digit_to_number = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }

    min_len = min([len(key) for key in map_spelled_digit_to_number.keys()])

    if len(value) < min_len:
        return None

    for key in map_spelled_digit_to_number.keys():
        if key in value:
            return map_spelled_digit_to_number[key]

    return None


def get_calibration_value_complete(calibration: str) -> int:
    if not isinstance(calibration, str):
        raise ValueError("calibration must be a string")

    calibration = calibration.strip()
    head = 0
    tail = len(calibration) - 1
    n = len(calibration)
    value: str = ""
    digit_found_head = False
    digit_found_tail = False
    while ((not digit_found_head or not digit_found_tail) and head <= tail):
        if not digit_found_head:
            if calibration[head].isdigit():
                value = calibration[head] + value
                digit_found_head = True
            else:
                digit = get_spelled_digit(calibration[:head + 1])
                if digit:
                    value = digit + value
                    digit_found_head = True

        if not digit_found_tail:
            if calibration[tail].isdigit():
                value = value + calibration[tail]
                digit_found_tail = True
            else:
                digit = get_spelled_digit(calibration[tail:])
                if digit:
                    value = value + digit
                    digit_found_tail = True

        if not digit_found_head and head < n - 1:
            head += 1

        if not digit_found_tail and tail > 0:
            tail -= 1

    try:
        return int(value)
    except ValueError:
        return 0


def get_fixed_calibration_value(calibrations: IO) -> int:
    return sum([get_calibration_value(line) for line in calibrations.readlines()])


def get_fixed_calibration_value_complete(calibrations: IO) -> int:
    return sum([get_calibration_value_complete(line) for line in calibrations.readlines()])


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        print(f"first star solution: {get_fixed_calibration_value(f)}")

    with open("input.txt", "r") as f:
        print(f"second star solution: {get_fixed_calibration_value_complete(f)}")
