from typing import Dict, List, Literal, Self

from imagewriter.encoding.language import Language
from imagewriter.encoding.mousetext import (
    DISABLE_MAP_MOUSETEXT,
    ENABLE_MAP_MOUSETEXT,
    encode_mousetext,
    is_mousetext,
    map_mousetext,
    MouseTextCharacter,
)
from imagewriter.encoding.switch import SoftwareSwitch

LANGUAGES_WITH_ENCODING: Dict[str, List[Language]] = {"£": [Language.BRITISH]}

Mode = Language | Literal[True]

MOUSETEXT_MODE: Mode = True


class SpecialCharacterEncoder:
    """
    An encoder for special characters sourced from either a language font or
    via MouseText.
    """

    def __init__(
        self: Self,
        language: Language = Language.AMERICAN,
        escape_mousetext: bool = True,
    ) -> None:
        self.language: Language = language
        self.mode: Mode = language
        self.escape_mousetext: bool = escape_mousetext

    def _set_mode(self: Self, mode: Mode) -> bytes:
        setting: bytes = b""

        if mode == self.mode:
            return setting

        if self.escape_mousetext:
            if mode is MOUSETEXT_MODE and self.mode is not MOUSETEXT_MODE:
                setting = ENABLE_MAP_MOUSETEXT
            elif mode is not MOUSETEXT_MODE and self.mode is MOUSETEXT_MODE:
                setting = DISABLE_MAP_MOUSETEXT

        # TODO: What if the prior mode was a language mode? We should be able
        # to optimize this
        if isinstance(mode, Language) and mode != self.mode:
            setting = SoftwareSwitch.set_language(mode)

        self.mode = mode

        return setting

    def _language_mode(self: Self, character: int) -> Mode:
        supported: List[Language] = LANGUAGES_WITH_ENCODING.get(
            chr(character), [self.language]
        )

        return self.mode if self.mode in supported else supported[0]

    def encode(self: Self, *text: str | MouseTextCharacter) -> bytes:
        encoded: bytes = encode_mousetext(*text)
        escaped: bytes = SoftwareSwitch.set_language(self.language)
        buffer = b""

        for c in encoded:
            if is_mousetext(c) and isinstance(self.mode, Language):
                # We are switching from a language mode to MouseText mode

                escaped += self.mode.encode(str(buffer))
                escaped += self._set_mode(MOUSETEXT_MODE)
                buffer = b""
            else:
                # We are encoding in a language

                mode: Mode = self._language_mode(c)

                if self.mode is MOUSETEXT_MODE:
                    # We are exiting mousetext mode and need to encode the
                    # current buffer as mousetext
                    escaped += map_mousetext(buffer)
                    buffer = b""
                elif self.mode != mode:
                    # We are changing languages and need to encode the current
                    # buffer as that language
                    assert isinstance(
                        self.mode, Language
                    ), "Expected current mode to be a language"
                    escaped += self.mode.encode(str(buffer))
                    buffer = b""

                self._set_mode(mode)

            # Save the new character to the buffer until we change modes
            buffer += bytes([c])

        # Close out the currently open mode
        if isinstance(self.mode, Language):
            escaped += self.mode.encode(str(buffer))
        else:
            escaped += map_mousetext(buffer)

        escaped += self._set_mode(self.language)

        return escaped
