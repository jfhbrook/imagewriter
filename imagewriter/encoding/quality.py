from typing import Self

from imagewriter.encoding.base import Esc
from imagewriter.quality import Quality


def _quality_code(quality: Quality, scribe_mode: bool) -> str:
    if scribe_mode:
        if quality == Quality.CORRESPONDENCE:
            return "m"
        if quality == Quality.NEAR_LETTER_QUALITY:
            return "M"

    return "a" + quality.value


class SelectQuality(Esc):
    """
    Select a Print-Quality Font, as per page 39 of the ImageWriter II
    Technical Reference Manual.

    This command includes support for Scribe compatibility mode, in the
    interest of completeness.
    """

    def __init__(self: Self, quality: Quality, scribe_mode: bool = False) -> None:
        self._quality = quality
        self._scribe_mode = scribe_mode

        super().__init__(_quality_code(quality, scribe_mode))

    def __repr__(self: Self) -> str:
        return f"SelectQuality({self._quality}, scribe_mode={self._scribe_mode})"
