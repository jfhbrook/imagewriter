from parsy import any_char, seq  # type: ignore

from imagewriter.decoding.base import esc, number
from imagewriter.encoding.repeat import Repeat


def _map_repeat(repeat: tuple[bytes, int]) -> Repeat:
    character = repeat[0].decode(encoding="ascii")
    n = repeat[1]
    return Repeat(character, n)


repeat = esc("R") >> seq(any_char, number(3)).map(_map_repeat)
