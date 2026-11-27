from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, Self, cast

from parsy import Parser, regex, string  # type: ignore

from imagewriter.base.pitch import Pitch
from imagewriter.base.settings import Settings
from imagewriter.base.switch import SoftwareSwitches
from imagewriter.encoding.base import (
    SPACE,
    Ctrl,
    Esc,
)
from imagewriter.encoding.base import (
    ctrl as encode_ctrl,
)
from imagewriter.encoding.base import (
    esc as encode_esc,
)


class State:
    """
    Track printer state. This is needed because some parsers depend on state.
    """

    def __init__(self: Self, settings: Settings) -> None:
        self.settings = settings.clone()

    @contextmanager
    def transaction(self: Self) -> Generator[None]:
        """
        Run parsers that can mutate state inside a transaction. On an exception, roll
        back state.
        """

        settings = self.settings.clone()
        try:
            yield
        except Exception:
            self.settings = settings
            raise

    @property
    def switches(self: Self) -> SoftwareSwitches:
        return self.settings.software_switches

    @switches.setter
    def switches(self: Self, switches: SoftwareSwitches) -> None:
        """
        Set software switches.
        """

        self.settings.software_switches = switches

    @property
    def pitch(self: Self) -> Pitch:
        return self.settings.pitch

    @pitch.setter
    def pitch(self: Self, pitch: Pitch) -> None:
        self.settings.pitch = pitch


def bytes_(expected_bytes: bytes) -> Parser:
    """
    Parse raw bytes. A thin wrapper around parsy's string parser.
    """

    return cast(Any, string)(expected_bytes)


space = bytes_(b" ").map(lambda _: SPACE)


def ctrl(character: str) -> Parser:
    return bytes_(encode_ctrl(character))


def esc(code: str) -> Parser:
    return bytes_(encode_esc(code))


def ctrl_command(command: Ctrl) -> Parser:
    """
    Parse a Ctrl command.
    """

    return bytes_(command.ctrl).map(lambda _: command)


def esc_command(command: Esc) -> Parser:
    """
    Parse an Esc command.
    """

    return bytes_(command.esc).map(lambda _: command)


def number(width: int = 0) -> Parser:
    """
    Parse a fixed width number.
    """

    re = f"[0-9]{{{width}}}"
    return regex(re).map(int)
