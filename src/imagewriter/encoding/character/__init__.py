from collections.abc import Generator
from typing import Self

from imagewriter.base.character import (
    Character,
    CustomCharacter,
    Language,
    LanguageCharacter,
    MouseTextCharacter,
    Text,
    map_to_low_ascii,
)
from imagewriter.encoding.base import Command, Print
from imagewriter.encoding.character.base import Mode
from imagewriter.encoding.character.custom import CustomCharacterMode
from imagewriter.encoding.character.language import LANGUAGE_MODES, LanguageMode
from imagewriter.encoding.character.mousetext import MouseTextMode
from imagewriter.encoding.character.parser import parse_text
from imagewriter.encoding.motion import CR, LF, TAB


def extract_characters(*text: Text, emoji_codes: bool) -> Generator[Character]:
    for tx in text:
        yield from parse_text(tx, emoji_codes=emoji_codes)


class CharacterEncoder:
    """
    An encoder for characters leveraging language fonts, MouseText and/or
    custom characters.
    """

    def __init__(
        self: Self,
        language: Language = Language.AMERICAN,
        include_eighth_data_bit: bool = True,
        emoji_codes: bool = True,
    ) -> None:
        default_mode: LanguageMode = LanguageMode(language)

        self.default_mode: LanguageMode = default_mode
        self.include_eighth_data_bit = include_eighth_data_bit
        self.emoji_codes: bool = emoji_codes

        self.language_mode: LanguageMode = default_mode
        self.mode: Mode = default_mode

    @property
    def map_ascii(self: Self) -> bool:
        """
        Whether or not to map low ASCII to high ASCII.

        Mapping to high ASCII is only necessary if the eighth data bit is not included.
        """

        return not self.include_eighth_data_bit

    def _next_mode(self: Self, character: Character) -> Mode:
        if isinstance(character, LanguageCharacter):
            return LanguageMode(character.language)
        if isinstance(character, MouseTextCharacter):
            return MouseTextMode(map_ascii=self.map_ascii)

        if isinstance(character, CustomCharacter):
            return CustomCharacterMode(map_ascii=self.map_ascii)

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
        encoded: list[Command] = []
        mode: Mode = self.language_mode
        buffer: bytes = b""

        for ch in extract_characters(*text, emoji_codes=self.emoji_codes):
            # Get the new mode
            mode = self._next_mode(ch)

            # If the mode is changing, add the buffer to the encoded output
            if mode != self.mode:
                encoded += self._from_buffer(buffer)
                buffer = b""

            # Set the new mode
            encoded += self._set_mode(mode)

            # Add the new text to the buffer
            if isinstance(ch, LanguageCharacter):
                buffer += bytes(ch.encoded, encoding="ascii")
            elif isinstance(ch, str):
                # Recall that we already extracted MouseText characters
                buffer += bytes(ch, encoding="ascii")
            elif isinstance(ch, MouseTextCharacter):
                if self.map_ascii:
                    buffer += bytes([map_to_low_ascii(ch.value)])
                else:
                    buffer += bytes([ch.value])
            else:
                if self.map_ascii:
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
