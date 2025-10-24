from typing import Callable, cast, Dict, Literal, Self, Type

import ipywidgets as widgets

from imagewriter.units import Centimeter, Distance, Inch, Millimeter, Pica, Point

UnitName = (
    Literal["in"] | Literal["cm"] | Literal["mm"] | Literal["pt"] | Literal["pica"]
)

UNIT_NAMES: Dict[Type[Distance], UnitName] = {
    Inch: "in",
    Centimeter: "cm",
    Millimeter: "mm",
    Point: "pt",
    Pica: "pica",
}

UNIT_CLASSES: Dict[str, Type[Distance]] = {
    name: cls for cls, name in UNIT_NAMES.items()
}


# TODO: Width styling
class UnitClassWidget(widgets.Dropdown):
    def __init__(self: Self, distance: Distance) -> None:
        super().__init__(
            options=list(UNIT_CLASSES.keys()),
            value=UNIT_NAMES[distance.__class__],
            description="",
            disabled=False,
        )

    @property
    def units(self: Self) -> UnitName:
        return cast(UnitName, self.value) if self.value else "in"

    @units.setter
    def units(self: Self, unit: UnitName) -> None:
        self.value = unit

    @property
    def cls(self: Self) -> Type[Distance]:
        return UNIT_CLASSES[self.units]

    @cls.setter
    def cls(self: Self, cls: Type[Distance]) -> None:
        self.value = UNIT_NAMES[cls]


UNIT_VALUES: Dict[Type[Distance], Callable[[Distance], float]] = {
    Inch: lambda distance: distance.inches,
    Centimeter: lambda distance: distance.centimeters,
    Millimeter: lambda distance: distance.millimeters,
    Point: lambda distance: distance.points,
    Pica: lambda distance: distance.picas,
}


# TODO: width styling
class UnitValueWidget(widgets.BoundedFloatText):
    def __init__(self: Self, start: Distance, max: Distance, step: Distance) -> None:
        self.cls = start.__class__
        self._max = max
        self._step = step

        super().__init__(
            value=self._start_value(start),
            min=0,
            max=self._max_value(self.cls),
            step=self._step_value(self.cls),
            description="",
            disabled=False,
        )

    def _start_value(self: Self, distance: Distance) -> float:
        return UNIT_VALUES[distance.__class__](distance)

    def _max_value(self: Self, cls: Type[Distance]) -> float:
        return UNIT_VALUES[cls](self._max)

    def _step_value(self: Self, cls: Type[Distance]) -> float:
        return UNIT_VALUES[cls](self._step)

    @property
    def distance(self: Self) -> Distance:
        return self.cls(self.value)

    @distance.setter
    def distance(self: Self, distance: Distance) -> None:
        self.cls = distance.__class__
        self.value = UNIT_VALUES[self.cls](distance)
        self.max = self._max_value(self.cls)
        self.step = self._step_value(self.cls)


class DistanceWidget(widgets.HBox):
    def __init__(self: Self, start: Distance, max: Distance, step: Distance) -> None:
        self._value_widget = UnitValueWidget(start, max, step)
        self._class_widget = UnitClassWidget(start)

        self._class_widget.observe(self._set_units, names="value")

        super().__init__([self._value_widget, self._class_widget])

    def _set_units(self: Self, change: str) -> None:
        cls = self._class_widget.cls
        distance = self._value_widget.distance
        self._value_widget.distance = distance.into(cls)

    @property
    def distance(self: Self) -> Distance:
        return self._value_widget.distance

    @distance.setter
    def distance(self: Self, distance: Distance) -> None:
        self._value_widget.distance = distance
        self._class_widget.cls = distance.__class__
