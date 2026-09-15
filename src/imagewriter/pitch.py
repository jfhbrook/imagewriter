from enum import Enum
from typing import Optional, Self

LINE_WIDTH = 8  # inches
VERTICAL_RESOLUTION = 72  # dots per inch


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
    def characters_per_inch(self: Self) -> int:
        """
        Characters per inch, as per page 66 of the ImageWriter II Technical
        Reference Manual.

        For non-proportional fonts, this corresponds to characters per inch.
        For proportional fonts, the value is not strict but still useful for
        setting tab stops.
        """

        return {
            Pitch.EXTENDED: 9,
            Pitch.PICA: 10,
            Pitch.ELITE: 12,
            Pitch.SEMICONDENSED: 13.4,
            Pitch.CONDENSED: 15,
            Pitch.ULTRACONDENSED: 17,
            Pitch.PICA_PROPORTIONAL: 9,
            Pitch.ELITE_PROPORTIONAL: 10,
        }[self]

    @property
    def characters_per_line(self: Self) -> int:
        """
        Characters per line, as per page 60 of the ImageWriter II Technical
        Reference Manual.

        For non-proportional fonts, this corresponds to characters per inch
        given an 8 inch line. For proportional fonts, the value is not strict
        but still useful for setting left margins.
        """

        return int(self.characters_per_inch * LINE_WIDTH)

    @property
    def max_character_position(self: Self) -> int:
        """
        The maximum character position, which is one less than the total
        characters per line.
        """

        return self.characters_per_line - 1

    @property
    def horizontal_resolution(self: Self) -> int:
        """
        The horizontal resolution in graphics mode, as per page 106 of the
        ImageWriter II Technical Reference Manual, in dots per inch.
        """

        return {
            Pitch.EXTENDED: 72,
            Pitch.PICA: 80,
            Pitch.ELITE: 96,
            Pitch.SEMICONDENSED: 107,
            Pitch.CONDENSED: 120,
            Pitch.ULTRACONDENSED: 136,
            Pitch.PICA_PROPORTIONAL: 144,
            Pitch.ELITE_PROPORTIONAL: 160,
        }[self]

    @property
    def vertical_resolution(self: Self) -> int:
        """
        The vertical resolution in graphics mode as per page 104 of the
        ImageWriter II Technical Reference Manual, which is 72 dpi regardless
        of pitch.
        """

        return VERTICAL_RESOLUTION

    @property
    def width(self: Self) -> int:
        """
        The maximum width in graphics mode, as per page 106 of the ImageWriter
        II Technical Reference Manual, in dots.
        """

        return {
            Pitch.EXTENDED: 576,
            Pitch.PICA: 640,
            Pitch.ELITE: 768,
            Pitch.SEMICONDENSED: 856,
            Pitch.CONDENSED: 960,
            Pitch.ULTRACONDENSED: 1088,
            Pitch.PICA_PROPORTIONAL: 1152,
            Pitch.ELITE_PROPORTIONAL: 1280,
        }[self]
