from contextlib import contextmanager
from typing import Generator, Self, Type


class CharacterError(Exception):
    """
    An error related to character operations.
    """

    @classmethod
    @contextmanager
    def capture(cls: Type[Self]) -> Generator[None, None, None]:
        try:
            yield
        except Exception as exc:
            raise cls(str(exc)) from exc


class CodePointError(CharacterError):
    """
    An error related to code point operations.
    """
