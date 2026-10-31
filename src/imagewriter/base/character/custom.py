"""
The ImageWriter II supports custom characters, sent to the printer by the user. These
custom characters may then be printed with a set of special modes.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Literal, Self, TypeGuard

from imagewriter.base.character.code_point import CodePoint, from_code_point
from imagewriter.base.character.repr import repr_code_point

CharacterMaxWidth = Literal[8, 16]


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
        return f"CustomCharacter({repr_code_point(self.point)})"


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
