from typing import Any, List, Optional, Self

import ipywidgets as widgets
import serial

from imagewriter.widgets.base import header
from imagewriter.widgets.connection import Activity, Connection
from imagewriter.widgets.switch import DIPSwitches, Settings
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
            titles=["Settings", "DIP Switches", "Activity"],
            children=[
                widgets.VBox(
                    [
                        header("Connection"),
                        self.connection,
                        header("Software Switches"),
                        self.software_switches,
                    ]
                ),
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

    def update(
        self: Self, switches: Optional[SoftwareSwitchSettings] = None, **changes: Any
    ) -> None:
        self.software_switches.update(switches, **changes)

    def apply(self: Self) -> None:
        self.software_switches.apply()


__all__: List[str] = [
    "Activity",
    "Connection",
    "Settings",
]
