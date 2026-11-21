from abc import ABC, abstractmethod
from typing import Self

ESC = bytes([27])
CTRL_OFFSET = 64


class InvalidControlCharacterError(ValueError):
    """
    An error raised when a control character is invalid.
    """

    def __init__(self: Self, character: str, point: int) -> None:
        super().__init__(f"{character} ({point}) must be between 64 and 95 inclusive")


class LengthError(ValueError):
    """
    An error raised when a character has no meaningful length.
    """


def is_ctrl_point(point: int) -> bool:
    """
    Whether or not the code point is valid for a control character.
    """

    return 64 <= point <= 95


def is_ctrl_character(character: str) -> bool:
    """
    Whether or not the character is a valid control character.
    """
    return is_ctrl_point(ord(character))


def ctrl(character: str) -> bytes:
    """
    Generate a control character, as per page 5 of the ImageWriter II Technical
    Reference Manual.
    """

    point: int = ord(character)

    if not is_ctrl_point(point):
        raise InvalidControlCharacterError(character, point)

    return bytes(chr(point - CTRL_OFFSET), encoding="ascii")


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

    @abstractmethod
    def __bytes__(self: Self) -> bytes:
        pass

    def __eq__(self: Self, other: object) -> bool:
        if not isinstance(other, Command):
            return False
        return bytes(self) == bytes(other)

    def __str__(self: Self) -> str:
        return bytes(self).decode(encoding="ascii")

    def __repr__(self: Self) -> str:
        return f"Command({self!s})"

    def __len__(self: Self) -> int:
        """
        The printed length of the command, in characters.

        Most commands are control characters or escape sequences, and have
        zero length.
        """

        return 0


class Bytes(Command):
    """
    A command containing raw bytes.
    """

    def __init__(self: Self, data: bytes) -> None:
        self.bytes: bytes = data

    def __bytes__(self: Self) -> bytes:
        return self.bytes

    def __repr__(self: Self) -> str:
        return f"Bytes({bytes(self)!r})"


class Print(Bytes):
    """
    A series of printable characters.
    """

    def __len__(self: Self) -> int:
        return len(bytes(self))

    def __repr__(self: Self) -> str:
        return repr(bytes(self))


class Space(Print):
    """
    A single space.
    """

    def __init__(self: Self) -> None:
        super().__init__(b" ")


SPACE = Space()


class Ctrl(Command):
    """
    A command containing a single control character.
    """

    def __init__(self: Self, character: str) -> None:
        self.character: str = character
        self.ctrl: bytes = ctrl(character)

    def __bytes__(self: Self) -> bytes:
        return self.ctrl

    def __repr__(self: Self) -> str:
        return f"Ctrl({self.character})"


class Esc(Command):
    """
    A command containing a single escape code.
    """

    def __init__(self: Self, code: str) -> None:
        self.code = code
        self.esc = esc(code)

    def __bytes__(self: Self) -> bytes:
        return self.esc

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
