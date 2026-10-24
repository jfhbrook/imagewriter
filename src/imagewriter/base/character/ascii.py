from imagewriter.base.character.error import CodePointError
from imagewriter.base.character.repr import repr_code_point


def is_low_ascii(point: int) -> bool:
    """
    Whether or not a code point is valid low ASCII.
    """

    return 32 <= point <= 126


def is_high_ascii(point: int) -> bool:
    """
    Whether or not a code point is valid high ASCII.
    """

    return 160 <= point <= 239


def is_ascii(point: int) -> bool:
    """
    Whether or not a code point is valid ASCII.
    """

    return is_low_ascii(point) or is_high_ascii(point)


def assert_low_ascii(point: int) -> None:
    """
    Assert that a code point is low ASCII.
    """
    with CodePointError.capture():
        assert is_low_ascii(
            point
        ), f"Code point {repr_code_point(point)} is not valid low ASCII"


def assert_high_ascii(point: int) -> None:
    """
    Assert that a code point is high ASCII.
    """

    with CodePointError.capture():
        assert is_high_ascii(
            point
        ), f"Code point {repr_code_point(point)} is not valid high ASCII"


def assert_ascii(point: int) -> None:
    """
    Assert that a code point is valid ASCII.
    """

    with CodePointError.capture():
        assert is_ascii(
            point
        ), f"Code point {repr_code_point(point)} is not valid ASCII"


def map_to_low_ascii(point: int) -> int:
    """
    Map a code point (either MouseText or a custom character) to low ASCII. This is
    necessary if the eighth data bit is ignored.

    For more information, see pages 40 and 45 - for MouseText and custom characters
    respectively - of the ImageWriter II Technical Reference Manual.
    """

    assert_high_ascii(point)
    return point - 128


def map_to_high_ascii(point: int) -> int:
    """
    Map a code point to high ASCII. This is necessary in character modes which map low
    ASCII to high ASCII. These modes allow for accessing high ASCII without the 8th
    data bit.

    For more information, see pages 40 and 45 - for MouseText and custom characters
    respectively - of the ImageWriter II Technical Reference Manual.
    """

    assert_low_ascii(point)
    return point + 128
