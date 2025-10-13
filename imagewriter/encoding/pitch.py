from enum import Enum
from typing import Optional, Self

from imagewriter.encoding.base import esc


class CharacterPitch(Enum):
    """
    Character pitches, as per page 48 of the ImageWriter II Technical
    Reference Manual.
    """

    EXTENDED = "Extended"
    PICA = "Pica"
    ELITE = "Elite"
    SEMICONDENSED = "Semicondensed"
    CONDENSED = "Condensed"
    ULTRACONDENSED = "Ultracondensed"
    PICA_PROPORTIONAL = "Pica (Proportional)"
    ELITE_PROPORTIONAL = "Elite (Proportional)"

    @property
    def is_proportional(self: Self) -> bool:
        """
        Whether or not the pitch is proportional.

        Note, proportional fonts will not be printed at draft quality.
        """

        return self in {
            CharacterPitch.PICA_PROPORTIONAL,
            CharacterPitch.ELITE_PROPORTIONAL,
        }

    @property
    def cpi(self: Self) -> Optional[int | float]:
        """
        The pitch's characters per inch. Note that proportional fonts do not
        have a set characters per inch, and are specified in dots per inch
        instead.
        """

        return {
            CharacterPitch.EXTENDED: 9,
            CharacterPitch.PICA: 10,
            CharacterPitch.ELITE: 12,
            CharacterPitch.SEMICONDENSED: 13.4,
            CharacterPitch.CONDENSED: 15,
            CharacterPitch.ULTRACONDENSED: 17,
        }.get(self, None)

    @property
    def dpi(self: Self) -> Optional[int]:
        """
        The pitch's dots per inch. Note that only proportional fonts have a
        set dots per inch; all other fonts are specified in characters per
        inch.
        """
        return {
            CharacterPitch.PICA_PROPORTIONAL: 144,
            CharacterPitch.ELITE_PROPORTIONAL: 180,
        }.get(self, None)

    def set_pitch(self: Self) -> bytes:
        """
        Set the pitch, as per page 47 of the ImageWriter II Technical Reference
        Manual.
        """

        return esc(
            {
                CharacterPitch.EXTENDED: "n",
                CharacterPitch.PICA: "N",
                CharacterPitch.ELITE: "E",
                CharacterPitch.SEMICONDENSED: "e",
                CharacterPitch.CONDENSED: "q",
                CharacterPitch.ULTRACONDENSED: "Q",
                CharacterPitch.PICA_PROPORTIONAL: "p",
                CharacterPitch.ELITE_PROPORTIONAL: "P",
            }[self]
        )

    def insert_spaces(self: Self, spaces: int) -> bytes:
        """
        Insert spaces before the next character, as per page 49 of the
        ImageWriter II Technical Reference Manual.

        Note that this command only works for proportional pitches.
        """

        if not self.is_proportional:
            raise ValueError(f"{self.value} is not a proportional pitch")

        if not (1 <= spaces <= 6):
            raise ValueError("Spaces must be from 1 to 6")

        return esc(str(spaces))

    def set_spacing(self: Self, spaces: int) -> bytes:
        """
        Set the amount of spaces inserted between each character, as per page
        49 of the ImageWriter II Technical Reference Manual.

        Note that this command only works for proportional pitches.
        """

        if not self.is_proportional:
            raise ValueError(f"{self.value} is not a proportional pitch")

        if not (1 <= spaces <= 6):
            raise ValueError("Spaces must be from 1 to 6")

        return esc("m", str(spaces))
