from typing import Self

import ipywidgets as widgets  # type: ignore

from imagewriter.base.settings import Settings
from imagewriter.connection import Connection
from imagewriter.container import Container
from imagewriter.serial import Serial
from imagewriter.widgets.activity import ActivityWidget
from imagewriter.widgets.base import header
from imagewriter.widgets.form_feed import TopOfFormWidget
from imagewriter.widgets.serial import SerialWidget
from imagewriter.widgets.settings import SettingsWidget
from imagewriter.widgets.switch import DIPSwitchWidget
from imagewriter.widgets.test import TestWidget


class ControlPanel(widgets.Tab):
    """
    A control panel widget for the ImageWriter II.
    """

    def __init__(self: Self) -> None:
        self._connection: Connection | None = None
        self.container: Container = Container()

        # Grab needed dependencies
        port = self.container.port()
        dip_switches = self.container.dip_switches()
        settings = self.container.settings()

        # Child widgets
        self._serial_widget = SerialWidget(port, dip_switches)
        self._settings_widget = SettingsWidget(dip_switches, settings)
        self._test_widget = TestWidget()
        self._top_of_form_widget = TopOfFormWidget()
        self._dip_switch_widget = DIPSwitchWidget(dip_switches)
        self._activity_widget = ActivityWidget()

        super().__init__(
            titles=["Settings", "DIP Switches", "Serial Activity"],
            children=[
                widgets.VBox(
                    [
                        header("Serial Connection", 3),
                        self._serial_widget,
                        header("Actions", 3),
                        self._top_of_form_widget,
                        self._test_widget,
                        header("Settings", 3),
                        self._settings_widget,
                    ]
                ),
                self._dip_switch_widget,
                self._activity_widget,
            ],
        )

        # UI hooks
        self._serial_widget.on_toggle(self._toggle_serial)
        self._settings_widget.on_apply(self._click_apply)
        self._top_of_form_widget.on_set_top_of_form(self._set_top_of_form)
        self._test_widget.on_print(self._print_test_page)
        self._test_widget.on_memory_test(self._run_memory_test)

    @property
    def settings(self: Self) -> Settings:
        return self.container.settings()

    def connection(self: Self) -> Connection:
        try:
            executor = self.container.executor()
            connection = self.container.connection()
        except Exception as exc:
            self._serial_widget.error(exc)
            raise

        serial = connection.serial

        self._activity_widget.instrument(serial, executor)

        if serial.is_open:
            self._serial_widget.connect()

        return connection

    # Reload the connection whenever underlying container settings change
    def _reload_connection(self: Self) -> None:
        if self._connection:
            self._connection.shutdown()
        self._connection = self.connection()

    def _connect(self: Self) -> Connection:
        if not self._connection:
            self._reload_connection()

        assert self._connection, "Connection was not established"

        return self._connection

    # Triggered when we reload the port, typically from clicking "connect".
    def _reload_port(self: Self) -> None:
        self.container.port.override(self._serial_widget.port)

        self._reload_connection()

    # Triggered when we reload the settings, typically from clicking "apply".
    def _reload_settings(self: Self) -> None:
        self.container.settings.override(self._settings_widget.settings)
        self._reload_connection()

    # Triggered when the "connect/disconnect" button is clicked
    def _toggle_serial(self: Self, widget: SerialWidget) -> None:
        if widget.connected:
            self.close_serial()
        else:
            self.open_serial()

    # Open the serial port
    def open_serial(self: Self) -> None:
        self._reload_port()

        assert self._connection, "Connection was not established"

        serial = self._connection.serial

        if not serial.is_open:
            try:
                serial.open()
            except Exception as exc:
                self._serial_widget.error(exc)
                raise

        self._serial_widget.connect()

    # Close the serial port
    def close_serial(self: Self) -> None:
        if self._connection:
            serial: Serial = self._connection.serial

            try:
                if serial.is_open:
                    serial.close()
            except Exception as exc:  # noqa
                self._serial_widget.error(exc)
            else:
                self._serial_widget.disconnect()
        else:
            self._serial_widget.disconnect()

        self._settings_widget.not_applied()

    # Triggered when the "apply" button is clicked.
    def _click_apply(self: Self, widget: SettingsWidget) -> None:
        self._reload_settings()

        connection = self._connect()

        widget.apply(connection)

    def _set_top_of_form(self: Self, widget: TopOfFormWidget) -> None:
        connection = self._connect()

        widget.set_top_of_form(connection)

    def _print_test_page(self: Self, widget: TestWidget) -> None:
        test_page = self.container.test_page()
        connection = self._connect()

        widget.print_test_page(connection, test_page)

    def _run_memory_test(self: Self, widget: TestWidget) -> None:
        connection = self._connect()
        widget.run_memory_test(connection.serial, connection)

    def shutdown(self: Self) -> None:
        self._activity_widget.shutdown()
