"""
Print quality settings for the ImageWriter II. Higher print qualities look better on
the page, but are slower to print and use more ribbon.
"""

from enum import Enum
from typing import Self


class Quality(Enum):
    """
    A Print-Quality Font, as per page 39 of the ImageWriter II Technical
    Reference Manual. There are three font qualities, listed from lowest to highest:

    * draft
    * correspondence
    * near letter quality (or NLQ)

    The default quality is "draft". This may either be set with the print quality
    button on the printer, or through software.

    Different qualities print at different speeds:

    | Name                | Print Speed (CPS) |
    |---------------------|-------------------|
    | draft               | 250               |
    | correspondence      | 180               |
    | near letter quality |  45               |

    Note that boldface, double-width, half-height, subscript, superscript
    and proportional printing will always print at the Correspondence quality
    setting.
    """

    DRAFT = "1"
    CORRESPONDENCE = "0"
    NEAR_LETTER_QUALITY = "2"

    @property
    def print_speed(self: Self) -> int:
        """
        Print speed, in characters per second.
        """

        return {
            Quality.NEAR_LETTER_QUALITY: 45,
            Quality.CORRESPONDENCE: 180,
            Quality.DRAFT: 250,
        }[self]
