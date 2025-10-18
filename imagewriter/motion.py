from typing import List, Literal, Self, Sequence

from imagewriter.pitch import Pitch
from imagewriter.units import Distance, Inch, Length, length_to_distance, length_to_int

LinesPerInch = Literal[6] | Literal[8]


class TabStops:
    """
    Tab stops, as per page 65 of the ImageWriter II Technical Reference Manual.

    Note that, if the character pitch changes, the tab stops remain the same.
    It is a good idea to clear and reset tab stops
    """

    def __init__(self: Self, pitch: Pitch) -> None:
        self._pitch: Pitch = pitch
        self.stops: List[Distance] = list()
        self.valid: bool = False

    def _to_int(self: Self, length: Length) -> int:
        stop: int = length_to_int(length, lambda lg: lg.characters(self.pitch))

        return min(stop, self.pitch.max_character_position)

    def _to_distance(self: Self, length: Length) -> Distance:
        return length_to_distance(
            length, lambda lg: Inch(lg / self.pitch.characters_per_inch)
        )

    def _sort_stops(self: Self) -> None:
        self.stops.sort(key=self._to_int)

    def set_many(self: Self, stops: Sequence[Length]) -> List[int]:
        # TODO: Does setting tab stops implicitly clear existing tab stops?

        current = {self._to_int(st) for st in self.stops}
        new = [self._to_int(st) for st in stops]
        new.sort()

        self.stops = [self._to_distance(st) for st in (current | set(new))]
        self._sort_stops()

        return new

    def set_one(self: Self, stop: Length) -> int:
        self.stops.append(self._to_distance(stop))
        self._sort_stops()

        return self._to_int(stop)

    def clear_many(self: Self, stops: Sequence[Length]) -> List[int]:
        """
        Returns tab stops to clear.
        """

        current = {self._to_int(st) for st in self.stops}
        cleared = {self._to_int(st) for st in stops}

        self.stops = [self._to_distance(st) for st in (current - cleared)]
        self._sort_stops()

        return list(cleared)

    def clear_all(self: Self) -> None:
        self.stops = list()

    @property
    def pitch(self: Self) -> Pitch:
        return self._pitch

    @pitch.setter
    def pitch(self: Self, pitch: Pitch) -> None:
        self._pitch = pitch
        self.valid = False

    def reset(self: Self) -> None:
        self.valud = True
