from abc import ABC, abstractmethod
from typing import Any, Self

from imagewriter.encoding.base import Command, Esc


class Mode(ABC):
    """
    A mode.
    """

    @abstractmethod
    def enable(self: Self) -> list[Command]:
        pass

    @abstractmethod
    def disable(self: Self) -> list[Command]:
        pass

    @abstractmethod
    def __eq__(self: Self, other: Any) -> bool:
        pass


class DisableMode(Esc):
    """
    Disable the current character mode, switching back to the standard character set.

    TODO: This is documented in multiple places...
    """

    def __init__(self: Self) -> None:
        super().__init__("$")

    def __repr__(self: Self) -> str:
        return "DisableMode()"


DISABLE_MODE = DisableMode()
