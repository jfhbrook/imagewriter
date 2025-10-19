from typing import List, Self

from imagewriter.encoding.base import Command, Ctrl, Esc
from imagewriter.encoding.switch import (
    CloseSoftwareSwitches,
    fmt_switch_banks,
    fmt_switch_position,
    OpenSoftwareSwitches,
)
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


START_DOUBLE_WIDTH = StartDoubleWidth()
STOP_DOUBLE_WIDTH = StopDoubleWidth()


def double_width(commands: List[Command]) -> List[Command]:
    return [
        START_DOUBLE_WIDTH,
        *commands,
        STOP_DOUBLE_WIDTH,
    ]


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


START_UNDERLINE = StartUnderline()
STOP_UNDERLINE = StopUnderline()


def underline(commands: List[Command]) -> List[Command]:
    return [START_UNDERLINE, *commands, STOP_UNDERLINE]


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


START_BOLDFACE = StartBoldface()
STOP_BOLDFACE = StopBoldface()


def boldface(commands: List[Command]) -> List[Command]:
    return [START_BOLDFACE, *commands, STOP_BOLDFACE]


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


START_HALF_HEIGHT = StartHalfHeight()
STOP_HALF_HEIGHT = StopHalfHeight()


def half_height(commands: List[Command]) -> List[Command]:
    return [START_HALF_HEIGHT, *commands, STOP_HALF_HEIGHT]


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


START_SUPERSCRIPT = StartSuperscript()
STOP_SUPERSCRIPT = StopSuperscriptOrSubscript()
START_SUBSCRIPT = StartSubscript()
STOP_SUBSCRIPT = STOP_SUPERSCRIPT


class PrintSlashedZero(CloseSoftwareSwitches):
    def __init__(self: Self) -> None:
        super().__init__({SoftwareSwitch.SLASHED_ZERO})

    def __repr__(self: Self) -> str:
        position = fmt_switch_position(False)
        banks = fmt_switch_banks(self.pack())

        return f"PrintSlashedZero({position}, {banks})"


class PrintUnslashedZero(OpenSoftwareSwitches):
    def __init__(self: Self) -> None:
        super().__init__({SoftwareSwitch.SLASHED_ZERO})

    def __repr__(self: Self) -> str:
        position = fmt_switch_position(True)
        banks = fmt_switch_banks(self.pack())

        return f"PrintUnslashedZero({position}, {banks})"


PRINT_SLASHED_ZERO = PrintSlashedZero()
PRINT_UNSLASHED_ZERO = PrintUnslashedZero()
