"""
Classes and utilities for working with MouseText and custom characters.
"""

from imagewriter.base.character.ascii import (
    assert_ascii,
    assert_high_ascii,
    assert_low_ascii,
    is_ascii,
    is_high_ascii,
    is_low_ascii,
    map_to_high_ascii,
    map_to_low_ascii,
)
from imagewriter.base.character.code_point import CodePoint
from imagewriter.base.character.custom import (
    CharacterMaxWidth,
    CustomCharacter,
    CustomCharacterData,
    is_valid_max_width,
    Wires,
)
from imagewriter.base.character.error import CharacterError, CodePointError
from imagewriter.base.character.language import Language, LanguageCharacter
from imagewriter.base.character.mousetext import MouseTextCharacter
from imagewriter.base.character.repr import repr_code_point

Character = str | LanguageCharacter | MouseTextCharacter | CustomCharacter
Text = Character | list[Character]

__all__ = [
    "Character",
    "CharacterError",
    "CharacterMaxWidth",
    "CodePoint",
    "CodePointError",
    "CustomCharacter",
    "CustomCharacterData",
    "Language",
    "LanguageCharacter",
    "Text",
    "Wires",
    "assert_ascii",
    "assert_high_ascii",
    "assert_low_ascii",
    "is_ascii",
    "is_high_ascii",
    "is_low_ascii",
    "is_valid_max_width",
    "map_to_high_ascii",
    "map_to_low_ascii",
    "repr_code_point",
]
