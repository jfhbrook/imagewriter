from typing import Optional, Self, Type

from dependency_injector import providers
import ipywidgets as widgets

from imagewriter.connection import Connection
from imagewriter.container import Container
from imagewriter.serial import Serial
from imagewriter.settings import Settings
from imagewriter.widgets.base import header
from imagewriter.widgets.serial import SerialWidget
from imagewriter.widgets.settings import SettingsWidget
from imagewriter.widgets.switch import DIPSwitchWidget


class ControlPanel(widgets.Tab):
    def __init__(self: Self, container_cls: Type[Container] = Container) -> None:
        # We need to hook some custom behavior onto the creation of the
        # serial port. We do that by subclassing the container here.

        self._serial: Optional[Serial] = None
        cls = self._bind_cls(container_cls)
        self.container: Container = cls()

        # Grab needed dependencies
        port = self.container.port()
        dip_switches = self.container.dip_switches()
        settings = self.container.settings()

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

    def _bind_cls(self: Self, cls: Type[Container]) -> Type[Container]:
        class Container(cls):
            serial = providers.Callable(self._provide_serial)

            connection = providers.Singleton(Connection, serial=serial)

        return Container

    def _provide_serial(self: Self) -> Serial:
        if not self._serial:
            try:
                self._serial = Serial(
                    port=self.container.port(),
                    baudrate=self.container.baud_rate(),
                    protocol=self.container.protocol(),
                )
            except Exception as exc:
                self.serial_widget.error(exc)
                raise exc
            if self._serial.is_open:
                self.serial_widget.connect()

        return self._serial

    @property
    def settings(self: Self) -> Settings:
        return self.container.settings()

    @property
    def serial(self: Self) -> Serial:
        return self.container.serial()

    @property
    def connection(self: Self) -> Connection:
        return self.container.connection()

    # Triggered when we reload the port, typically from clicking "connect".
    def _reload_port(self: Self) -> None:
        self.container.port.override(self.serial_widget.port)

        try:
            if self._serial:
                self._serial.port = self.serial_widget.port
        except Exception as exc:
            self.serial_widget.error(exc)
            raise

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
        serial: Serial = self.container.serial()

        if not serial.is_open:
            try:
                serial.open()
            except Exception as exc:
                self.serial_widget.error(exc)
                raise exc

        self.serial_widget.connect()

    # Close the serial port
    def _close_serial(self: Self) -> None:
        serial: Serial = self.container.serial()

        try:
            if serial.is_open:
                serial.close()
        except Exception as exc:
            self.serial_widget.error(exc)
        else:
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
