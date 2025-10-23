from typing import Optional, Self

import ipywidgets as widgets

from imagewriter.container import Container
from imagewriter.settings import Settings
from imagewriter.switch import DIPSwitches
from imagewriter.widgets.settings import SettingsWidget
from imagewriter.widgets.switch import DIPSwitchWidget


class ControlPanel(widgets.Tab):
    def __init__(
        self: Self,
        dip_switches: Optional[DIPSwitches] = None,
        settings: Optional[Settings] = None,
    ) -> None:
        self._dip_switches = (
            dip_switches if dip_switches is not None else DIPSwitches.defaults()
        )
        self._settings = (
            settings if settings is not None else Settings.defaults(self._dip_switches)
        )

        self._settings_widget = SettingsWidget(self._dip_switches, self._settings)
        self._dip_switch_widget = DIPSwitchWidget(self._dip_switches)

        super().__init__(
            titles=["Settings", "DIP Switches"],
            children=[
                self._settings_widget,
                self._dip_switch_widget,
            ],
        )

    @property
    def container(self: Self) -> Container:
        raise NotImplementedError("ControlPanel().container")
