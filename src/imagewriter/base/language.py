from enum import Enum


class Language(Enum):
    """
    Languages supported by the ImageWriter II.

    Switch settings are documented in Chapters 1 and 2 of the ImageWriter II
    Technical Reference Manual. Alternate language characters are documented on page
    42 of the ImageWriter II Technical Reference manual.
    """

    AMERICAN = "American"
    BRITISH = "British"
    GERMAN = "German"
    FRENCH = "French"
    SWEDISH = "Swedish"
    ITALIAN = "Italian"
    SPANISH = "Spanish"
    DANISH = "Danish"
