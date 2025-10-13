from imagewriter.encoding.attributes import Pitch
from imagewriter.encoding.base import esc, format_number
from imagewriter.encoding.length import Inch, Length

LINE_WIDTH = Inch(8)
LENGTH_CONVERSION = 144  # Units per inch


def set_left_margin(width: Length | int, pitch: Pitch) -> bytes:
    """
    Set the left margin, as per page 59 of the ImageWriter II Technical
    Reference Manual.
    """

    conversion: float = (pitch.characters_per_line - 1) / LINE_WIDTH.inches
    set_to: int = 0

    if isinstance(width, Length):
        set_to = int(width.inches * conversion)
    else:
        set_to = width

    set_to = min(set_to, pitch.characters_per_line - 1)

    return esc("L", format_number(set_to, 3))


def set_page_length(length: Length | int) -> bytes:
    """
    Set the page length, as per page 61 of the ImageWriter II Technical
    Reference Manual.
    """

    set_to: int = 0

    if isinstance(length, Length):
        set_to = int(length.inches) * LENGTH_CONVERSION
    else:
        set_to = length

    return esc("H", format_number(set_to, 4))
