"""
Classes and utilities for working with MouseText and custom characters.
"""

from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from typing import Generator, Literal, Self, Type, TypeGuard

from imagewriter.base.language import Language

CodePoint = str | bytes | int
CharacterMaxWidth = Literal[8] | Literal[16]


class CodePointError(Exception):
    """
    An error related to code point operations.
    """

    @classmethod
    @contextmanager
    def capture(cls: Type[Self]) -> Generator[None, None, None]:
        try:
            yield
        except Exception as exc:
            raise CodePointError(str(exc)) from exc


def repr_code_point(point: int) -> str:
    """
    A representation of a code point.
    """

    character = ""

    try:
        character = chr(point)
    except ValueError:
        return f"{point}"
    else:
        return f"{point} ({character!r})"


def is_low_ascii(point: int) -> bool:
    """
    Whether or not a code point is valid low ASCII.
    """

    return 32 <= point <= 126


def is_high_ascii(point: int) -> bool:
    """
    Whether or not a code point is valid high ASCII.
    """

    return 160 <= point <= 239


def is_ascii(point: int) -> bool:
    """
    Whether or not a code point is valid ASCII.
    """

    return is_low_ascii(point) or is_high_ascii(point)


def assert_low_ascii(point: int) -> None:
    """
    Assert that a code point is low ASCII.
    """
    with CodePointError.capture():
        assert is_low_ascii(
            point
        ), f"Code point {repr_code_point(point)} is not valid low ASCII"


def assert_high_ascii(point: int) -> None:
    """
    Assert that a code point is high ASCII.
    """

    with CodePointError.capture():
        assert is_high_ascii(
            point
        ), f"Code point {repr_code_point(point)} is not valid high ASCII"


def assert_ascii(point: int) -> None:
    """
    Assert that a code point is valid ASCII.
    """

    with CodePointError.capture():
        assert is_ascii(
            point
        ), f"Code point {repr_code_point(point)} is not valid ASCII"


def map_to_low_ascii(point: int) -> int:
    """
    Map a code point (either MouseText or a custom character) to low ASCII. This is
    necessary if the eighth data bit is ignored.

    For more information, see pages 40 and 45 - for MouseText and custom characters
    respectively - of the ImageWriter II Technical Reference Manual.
    """

    assert_high_ascii(point)
    return point - 128


def map_to_high_ascii(point: int) -> int:
    """
    Map a code point to high ASCII. This is necessary in character modes which map low
    ASCII to high ASCII. These modes allow for accessing high ASCII without the 8th
    data bit.

    For more information, see pages 40 and 45 - for MouseText and custom characters
    respectively - of the ImageWriter II Technical Reference Manual.
    """

    assert_low_ascii(point)
    return point + 128


def is_single_byte(point: bytes) -> bool:
    """
    Check that a code point is a single byte.
    """

    return len(point) == 1


def from_code_point(point: CodePoint) -> int:
    """
    Convert a code point to an integer value.
    """

    buffer: bytes = b""
    result: int = -1

    if isinstance(point, str):
        buffer = point.encode(encoding="ascii")
    elif isinstance(point, bytes):
        buffer = point
    else:
        result = point

    if buffer:
        assert is_single_byte(buffer)
        result = buffer[0]

    assert_ascii(result)

    return result


@dataclass
class LanguageCharacter:
    """
    A character encoded in a language. Certain non-ASCII characters are
    encoded as corresponding ASCII characters in a particular language.

    For more information, see page 42 of the ImageWriter II Technical Reference manual.
    """

    language: Language
    encoded: str


class MouseTextCharacter(Enum):
    """
    A MouseText character.

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


class Wires(Enum):
    """
    The print head has 9 wires (the part of the print head that strikes the paper).
    Only 8 of which can be used for a given custom character.

    The "top wires" are wires 1-8, and the "bottom wires" are wires 2-9.

    For more information, see page 93 of the ImageWriter II Technical Reference Manual.
    """

    TOP = "top"
    BOTTOM = "bottom"


def is_valid_max_width(width: int) -> TypeGuard[CharacterMaxWidth]:
    return width == 8 or width == 16


class CustomCharacter:
    """
    A custom character, as specified by an ASCII code point.
    """

    def __init__(self: Self, point: CodePoint) -> None:
        self.point: int = from_code_point(point)

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
    wires: Wires = Wires.TOP


Character = str | LanguageCharacter | MouseTextCharacter | CustomCharacter
Text = Character | list[Character]

__all__: list[str] = [
    "CodePoint",
    "Character",
    "Text",
    "is_low_ascii",
    "is_high_ascii",
    "assert_low_ascii",
    "assert_high_ascii",
    "map_to_low_ascii",
    "map_to_high_ascii",
    "from_code_point",
    "MouseTextCharacter",
    "CustomCharacter",
    "CustomCharacterData",
    "Wires",
    "is_valid_max_width",
]
