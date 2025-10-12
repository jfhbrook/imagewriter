from enum import Enum
from typing import Dict, Self

ALTERNATE_CHARACTER_ENCODINGS: "Dict[Language, Dict[str, str]]" = dict()


def _encode_alternate_characters(characters: str, character_set: "Language") -> bytes:
    encoded = ""
    for character in characters:
        encoded += ALTERNATE_CHARACTER_ENCODINGS[character_set].get(
            character, character
        )
    return bytes(encoded, encoding="ascii")


class Language(Enum):
    """
    Languages supported by the ImageWriter II, as per the ImageWriter II
    Technical Reference Manual.
    """

    AMERICAN = "American"
    BRITISH = "British"
    GERMAN = "German"
    FRENCH = "French"
    SWEDISH = "Swedish"
    ITALIAN = "Italian"
    SPANISH = "Spanish"
    DANISH = "Danish"

    def encode(self: Self, characters: str) -> bytes:
        """
        Encode characters using an alternate character set, as per page 24 of
        the ImageWriter II Technical Reference Manual.
        """
        return _encode_alternate_characters(characters, self)


# TODO: Print a test page of alternate language characters, figure out what
# the alternate characters are, and complete this table.
ALTERNATE_CHARACTER_ENCODINGS = {
    Language.AMERICAN: dict(),
    Language.BRITISH: {"£": "#"},
    Language.GERMAN: dict(),
    Language.FRENCH: dict(),
    Language.SWEDISH: dict(),
    Language.ITALIAN: dict(),
    Language.SPANISH: dict(),
    Language.DANISH: dict(),
}
