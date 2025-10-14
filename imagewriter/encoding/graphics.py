from imagewriter.encoding.base import esc, format_number
from imagewriter.encoding.motion import LineFeed
from imagewriter.encoding.units import Point


def print_graphics_data(data: bytes) -> bytes:
    """
    Print graphics data, as per page 105 of the ImageWriter II Technical
    Reference Manual.
    """

    length: int = len(data)
    encoded: bytes = b""

    if length % 8 == 0:
        encoded = esc("g", format_number(length // 8, 3))
    else:
        encoded = esc("G", format_number(length, 4))

    encoded += data

    return encoded


def set_graphics_distance_between_lines() -> bytes:
    """
    Set the distance between lines such that two adjacent graphics lines are
    flush with each other, given the pitch.

    See page 112 of the ImageWriter II Technical Reference Manual for more
    details.
    """

    return LineFeed.set_distance_between_lines(Point(1))
