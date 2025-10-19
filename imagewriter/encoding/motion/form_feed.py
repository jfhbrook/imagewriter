from typing import Self

from imagewriter.encoding.base import Ctrl, Esc
from imagewriter.encoding.switch import (
    fmt_switch_banks,
    fmt_switch_position,
    SetSoftwareSwitches,
)
from imagewriter.switch import SoftwareSwitch


class FormFeed(Ctrl):
    """
    A form feed. When encountered, feeds the paper up to a new sheet.
    """

    def __init__(self: Self) -> None:
        super().__init__("L")

    def __repr__(self: Self) -> str:
        return "FormFeed()"


FF = FormFeed()


class SetTopOfForm(Esc):
    """
    Set the current position as the top of the current form. This, combined
    with page/form length, controls how far a form feed command will move
    the paper.
    """

    def __init__(self: Self) -> None:
        super().__init__("v")

    def __repr__(self: Self) -> str:
        return "SetTopOfForm()"


SET_TOP_OF_FORM = SetTopOfForm()


class SetPerforationSkip(SetSoftwareSwitches):
    """
    Configure automatic perforation skip, as per page 34 of the ImageWriter II
    Technical Reference Manual.
    """

    def __init__(self: Self, enabled: bool) -> None:
        super().__init__(not enabled, {SoftwareSwitch.PERFORATION_SKIP_DISABLED})

    def __repr__(self: Self) -> str:
        position = fmt_switch_position(self.closed)
        banks = fmt_switch_banks(self.pack())

        return f"SetPerforationSkip({not self.closed}, {position}, {banks})"
