from abc import ABC
from typing import List, Self, Set

from imagewriter.encoding.base import Command, esc
from imagewriter.language import Language
from imagewriter.switch import SoftwareSwitch


class SetSoftwareSwitches(Command, ABC):
    def __init__(self: Self, closed: bool, switches: Set[SoftwareSwitch]) -> None:
        self._closed: bool = closed
        self.switches: Set[SoftwareSwitch] = switches

    @property
    def open(self: Self) -> bool:
        return not self._closed

    @property
    def closed(self: Self) -> bool:
        return self._closed

    def pack(self: Self) -> bytes:
        bank_a = 0
        bank_b = 0

        # Collect the bits into a short
        short = 0

        for sw in sorted(self.switches, key=lambda s: s.value):
            short |= sw.value

        # Store data in two little endian bytes
        for i in range(0, 16):
            if short & (1 << i):
                if i < 8:
                    bank_a |= 0x80 >> i
                else:
                    bank_b |= 0x8000 >> i

        return bytes([bank_a, bank_b])

    def __bytes__(self: Self) -> bytes:
        code: bytes = esc("D") if self.closed else esc("Z")

        return code + self.pack()


class OpenSoftwareSwitches(SetSoftwareSwitches):
    def __init__(self: Self, switches: Set[SoftwareSwitch]) -> None:
        return super().__init__(False, switches)


class CloseSoftwareSwitches(SetSoftwareSwitches):
    def __init__(self: Self, switches: Set[SoftwareSwitch]) -> None:
        return super().__init__(True, switches)


def set_software_switches(switches: Set[SoftwareSwitch]) -> List[Command]:
    """
    Close the software switches provided, and open all other software
    switches.
    """

    return [
        OpenSoftwareSwitches(SoftwareSwitch.difference(*switches)),
        CloseSoftwareSwitches(switches),
    ]


def set_language(language: Language) -> List[Command]:
    return [
        OpenSoftwareSwitches(SoftwareSwitch.open_language_switches(language)),
        CloseSoftwareSwitches(SoftwareSwitch.language_switches(language)),
    ]


def enable_software_select_response() -> Command:
    """
    Enable Software Select-Deselect Response, as per page 34 of the
    ImageWriter II Technical Reference Manual.
    """

    return OpenSoftwareSwitches({SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED})


def disable_software_select_response() -> Command:
    """
    Disable Software Select-Deselect Response, as per page 34 of the
    ImageWriter II Technical Reference Manual.
    """

    return CloseSoftwareSwitches({SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED})


def enable_lf_when_line_full() -> Command:
    """
    Enable the automatic insertion of a line feed when the line is full, as
    per page 34 of the ImageWriter II Technical Reference
    Manual.
    """

    return CloseSoftwareSwitches({SoftwareSwitch.LF_WHEN_LINE_FULL})


def disable_lf_when_line_full() -> Command:
    """
    Disable the automatic insertion of a line feed when the line is full,
    as per page 34 of the ImageWriter II Technical Reference Manual.
    """

    return OpenSoftwareSwitches({SoftwareSwitch.LF_WHEN_LINE_FULL})


def enable_lf_ff_print_commands() -> Command:
    """
    Enable the treatment of LF and FF as print commands, as per page 34
    of the ImageWriter II Technical Reference Manual.
    """

    return CloseSoftwareSwitches({SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF})


def disable_lf_ff_print_commands() -> Command:
    """
    Disable the treatment of LF and FF as print commands, as per page 34
    of the ImageWriter II Technical Reference Manual.
    """

    return OpenSoftwareSwitches({SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF})


def enable_auto_lf_after_cr() -> Command:
    """
    Enable an automatic LF after a CR, as per page 34 of the ImageWriter II
    Technical Reference Manual.
    """

    return CloseSoftwareSwitches({SoftwareSwitch.AUTO_LF_AFTER_CR})


def disable_auto_lf_after_cr() -> Command:
    """
    Disable an automatic LF after a CR, as per page 34 of the ImageWriter
    II Technical Reference Manual.
    """

    return OpenSoftwareSwitches({SoftwareSwitch.AUTO_LF_AFTER_CR})


def print_slashed_zero() -> Command:
    """
    Print zeroes with a slash, as per page 34 of the ImageWriter II
    Technical Reference Manual.
    """

    return CloseSoftwareSwitches({SoftwareSwitch.SLASHED_ZERO})


def print_unslashed_zero() -> Command:
    """
    Print zeroes without a slash, as per page 34 of the ImageWriter II
    Technical Reference Manual.
    """

    return OpenSoftwareSwitches({SoftwareSwitch.SLASHED_ZERO})


def enable_perforation_skip() -> Command:
    """
    Enable automatic perforation skip, as per page 34 of the ImageWriter II
    Technical Reference Manual.
    """

    return OpenSoftwareSwitches({SoftwareSwitch.PERFORATION_SKIP_DISABLED})


def disable_perforation_skip() -> Command:
    """
    Disable automatic perforation skip, as per page 34 of the ImageWriter
    II Technical Reference Manual.
    """

    return CloseSoftwareSwitches({SoftwareSwitch.PERFORATION_SKIP_DISABLED})


def ignore_eighth_data_bit() -> Command:
    """
    Ignore the eighth data bit of each byte sent, as per page 34 of the
    ImageWriter II Technical Reference Manual.

    This setting is for the benefit of Applesoft Basic, which does not
    support an eighth bit. Pure ASCII does not use the eighth bit, and the
    ImageWriter II supports escape sequences for "high-ASCII", as per
    Chapter 4 and Chapter 7 of the manual.

    Note that the ImageWriter II will automatically switch to 8-bit mode
    when an escape sequence sent to it uses 8-bit data - examples include
    custom characters and graphics.
    """

    return CloseSoftwareSwitches({SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT})


def include_eighth_data_bit() -> Command:
    """
    Include the eighth data bit of each byte sent, as per page 34 of the
    ImageWriter II Technical Reference Manual.

    This setting is for the benefit of Applesoft Basic, which does not
    support an eighth bit. Pure ASCII does not use the eighth bit, and the
    ImageWriter II supports escape sequences for "high-ASCII", as per
    Chapter 4 and Chapter 7 of the manual.

    Note that the ImageWriter II will automatically switch to 8-bit mode
    when an escape sequence sent to it uses 8-bit data - examples include
    custom characters and graphics.
    """

    return OpenSoftwareSwitches({SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT})
