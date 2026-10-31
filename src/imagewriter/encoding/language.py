from typing import Self

from imagewriter.base.character import Language
from imagewriter.base.switch import SoftwareSwitch
from imagewriter.encoding.base import Command
from imagewriter.encoding.switch import (
    CloseSoftwareSwitches,
    OpenSoftwareSwitches,
    fmt_switch_banks,
    fmt_switch_position,
)


class OpenLanguageSwitches(OpenSoftwareSwitches):
    def __init__(self: Self, language: Language) -> None:
        self._language = language
        super().__init__(SoftwareSwitch.open_language_switches(language))

    def __repr__(self: Self) -> str:
        position = fmt_switch_position(self.closed)
        banks = fmt_switch_banks(self.pack())

        return f"OpenLanguageSwitches({self._language}, {position}, {banks})"


class CloseLanguageSwitches(CloseSoftwareSwitches):
    def __init__(self: Self, language: Language) -> None:
        self._language = language
        super().__init__(SoftwareSwitch.language_switches(language))

    def __repr__(self: Self) -> str:
        position = fmt_switch_position(self.closed)
        banks = fmt_switch_banks(self.pack())

        return f"CloseLanguageSwitches({self._language}, {position}, {banks})"


def set_language(language: Language) -> list[Command]:
    """
    Set the language, irrespective of current software switch or language
    settings.
    """

    commands: list[Command] = []

    open = OpenLanguageSwitches(language)
    close = CloseLanguageSwitches(language)

    if open.pack() != bytes([0, 0]):
        commands.append(open)

    if close.pack() != bytes([0, 0]):
        commands.append(close)

    return commands
