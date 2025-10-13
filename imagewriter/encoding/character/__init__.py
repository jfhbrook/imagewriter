from abc import abstractmethod
from typing import Any, Dict, Generator, List, Self

from imagewriter.encoding.base import esc
from imagewriter.encoding.character.custom import CustomCharacter, CustomCharacters
from imagewriter.encoding.character.mousetext import MouseText, MouseTextCharacter
from imagewriter.encoding.language import Language
from imagewriter.encoding.switch import SoftwareSwitch

Text = str | MouseText | CustomCharacters
Character = str | MouseTextCharacter | CustomCharacter

# TODO: Print a test page of alternate language characters, figure out what
# the alternate characters are, and complete this table.

LANGUAGE_ENCODINGS: Dict[Language, Dict[str, str]] = {
    Language.AMERICAN: dict(),
    Language.BRITISH: {"£": "#"},
    Language.GERMAN: dict(),
    Language.FRENCH: dict(),
    Language.SWEDISH: dict(),
    Language.ITALIAN: dict(),
    Language.SPANISH: dict(),
    Language.DANISH: dict(),
}

# TODO: Refactor to a List[LanguageMode] ?
LANGUAGES_WITH_ENCODING: Dict[str, List[Language]] = {"£": [Language.BRITISH]}

MOUSETEXT_CHARACTERS: Dict[str, MouseTextCharacter] = {
    "⌛︎": MouseTextCharacter.HOURGLASS,
    "←": MouseTextCharacter.LEFTWARDS_ARROW,
    "…": MouseTextCharacter.ELLIPSIS,
    "↓": MouseTextCharacter.DOWNWARDS_ARROW,
    "↑": MouseTextCharacter.UPWARDS_ARROW,
    "↵": MouseTextCharacter.CARRIAGE_RETURN,
    "▉": MouseTextCharacter.FULL_BLOCK,
    "→": MouseTextCharacter.RIGHTWARDS_ARROW,
    "▕": MouseTextCharacter.RIGHT_ONE_EIGHTH_BLOCK,
    "◆": MouseTextCharacter.BLACK_DIAMOND,
    "▏": MouseTextCharacter.LEFT_ONE_EIGHTH_BLOCK,
}

DISABLE_MODE = esc("$")


class Mode:
    @abstractmethod
    def enable(self: Self) -> bytes:
        pass

    @abstractmethod
    def disable(self: Self) -> bytes:
        pass

    @abstractmethod
    def __eq__(self: Self, other: Any) -> bool:
        pass


class LanguageMode(Mode):
    def __init__(self: Self, language: Language) -> None:
        self.language: Language = language

    def enable(self: Self) -> bytes:
        return SoftwareSwitch.set_language(self.language)

    def disable(self: Self) -> bytes:
        # Language modes can not be disabled
        return b""

    def __eq__(self: Self, other: Any) -> bool:
        return isinstance(other, LanguageMode) and self.language == other.language


class MouseTextMode(Mode):
    def __init__(self, map: bool = True) -> None:
        self.map: bool = map

    def enable(self: Self) -> bytes:
        return esc("&") if self.map else b""

    def disable(self: Self) -> bytes:
        return DISABLE_MODE if self.map else b""

    def __eq__(self: Self, other: Any) -> bool:
        return isinstance(other, MouseTextMode) and self.map == other.map


class CustomCharacterMode(Mode):
    def __init__(self: Self, map: bool = True) -> None:
        self.map: bool = map

    def enable(self: Self) -> bytes:
        return esc("*") if self.map else esc("'")

    def disable(self: Self) -> bytes:
        return DISABLE_MODE

    def __eq__(self: Self, other: Any) -> bool:
        return isinstance(other, MouseTextMode) and self.map == other.map


def map_to_low_ascii(point: int) -> int:
    """
    Map a code point (either MouseText or a custom character) to low ASCII, as
    per page 40 (MouseText) and page 45 (custom characters) of the ImageWriter
    II Technical Reference Manual.

    This is necessary if the eighth data bit is ignored.
    """

    assert 160 <= point <= 239, "Code point is not valid upper ASCII"
    return point - 128


def extract_characters(*text: Text) -> Generator[Character, None, None]:
    for tx in text:
        if isinstance(tx, str):
            for c in tx:
                if c in MOUSETEXT_CHARACTERS:
                    yield MOUSETEXT_CHARACTERS[c]
                else:
                    yield c
        elif isinstance(tx, list):
            for c in tx:
                yield c
        else:
            yield tx


class CharacterEncoder:
    """
    An encoder for characters leveraging language fonts, MouseText and/or
    custom characters.
    """

    def __init__(
        self: Self,
        language: Language = Language.AMERICAN,
        map_mousetext: bool = True,
        map_custom: bool = True,
    ) -> None:
        # TODO: Refactor to store default language mode
        self.language: Language = language
        self.map_mousetext: bool = map_mousetext
        self.map_custom: bool = map_custom

        self.language_mode: LanguageMode = LanguageMode(language)
        self.mode: Mode = self.language_mode

    def _next_mode(self: Self, character: Character) -> Mode:
        if isinstance(character, MouseTextCharacter):
            return MouseTextMode(map=self.map_mousetext)

        if isinstance(character, CustomCharacter):
            return CustomCharacterMode(map=self.map_custom)

        # TODO: If this encoding table is complete, it should be safe to
        # default to self.language_mode.language.
        supported: List[Language] = LANGUAGES_WITH_ENCODING.get(
            character, [self.language]
        )

        if self.language_mode.language in supported:
            return self.language_mode
        else:
            return LanguageMode(supported[0])

    def _set_mode(self: Self, mode: Mode) -> bytes:
        if mode == self.mode:
            return b""

        # Disable the current mode and enable the new mode
        encoded: bytes = self.mode.disable() + mode.enable()

        # Save the newest language mode
        if isinstance(mode, LanguageMode):
            self.language_mode = mode

        self.mode = mode

        return encoded

    def enable_default_language(self: Self) -> bytes:
        return LanguageMode(self.language).enable()

    def encode(self: Self, *text: Text) -> bytes:
        encoded: bytes = b""
        mode: Mode = self.language_mode
        buffer: bytes = b""

        for ch in extract_characters(*text):
            # Get the new mode
            mode = self._next_mode(ch)

            # If the mode is changing, add the buffer to the encoded output
            if mode != self.mode:
                encoded += buffer
                buffer = b""

            # Set the new mode
            encoded += self._set_mode(mode)

            # Add the new text to the buffer
            if isinstance(ch, str):
                # Recall that we already extracted MouseText characters
                buffer += bytes(ch, encoding="ascii")
            elif isinstance(ch, MouseTextCharacter):
                buffer += bytes([ch.value])
            else:
                buffer += bytes([ch.point])

        # Attach the final buffer
        encoded += buffer
        encoded += self.mode.disable()

        # Enable the default language if need be
        if self.language_mode.language != self.language:
            encoded += self.enable_default_language()

        return encoded
