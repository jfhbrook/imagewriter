from enum import Enum


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
