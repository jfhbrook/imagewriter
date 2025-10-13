from enum import Enum
from typing import Dict, List

from imagewriter.encoding.base import esc


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
    TITLE_BAR = 199  # Referred to as HORIZONTAL ONE EIGHTH BLOCK in Unicode
    LEFTWARDS_ARROW = 200
    ELLIPSIS = 201
    DOWNWARDS_ARROW = 202
    UPWARDS_ARROW = 203
    UPPER_ONE_EIGHTS_BLOCK = 204  # TODO: incorrect
    CARRIAGE_RETURN = 205
    FULL_BLOCK = 206  # In "block characters" unicode block
    LEFTWARDS_ARROW_AND_UPPER_AND_LOWER_ONE_EIGHTH_BLOCK = 207
    RIGHTWARDS_ARROW_AND_UPPER_AND_LOWER_ONE_EIGHTH_BLOCK = 208
    DOWNWARDS_ARROW_AND_RIGHT_ONE_EIGHTH_BLOCK = 209
    UPWARDS_ARROW_AND_RIGHT_ONE_EIGHTH_BLOCK = 210
    ALSO_UPPER_ONE_EIGHTS_BLOCK = 211  # TODO: incorrect
    LEFT_AND_LOWER_ONE_EIGHTH_BLOCK = 212
    RIGHTWARDS_ARROW = 213
    BLOCK_2 = 214  # TODO: incorrect
    BLOCK_3 = 215  # TODO: incorrect
    LEFT_HALF_FOLDER = 216  # Paired with RIGHT_HALF_FOLDER
    RIGHT_HALF_FOLDER = 217  # Paired with LEFT_HALF_FOLDER
    RIGHT_ONE_EIGHTH_BLOCK = 218
    BLACK_DIAMOND = 219
    UPPER_AND_LOWER_ONE_EIGHTH_BLOCK = 220
    VOIDED_GREEK_CROSS = 221
    RIGHT_OPEN_SQUARED_DOT = 222
    LEFT_ONE_EIGHTH_BLOCK = 223


UNICODE_TO_MOUSETEXT: Dict[str, MouseTextCharacter] = {
    "⌛︎": MouseTextCharacter.HOURGLASS,
    "←": MouseTextCharacter.LEFTWARDS_ARROW,
    "…": MouseTextCharacter.ELLIPSIS,
    "↓": MouseTextCharacter.DOWNWARDS_ARROW,
    "↑": MouseTextCharacter.UPWARDS_ARROW,
    "↵": MouseTextCharacter.CARRIAGE_RETURN,
    "▉": MouseTextCharacter.FULL_BLOCK,
    "→": MouseTextCharacter.RIGHTWARDS_ARROW,
    "▕": MouseTextCharacter.RIGHT_ONE_EIGHTH_BLOCK,
    "◆": MouseTextCharacter.BLACK_DIAMOND,
    "▏": MouseTextCharacter.LEFT_ONE_EIGHTH_BLOCK,
}


def encode_mousetext(*text: str | MouseTextCharacter) -> bytes:
    """
    Encode a combination of text and MouseTextCharacters into valid bytes.

    Note that this function does not escape MouseText characters.
    """

    encoded: List[int] = []

    for chunk in text:
        if isinstance(chunk, str):
            for c in chunk:
                if c in UNICODE_TO_MOUSETEXT:
                    encoded.append(UNICODE_TO_MOUSETEXT[c].value)
                else:
                    encoded.append(ord(c))
        else:
            encoded.append(chunk.value)

    return bytes(encoded)


ENABLE_MAP_MOUSETEXT = esc("&")
DISABLE_MAP_MOUSETEXT = esc("$")


def map_mousetext(text: bytes) -> bytes:
    """
    Map a series of MouseText characters to low ASCII, as per page 40 of the
    ImageWriter II Technical Reference Manual.

    This is necessary if the eighth data bit is ignored.
    """

    assert all([is_mousetext(c) for c in text]), "All characters must be MouseText"

    return bytes([c - 128 for c in text])


def is_mousetext(point: int) -> bool:
    """
    Check if code point corresponds to MouseText, as per page 150 of the
    ImageWriter II Technical Reference Manual.
    """
    return 192 <= point <= 223
