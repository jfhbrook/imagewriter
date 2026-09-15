from typing import Self

from imagewriter.encoding.base import Esc

"""
Control of the paper-out sensor, as per page 74 of the ImageWriter II
Technical Reference Manual.

When enabled (the default), if the printer runs out of paper, the error light
will come on and the printer will become deselected.

Note that installing a SheetFeeder will change the behavior to trigger sheet
feeds.
"""


class SetPaperOutSensor(Esc):
    def __init__(self: Self, enabled: bool) -> None:
        self.enabled = enabled

        super().__init__("O" if enabled else "o")

    def __repr__(self: Self) -> str:
        return f"SetPaperOutSensor({self.enabled})"
