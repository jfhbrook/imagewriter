from typing import Self

from imagewriter.encoding.base import Esc
from imagewriter.pitch import Pitch


class SetPitch(Esc):
    """
    Set the pitch, as per page 47 of the ImageWriter II Technical Reference
    Manual.
    """

    def __init__(self: Self, pitch: Pitch) -> None:
        self._pitch = pitch

        super().__init__(
            {
                Pitch.EXTENDED: "n",
                Pitch.PICA: "N",
                Pitch.ELITE: "E",
                Pitch.SEMICONDENSED: "e",
                Pitch.CONDENSED: "q",
                Pitch.ULTRACONDENSED: "Q",
                Pitch.PICA_PROPORTIONAL: "p",
                Pitch.ELITE_PROPORTIONAL: "P",
            }[pitch]
        )

    def __repr__(self: Self) -> str:
        return f"SetPitch({self._pitch})"


class InsertSpaces(Esc):
    """
    Insert spaces before the next character, as per page 49 of the
    ImageWriter II Technical Reference Manual.

    Note that this command only works for proportional pitches.
    """

    def __init__(self: Self, pitch: Pitch, spaces: int) -> None:
        if not pitch.is_proportional:
            raise ValueError(f"{pitch.value} is not a proportional pitch")

        if not (1 <= spaces <= 6):
            raise ValueError("Spaces must be from 1 to 6")

        self._pitch = pitch
        self._spaces = spaces

        return super().__init__(str(spaces))


class SetSpacing(Esc):
    """
    Set the amount of spaces inserted between each character, as per page
    49 of the ImageWriter II Technical Reference Manual.

    Note that this command only works for proportional pitches.
    """

    def __init__(self: Self, pitch: Pitch, spaces: int) -> None:
        if not pitch.is_proportional:
            raise ValueError(f"{pitch.value} is not a proportional pitch")

        if not (1 <= spaces <= 6):
            raise ValueError("Spaces must be from 1 to 6")

        self._pitch = pitch
        self._spaces = spaces

        return super().__init__("m" + str(spaces))

    def __repr__(self: Self) -> str:
        return f"SetSpacing({self._pitch}, {self._spaces})"
