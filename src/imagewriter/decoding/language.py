from collections.abc import Generator

from parsy import Parser, generate  # type: ignore

from imagewriter.base.character import Language
from imagewriter.base.switch import SoftwareSwitches
from imagewriter.decoding.base import State
from imagewriter.decoding.switch import close_software_switches, open_software_switches
from imagewriter.encoding.language import CloseLanguageSwitches, OpenLanguageSwitches
from imagewriter.encoding.switch import (
    CloseSoftwareSwitches,
    OpenSoftwareSwitches,
    SetSoftwareSwitches,
    SoftwareSwitch,
)


def _is_language_command(command: SetSoftwareSwitches) -> bool:
    packed = command.pack()

    return (packed[0] & 0b11111000) == 0 and packed[1] == 0


def _from_closed_switches(
    state: State, closed_switches: set[SoftwareSwitch]
) -> Language:
    switches = state.switches.switches | closed_switches

    return SoftwareSwitches.language_from_switches(switches)


def _from_open_switches(state: State, opened_switches: set[SoftwareSwitch]) -> Language:
    switches = state.switches.switches - opened_switches

    return SoftwareSwitches.language_from_switches(switches)


def open_language_switches(state: State) -> Parser:
    @generate
    def parser() -> Generator[Parser, OpenSoftwareSwitches, OpenLanguageSwitches]:
        with state.transaction():
            open_ = yield open_software_switches(state)

            if _is_language_command(open_):
                language = _from_open_switches(state, open_.switches)
                return OpenLanguageSwitches(language)

            raise ValueError(f"Unexpected opened switches: {open_}")

    return parser


def close_language_switches(state: State) -> Parser:
    @generate
    def parser() -> Generator[Parser, CloseSoftwareSwitches, CloseLanguageSwitches]:
        with state.transaction():
            close_ = yield close_software_switches(state)

            if _is_language_command(close_):
                language = _from_closed_switches(state, close_.switches)
                return CloseLanguageSwitches(language)

            raise ValueError(f"Unexpected closed switches: {close_}")

    return parser
