"""
Languages on the ImageWriter II correspond to localized fonts. For example, the
"British" language allows the ImageWriter II to print the "£" symbol. These alternate
language characters are documented on page 42 of the ImageWriter II Technical Reference
manual.

Languages are configured through switch settings, documented in Chapters 1 and 2 of the
ImageWriter II Technical Reference Manual.
"""

from dataclasses import dataclass
from enum import Enum


class Language(Enum):
    """
    Languages supported by the ImageWriter II.

    Switch settings are documented in Chapters 1 and 2 of the ImageWriter II
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


@dataclass
class LanguageCharacter:
    """
    A character encoded in a language.
    """

    language: Language
    encoded: str
