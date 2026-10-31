from typing import Self

from imagewriter.base.character import MouseTextCharacter
from imagewriter.encoding.base import Command, Esc
from imagewriter.encoding.character.base import DISABLE_MODE, Mode

_M = MouseTextCharacter

# Lookup for codes that parse to MouseText
MOUSETEXT_CODE_LOOKUP: dict[str, list[MouseTextCharacter]] = {
    ":folder:": [_M.LEFT_HALF_FOLDER, _M.RIGHT_HALF_FOLDER],
    ":squared_dot:": [_M.RIGHT_ONE_EIGHT_BLOCK, _M.RIGHT_OPEN_SQUARED_DOT],
}

# Lookup for emojis/symbols to MouseText
MOUSETEXT_LOOKUP: dict[str, list[MouseTextCharacter]] = {
    # Codes which require multiple mousetext characters
    "📁": [_M.LEFT_HALF_FOLDER, _M.RIGHT_HALF_FOLDER],
    "⊡": [_M.RIGHT_ONE_EIGHT_BLOCK, _M.RIGHT_OPEN_SQUARED_DOT],
    "🮼": [_M.RIGHT_OPEN_SQUARED_DOT],
}

# Emoji codes which correspond to a given MouseText character
MOUSETEXT_EMOJI_CODES: dict[MouseTextCharacter, list[str]] = {
    _M.DARK_APPLE: [":dark_apple:"],
    _M.LIGHT_APPLE: [":light_apple:"],
    _M.HOURGLASS: [":hourglass:"],
    _M.CHECK_MARK: [":white_check_mark:", ":heavy_check_mark:"],
    _M.INVERSE_CHECK_MARK: [":ballot_box_with_check:"],
    _M.LEFTWARDS_ARROW: [":arrow_left:"],
    _M.RIGHTWARDS_ARROW: [":arrow_right:"],
    _M.DOWNWARDS_ARROW: [":arrow_down:"],
    _M.UPWARDS_ARROW: [":arrow_up:"],
}

# Emojis which correspond to a given MouseText character
MOUSETEXT_EMOJIS: dict[MouseTextCharacter, list[str]] = {
    _M.DARK_APPLE: ["🍎"],
    _M.LIGHT_APPLE: ["🍏"],
    _M.HOURGLASS: ["⏳", "⌛"],  # TODO: "⌛︎" fails to parse
    _M.CHECK_MARK: ["✅", "✔️"],
    _M.INVERSE_CHECK_MARK: ["☑️"],
    _M.LEFTWARDS_ARROW: ["⬅️", "←"],
    _M.RIGHTWARDS_ARROW: ["➡️", "→"],
    _M.DOWNWARDS_ARROW: ["⬇️", "↓"],
    _M.UPWARDS_ARROW: ["⬆️", "↑"],
}

MOUSETEXT_SMART_TEXT: dict[MouseTextCharacter, list[str]] = {_M.ELLIPSIS: ["…"]}

MOUSETEXT_SYMBOL_CODES: dict[MouseTextCharacter, list[str]] = {
    _M.ARROWHEAD_SHAPED_POINTER: [":pointer:"],
    _M.TITLE_BAR: [":title_bar:"],
    _M.CARRIAGE_RETURN: [":cr:", ":carriage_return:"],
    _M.BLACK_DIAMOND: [":diamond:", ":black_diamond:"],
    _M.VOIDED_GREEK_CROSS: [":greek_cross:"],
}

MOUSETEXT_SYMBOLS: dict[MouseTextCharacter, list[str]] = {
    _M.ARROWHEAD_SHAPED_POINTER: ["🮰"],
    _M.TITLE_BAR: ["🮁"],
    _M.CARRIAGE_RETURN: ["↵", "⏎"],
    _M.BLACK_DIAMOND: ["◆"],
    _M.VOIDED_GREEK_CROSS: ["✙"],
}

MOUSETEXT_BLOCKS: dict[MouseTextCharacter, list[str]] = {
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

# Populate the actual lookups
for block in [MOUSETEXT_EMOJI_CODES, MOUSETEXT_SYMBOL_CODES]:
    for char, codes in block.items():
        for name in codes:
            MOUSETEXT_CODE_LOOKUP[name] = [char]

for block in [
    MOUSETEXT_EMOJIS,
    MOUSETEXT_SMART_TEXT,
    MOUSETEXT_SYMBOLS,
    MOUSETEXT_BLOCKS,
]:
    for char, codes in block.items():
        for name in codes:
            MOUSETEXT_LOOKUP[name] = [char]


def mousetext_lookup(name: str) -> list[MouseTextCharacter]:
    """
    Look up a MouseText character.
    """

    try:
        return MOUSETEXT_LOOKUP[name]
    except KeyError as exc:
        try:
            return MOUSETEXT_CODE_LOOKUP[name]
        except Exception as code_exc:
            raise code_exc from exc


class EnableMouseTextMappingMode(Esc):
    """
    Enable MouseText mapping mode. In this mode, low ascii is mapped to the high ascii
    points that typically encode MouseText.

    For more information, see page 41 of the ImageWriter II Technical Reference Manual.
    """

    def __init__(self: Self) -> None:
        super().__init__("&")

    def __repr__(self: Self) -> str:
        return "EnableMouseTextMappingMode()"


ENABLE_MOUSETEXT_MAPPING_MODE = EnableMouseTextMappingMode()


class MouseTextMode(Mode):
    """
    A MouseText mode.

    MouseText is available in the standard mode as high ASCII. However, MouseText also
    supports a mode that maps low ASCII to high ASCII by adding 128 (0x80) to the code
    point.

    For more information, see page 41 of the ImageWriter II Technical Reference Manual.
    """

    def __init__(self, map_ascii: bool = False) -> None:
        self.map_ascii: bool = map_ascii

    def enable(self: Self) -> list[Command]:
        if self.map_ascii:
            return [ENABLE_MOUSETEXT_MAPPING_MODE]

        return []

    def disable(self: Self) -> list[Command]:
        if self.map_ascii:
            return [DISABLE_MODE]
        return []

    def __eq__(self: Self, other: object) -> bool:
        return isinstance(other, MouseTextMode) and self.map_ascii == other.map_ascii
