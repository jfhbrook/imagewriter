from typing import Optional, Self

import ipywidgets as widgets

from imagewriter.connection import Connection
from imagewriter.container import Container
from imagewriter.serial import Serial
from imagewriter.widgets.base import header
from imagewriter.widgets.serial import SerialWidget
from imagewriter.widgets.settings import SettingsWidget
from imagewriter.widgets.switch import DIPSwitchWidget


class ControlPanel(widgets.Tab):
    def __init__(self: Self, container: Container = Container()) -> None:
        self.container = container

        # Grab needed dependencies
        port = container.port()
        dip_switches = container.dip_switches()
        settings = container.settings()

        # Serial port is fetched lazily
        self._serial: Optional[Serial] = None
        self._connection: Optional[Connection] = None

        # Child widgets
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

        # UI hooks
        self.serial_widget.on_toggle(self._toggle_serial)
        self.settings_widget.on_apply(self._click_apply)

    # The serial port is already a singleton in the container, but we
    # also need to hook some behavior onto it, so we do it here.
    @property
    def serial(self: Self) -> Serial:
        if not self._serial:
            self._serial = self.container.serial()
            # TODO: This means that the serial port will be incorrect prior
            # to it being accessed here...
            self.container.serial.override(self._serial)
            if self._serial.is_open:
                self.serial_widget.connect()

        return self._serial

    # Triggered when we reload the port, typically from clicking "connect".
    def _reload_port(self: Self) -> None:
        self.container.port.override(self.serial_widget.port)

        if self._serial:
            self._serial.port = self.serial_widget.port

    # Triggered when we reload the settings, typically from clicking "apply".
    def _reload_settings(self: Self) -> None:
        self.container.settings.override(self.settings_widget.settings)

    # Triggered when the "connect/disconnect" button is clicked
    def _toggle_serial(self: Self, widget: SerialWidget) -> None:
        if widget.connected:
            self._close_serial()
        else:
            self._open_serial()

    # Open the serial port
    def _open_serial(self: Self) -> None:
        self._reload_port()

        if not self.serial.is_open:
            self.serial.open()

        self.serial_widget.connect()

    # Close the serial port
    def _close_serial(self: Self) -> None:
        if self.serial.is_open:
            self.serial.close()

        self.serial_widget.disconnect()
        self.settings_widget.not_applied()

    # Triggered when the "apply" button is clicked.
    def _click_apply(self: Self, widget: SettingsWidget) -> None:
        self._reload_settings()

        try:
            self._apply_settings()
        except Exception as exc:
            widget.error(exc)

    # Apply the settings to the serial connection.
    def _apply_settings(self: Self) -> None:
        raise NotImplementedError("Applying settings")
