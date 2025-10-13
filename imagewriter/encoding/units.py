from abc import ABC, abstractmethod
from typing import Callable, Self, Type, TypeVar

from imagewriter.encoding.pitch import Pitch

VERTICAL_RESOLUTION = 144  # Per inch

D = TypeVar("D", bound="Distance")


class Distance(ABC):
    def __init__(self: Self, value: int | float) -> None:
        self.value: float = float(value)

    @property
    @abstractmethod
    def inches(self: Self) -> float:
        """
        The distance in inches.
        """

        raise NotImplementedError("inches")

    @property
    @abstractmethod
    def centimeters(self: Self) -> float:
        """
        The distance in centimeters.
        """

        raise NotImplementedError("centimeters")

    @property
    @abstractmethod
    def millimeters(self: Self) -> float:
        """
        The distance in millimeters.
        """

        raise NotImplementedError("millimeters")

    @property
    def vertical(self: Self) -> int:
        """
        The distance in vertical units of 144 units per inch.
        """

        return int(self.inches * VERTICAL_RESOLUTION)

    def horizontal_dpi(self: Self, pitch: Pitch) -> int:
        """
        The distance in horizontal dots per inch, as in graphics mode.
        """

        return int(self.inches * pitch.horizontal_resolution)

    def characters(self: Self, pitch: Pitch) -> int:
        """
        The distance in horizontal characters, depending on the pitch.
        """

        return int(self.inches * pitch.characters_per_inch)

    @classmethod
    def from_(cls: Type[Self], from_: "Distance") -> Self:
        raise NotImplementedError("Distance.from")

    def convert_to(self: Self, cls: Type[D]) -> D:
        return cls.from_(self)


class Inch(Distance):
    @property
    def inches(self: Self) -> float:
        return self.value

    @property
    def centimeters(self: Self) -> float:
        return self.value * 2.54

    @property
    def millimeters(self: Self) -> float:
        return self.value * 2.54

    @classmethod
    def from_(cls: Type[Self], from_: Distance) -> Self:
        return cls(from_.inches)


class Centimeter(Distance):
    @property
    def inches(self: Self) -> float:
        return self.value / 2.54

    @property
    def centimeters(self: Self) -> float:
        return self.value

    @property
    def millimeters(self: Self) -> float:
        return self.value * 10

    @classmethod
    def from_(cls: Type[Self], from_: Distance) -> Self:
        return cls(from_.centimeters)


class Millimeter(Distance):
    @property
    def inches(self: Self) -> float:
        return self.value / 25.4

    @property
    def centimeters(self: Self) -> float:
        return self.value / 10

    @property
    def millimeters(self: Self) -> float:
        return self.value

    @classmethod
    def from_(cls: Type[Self], from_: Distance) -> Self:
        return cls(from_.millimeters)


Length = Distance | int


def length_to_int(length: Length, get: Callable[[Distance], int | float]) -> int:
    """
    Convert a length to a raw int.
    """

    if isinstance(length, Distance):
        return int(get(length))
    return length


def length_to_distance(length: Length, convert: Callable[[int], Distance]) -> Distance:
    """
    Convert a length to an Distance.
    """

    if isinstance(length, Distance):
        return length
    return convert(length)


LINE_WIDTH = Inch(8)
