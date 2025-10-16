from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Literal, Optional, Self, Sequence, Set, Type

from imagewriter.encoding.base import Command, esc
from imagewriter.encoding.language import Language
from imagewriter.encoding.pitch import Pitch
from imagewriter.serial import BaudRate, SerialProtocol


class DIPSwitch(Enum):
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


@dataclass
class DIPSwitchSettings:
    language: Language
    form_length: Literal[11] | Literal[12]
    perforation_skip: bool
    pitch: Pitch
    auto_lf_after_cr: bool
    baud_rate: BaudRate
    protocol: SerialProtocol

    @classmethod
    def language_from_switches(cls: Type[Self], switches: Set[DIPSwitch]) -> Language:
        key: int = 0b000
        if DIPSwitch.LANGUAGE_1 in switches:
            key |= 0b100
        if DIPSwitch.LANGUAGE_2 in switches:
            key |= 0b010
        if DIPSwitch.LANGUAGE_3 in switches:
            key |= 0b001

        return {
            0b000: Language.AMERICAN,
            0b100: Language.ITALIAN,
            0b010: Language.DANISH,
            0b110: Language.BRITISH,
            0b001: Language.GERMAN,
            0b101: Language.SWEDISH,
            0b011: Language.FRENCH,
            0b111: Language.SPANISH,
        }[key]

    @classmethod
    def pitch_from_switches(cls: Type[Self], switches: Set[DIPSwitch]) -> Pitch:
        key: int = 0b00
        if DIPSwitch.PITCH_1 in switches:
            key |= 0b10
        if DIPSwitch.PITCH_2 in switches:
            key |= 0b01

        return {
            0b00: Pitch.PICA,
            0b10: Pitch.ELITE,
            0b01: Pitch.ULTRACONDENSED,
            0b11: Pitch.ELITE_PROPORTIONAL,
        }[key]

    @classmethod
    def baud_rate_from_switches(cls: Type[Self], switches: Set[DIPSwitch]) -> BaudRate:
        key: int = 0b00
        if DIPSwitch.BAUD_RATE_1 in switches:
            key |= 0b10
        if DIPSwitch.BAUD_RATE_2 in switches:
            key |= 0b01

        baud_rates: Dict[int, BaudRate] = {
            0b00: 300,
            0b10: 1200,
            0b01: 2400,
            0b11: 9600,
        }

        return baud_rates[key]

    @classmethod
    def from_switches(cls: Type[Self], switches: Set[DIPSwitch]) -> Self:
        """
        Get the DIP switch settings based on which switches are closed, as per
        Chapter 2 of the ImageWriter II Technical Reference Manual.
        """

        return cls(
            language=cls.language_from_switches(switches),
            form_length=12 if DIPSwitch.FORM_LENGTH else 11,
            perforation_skip=DIPSwitch.PERFORATION_SKIP in switches,
            pitch=cls.pitch_from_switches(switches),
            auto_lf_after_cr=DIPSwitch.AUTO_LF_AFTER_CR in switches,
            baud_rate=cls.baud_rate_from_switches(switches),
            protocol=(
                SerialProtocol.XONXOFF
                if DIPSwitch.PROTOCOL in switches
                else SerialProtocol.HARDWARE_HANDSHAKE
            ),
        )

    @classmethod
    def defaults(cls: Type[Self]) -> Self:
        """
        Get the factory default DIP switch settings for printers sold in
        North America, as per Chapter 2 of the ImageWriter II Technical
        Reference Manual.
        """

        return cls.from_switches({DIPSwitch["1-6"], DIPSwitch["2-1"], DIPSwitch["2-2"]})


class SetSoftwareSwitches(Command):
    """
    Set software switch settings.
    """

    def __init__(
        self: Self, closed: bool, switches: "Sequence[SoftwareSwitch]"
    ) -> None:
        self.closed: bool = closed
        self.switches: Set[SoftwareSwitch] = set(switches)

    @property
    def open(self: Self) -> bool:
        return not self.closed

    @open.setter
    def open(self: Self, open: bool) -> None:
        self.closed = not open

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


class SoftwareSwitch(Enum):
    """
    Software switches, as per Chapter 3 of the ImageWriter II Technical
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
    def open(cls: Type[Self], *switches: "SoftwareSwitch") -> Command:
        """
        Open the provided software switches, as per page 31 of the ImageWriter
        II Technical Reference Manual. This does not affect switches which
        aren't provided.
        """
        return SetSoftwareSwitches(False, switches)

    @classmethod
    def close(cls: Type[Self], *switches: "SoftwareSwitch") -> Command:
        """
        Close the provided software switches, as per page 31 of the ImageWriter
        II Technical Reference Manual. This does not affect switches which
        aren't provided.
        """
        return SetSoftwareSwitches(True, switches)

    @classmethod
    def difference(
        cls: Type[Self], *switches: "SoftwareSwitch"
    ) -> "Set[SoftwareSwitch]":
        """
        Returns the software switches **not** provided.
        """
        return set(cls) - set(switches)

    @classmethod
    def toggle(cls: Type[Self], *switches: "SoftwareSwitch") -> List[Command]:
        """
        Close the software switches provided, and open all other software
        switches.
        """
        return [cls.open(*cls.difference(*switches)), cls.close(*switches)]

    @classmethod
    def defaults(
        cls: Type[Self], dip_switch_settings: Optional[DIPSwitchSettings] = None
    ) -> "Set[SoftwareSwitch]":
        """
        Returns software switches which are closed by default, as per page 32
        of the ImageWriter II Technical Reference Manual.

        Settings for language, automatic line feed and perforation skip are
        as per DIP switches. By default, this method assumes the DIP switches
        are configured as they would have been from the factory for sale in
        North America.
        """

        settings = (
            dip_switch_settings if dip_switch_settings else DIPSwitchSettings.defaults()
        )

        defaults: "Set[SoftwareSwitch]" = {
            SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED,
            SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF,
            SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT,
        }

        defaults |= cls.language_switches(settings.language)

        if settings.auto_lf_after_cr:
            defaults.add(SoftwareSwitch.AUTO_LF_AFTER_CR)

        if not settings.perforation_skip:
            defaults.add(SoftwareSwitch.PERFORATION_SKIP_DISABLED)

        return defaults

    @classmethod
    def set_defaults(
        cls: Type[Self], dip_switch_settings: Optional[DIPSwitchSettings] = None
    ) -> List[Command]:
        """
        Reset software switches to their defaults, as per page 32 of the
        ImageWriter II Technical Reference Manual.

        Settings for language, automatic line feed and perforation skip are
        as per DIP switches. By default, this method assumes the DIP switches
        are configured as they would have been from the factory for sale in
        North America.
        """

        defaults = cls.defaults(dip_switch_settings=dip_switch_settings)
        return cls.toggle(*defaults)

    @classmethod
    def language_switches(cls: Type[Self], language: Language) -> "Set[SoftwareSwitch]":
        """
        Language switches which should be closed, as per page 32 of the
        ImageWriter II Technical Reference Manual.
        """

        return {
            Language.AMERICAN: set(),
            Language.BRITISH: {cls.LANGUAGE_1, cls.LANGUAGE_2},
            Language.GERMAN: {cls.LANGUAGE_3},
            Language.FRENCH: {cls.LANGUAGE_2, cls.LANGUAGE_3},
            Language.SWEDISH: {cls.LANGUAGE_1, cls.LANGUAGE_3},
            Language.ITALIAN: {cls.LANGUAGE_1},
            Language.SPANISH: {cls.LANGUAGE_1, cls.LANGUAGE_2, cls.LANGUAGE_3},
            Language.DANISH: {cls.LANGUAGE_2},
        }[language]

    @classmethod
    def open_language_switches(
        cls: Type[Self], language: Language
    ) -> "Set[SoftwareSwitch]":
        return {
            cls.LANGUAGE_1,
            cls.LANGUAGE_2,
            cls.LANGUAGE_3,
        } - cls.open_language_switches(language)

    @classmethod
    def set_language(cls: Type[Self], language: Language) -> List[Command]:
        return [
            cls.open(*cls.open_language_switches(language)),
            cls.close(*cls.language_switches(language)),
        ]

    @classmethod
    def enable_software_select_response(cls: Type[Self]) -> Command:
        """
        Enable Software Select-Deselect Response, as per page 34 of the
        ImageWriter II Technical Reference Manual.
        """

        return cls.open(SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED)

    @classmethod
    def disable_software_select_response(cls: Type[Self]) -> Command:
        """
        Disable Software Select-Deselect Response, as per page 34 of the
        ImageWriter II Technical Reference Manual.
        """

        return cls.close(SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED)

    @classmethod
    def enable_lf_when_line_full(cls: Type[Self]) -> Command:
        """
        Enable the automatic insertion of a line feed when the line is full, as
        per page 34 of the ImageWriter II Technical Reference
        Manual.
        """

        return cls.close(SoftwareSwitch.LF_WHEN_LINE_FULL)

    @classmethod
    def disable_lf_when_line_full(cls: Type[Self]) -> Command:
        """
        Disable the automatic insertion of a line feed when the line is full,
        as per page 34 of the ImageWriter II Technical Reference Manual.
        """

        return cls.open(SoftwareSwitch.LF_WHEN_LINE_FULL)

    @classmethod
    def enable_lf_ff_print_commands(cls: Type[Self]) -> Command:
        """
        Enable the treatment of LF and FF as print commands, as per page 34
        of the ImageWriter II Technical Reference Manual.
        """

        return cls.close(SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF)

    @classmethod
    def disable_lf_ff_print_commands(cls: Type[Self]) -> Command:
        """
        Disable the treatment of LF and FF as print commands, as per page 34
        of the ImageWriter II Technical Reference Manual.
        """

        return cls.open(SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF)

    @classmethod
    def enable_auto_lf_after_cr(cls: Type[Self]) -> Command:
        """
        Enable an automatic LF after a CR, as per page 34 of the ImageWriter II
        Technical Reference Manual.
        """

        return cls.close(SoftwareSwitch.AUTO_LF_AFTER_CR)

    @classmethod
    def disable_auto_lf_after_cr(cls: Type[Self]) -> Command:
        """
        Disable an automatic LF after a CR, as per page 34 of the ImageWriter
        II Technical Reference Manual.
        """

        return cls.open(SoftwareSwitch.AUTO_LF_AFTER_CR)

    @classmethod
    def print_slashed_zero(cls: Type[Self]) -> Command:
        """
        Print zeroes with a slash, as per page 34 of the ImageWriter II
        Technical Reference Manual.
        """

        return cls.close(SoftwareSwitch.SLASHED_ZERO)

    @classmethod
    def print_unslashed_zero(cls: Type[Self]) -> Command:
        """
        Print zeroes without a slash, as per page 34 of the ImageWriter II
        Technical Reference Manual.
        """

        return cls.open(SoftwareSwitch.SLASHED_ZERO)

    @classmethod
    def enable_perforation_skip(cls: Type[Self]) -> Command:
        """
        Enable automatic perforation skip, as per page 34 of the ImageWriter II
        Technical Reference Manual.
        """

        return cls.open(SoftwareSwitch.PERFORATION_SKIP_DISABLED)

    @classmethod
    def disable_perforation_skip(cls: Type[Self]) -> Command:
        """
        Disable automatic perforation skip, as per page 34 of the ImageWriter
        II Technical Reference Manual.
        """

        return cls.close(SoftwareSwitch.PERFORATION_SKIP_DISABLED)

    @classmethod
    def ignore_eighth_data_bit(cls: Type[Self]) -> Command:
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

        return cls.close(SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT)

    @classmethod
    def include_eighth_data_bit(cls: Type[Self]) -> Command:
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

        return cls.open(SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT)
