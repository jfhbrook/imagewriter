from typing import Dict, Literal, Self, Sequence

from imagewriter.character import CustomCharacterData
from imagewriter.encoding.base import Bytes, ctrl, esc, Esc

TOP_WIRES = True
BOTTOM_WIRES = False

TOP_WIRE_CHARACTER_WIDTHS: Dict[int, bytes] = {
    1: b"A",
    2: b"B",
    3: b"C",
    4: b"D",
    5: b"E",
    6: b"F",
    7: b"G",
    8: b"H",
    9: b"I",
    10: b"J",
    11: b"K",
    12: b"L",
    13: b"M",
    14: b"N",
    15: b"O",
    16: b"P",
}

BOTTOM_WIRE_CHARACTER_WIDTHS: Dict[int, bytes] = {
    1: b"a",
    2: b"b",
    3: b"c",
    4: b"d",
    5: b"e",
    6: b"f",
    7: b"g",
    8: b"h",
    9: b"i",
    10: b"j",
    11: b"k",
    12: b"l",
    13: b"m",
    14: b"n",
    15: b"o",
    16: b"p",
}


CharacterMaxWidth = Literal[8] | Literal[16]


class SetMaxCustomCharacterWidth(Esc):
    def __init__(self: Self, width: CharacterMaxWidth) -> None:
        assert (
            width == 8 or width == 16
        ), "Character width must be either 8 or 16 dots wide"

        self.width = width

        if width == 8:
            super().__init__("-")
        else:
            super().__init__("+")

    def __repr__(self: Self) -> str:
        return f"SetMaxCustomCharacterWidth({self.width})"


START_CUSTOM_CHARACTER_LOAD = esc("I")
STOP_CUSTOM_CHARACTER_LOAD = ctrl("D")


def pack_character_data(data: CustomCharacterData) -> bytes:
    length = (
        TOP_WIRE_CHARACTER_WIDTHS[len(data.data)]
        if data.top_wires
        else BOTTOM_WIRE_CHARACTER_WIDTHS[len(data.data)]
    )

    encoded: bytes = bytes([data.character.point]) + length + data.data

    return encoded


class LoadCustomCharacters(Bytes):
    def __init__(self: Self, character_data: Sequence[CustomCharacterData]) -> None:
        """
        Load a series of characters, as per page 96 of the ImageWriter II
        Technical Reference Manual.
        """

        self.character_data = character_data

        encoded: bytes = START_CUSTOM_CHARACTER_LOAD

        for data in character_data:
            encoded += pack_character_data(data)
        encoded += STOP_CUSTOM_CHARACTER_LOAD

        super().__init__(encoded)

    def __repr__(self: Self) -> str:
        return f"LoadCustomCharacters({self.character_data})"
