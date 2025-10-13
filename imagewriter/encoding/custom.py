from typing import Self

from imagewriter.encoding.base import esc

ENABLE_CUSTOM_CHARACTER = esc("'")
ENABLE_MAP_CUSTOM_CHARACTER = esc("*")


class CustomCharacter:
    def __init__(self: Self, point: int) -> None:
        assert (32 <= point <= 126) or (
            160 <= point <= 239
        ), "Point must be within either low or high ASCII"
        self.point: int = point


# TODO: Mapping mousetext is the same as mapping custom characters
