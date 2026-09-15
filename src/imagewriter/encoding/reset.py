from typing import Self

from imagewriter.encoding.base import Esc


class Reset(Esc):
    """
    Resetting the printer will do the following:

    * Print all data currently in the print buffer
    * Clear the print buffer
    * Reset switches and other configuration to their defaults
    * Clear custom characters

    See page 87 of the ImageWriter II Technical Reference Manual for more details.
    """

    def __init__(self: Self) -> None:
        super().__init__("c")

    def __repr__(self: Self) -> str:
        return "Reset()"


RESET = Reset()
