from imagewriter.encoding.base import Command, Esc
from imagewriter.pitch import Pitch


def set_pitch(pitch: Pitch) -> Command:
    """
    Set the pitch, as per page 47 of the ImageWriter II Technical Reference
    Manual.
    """

    return Esc(
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


def insert_spaces(pitch: Pitch, spaces: int) -> Command:
    """
    Insert spaces before the next character, as per page 49 of the
    ImageWriter II Technical Reference Manual.

    Note that this command only works for proportional pitches.
    """

    if not pitch.is_proportional:
        raise ValueError(f"{pitch.value} is not a proportional pitch")

    if not (1 <= spaces <= 6):
        raise ValueError("Spaces must be from 1 to 6")

    return Esc(str(spaces))


def set_spacing(pitch: Pitch, spaces: int) -> Command:
    """
    Set the amount of spaces inserted between each character, as per page
    49 of the ImageWriter II Technical Reference Manual.

    Note that this command only works for proportional pitches.
    """

    if not pitch.is_proportional:
        raise ValueError(f"{pitch.value} is not a proportional pitch")

    if not (1 <= spaces <= 6):
        raise ValueError("Spaces must be from 1 to 6")

    return Esc("m" + str(spaces))
