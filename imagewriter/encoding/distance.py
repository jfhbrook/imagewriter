from abc import ABC, abstractmethod
from typing import Self, Type, TypeVar

Value = int | float

D = TypeVar("D", bound="Distance")


class Distance(ABC):
    def __init__(self: Self, value: Value) -> None:
        self.value: Value = value

    @property
    @abstractmethod
    def inches(self: Self) -> Value:
        raise NotImplementedError("inches")

    @property
    @abstractmethod
    def centimeters(self: Self) -> Value:
        raise NotImplementedError("centimeters")

    @property
    @abstractmethod
    def millimeters(self: Self) -> Value:
        raise NotImplementedError("millimeters")

    @classmethod
    def from_(cls: Type[Self], from_: "Distance") -> Self:
        raise NotImplementedError("Distance.from")

    def convert_to(self: Self, cls: Type[D]) -> D:
        return cls.from_(self)


class Inch(Distance):
    @property
    def inches(self: Self) -> Value:
        return self.value

    @property
    def centimeters(self: Self) -> Value:
        return self.value * 2.54

    @property
    def millimeters(self: Self) -> Value:
        return self.value * 2.54

    @classmethod
    def from_(cls: Type[Self], from_: "Distance") -> Self:
        return cls(from_.inches)


class Centimeter(Distance):
    @property
    def inches(self: Self) -> Value:
        return self.value / 2.54

    @property
    def centimeters(self: Self) -> Value:
        return self.value

    @property
    def millimeters(self: Self) -> Value:
        return self.value * 10

    @classmethod
    def from_(cls: Type[Self], from_: "Distance") -> Self:
        return cls(from_.centimeters)


class Millimeter(Distance):
    @property
    def inches(self: Self) -> Value:
        return self.value / 25.4

    @property
    def centimeters(self: Self) -> Value:
        return self.value / 10

    @property
    def millimeters(self: Self) -> Value:
        return self.value

    @classmethod
    def from_(cls: Type[Self], from_: "Distance") -> Self:
        return cls(from_.millimeters)
