from typing import List

from imagewriter.base.identification import (
    FEAT_COLOR_RIBBON,
    FEAT_SHEET_FEEDER,
    Feature,
    Identification,
)
from imagewriter.base.language import Language
from imagewriter.base.pitch import Pitch
from imagewriter.base.print import PrintCommands
from imagewriter.base.quality import Quality
from imagewriter.base.settings import Settings
from imagewriter.base.switch import (
    DIPSwitch,
    DIPSwitches,
    SoftwareSwitch,
    SoftwareSwitches,
)
from imagewriter.base.units import (
    Centimeter,
    Distance,
    Inch,
    Length,
    length_to_distance,
    length_to_int,
    Millimeter,
    Pica,
    Point,
)
from imagewriter.connection import Connection
from imagewriter.container import Container
from imagewriter.serial import Serial, SerialProtocol

__all__: List[str] = [
    "Connection",
    "Container",
    "FEAT_COLOR_RIBBON",
    "FEAT_SHEET_FEEDER",
    "Feature",
    "Identification",
    "Language",
    "Pitch",
    "PrintCommands",
    "Quality",
    "Serial",
    "SerialProtocol",
    "Settings",
    "DIPSwitch",
    "DIPSwitches",
    "SoftwareSwitch",
    "SoftwareSwitches",
    "Centimeter",
    "Distance",
    "Inch",
    "Length",
    "length_to_distance",
    "length_to_int",
    "Millimeter",
    "Pica",
    "Point",
]
