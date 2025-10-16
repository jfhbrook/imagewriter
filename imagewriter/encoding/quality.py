from imagewriter.encoding.base import Command, Esc
from imagewriter.quality import Quality


def select_quality(quality: Quality, scribe_mode=False) -> Command:
    """
    Select a Print-Quality Font, as per page 39 of the ImageWriter II
    Technical Reference Manual.

    This function includes support for Scribe compatibility mode, in the
    interest of completeness.
    """

    if scribe_mode:
        if quality == Quality.CORRESPONDENCE:
            return Esc("m")
        if quality == Quality.NEAR_LETTER_QUALITY:
            return Esc("M")

    return Esc("a" + quality.value)
