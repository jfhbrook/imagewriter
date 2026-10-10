"""
Classes and utilities for working with MouseText and custom characters.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Self, Type


def map_to_low_ascii(point: int) -> int:
    """
    Map a code point (either MouseText or a custom character) to low ASCII, as
    per page 40 (MouseText) and page 45 (custom characters) of the ImageWriter
    II Technical Reference Manual.

    This is necessary if the eighth data bit is ignored.
    """

    assert 160 <= point <= 239, "Code point is not valid upper ASCII"
    return point - 128


def map_to_high_ascii(point: int) -> int:
    """
    Map a code point to high ascii.
    """

    assert point < 160, "Code point is already upper ASCII"
    return point + 128


class MouseTextCharacter(Enum):
    """
    MouseText characters.

    Many of these characters are included in the Symbols for Legacy Computing
    Unicode block:

    <https://www.unicode.org/charts/PDF/U1FB00.pdf>

    However, some of them suffer from false unification issues:

    https://www.unicode.org/L2/L2025/25037-legacy-box-drawing-disunification.pdf
    """

    DARK_APPLE = 192
    LIGHT_APPLE = 193
    ARROWHEAD_SHAPED_POINTER = 194
    HOURGLASS = 195
    CHECK_MARK = 196
    INVERSE_CHECK_MARK = 197
    DOWNWARDS_ARROW_WITH_TIP_LEFTWARDS = 198
    # As in the UI element on a classic Mac - Referred to as HORIZONTAL ONE EIGHTH
    # BLOCK in Unicode
    TITLE_BAR = 199
    LEFTWARDS_ARROW = 200
    ELLIPSIS = 201
    DOWNWARDS_ARROW = 202
    UPWARDS_ARROW = 203
    UPPER_RIGHT_ONE_EIGHT_BLOCK = 204
    CARRIAGE_RETURN = 205
    FULL_BLOCK = 206  # In "block characters" unicode block
    LEFTWARDS_ARROW_AND_UPPER_AND_LOWER_ONE_EIGHT_BLOCK = 207
    RIGHTWARDS_ARROW_AND_UPPER_AND_LOWER_ONE_EIGHT_BLOCK = 208
    DOWNWARDS_ARROW_AND_RIGHT_ONE_EIGHT_BLOCK = 209
    UPWARDS_ARROW_AND_RIGHT_ONE_EIGHT_BLOCK = 210
    UPPER_ONE_EIGHT_BLOCK = 211
    LEFT_AND_LOWER_ONE_EIGHT_BLOCK = 212
    RIGHTWARDS_ARROW = 213
    MEDIUM_SHADE = 214
    DARK_SHADE = 215
    LEFT_HALF_FOLDER = 216  # Paired with RIGHT_HALF_FOLDER
    RIGHT_HALF_FOLDER = 217  # Paired with LEFT_HALF_FOLDER
    RIGHT_ONE_EIGHT_BLOCK = 218
    BLACK_DIAMOND = 219
    LOWER_ONE_EIGHT_BLOCK = 220
    VOIDED_GREEK_CROSS = 221
    RIGHT_OPEN_SQUARED_DOT = 222
    LEFT_ONE_EIGHT_BLOCK = 223

    @classmethod
    def parse(
        cls: Type[Self], unicode: str
    ) -> tuple[list[MouseTextCharacter] | None, str]:
        for name in MOUSETEXT_LOOKUP.keys():
            if unicode.startswith(name):
                return MOUSETEXT_LOOKUP[name], unicode[len(name) :]

        return None, unicode


_M = MouseTextCharacter

# The full lookup from name to mousetext characters
MOUSETEXT_LOOKUP: dict[str, list[MouseTextCharacter]] = {
    # Codes which require multiple mousetext characters
    ":folder:": [_M.LEFT_HALF_FOLDER, _M.RIGHT_HALF_FOLDER],
    "📁": [_M.LEFT_HALF_FOLDER, _M.RIGHT_HALF_FOLDER],
    ":squared_dot:": [_M.RIGHT_ONE_EIGHT_BLOCK, _M.RIGHT_OPEN_SQUARED_DOT],
    "⊡": [_M.RIGHT_ONE_EIGHT_BLOCK, _M.RIGHT_OPEN_SQUARED_DOT],
    "🮼": [_M.RIGHT_OPEN_SQUARED_DOT],
}

# Characters and codes which correspond to a given mousetect character

MOUSETEXT_EMOJI_CODES: dict[MouseTextCharacter, list[str]] = {
    _M.DARK_APPLE: [":dark_apple:", "🍎"],
    _M.LIGHT_APPLE: [":light_apple:", "🍏"],
    _M.HOURGLASS: [":hourglass:", "⏳", "⌛"],
    _M.CHECK_MARK: [":white_check_mark:", ":heavy_check_mark:", "✅", "✔️"],
    _M.INVERSE_CHECK_MARK: [":ballot_box_with_check:", "☑️"],
    _M.LEFTWARDS_ARROW: [":arrow_left:", "⬅️"],
    _M.RIGHTWARDS_ARROW: [":arrow_right:", "➡️"],
    _M.DOWNWARDS_ARROW: [":arrow_down:", "⬇️"],
    _M.UPWARDS_ARROW: [":arrow_up:", "⬆️"],
}

MOUSETEXT_SMART_TEXT_CODES: dict[MouseTextCharacter, list[str]] = {_M.ELLIPSIS: ["…"]}

MOUSETEXT_SYMBOL_CODES: dict[MouseTextCharacter, list[str]] = {
    _M.ARROWHEAD_SHAPED_POINTER: [":pointer:", "🮰"],
    _M.TITLE_BAR: [":title_bar:", "🮁"],
    _M.CARRIAGE_RETURN: [":cr:", ":carriage_return:", "↵", "⏎"],
    _M.BLACK_DIAMOND: [":diamond:", ":black_diamond:", "◆"],
    _M.VOIDED_GREEK_CROSS: [":greek_cross:", "✙"],
}

MOUSETEXT_BLOCK_CODES: dict[MouseTextCharacter, list[str]] = {
    _M.FULL_BLOCK: ["█"],
    _M.UPPER_ONE_EIGHT_BLOCK: ["▔"],
    _M.LEFT_AND_LOWER_ONE_EIGHT_BLOCK: ["▙"],
    _M.MEDIUM_SHADE: ["▒"],
    _M.DARK_SHADE: ["▓"],
    _M.RIGHT_ONE_EIGHT_BLOCK: ["▕"],
    _M.LOWER_ONE_EIGHT_BLOCK: ["▁"],
    _M.LEFT_ONE_EIGHT_BLOCK: ["▏"],
    _M.LEFTWARDS_ARROW_AND_UPPER_AND_LOWER_ONE_EIGHT_BLOCK: ["🮵"],
    _M.RIGHTWARDS_ARROW_AND_UPPER_AND_LOWER_ONE_EIGHT_BLOCK: ["🮶"],
    _M.DOWNWARDS_ARROW_AND_RIGHT_ONE_EIGHT_BLOCK: ["🮷"],
    _M.UPWARDS_ARROW_AND_RIGHT_ONE_EIGHT_BLOCK: ["🮸"],
}

# Populate the actual lookup
for block in [
    MOUSETEXT_EMOJI_CODES,
    MOUSETEXT_SMART_TEXT_CODES,
    MOUSETEXT_SYMBOL_CODES,
    MOUSETEXT_BLOCK_CODES,
]:
    for char, codes in block.items():
        for name in codes:
            MOUSETEXT_LOOKUP[name] = [char]


class CustomCharacter:
    """
    A custom character.
    """

    def __init__(self: Self, point: str | bytes | int) -> None:
        if isinstance(point, str):
            buffer: bytes = b""
            buffer = point.encode(encoding="ascii")
            assert len(buffer) == 1, f"Invalid character {point}"
            self.point = buffer[0]
        elif isinstance(point, bytes):
            self.point = point[0]
        elif isinstance(point, int):
            self.point = point
        else:
            assert False, f"Unknown type {type(point)}"

        if self.point < 160:
            self.point = map_to_high_ascii(self.point)

        assert 160 <= self.point <= 239, "Point must be valid ASCII"

    def __repr__(self: Self) -> str:
        return f"CustomCharacter({self.point})"


@dataclass
class CustomCharacterData:
    """
    Custom character data.

    If top_wires is True, then the character will be written on the top
    8 wires (out of 9). When top_wires is False, the character will be
    written to the bottom 8 wires.

    See page 96 of the ImageWriter II Technical Reference Manual for more
    details.
    """

    character: CustomCharacter
    data: bytes
    top_wires: bool = True


Character = str | MouseTextCharacter | CustomCharacter
Text = Character | list[Character]
