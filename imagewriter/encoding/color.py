from imagewriter.color import Color
from imagewriter.encoding.base import Bytes, Command, esc


def set_color(color: Color) -> Command:
    return Bytes(esc("K") + color.code.encode(encoding="ascii"))
