from enum import Enum
from typing import Dict, Self

ENCODINGS: "Dict[Language, Dict[str, str]]" = dict()


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

        encoded = ""
        for character in characters:
            encoded += ENCODINGS[self].get(character, character)
        return bytes(encoded, encoding="ascii")


# TODO: Print a test page of alternate language characters, figure out what
# the alternate characters are, and complete this table.

ENCODINGS = {
    Language.AMERICAN: dict(),
    Language.BRITISH: {"£": "#"},
    Language.GERMAN: dict(),
    Language.FRENCH: dict(),
    Language.SWEDISH: dict(),
    Language.ITALIAN: dict(),
    Language.SPANISH: dict(),
    Language.DANISH: dict(),
}
