from enum import Enum
from typing import Optional, Self

from imagewriter.encoding.base import ctrl, esc


class Pitch(Enum):
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
            Pitch.PICA_PROPORTIONAL,
            Pitch.ELITE_PROPORTIONAL,
        }

    @property
    def cpi(self: Self) -> Optional[int | float]:
        """
        The pitch's characters per inch. Note that proportional fonts do not
        have a set characters per inch, and are specified in dots per inch
        instead.
        """

        return {
            Pitch.EXTENDED: 9,
            Pitch.PICA: 10,
            Pitch.ELITE: 12,
            Pitch.SEMICONDENSED: 13.4,
            Pitch.CONDENSED: 15,
            Pitch.ULTRACONDENSED: 17,
        }.get(self, None)

    @property
    def dpi(self: Self) -> Optional[int]:
        """
        The pitch's dots per inch. Note that only proportional fonts have a
        set dots per inch; all other fonts are specified in characters per
        inch.
        """
        return {
            Pitch.PICA_PROPORTIONAL: 144,
            Pitch.ELITE_PROPORTIONAL: 180,
        }.get(self, None)

    @property
    def characters_per_line(self: Self) -> int:
        """
        Characters per line, as per page 60 of the ImageWriter II Technical
        Reference Manual.

        For non-proportional fonts, this corresponds to characters per inch
        given an 8 inch line. For proportional fonts, the value is not strict
        but still useful for settings left margins.
        """
        return {
            Pitch.EXTENDED: 72,
            Pitch.PICA: 80,
            Pitch.ELITE: 96,
            Pitch.SEMICONDENSED: 107,
            Pitch.CONDENSED: 120,
            Pitch.ULTRACONDENSED: 136,
            Pitch.PICA_PROPORTIONAL: 72,
            Pitch.ELITE_PROPORTIONAL: 79,
        }[self]

    def set_pitch(self: Self) -> bytes:
        """
        Set the pitch, as per page 47 of the ImageWriter II Technical Reference
        Manual.
        """

        return esc(
            {
                Pitch.EXTENDED: "n",
                Pitch.PICA: "N",
                Pitch.ELITE: "E",
                Pitch.SEMICONDENSED: "e",
                Pitch.CONDENSED: "q",
                Pitch.ULTRACONDENSED: "Q",
                Pitch.PICA_PROPORTIONAL: "p",
                Pitch.ELITE_PROPORTIONAL: "P",
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


START_DOUBLE_WIDTH: bytes = ctrl("N")
STOP_DOUBLE_WIDTH: bytes = ctrl("O")
START_UNDERLINE: bytes = esc("X")
STOP_UNDERLINE: bytes = esc("Y")
START_BOLDFACE: bytes = esc("!")
STOP_BOLDFACE: bytes = esc('"')
START_HALF_HEIGHT: bytes = esc("w")
STOP_HALF_HEIGHT: bytes = esc("W")
START_SUPERSCRIPT: bytes = esc("x")
STOP_SUPERSCRIPT: bytes = esc("z")
START_SUBSCRIPT: bytes = esc("y")
STOP_SUBSCRIPT: bytes = STOP_SUPERSCRIPT
