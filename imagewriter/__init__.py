from typing import List

from imagewriter.identification import (
    FEAT_COLOR_RIBBON,
    FEAT_SHEET_FEEDER,
    Feature,
    Identification,
)
from imagewriter.language import Language
from imagewriter.serial import Serial, SerialProtocol
from imagewriter.switch import (
    DIPSwitch,
    DIPSwitchSettings,
    SoftwareSwitch,
    SoftwareSwitchSettings,
)

__all__: List[str] = [
    "FEAT_COLOR_RIBBON",
    "FEAT_SHEET_FEEDER",
    "Feature",
    "Identification",
    "Language",
    "Serial",
    "SerialProtocol",
    "DIPSwitch",
    "DIPSwitchSettings",
    "SoftwareSwitch",
    "SoftwareSwitchSettings",
]
