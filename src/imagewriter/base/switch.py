"""
Representations of state for both the ImageWriter II's physical DIP switches and its
in-memory software switches.
"""

from enum import Enum
from typing import Self

from imagewriter.base.character import Language
from imagewriter.base.motion import FormLength
from imagewriter.base.pitch import Pitch
from imagewriter.base.print import PrintCommands
from imagewriter.serial import BaudRate, SerialProtocol

LANGUAGE_LOOKUP = {
    0b000: Language.AMERICAN,
    0b100: Language.ITALIAN,
    0b010: Language.DANISH,
    0b110: Language.BRITISH,
    0b001: Language.GERMAN,
    0b101: Language.SWEDISH,
    0b011: Language.FRENCH,
    0b111: Language.SPANISH,
}

BAUD_RATE_LOOKUP: dict[int, BaudRate] = {
    0b00: 300,
    0b10: 1200,
    0b01: 2400,
    0b11: 9600,
}

PITCH_LOOKUP = {
    0b00: Pitch.PICA,
    0b10: Pitch.ELITE,
    0b01: Pitch.ULTRACONDENSED,
    0b11: Pitch.ELITE_PROPORTIONAL,
}


class DIPSwitch(Enum):
    """
    A DIP switch.
    """

    LANGUAGE_1 = "1-1"
    LANGUAGE_2 = "1-2"
    LANGUAGE_3 = "1-3"
    FORM_LENGTH = "1-4"
    PERFORATION_SKIP = "1-5"
    PITCH_1 = "1-6"
    PITCH_2 = "1-7"
    AUTO_LF_AFTER_CR = "1-8"
    BAUD_RATE_1 = "2-1"
    BAUD_RATE_2 = "2-2"
    PROTOCOL = "2-3"
    OPTION_CARD = "2-4"


class DIPSwitches:
    """
    DIP switch settings, as per Chapter 2 of the ImageWriter II Technical
    Reference Manual

    This class wraps a set of DIPSwitch and exposes semantic properties encoded
    by those switches.
    """

    def __init__(self: Self, switches: set[DIPSwitch]) -> None:
        self.switches = switches

    @property
    def language(self: Self) -> Language:
        key: int = 0b000
        if DIPSwitch.LANGUAGE_1 in self.switches:
            key |= 0b100
        if DIPSwitch.LANGUAGE_2 in self.switches:
            key |= 0b010
        if DIPSwitch.LANGUAGE_3 in self.switches:
            key |= 0b001

        return LANGUAGE_LOOKUP[key]

    @property
    def form_length(self: Self) -> FormLength:
        return 12 if DIPSwitch.FORM_LENGTH in self.switches else 11

    @property
    def perforation_skip(self: Self) -> bool:
        return DIPSwitch.PERFORATION_SKIP in self.switches

    @property
    def pitch(self: Self) -> Pitch:
        key: int = 0b00
        if DIPSwitch.PITCH_1 in self.switches:
            key |= 0b10
        if DIPSwitch.PITCH_2 in self.switches:
            key |= 0b01

        return PITCH_LOOKUP[key]

    @property
    def auto_lf_after_cr(self: Self) -> bool:
        return DIPSwitch.AUTO_LF_AFTER_CR in self.switches

    @property
    def baud_rate(self: Self) -> BaudRate:
        key: int = 0b00
        if DIPSwitch.BAUD_RATE_1 in self.switches:
            key |= 0b10
        if DIPSwitch.BAUD_RATE_2 in self.switches:
            key |= 0b01

        return BAUD_RATE_LOOKUP[key]

    @property
    def protocol(self: Self) -> SerialProtocol:
        return (
            SerialProtocol.XONXOFF
            if DIPSwitch.PROTOCOL in self.switches
            else SerialProtocol.HARDWARE_HANDSHAKE
        )

    @classmethod
    def defaults(cls: type[Self]) -> Self:
        """
        The factory default DIP switch settings for printers sold in
        North America, as per Chapter 2 of the ImageWriter II Technical
        Reference Manual.
        """

        return cls({DIPSwitch.PITCH_1, DIPSwitch.BAUD_RATE_1, DIPSwitch.BAUD_RATE_2})


class SoftwareSwitch(Enum):
    """
    A software switch, as per Chapter 3 of the ImageWriter II Technical
    Reference Manual.
    """

    # A bank
    LANGUAGE_1 = 1
    LANGUAGE_2 = 1 << 1
    LANGUAGE_3 = 1 << 2
    # Switch A-4 not used
    SOFTWARE_SELECT_RESPONSE_DISABLED = 1 << 4
    LF_WHEN_LINE_FULL = 1 << 5
    PRINT_COMMANDS_INCLUDE_LF_FF = 1 << 6
    AUTO_LF_AFTER_CR = 1 << 7
    # B bank
    SLASHED_ZERO = 1 << 8
    # Switch B-2 not used
    PERFORATION_SKIP_DISABLED = 1 << (8 + 2)
    # Switch B-4 not used
    # Switch B-5 not used
    IGNORE_EIGHTH_DATA_BIT = 1 << (8 + 5)
    # Switch B-7 not used
    # Switch B-8 not used

    @classmethod
    def defaults(cls: type[Self], dip_switches: DIPSwitches) -> set[SoftwareSwitch]:
        """
        Returns software switches which are closed by default, as per page 32
        of the ImageWriter II Technical Reference Manual.

        Settings for language, automatic line feed and perforation skip are
        as per DIP switches. By default, this method assumes the DIP switches
        are configured as they would have been from the factory for sale in
        North America.
        """

        defaults: set[SoftwareSwitch] = {
            SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED,
            SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF,
            SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT,
        }

        defaults |= SoftwareSwitchLanguage.closed(dip_switches.language)

        if dip_switches.auto_lf_after_cr:
            defaults.add(SoftwareSwitch.AUTO_LF_AFTER_CR)

        if not dip_switches.perforation_skip:
            defaults.add(SoftwareSwitch.PERFORATION_SKIP_DISABLED)

        return defaults

    @classmethod
    def open(cls: type[Self], switches: set[SoftwareSwitch]) -> set[SoftwareSwitch]:
        """
        Open software switches.
        """
        return set(cls) - switches


class SoftwareSwitchLanguage:
    """
    Helpers for working with language software switches.
    """

    @classmethod
    def language(cls: type[Self], switches: set[SoftwareSwitch]) -> Language:
        """
        The language that corresponds with closed switches.
        """

        key: int = 0b000
        if SoftwareSwitch.LANGUAGE_1 in switches:
            key |= 0b100
        if SoftwareSwitch.LANGUAGE_2 in switches:
            key |= 0b010
        if SoftwareSwitch.LANGUAGE_3 in switches:
            key |= 0b001

        return LANGUAGE_LOOKUP[key]

    @classmethod
    def closed(cls: type[Self], language: Language) -> set[SoftwareSwitch]:
        """
        Language switches which should be closed, as per page 32 of the
        ImageWriter II Technical Reference Manual.
        """

        return {
            Language.AMERICAN: set(),
            Language.BRITISH: {SoftwareSwitch.LANGUAGE_1, SoftwareSwitch.LANGUAGE_2},
            Language.GERMAN: {SoftwareSwitch.LANGUAGE_3},
            Language.FRENCH: {SoftwareSwitch.LANGUAGE_2, SoftwareSwitch.LANGUAGE_3},
            Language.SWEDISH: {SoftwareSwitch.LANGUAGE_1, SoftwareSwitch.LANGUAGE_3},
            Language.ITALIAN: {SoftwareSwitch.LANGUAGE_1},
            Language.SPANISH: {
                SoftwareSwitch.LANGUAGE_1,
                SoftwareSwitch.LANGUAGE_2,
                SoftwareSwitch.LANGUAGE_3,
            },
            Language.DANISH: {SoftwareSwitch.LANGUAGE_2},
        }[language]

    @classmethod
    def open(cls: type[Self], language: Language) -> set[SoftwareSwitch]:
        """
        Language switches that should be open.
        """

        return {
            SoftwareSwitch.LANGUAGE_1,
            SoftwareSwitch.LANGUAGE_2,
            SoftwareSwitch.LANGUAGE_3,
        } - cls.closed(language)


class SoftwareSwitches:
    def __init__(self: Self, switches: set[SoftwareSwitch]) -> None:
        self.switches = switches

    @classmethod
    def defaults(cls: type[Self], dip_switches: DIPSwitches) -> Self:
        switches = SoftwareSwitch.defaults(dip_switches)
        return cls(switches)

    @property
    def language(self: Self) -> Language:
        return SoftwareSwitchLanguage.language(self.switches)

    @language.setter
    def language(self: Self, language: Language) -> None:
        self.switches |= SoftwareSwitchLanguage.closed(language)

    @property
    def software_select_response_disabled(self: Self) -> bool:
        return SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED in self.switches

    @software_select_response_disabled.setter
    def software_select_response_disabled(self: Self, disabled: bool) -> None:
        if disabled:
            self.switches.add(SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED)
        else:
            self.switches.remove(SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED)

    @property
    def lf_when_line_full(self: Self) -> bool:
        return SoftwareSwitch.LF_WHEN_LINE_FULL in self.switches

    @lf_when_line_full.setter
    def lf_when_line_full(self: Self, enabled: bool) -> None:
        if enabled:
            self.switches.add(SoftwareSwitch.LF_WHEN_LINE_FULL)
        else:
            self.switches.remove(SoftwareSwitch.LF_WHEN_LINE_FULL)

    @property
    def print_commands(self: Self) -> PrintCommands:
        return (
            PrintCommands.CR_LF_AND_FF
            if SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF in self.switches
            else PrintCommands.CR_ONLY
        )

    @print_commands.setter
    def print_commands(self: Self, commands: PrintCommands) -> None:
        if commands == PrintCommands.CR_LF_AND_FF:
            self.switches.add(SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF)
        else:
            self.switches.remove(SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF)

    @property
    def auto_lf_after_cr(self: Self) -> bool:
        return SoftwareSwitch.AUTO_LF_AFTER_CR in self.switches

    @auto_lf_after_cr.setter
    def auto_lf_after_cr(self: Self, enabled: bool) -> None:
        if enabled:
            self.switches.add(SoftwareSwitch.AUTO_LF_AFTER_CR)
        else:
            self.switches.remove(SoftwareSwitch.AUTO_LF_AFTER_CR)

    @property
    def slashed_zero(self: Self) -> bool:
        return SoftwareSwitch.SLASHED_ZERO in self.switches

    @slashed_zero.setter
    def slashed_zero(self: Self, enabled: bool) -> None:
        if enabled:
            self.switches.add(SoftwareSwitch.SLASHED_ZERO)
        else:
            self.switches.remove(SoftwareSwitch.SLASHED_ZERO)

    @property
    def perforation_skip_disabled(self: Self) -> bool:
        return SoftwareSwitch.PERFORATION_SKIP_DISABLED in self.switches

    @perforation_skip_disabled.setter
    def perforation_skip_disabled(self: Self, disabled: bool) -> None:
        if disabled:
            self.switches.add(SoftwareSwitch.PERFORATION_SKIP_DISABLED)
        else:
            self.switches.remove(SoftwareSwitch.PERFORATION_SKIP_DISABLED)

    @property
    def ignore_eighth_data_bit(self: Self) -> bool:
        return SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT in self.switches

    @ignore_eighth_data_bit.setter
    def ignore_eighth_data_bit(self: Self, ignored: bool) -> None:
        if ignored:
            self.switches.add(SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT)
        else:
            self.switches.remove(SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT)

    def clone(self: Self) -> Self:
        return self.__class__(self.switches.copy())
