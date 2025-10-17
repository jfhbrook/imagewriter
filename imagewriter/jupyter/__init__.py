from typing import List, Self

import ipywidgets as widgets
import serial

from imagewriter.jupyter.connection import Activity, Connection
from imagewriter.jupyter.switch import DIPSwitches, Settings
from imagewriter.switch import DIPSwitchSettings, SoftwareSwitchSettings


class ControlPanel(widgets.Tab):
    def __init__(
        self: Self,
        dip_switches: DIPSwitchSettings,
        software_switches: SoftwareSwitchSettings,
    ) -> None:
        self.connection = Connection()
        self.dip_switches = DIPSwitches(dip_switches)
        self.software_switches = Settings(software_switches, self.connection)

        self.activity = self.connection.activity

        super().__init__(
            titles=["Connection", "Software Switches", "DIP Switches", "Activity"],
            children=[
                self.connection,
                self.software_switches,
                self.dip_switches,
                self.connection.activity,
            ],
        )

    @property
    def port(self: Self) -> serial.Serial:
        return self.connection.port

    def open_port(self: Self) -> None:
        self.connection.open_port()

    def close_port(self: Self) -> None:
        self.connection.close_port()


__all__: List[str] = [
    "Activity",
    "Connection",
    "Settings",
]
