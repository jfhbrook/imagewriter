from imagewriter.encoding.attributes import Pitch
from imagewriter.encoding.base import esc, format_number
from imagewriter.encoding.distance import Distance, Inch

LINE_WIDTH = Inch(8)


def set_left_margin(distance: Distance | int, pitch: Pitch) -> bytes:
    """
    Set the left margin, as per page 59 of the ImageWriter II Technical
    Reference Manual.
    """

    conversion: float = (pitch.characters_per_line - 1) / LINE_WIDTH.inches
    set_to: int = 0

    if isinstance(distance, Distance):
        set_to = int(distance.inches * conversion)
    else:
        set_to = distance

    set_to = min(set_to, pitch.characters_per_line - 1)

    return esc("L", format_number(set_to, 3))
