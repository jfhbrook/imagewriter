from typing import Self

from imagewriter.encoding.base import Ctrl, Esc
from imagewriter.encoding.switch import SetSoftwareSwitches
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
        self._enabled = enabled
        super().__init__(not enabled, {SoftwareSwitch.PERFORATION_SKIP_DISABLED})

    def __repr__(self: Self) -> str:
        packed = self.pack()
        return f"SetPerforationSkip({self._enabled}, {packed[0]:b} {packed[1]:b})"
