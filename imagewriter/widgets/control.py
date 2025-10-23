from typing import Optional, Self

import ipywidgets as widgets

from imagewriter.container import Container
from imagewriter.switch import DIPSwitches

# from imagewriter.widgets.settings import SettingsWidget


class ControlPanel(widgets.Tab):
    def __init__(self: Self, dip_switches: Optional[DIPSwitches] = None) -> None:
        self._dip_switches = dip_switches
        self._container: Optional[Container] = None

    @property
    def container(self: Self) -> Container:
        raise NotImplementedError("ControlPanel().container")
