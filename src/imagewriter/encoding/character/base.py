from abc import ABC, abstractmethod
from typing import Any, Self

from imagewriter.encoding.base import Command, Esc


class Mode(ABC):
    """
    A mode.
    """

    @abstractmethod
    def enable(self: Self) -> list[Command]:
        """
        Enable the mode. Once enabled, the printer is in this mode.
        """

        pass

    @abstractmethod
    def disable(self: Self) -> list[Command]:
        """
        Disable the mode. Once disabled, the printer is in its standard state.
        """

        pass

    @abstractmethod
    def __eq__(self: Self, other: Any) -> bool:
        """
        Check if two modes are equivalent.
        """

        pass


class DisableMode(Esc):
    """
    Disable the current character mode, switching back to the standard character set.

    This command is used with both MouseText high ASCII mode and custom characters
    modes - see pages 41 and 98 of the ImageWriter II Technical Reference Manual,
    respectively.
    """

    def __init__(self: Self) -> None:
        super().__init__("$")

    def __repr__(self: Self) -> str:
        return "DisableMode()"


DISABLE_MODE = DisableMode()
