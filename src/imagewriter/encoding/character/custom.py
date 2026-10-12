"""
Custom character encoding.

For more information, see page 92 of the ImageWriter II Technical Reference Manual.
"""

from typing import Any, Self, Sequence

from imagewriter.base.character import (
    CharacterMaxWidth,
    CustomCharacterData,
    is_valid_max_width,
    Wires,
)
from imagewriter.encoding.base import Bytes, Command, ctrl, esc, Esc
from imagewriter.encoding.character.base import DISABLE_MODE, Mode

CUSTOM_CHARACTER_WIDTH_CODES: dict[Wires, dict[int, bytes]] = {
    Wires.TOP: {
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
    },
    Wires.BOTTOM: {
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
    },
}


def character_width_code(wires: Wires, width: int) -> bytes:
    """
    When encoding custom characters, a special width code is used to tell the printer
    how wide the character is. This code depends on both the wires used and the actual
    character width.

    For more information, see Table 7-2 from page 97 of the ImageWriter II Technical
    Reference Manual.
    """
    return CUSTOM_CHARACTER_WIDTH_CODES[wires][width]


SET_WIDTH_ESCAPE_CODE: dict[CharacterMaxWidth, str] = {8: "-", 16: "+"}


class SetMaxCustomCharacterWidth(Esc):
    """
    Set the maximum custom character width. The ImageWriter II supports widths of
    either 8 or 16.

    For more information, see page 95 of the ImageWriter II Technical Reference Manual.
    """

    def __init__(self: Self, width: CharacterMaxWidth) -> None:
        assert is_valid_max_width(
            width
        ), "Character width must be either 8 or 16 dots wide"

        self.width: CharacterMaxWidth = width

        super().__init__(SET_WIDTH_ESCAPE_CODE[width])

    def __repr__(self: Self) -> str:
        return f"SetMaxCustomCharacterWidth({self.width})"


START_CUSTOM_CHARACTER_LOAD = esc("I")
STOP_CUSTOM_CHARACTER_LOAD = ctrl("D")


def pack_custom_character_data(data: CustomCharacterData) -> bytes:
    """
    Pack custom character data, as per page 95 of the ImageWriter II Technical
    Reference Manual.
    """

    width = character_width_code(data.wires, len(data.data))

    encoded: bytes = bytes([data.character.point]) + width + data.data

    return encoded


def load_custom_characters(characters: Sequence[CustomCharacterData]) -> bytes:
    """
    Load multiple custom characters onto the ImageWriter II, as per page 95 of the
    ImageWriter II Technical Reference Manual.
    """

    encoded: bytes = START_CUSTOM_CHARACTER_LOAD

    for data in characters:
        encoded += pack_custom_character_data(data)

    encoded += STOP_CUSTOM_CHARACTER_LOAD

    return encoded


class LoadCustomCharacters(Bytes):
    def __init__(self: Self, characters: Sequence[CustomCharacterData]) -> None:
        """
        Load a series of characters, as per page 96 of the ImageWriter II
        Technical Reference Manual.
        """

        self.characters: list[CustomCharacterData] = list(characters)

        encoded: bytes = load_custom_characters(characters)

        super().__init__(encoded)

    def __repr__(self: Self) -> str:
        return f"LoadCustomCharacters({self.characters})"


STANDARD_MODE = "'"
HIGH_ASCII_MODE = "*"


class EnableCustomCharacterMode(Esc):
    """
    Enable a custom character mode.

    Custom characters support two modes: standard and high ASCII mode.

    In standard mode, characters assigned to both low ASCII (decimal values 32-126)
    and high ASCII (decimal values 160-239) are used. This mode is able to access the
    whole range of custom characters, but requires access to the 8th data bit.

    In high ASCII mode, low ASCII code points are mapped to high ASCII by adding 128 (0x80) to the sent code point. This allows for use of high ASCII characters without using the 8th data bit.

    For more information on these modes, see page 99 of the ImageWriter II Technical
    Reference Manual.
    """

    def __init__(self: Self, high_ascii: bool = False) -> None:
        self.high_ascii: bool = high_ascii
        super().__init__(HIGH_ASCII_MODE if high_ascii else STANDARD_MODE)

    def __repr__(self: Self) -> str:
        return f"EnableCustomCharacterMode(high_ascii={self.high_ascii})"


class CustomCharacterMode(Mode):
    """
    A custom character mode.
    """

    def __init__(self: Self, high_ascii: bool = False) -> None:
        self.high_ascii: bool = high_ascii

    def enable(self: Self) -> list[Command]:
        return [EnableCustomCharacterMode(self.high_ascii)]

    def disable(self: Self) -> list[Command]:
        return [DISABLE_MODE]

    def __eq__(self: Self, other: Any) -> bool:
        return (
            isinstance(other, CustomCharacterMode)
            and self.high_ascii == other.high_ascii
        )
