from typing import Dict, List, Literal, Self, Sequence, Tuple, Type

from imagewriter.encoding.base import ctrl, esc

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


class CustomCharacter:
    def __init__(self: Self, point: int) -> None:
        assert (32 <= point <= 126) or (
            160 <= point <= 239
        ), "Point must be within either low or high ASCII"
        self.point: int = point

    @classmethod
    def set_max_width(cls: Type[Self], width: Literal[8] | Literal[16]) -> bytes:
        """
        Set the max width for custom characters, as per page 85 of the
        ImageWriter II Technical Reference Manual. Note that sending such a
        command will erase existing custom characters from memory.
        """

        assert (
            width == 8 or width == 16
        ), "Character width must be either 8 or 16 dots wide"

        if width == 8:
            return esc("-")

        return esc("+")

    @classmethod
    def start_load(cls: Type[Self]) -> bytes:
        return esc("I")

    @classmethod
    def stop_load(cls: Type[Self]) -> bytes:
        return ctrl("D")

    def load_character(self: Self, data: bytes, top_wires: bool = True) -> bytes:
        length = (
            TOP_WIRE_CHARACTER_WIDTHS[len(data)]
            if top_wires
            else BOTTOM_WIRE_CHARACTER_WIDTHS[len(data)]
        )
        encoded: bytes = bytes([self.point]) + length + data

        return encoded

    @classmethod
    def load(cls: Type[Self], characters: "Sequence[CharacterData]") -> bytes:
        """
        Load a series of characters, as per page 96 of the ImageWriter II
        Technical Reference Manual.
        """

        encoded: bytes = cls.start_load()

        for char, data, top_wires in characters:
            encoded += char.load_character(data, top_wires)

        encoded += cls.stop_load()
        return encoded


CharacterData = Tuple[CustomCharacter, bytes, bool]


def character_data(
    character: CustomCharacter, data: bytes, top_wires: bool = True
) -> CharacterData:
    """
    Pack character date for loading.

    If top_wires is True, then the character will be written on the top
    8 wires (out of 9). When top_wires is False, the character will be
    written to the bottom 8 wires.

    See page 96 of the ImageWriter II Technical Reference Manual for more
    details.
    """

    return (character, data, top_wires)


CustomCharacters = CustomCharacter | List[CustomCharacter]
