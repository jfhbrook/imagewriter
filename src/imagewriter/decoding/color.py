from imagewriter.base.color import Color
from imagewriter.decoding.base import esc, number
from imagewriter.encoding.color import SetColor


def _map_color(n: int) -> SetColor:
    return SetColor(Color[str(n)])


set_color = esc("K") >> number(1).map(_map_color)
