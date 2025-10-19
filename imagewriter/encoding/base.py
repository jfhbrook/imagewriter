from abc import ABC, abstractmethod
from typing import Any, Self

ESC = bytes([27])


def ctrl(character: str) -> bytes:
    """
    Generate a control character, as per page 5 of the ImageWriter II Technical
    Reference Manual.
    """

    point: int = ord(character)

    if not (64 <= point <= 95):
        raise ValueError(f"{character} ({point}) must be between 64 and 95 inclusive")

    return bytes(chr(point - 64), encoding="ascii")


def esc(character: str) -> bytes:
    """
    Generate an escape code, as per page 5 of the ImageWriter II Technical
    Reference Manual.
    """

    return ESC + bytes(character, encoding="ascii")


class Command(ABC):
    """
    A chunk of data which should be written as a single unit, even if CTS is
    de-asserted.
    """

    def __len__(self: Self) -> int:
        return len(self.__bytes__())

    @abstractmethod
    def __bytes__(self: Self) -> bytes:
        pass

    def __eq__(self: Self, other: Any) -> bool:
        if not isinstance(other, Command):
            return False
        return bytes(self) == bytes(other)

    def __str__(self: Self) -> str:
        return bytes(self).decode(encoding="ascii")

    def __repr__(self: Self) -> str:
        return f"Command({str(self)})"


class Bytes(Command):
    """
    A packet containing raw bytes.
    """

    def __init__(self: Self, data: bytes) -> None:
        self.bytes: bytes = data

    def __bytes__(self: Self) -> bytes:
        return self.bytes

    def __repr__(self: Self) -> str:
        return repr(bytes(self))


class Ctrl(Command):
    """
    A packet containing a single control character.
    """

    def __init__(self: Self, character: str) -> None:
        self.character: bytes = ctrl(character)

    def __bytes__(self: Self) -> bytes:
        return self.character

    def __repr__(self: Self) -> str:
        return f"Ctrl({self.character})"


class Esc(Command):
    """
    A packet containing a single escape code.
    """

    def __init__(self: Self, code: str) -> None:
        self.code = code

    def __bytes__(self: Self) -> bytes:
        return esc(self.code)

    def __repr__(self: Self) -> str:
        return f"Esc({self.code})"


def number(n: int, width: int = 0) -> bytes:
    """
    A number, formatted with leading zeros.
    """

    formatted = str(n)

    while len(formatted) < width:
        formatted = "0" + formatted

    return formatted.encode(encoding="ascii")
