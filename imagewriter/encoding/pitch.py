from enum import Enum
from typing import Optional, Self

from imagewriter.encoding.base import esc


class CharacterPitch(Enum):
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
        return self in {
            CharacterPitch.PICA_PROPORTIONAL,
            CharacterPitch.ELITE_PROPORTIONAL,
        }

    @property
    def cpi(self: Self) -> Optional[int | float]:
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
        return {
            CharacterPitch.PICA_PROPORTIONAL: 144,
            CharacterPitch.ELITE_PROPORTIONAL: 180,
        }.get(self, None)

    def set_pitch(self: Self) -> bytes:
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
        if not self.is_proportional:
            raise ValueError(f"{self.value} is not a proportional pitch")

        if not (1 <= spaces <= 6):
            raise ValueError("Spaces must be from 1 to 6")

        return esc(str(spaces))

    def set_spacing(self: Self, spaces: int) -> bytes:
        if not self.is_proportional:
            raise ValueError(f"{self.value} is not a proportional pitch")

        if not (1 <= spaces <= 6):
            raise ValueError("Spaces must be from 1 to 6")

        return esc("m", str(spaces))
