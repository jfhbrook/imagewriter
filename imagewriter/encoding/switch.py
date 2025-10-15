from enum import Enum
from typing import List, Self, Sequence, Set, Type

from imagewriter.encoding.base import esc, Packet
from imagewriter.encoding.language import Language


class SetSoftwareSwitches(Packet):
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

    def _pack(self: Self) -> bytes:
        a = 0
        b = 0
        for sw in self.switches:
            v = sw.value
            if v > 128:
                b |= v >> 8
            else:
                a |= v

        return bytes([a, b])

    def data(self: Self) -> bytes:
        code: bytes = esc("D") if self.closed else esc("Z")

        return code + self._pack()


class SoftwareSwitch(Enum):
    """
    Software switches, as per Chapter 3 of the ImageWriter II Technical
    Reference Manual.
    """

    LANGUAGE_1 = 1
    LANGUAGE_2 = 1 << 1
    LANGUAGE_3 = 1 << 2
    SOFTWARE_SELECT_RESPONSE_DISABLED = 1 << 4
    LF_WHEN_LINE_FULL = 1 << 5
    PRINT_COMMANDS_INCLUDE_LF_FF = 1 << 6
    AUTO_LF_AFTER_CR = 1 << 7
    SLASHED_ZERO = 1 << 8
    PERFORATION_SKIP_DISABLED = 1 << (8 + 2)
    IGNORE_EIGHTH_DATA_BIT = 1 << (8 + 5)

    @classmethod
    def open(cls: Type[Self], *switches: "SoftwareSwitch") -> Packet:
        """
        Open the provided software switches, as per page 31 of the ImageWriter
        II Technical Reference Manual. This does not affect switches which
        aren't provided.
        """
        return SetSoftwareSwitches(False, switches)

    @classmethod
    def close(cls: Type[Self], *switches: "SoftwareSwitch") -> Packet:
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
    def toggle(cls: Type[Self], *switches: "SoftwareSwitch") -> List[Packet]:
        """
        Close the software switches provided, and open all other software
        switches.
        """
        return [cls.open(*cls.difference(*switches)), cls.close(*switches)]

    @classmethod
    def defaults(
        cls: Type[Self],
        language: Language = Language.AMERICAN,
        auto_lf_after_cr: bool = False,
        perforation_skip_disabled: bool = True,
    ) -> "Set[SoftwareSwitch]":
        """
        Returns software switches which are closed by default, as per page 32
        of the ImageWriter II Technical Reference Manual.

        Settings for language, automatic line feed and perforation skip are
        as per DIP switches. By default, this method assumes the DIP switches
        are configured as they would have been from the factory for sale in
        North America.
        """

        defaults: "Set[SoftwareSwitch]" = {
            SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED,
            SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF,
            SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT,
        }

        defaults |= cls.language(language)

        if auto_lf_after_cr:
            defaults.add(SoftwareSwitch.AUTO_LF_AFTER_CR)

        if perforation_skip_disabled:
            defaults.add(SoftwareSwitch.PERFORATION_SKIP_DISABLED)

        return defaults

    @classmethod
    def set_defaults(
        cls: Type[Self],
        language: Language = Language.AMERICAN,
        auto_lf_after_cr: bool = False,
        perforation_skip_disabled: bool = True,
    ) -> List[Packet]:
        """
        Reset software switches to their defaults, as per page 32 of the
        ImageWriter II Technical Reference Manual.

        Settings for language, automatic line feed and perforation skip are
        as per DIP switches. By default, this method assumes the DIP switches
        are configured as they would have been from the factory for sale in
        North America.
        """

        defaults = cls.defaults(
            language=language,
            auto_lf_after_cr=auto_lf_after_cr,
            perforation_skip_disabled=perforation_skip_disabled,
        )
        return cls.toggle(*defaults)

    @classmethod
    def language(cls: Type[Self], language: Language) -> "Set[SoftwareSwitch]":
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
    def language_difference(
        cls: Type[Self], language: Language
    ) -> "Set[SoftwareSwitch]":
        return {cls.LANGUAGE_1, cls.LANGUAGE_2, cls.LANGUAGE_3} - cls.language(language)

    @classmethod
    def set_language(cls: Type[Self], language: Language) -> List[Packet]:
        return [
            cls.open(*cls.language_difference(language)),
            cls.close(*cls.language(language)),
        ]

    @classmethod
    def enable_software_select_response(cls: Type[Self]) -> Packet:
        """
        Enable Software Select-Deselect Response, as per page 34 of the
        ImageWriter II Technical Reference Manual.
        """

        return cls.open(SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED)

    @classmethod
    def disable_software_select_response(cls: Type[Self]) -> Packet:
        """
        Disable Software Select-Deselect Response, as per page 34 of the
        ImageWriter II Technical Reference Manual.
        """

        return cls.close(SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED)

    @classmethod
    def enable_lf_when_line_full(cls: Type[Self]) -> Packet:
        """
        Enable the automatic insertion of a line feed when the line is full, as
        per page 34 of the ImageWriter II Technical Reference
        Manual.
        """

        return cls.close(SoftwareSwitch.LF_WHEN_LINE_FULL)

    @classmethod
    def disable_lf_when_line_full(cls: Type[Self]) -> Packet:
        """
        Disable the automatic insertion of a line feed when the line is full,
        as per page 34 of the ImageWriter II Technical Reference Manual.
        """

        return cls.open(SoftwareSwitch.LF_WHEN_LINE_FULL)

    @classmethod
    def enable_lf_ff_print_commands(cls: Type[Self]) -> Packet:
        """
        Enable the treatment of LF and FF as print commands, as per page 34
        of the ImageWriter II Technical Reference Manual.
        """

        return cls.close(SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF)

    @classmethod
    def disable_lf_ff_print_commands(cls: Type[Self]) -> Packet:
        """
        Disable the treatment of LF and FF as print commands, as per page 34
        of the ImageWriter II Technical Reference Manual.
        """

        return cls.open(SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF)

    @classmethod
    def enable_auto_lf_after_cr(cls: Type[Self]) -> Packet:
        """
        Enable an automatic LF after a CR, as per page 34 of the ImageWriter II
        Technical Reference Manual.
        """

        return cls.close(SoftwareSwitch.AUTO_LF_AFTER_CR)

    @classmethod
    def disable_auto_lf_after_cr(cls: Type[Self]) -> Packet:
        """
        Disable an automatic LF after a CR, as per page 34 of the ImageWriter
        II Technical Reference Manual.
        """

        return cls.open(SoftwareSwitch.AUTO_LF_AFTER_CR)

    @classmethod
    def print_slashed_zero(cls: Type[Self]) -> Packet:
        """
        Print zeroes with a slash, as per page 34 of the ImageWriter II
        Technical Reference Manual.
        """

        return cls.close(SoftwareSwitch.SLASHED_ZERO)

    @classmethod
    def print_unslashed_zero(cls: Type[Self]) -> Packet:
        """
        Print zeroes without a slash, as per page 34 of the ImageWriter II
        Technical Reference Manual.
        """

        return cls.open(SoftwareSwitch.SLASHED_ZERO)

    @classmethod
    def enable_perforation_skip(cls: Type[Self]) -> Packet:
        """
        Enable automatic perforation skip, as per page 34 of the ImageWriter II
        Technical Reference Manual.
        """

        return cls.open(SoftwareSwitch.PERFORATION_SKIP_DISABLED)

    @classmethod
    def disable_perforation_skip(cls: Type[Self]) -> Packet:
        """
        Disable automatic perforation skip, as per page 34 of the ImageWriter
        II Technical Reference Manual.
        """

        return cls.close(SoftwareSwitch.PERFORATION_SKIP_DISABLED)

    @classmethod
    def ignore_eighth_data_bit(cls: Type[Self]) -> Packet:
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
    def include_eighth_data_bit(cls: Type[Self]) -> Packet:
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
