from typing import Optional, Self

import ipywidgets as widgets

from imagewriter.container import Container
from imagewriter.serial import Serial
from imagewriter.settings import Settings
from imagewriter.switch import DIPSwitches
from imagewriter.widgets.base import header
from imagewriter.widgets.serial import SerialWidget
from imagewriter.widgets.settings import SettingsWidget
from imagewriter.widgets.switch import DIPSwitchWidget


class ControlPanelContainer(Container):
    def __init__(self: Self, widget: "ControlPanel") -> None:
        self.widget = widget
        super().__init__(port=None, dip_switches=widget.dip_switches)

    def create_port(self: Self) -> str:
        return self.widget.port

    def reload_port(self: Self) -> None:
        super().reload_port()
        self.widget.port = self.port

    def create_settings(self: Self) -> Settings:
        return self.widget.settings

    def reload_settings(self: Self) -> None:
        super().reload_settings()
        self.widget.settings_widget.settings = self.settings

    def create_serial(self: Self) -> Serial:
        serial = super().create_serial()

        self.widget.serial_widget.connect()

        return serial


class ControlPanel(widgets.Tab):
    def __init__(
        self: Self,
        dip_switches: Optional[DIPSwitches] = None,
        settings: Optional[Settings] = None,
    ) -> None:
        self.dip_switches = (
            dip_switches if dip_switches is not None else DIPSwitches.defaults()
        )
        self._settings = (
            settings if settings is not None else Settings.defaults(self.dip_switches)
        )

        self._container = ControlPanelContainer(self)

        self.serial_widget = SerialWidget(self.dip_switches)
        self.settings_widget = SettingsWidget(self.dip_switches, self._settings)
        self._dip_switch_widget = DIPSwitchWidget(self.dip_switches)

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

    @property
    def container(self: Self) -> Container:
        raise NotImplementedError("ControlPanel().container")
