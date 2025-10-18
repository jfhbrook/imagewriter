from dataclasses import dataclass
from enum import Enum
from typing import Dict, Literal, Optional, Self, Set, Type

from imagewriter.language import Language
from imagewriter.pitch import Pitch
from imagewriter.serial import BaudRate, SerialProtocol


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


@dataclass
class DIPSwitches:
    """
    DIP switch settings, as per Chapter 2 of the ImageWriter II Technical
    Reference Manual
    """

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
            form_length=12 if DIPSwitch.FORM_LENGTH in switches else 11,
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

        return cls.from_switches(
            {DIPSwitch.PITCH_1, DIPSwitch.BAUD_RATE_1, DIPSwitch.BAUD_RATE_2}
        )


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
    def difference(
        cls: Type[Self], switches: "Set[SoftwareSwitch]"
    ) -> "Set[SoftwareSwitch]":
        """
        Returns the software switches **not** provided.
        """
        return set(cls) - set(switches)

    @classmethod
    def defaults(
        cls: Type[Self], dip_switch_settings: Optional[DIPSwitches] = None
    ) -> "Set[SoftwareSwitch]":
        """
        Returns software switches which are closed by default, as per page 32
        of the ImageWriter II Technical Reference Manual.

        Settings for language, automatic line feed and perforation skip are
        as per DIP switches. By default, this method assumes the DIP switches
        are configured as they would have been from the factory for sale in
        North America.
        """

        settings: DIPSwitches = (
            dip_switch_settings if dip_switch_settings else DIPSwitches.defaults()
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
        } - cls.language_switches(language)


@dataclass
class SoftwareSwitches:
    language: Language
    software_select_response_disabled: bool
    lf_when_line_full: bool
    print_commands_include_lf_ff: bool
    auto_lf_after_cr: bool
    slashed_zero: bool
    perforation_skip_disabled: bool
    ignore_eighth_data_bit: bool

    @classmethod
    def defaults(
        cls: Type[Self], dip_switch_settings: Optional[DIPSwitches] = None
    ) -> Self:
        return cls.from_switches(SoftwareSwitch.defaults(dip_switch_settings))

    @classmethod
    def language_from_switches(
        cls: Type[Self], switches: Set[SoftwareSwitch]
    ) -> Language:
        key: int = 0b000
        if SoftwareSwitch.LANGUAGE_1 in switches:
            key |= 0b100
        if SoftwareSwitch.LANGUAGE_2 in switches:
            key |= 0b010
        if SoftwareSwitch.LANGUAGE_3 in switches:
            key |= 0b001

        return {
            0b000: Language.AMERICAN,
            0b110: Language.BRITISH,
            0b001: Language.GERMAN,
            0b011: Language.FRENCH,
            0b101: Language.SWEDISH,
            0b100: Language.ITALIAN,
            0b111: Language.SPANISH,
            0b010: Language.DANISH,
        }[key]

    @classmethod
    def from_switches(cls: Type[Self], switches: Set[SoftwareSwitch]) -> Self:
        """
        Get the software switch settings based on which switches are closed.
        """

        return cls(
            language=cls.language_from_switches(switches),
            software_select_response_disabled=(
                SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED
            )
            in switches,
            lf_when_line_full=SoftwareSwitch.LF_WHEN_LINE_FULL in switches,
            print_commands_include_lf_ff=SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF
            in switches,
            auto_lf_after_cr=SoftwareSwitch.AUTO_LF_AFTER_CR in switches,
            slashed_zero=SoftwareSwitch.SLASHED_ZERO in switches,
            perforation_skip_disabled=SoftwareSwitch.PERFORATION_SKIP_DISABLED
            in switches,
            ignore_eighth_data_bit=SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT in switches,
        )

    def switches(self: Self) -> Set[SoftwareSwitch]:
        switches: Set[SoftwareSwitch] = SoftwareSwitch.language_switches(self.language)

        if self.software_select_response_disabled:
            switches.add(SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED)
        if self.lf_when_line_full:
            switches.add(SoftwareSwitch.LF_WHEN_LINE_FULL)
        if self.print_commands_include_lf_ff:
            switches.add(SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF)
        if self.auto_lf_after_cr:
            switches.add(SoftwareSwitch.AUTO_LF_AFTER_CR)
        if self.slashed_zero:
            switches.add(SoftwareSwitch.SLASHED_ZERO)
        if self.perforation_skip_disabled:
            switches.add(SoftwareSwitch.PERFORATION_SKIP_DISABLED)
        if self.ignore_eighth_data_bit:
            switches.add(SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT)

        return switches
