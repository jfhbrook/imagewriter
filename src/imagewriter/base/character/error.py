from collections.abc import Generator
from contextlib import contextmanager
from typing import Self


class CharacterError(Exception):
    """
    An error related to character operations.
    """

    @classmethod
    @contextmanager
    def capture(cls: type[Self]) -> Generator[None]:
        try:
            yield
        except Exception as exc:
            raise cls(str(exc)) from exc


class CodePointError(CharacterError):
    """
    An error related to code point operations.
    """
