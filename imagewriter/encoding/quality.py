from enum import Enum
from typing import Self

from imagewriter.encoding.base import esc


class PrintQuality(Enum):
    """
    A Print-Quality Font, as per page 39 of the ImageWriter II Technical
    Reference Manual. Lower quality fonts print more quickly.

    | Font                      | Print Speed |
    |---------------------------|-------------|
    | NLQ (Near Letter Quality) |      45 CPS |
    | Correspondence            |     180 CPS |
    | Draft                     |     250 CPS |

    Note that boldface, double-width, half-height, subscript, superscript
    and proportional printing will always print at the Correspondence quality
    setting.
    """

    CORRESPONDENCE = "0"
    DRAFT = "1"
    NLQ = "2"

    def select(self: Self) -> bytes:
        """
        Select a Print-Quality Font, as per page 39 of the ImageWriter II
        Technical Reference Manual.
        """

        return esc("a", self.value)

    def select_scribe(self: Self) -> bytes:
        """
        Select a Print-Quality Font, using the Scribe compatibility modes, as
        per page 39 of the ImageWriter II Technical Reference Manual.

        This method is included in the interest of completeness.
        """

        if self == PrintQuality.CORRESPONDENCE:
            return esc("m")
        elif self == PrintQuality.NLQ:
            return esc("M")
        else:
            return self.select()
