from typing import Self

from imagewriter.encoding.base import Ctrl, Esc
from imagewriter.encoding.switch import CloseSoftwareSwitches, OpenSoftwareSwitches
from imagewriter.switch import SoftwareSwitch


class StartDoubleWidth(Ctrl):
    def __init__(self: Self) -> None:
        super().__init__("N")

    def __repr__(self: Self) -> str:
        return "StartDoubleWidth()"


class StopDoubleWidth(Ctrl):
    def __init__(self: Self) -> None:
        super().__init__("O")

    def __repr__(self: Self) -> str:
        return "StopDoubleWidth()"


class StartUnderline(Esc):
    def __init__(self: Self) -> None:
        super().__init__("X")

    def __repr__(self: Self) -> str:
        return "StartUnderline()"


class StopUnderline(Esc):
    def __init__(self: Self) -> None:
        super().__init__("Y")

    def __repr__(self: Self) -> str:
        return "StopUnderline()"


class StartBoldface(Esc):
    def __init__(self: Self) -> None:
        super().__init__("!")

    def __repr__(self: Self) -> str:
        return "StartBoldface()"


class StopBoldface(Esc):
    def __init__(self: Self) -> None:
        super().__init__('"')

    def __repr__(self: Self) -> str:
        return "StopBoldface()"


class StartHalfHeight(Esc):
    def __init__(self: Self) -> None:
        super().__init__("w")

    def __repr__(self: Self) -> str:
        return "StartHalfHeight()"


class StopHalfHeight(Esc):
    def __init__(self: Self) -> None:
        super().__init__("W")

    def __repr__(self: Self) -> str:
        return "StopHalfHeight()"


class StartSuperscript(Esc):
    def __init__(self: Self) -> None:
        super().__init__("x")

    def __repr__(self: Self) -> str:
        return "StartSuperscript()"


class StartSubscript(Esc):
    def __init__(self: Self) -> None:
        super().__init__("y")

    def __repr__(self: Self) -> str:
        return "StartSubscript()"


class StopSuperscriptOrSubscript(Esc):
    def __init__(self: Self) -> None:
        super().__init__("z")

    def __repr__(self: Self) -> str:
        return "StopSuperscriptOrSubscript()"


class PrintSlashedZero(CloseSoftwareSwitches):
    def __init__(self: Self) -> None:
        super().__init__({SoftwareSwitch.SLASHED_ZERO})

    def __repr__(self: Self) -> str:
        packed = self.pack()

        return f"PrintSlashedZero({packed[0]:b} {packed[1]:b}"


class PrintUnslashedZero(OpenSoftwareSwitches):
    def __init__(self: Self) -> None:
        super().__init__({SoftwareSwitch.SLASHED_ZERO})

    def __repr__(self: Self) -> str:
        packed = self.pack()

        return f"PrintUnslashedZero({packed[0]:b} {packed[1]:b}"


START_DOUBLE_WIDTH = StartDoubleWidth()
STOP_DOUBLE_WIDTH = StopDoubleWidth()
START_UNDERLINE = StartUnderline()
STOP_UNDERLINE = StopUnderline()
START_BOLDFACE = StartBoldface()
STOP_BOLDFACE = StopBoldface()
START_HALF_HEIGHT = StartHalfHeight()
STOP_HALF_HEIGHT = StopHalfHeight()
START_SUPERSCRIPT = StartSuperscript()
STOP_SUPERSCRIPT = StopSuperscriptOrSubscript()
START_SUBSCRIPT = StartSubscript()
STOP_SUBSCRIPT = STOP_SUPERSCRIPT

PRINT_SLASHED_ZERO = PrintSlashedZero()
PRINT_UNSLASHED_ZERO = PrintUnslashedZero()
