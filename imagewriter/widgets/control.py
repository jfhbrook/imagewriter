from typing import Self

from dependency_injector.wiring import inject, Provide
import ipywidgets as widgets

from imagewriter.container import Container
from imagewriter.serial import BaudRate, SerialProtocol
from imagewriter.settings import Settings
from imagewriter.switch import DIPSwitches
from imagewriter.widgets.base import header
from imagewriter.widgets.serial import SerialWidget
from imagewriter.widgets.settings import SettingsWidget
from imagewriter.widgets.switch import DIPSwitchWidget


class ControlPanel(widgets.Tab):
    @inject
    def __init__(
        self: Self,
        port: str = Provide[Container.port],
        baud_rate: BaudRate = Provide[Container.baud_rate],
        protocol: SerialProtocol = Provide[Container.protocol],
        dip_switches: DIPSwitches = Provide[Container.dip_switches],
        settings: Settings = Provide[Container.settings],
    ) -> None:
        self._baud_rate = baud_rate
        self._protocol = protocol

        self.serial_widget = SerialWidget(port, dip_switches)
        self.settings_widget = SettingsWidget(dip_switches, settings)
        self._dip_switch_widget = DIPSwitchWidget(dip_switches)

        super().__init__(
            titles=["Settings", "DIP Switches"],
            children=[
                widgets.VBox(
                    [
                        header("Serial Connection", 3),
                        self.serial_widget,
                        header("Printer Settings", 3),
                        self.settings_widget,
                    ]
                ),
                self._dip_switch_widget,
            ],
        )

        self.serial_widget.on_toggle(self._serial_toggle)
        self.settings_widget.on_apply(self._settings_apply)

    @property
    def port(self: Self) -> str:
        return self.serial_widget.port

    @port.setter
    def port(self: Self, port: str) -> None:
        self.serial_widget.port = port

    @property
    def settings(self: Self) -> Settings:
        return self.settings_widget.settings

    def _serial_toggle(self: Self, widget: SerialWidget) -> None:
        if widget.connected:
            widget.disconnect()
            self.settings_widget.not_applied()
        else:
            widget.connect()

        print(widget.port)
        print(widget.baud_rate)
        print(widget.protocol)

    def _settings_apply(self: Self, widget: SettingsWidget) -> None:
        if self.serial_widget.connected:
            widget.applied()
        else:
            widget.error(Exception("Not connected"))

        print(widget.settings)
