from typing import Self

from imagewriter.encoding.base import Esc


class SetCarriageReturnInsertion(Esc):
    """
    As per page 75 of the ImageWriter II Technical Reference Manual, when carriage
    return insertion is enabled, an CR (\\r) will be inserted before every LF (\\n)
    or FF (^L) character. This is enabled by default.

    Note that this does not control whether or not LF or FF will trigger printing.

    Note that this is also different from automatic LF insertion after a CR, the
    opposite behavior. This is controlled by switches, as per page 77 of the
    ImageWriter II Technical Reference Manual.
    """

    def __init__(self: Self, enabled: bool) -> None:
        self._enabled = enabled
        super().__init__("l1" if enabled else "l0")

    def __repr__(self: Self) -> str:
        return f"SetCarriageReturnInsertion({self._enabled})"


ENABLE_CARRIAGE_RETURN_INSERTION = SetCarriageReturnInsertion(True)
DISABLE_CARRIAGE_RETURN_INSERTION = SetCarriageReturnInsertion(False)
