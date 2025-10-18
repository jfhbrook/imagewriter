from typing import List

from imagewriter.connection import Connection
from imagewriter.identification import (
    FEAT_COLOR_RIBBON,
    FEAT_SHEET_FEEDER,
    Feature,
    Identification,
)
from imagewriter.language import Language
from imagewriter.pitch import Pitch
from imagewriter.quality import Quality
from imagewriter.serial import Serial, SerialProtocol
from imagewriter.state import State
from imagewriter.switch import (
    DIPSwitch,
    DIPSwitches,
    SoftwareSwitch,
    SoftwareSwitches,
)
from imagewriter.units import (
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

__all__: List[str] = [
    "Connection",
    "FEAT_COLOR_RIBBON",
    "FEAT_SHEET_FEEDER",
    "Feature",
    "Identification",
    "Language",
    "Pitch",
    "Quality",
    "Serial",
    "SerialProtocol",
    "State",
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
