from typing import Any, Self

from imagewriter.base.character import MouseTextCharacter
from imagewriter.encoding.base import Command, Esc
from imagewriter.encoding.character.base import DISABLE_MODE, Mode

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
    _M.HOURGLASS: [":hourglass:", "⏳", "⌛"],  # TODO: "⌛︎" fails to parse
    _M.CHECK_MARK: [":white_check_mark:", ":heavy_check_mark:", "✅", "✔️"],
    _M.INVERSE_CHECK_MARK: [":ballot_box_with_check:", "☑️"],
    _M.LEFTWARDS_ARROW: [":arrow_left:", "⬅️", "←"],
    _M.RIGHTWARDS_ARROW: [":arrow_right:", "➡️", "→"],
    _M.DOWNWARDS_ARROW: [":arrow_down:", "⬇️", "↓"],
    _M.UPWARDS_ARROW: [":arrow_up:", "⬆️", "↑"],
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


def mousetext_lookup(name: str) -> list[MouseTextCharacter]:
    """
    Look up a MouseText character.
    """

    return MOUSETEXT_LOOKUP[name]


class EnableMouseTextMappingMode(Esc):
    """
    Enable MouseText mapping mode. In this mode, low ascii is mapped to the high ascii
    points that typically encode MouseText.
    """

    def __init__(self: Self) -> None:
        super().__init__("&")

    def __repr__(self: Self) -> str:
        return "EnableMouseTextMappingMode()"


ENABLE_MOUSE_TEXT_MAPPING_MODE = EnableMouseTextMappingMode()


class MouseTextMode(Mode):
    """
    A MouseText mode. Supports mapping to high ASCII, otherwise a no-op.
    """

    def __init__(self, map: bool = True) -> None:
        self.map: bool = map

    def enable(self: Self) -> list[Command]:
        return [ENABLE_MOUSE_TEXT_MAPPING_MODE] if self.map else list()

    def disable(self: Self) -> list[Command]:
        return [DISABLE_MODE] if self.map else list()

    def __eq__(self: Self, other: Any) -> bool:
        return isinstance(other, MouseTextMode) and self.map == other.map
