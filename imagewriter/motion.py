from enum import Enum
from typing import List, Literal, Self, Sequence

from imagewriter.pitch import Pitch
from imagewriter.units import Distance, Inch, Length, length_to_distance, length_to_int

LinesPerInch = Literal[6] | Literal[8]


class LineFeedDirection(Enum):
    FORWARD = "Forward"
    REVERSE = "Reverse"


class InvalidTabStopsError(Exception):
    """
    An error raised when tab stop positions have been invalidated by a change
    in pitch.
    """

    def __init__(self: Self) -> None:
        super().__init__(
            "The pitch has been changed; previously set tab stops are invalid"
        )


class TabStops:
    """
    Tab stops, as per page 65 of the ImageWriter II Technical Reference Manual.
    """

    def __init__(self: Self, pitch: Pitch) -> None:
        self._pitch: Pitch = pitch
        self._stops: List[Distance] = list()
        self.valid: bool = False

    @property
    def stops(self: Self) -> List[Distance]:
        """
        Get currently set tab stops. When tab stops have been invalidated by
        a change in pitch, this method riases an InvalidTabStopsError.
        """

        if self.valid:
            return self._stops

        raise InvalidTabStopsError()

    def _to_int(self: Self, length: Length) -> int:
        stop: int = length_to_int(length, lambda lg: lg.characters(self.pitch))

        return min(stop, self.pitch.max_character_position)

    def _to_distance(self: Self, length: Length) -> Distance:
        return length_to_distance(
            length, lambda lg: Inch(lg / self.pitch.characters_per_inch)
        )

    def _sort_stops(self: Self) -> None:
        self._stops.sort(key=self._to_int)

    def set_many(self: Self, stops: Sequence[Length]) -> List[int]:
        """
        Set many tab stops, and return a list of integer valued tab stops
        to set.
        """

        current = {self._to_int(st) for st in self.stops}
        new = [self._to_int(st) for st in stops]
        new.sort()

        self._stops = [self._to_distance(st) for st in (current | set(new))]
        self._sort_stops()

        return new

    def set_one(self: Self, stop: Length) -> int:
        """
        Set a single tab stop, and return an integer valued tab stop to set.
        """

        return self.set_many([stop])[0]

    def clear_many(self: Self, stops: Sequence[Length]) -> List[int]:
        """
        Clear multiple tab stops by position, and return a list of integer
        valued tab stops to clear.
        """

        current = {self._to_int(st) for st in self.stops}
        cleared = {self._to_int(st) for st in stops}

        self._stops = [self._to_distance(st) for st in (current - cleared)]
        self._sort_stops()

        return list(cleared)

    def clear_all(self: Self) -> None:
        """
        Clear all tab stops.

        As per page 68 of the ImageWriter II Technical Reference Manual, if
        the pitch is changed, the tab stops remain in their existing locations
        and no longer correspond to character column positions. Clearing
        all tab positions will ensure that tab positions going forward are
        valid.
        """

        self._stops = list()
        self.valid = True

    @property
    def pitch(self: Self) -> Pitch:
        """
        The current pitch.
        """

        return self._pitch

    @pitch.setter
    def pitch(self: Self, pitch: Pitch) -> None:
        """
        Set the pitch.

        As per page 68 of the ImageWriter II Technical Reference Manual, if
        the pitch is changed, the tab stops remain in their existing locations
        and no longer correspond to character column positions. Setting the
        pitch will invalidate current tab positions.
        """

        self._pitch = pitch
        self.valid = False
