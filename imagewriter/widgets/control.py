from typing import Optional, Self

import ipywidgets as widgets

from imagewriter.container import Container
from imagewriter.serial import Serial
from imagewriter.settings import Settings
from imagewriter.widgets.base import header
from imagewriter.widgets.serial import SerialWidget
from imagewriter.widgets.settings import SettingsWidget
from imagewriter.widgets.switch import DIPSwitchWidget


class ControlPanel(widgets.Tab):
    def __init__(
        self: Self,
        container: Container,
    ) -> None:
        self.container = container

        port = container.port()
        dip_switches = container.dip_switches()
        settings = container.settings()

        self._serial: Optional[Serial] = None

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

        self.serial_widget.on_toggle(self._toggle_serial)
        self.settings_widget.on_apply(self._click_apply)

    @property
    def port(self: Self) -> str:
        return self.serial_widget.port

    @port.setter
    def port(self: Self, port: str) -> None:
        self.serial_widget.port = port
        self.container.port.override(port)

        if self._serial:
            self._serial.port = self.serial_widget.port

    @property
    def settings(self: Self) -> Settings:
        return self.settings_widget.settings

    @settings.setter
    def settings(self: Self, settings: Settings) -> None:
        self.settings_widget.settings = settings
        self.container.settings.override(settings)

    @property
    def serial(self: Self) -> Serial:
        if not self._serial:
            self._serial = self.container.serial()
            if self._serial.is_open:
                self.serial_widget.connect()

        return self._serial

    def _toggle_serial(self: Self, widget: SerialWidget) -> None:
        self.port = widget.port

        if widget.connected:
            self._close_serial()
        else:
            self._open_serial()
            widget.connect()

    def _open_serial(self: Self) -> None:
        if not self.serial.is_open:
            self.serial.open()

        self.serial_widget.connect()

    def _close_serial(self: Self) -> None:
        if self.serial.is_open:
            self.serial.close()

        self.serial_widget.disconnect()
        self.settings_widget.not_applied()

    def _click_apply(self: Self, widget: SettingsWidget) -> None:
        self.settings = widget.settings
        try:
            self._apply_settings()
        except Exception as exc:
            widget.error(exc)

    def _apply_settings(self: Self) -> None:
        raise NotImplementedError("Applying settings")
