from enum import Enum
from typing import Self

from imagewriter.encoding.base import Esc, Packet


class Quality(Enum):
    """
    A Print-Quality Font, as per page 39 of the ImageWriter II Technical
    Reference Manual. Lower quality fonts print more quickly.

    Note that boldface, double-width, half-height, subscript, superscript
    and proportional printing will always print at the Correspondence quality
    setting.
    """

    CORRESPONDENCE = "0"
    DRAFT = "1"
    NEAR_LETTER_QUALITY = "2"  # or "NLQ"

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

    def select(self: Self) -> Packet:
        """
        Select a Print-Quality Font, as per page 39 of the ImageWriter II
        Technical Reference Manual.
        """

        return Esc("a" + self.value)

    def select_scribe(self: Self) -> Packet:
        """
        Select a Print-Quality Font, using the Scribe compatibility modes, as
        per page 39 of the ImageWriter II Technical Reference Manual.

        This method is included in the interest of completeness.
        """

        if self == Quality.CORRESPONDENCE:
            return Esc("m")
        elif self == Quality.NEAR_LETTER_QUALITY:
            return Esc("M")
        else:
            return self.select()
