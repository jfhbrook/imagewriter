from imagewriter.encoding.base import esc, format_number
from imagewriter.encoding.pitch import Pitch
from imagewriter.encoding.units import Length, length_to_int


def set_left_margin(width: Length, pitch: Pitch) -> bytes:
    """
    Set the left margin, as per page 59 of the ImageWriter II Technical
    Reference Manual.
    """

    set_to: int = length_to_int(width, lambda w: w.characters(pitch))

    return esc("L", format_number(set_to, 3))


def set_page_length(length: Length) -> bytes:
    """
    Set the page length, as per page 61 of the ImageWriter II Technical
    Reference Manual.
    """

    set_to: int = length_to_int(length, lambda lg: lg.vertical)

    return esc("H", format_number(set_to, 4))
