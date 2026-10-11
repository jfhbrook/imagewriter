from abc import ABC, abstractmethod
from typing import Any, Generator, Self

from imagewriter.base.character import (
    Character,
    CustomCharacter,
    map_to_low_ascii,
    MouseTextCharacter,
    Text,
)
from imagewriter.base.language import Language
from imagewriter.encoding.base import Command, Esc, Print
from imagewriter.encoding.character.custom import (
    BOTTOM_WIRES,
    LoadCustomCharacters,
    SetMaxCustomCharacterWidth,
    TOP_WIRES,
)
from imagewriter.encoding.character.language import LANGUAGE_CHARACTERS
from imagewriter.encoding.character.mousetext import MOUSETEXT_LOOKUP
from imagewriter.encoding.language import set_language
from imagewriter.encoding.motion import CR, LF, TAB

# TODO: Print a test page of alternate language characters, figure out what
# the alternate characters are, and complete this table.

# TODO: Deprecate and remove
MOUSETEXT_CHARACTERS: dict[str, MouseTextCharacter] = {
    name: char[0] for name, char in MOUSETEXT_LOOKUP.items()
}


class DisableMode(Esc):
    def __init__(self: Self) -> None:
        super().__init__("$")

    def __repr__(self: Self) -> str:
        return "DisableMode()"


DISABLE_MODE = DisableMode()


class EnableMouseTextMappingMode(Esc):
    def __init__(self: Self) -> None:
        super().__init__("&")

    def __repr__(self: Self) -> str:
        return "EnableMouseTextMappingMode()"


ENABLE_MOUSE_TEXT_MAPPING_MODE = EnableMouseTextMappingMode()


class EnableCustomCharacterMode(Esc):
    def __init__(self: Self, map: bool) -> None:
        self._map = map
        super().__init__("*" if map else "'")

    def __repr__(self: Self) -> str:
        return f"EnableCustomCharacterMode(map={self._map})"


class Mode(ABC):
    @abstractmethod
    def enable(self: Self) -> list[Command]:
        pass

    @abstractmethod
    def disable(self: Self) -> list[Command]:
        pass

    @abstractmethod
    def __eq__(self: Self, other: Any) -> bool:
        pass


class LanguageMode(Mode):
    def __init__(self: Self, language: Language) -> None:
        self.language: Language = language

    def enable(self: Self) -> list[Command]:
        return set_language(self.language)

    def disable(self: Self) -> list[Command]:
        # Language modes can not be disabled
        return []

    def __eq__(self: Self, other: Any) -> bool:
        return isinstance(other, LanguageMode) and self.language == other.language


LANGUAGE_MODES: dict[str, list[LanguageMode]] = {
    ch: [LanguageMode(lang) for lang in langs]
    for ch, langs in LANGUAGE_CHARACTERS.items()
}


class MouseTextMode(Mode):
    def __init__(self, map: bool = True) -> None:
        self.map: bool = map

    def enable(self: Self) -> list[Command]:
        return [ENABLE_MOUSE_TEXT_MAPPING_MODE] if self.map else list()

    def disable(self: Self) -> list[Command]:
        return [DISABLE_MODE] if self.map else list()

    def __eq__(self: Self, other: Any) -> bool:
        return isinstance(other, MouseTextMode) and self.map == other.map


class CustomCharacterMode(Mode):
    def __init__(self: Self, map: bool = True) -> None:
        self.map: bool = map

    def enable(self: Self) -> list[Command]:
        return [EnableCustomCharacterMode(self.map)]

    def disable(self: Self) -> list[Command]:
        return [DISABLE_MODE]

    def __eq__(self: Self, other: Any) -> bool:
        return isinstance(other, MouseTextMode) and self.map == other.map


def extract_characters(*text: Text) -> Generator[Character, None, None]:
    for tx in text:
        if isinstance(tx, str):
            for c in tx:
                if c in MOUSETEXT_CHARACTERS:
                    yield MOUSETEXT_CHARACTERS[c]
                else:
                    yield c
        elif isinstance(tx, list):
            for s in tx:
                yield s
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
        default_mode: LanguageMode = LanguageMode(language)

        self.default_mode: LanguageMode = default_mode
        self.map_mousetext: bool = map_mousetext
        self.map_custom: bool = map_custom

        self.language_mode: LanguageMode = default_mode
        self.mode: Mode = default_mode

    def _next_mode(self: Self, character: Character) -> Mode:
        if isinstance(character, MouseTextCharacter):
            return MouseTextMode(map=self.map_mousetext)

        if isinstance(character, CustomCharacter):
            return CustomCharacterMode(map=self.map_custom)

        supported: list[LanguageMode] = LANGUAGE_MODES.get(
            character, [self.language_mode]
        )

        if self.language_mode.language in supported:
            return self.language_mode
        else:
            return supported[0]

    def _set_mode(self: Self, mode: Mode) -> list[Command]:
        if mode == self.mode:
            return []

        # Disable the current mode and enable the new mode
        encoded: list[Command] = self.mode.disable() + mode.enable()

        # Save the newest language mode
        if isinstance(mode, LanguageMode):
            self.language_mode = mode

        self.mode = mode

        return encoded

    def _from_buffer(self: Self, buffer: bytes) -> list[Command]:
        def _to_command(byte: int) -> Command:
            data = byte.to_bytes(byteorder="big")
            if data == b"\r":
                return CR
            if data == b"\n":
                return LF
            if data == b"\t":
                return TAB
            return Print(data)

        return [_to_command(byte) for byte in buffer]

    def encode(self: Self, *text: Text) -> list[Command]:
        encoded: list[Command] = list()
        mode: Mode = self.language_mode
        buffer: bytes = b""

        for ch in extract_characters(*text):
            # Get the new mode
            mode = self._next_mode(ch)

            # If the mode is changing, add the buffer to the encoded output
            if mode != self.mode:
                encoded += self._from_buffer(buffer)
                buffer = b""

            # Set the new mode
            encoded += self._set_mode(mode)

            # Add the new text to the buffer
            if isinstance(ch, str):
                # Recall that we already extracted MouseText characters
                buffer += bytes(ch, encoding="ascii")
            elif isinstance(ch, MouseTextCharacter):
                if self.map_mousetext:
                    buffer += bytes([map_to_low_ascii(ch.value)])
                else:
                    buffer += bytes([ch.value])
            else:
                if self.map_custom:
                    buffer += bytes([map_to_low_ascii(ch.point)])
                else:
                    buffer += bytes([ch.point])

        # Attach the final buffer
        encoded += self._from_buffer(buffer)
        encoded += self.mode.disable()

        # Enable the default language if need be
        if self.language_mode != self.default_mode:
            encoded += self.default_mode.enable()

        return encoded


__all__: list[str] = [
    "SetMaxCustomCharacterWidth",
    "LoadCustomCharacters",
    "DisableMode",
    "DISABLE_MODE",
    "EnableMouseTextMappingMode",
    "ENABLE_MOUSE_TEXT_MAPPING_MODE",
    "EnableCustomCharacterMode",
    "CharacterEncoder",
    "TOP_WIRES",
    "BOTTOM_WIRES",
]
