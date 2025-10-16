from typing import cast, List, Optional, Self

import ipywidgets as widgets
import serial
from serial.tools.list_ports import comports


class Connection(widgets.VBox):
    def __init__(self: Self) -> None:
        ports: List[str] = [port.device for port in comports()]
        self._serial_port = widgets.Dropdown(
            options=ports, value=ports[-1], description="Serial Port:", disabled=False
        )

        self._baud_rate = widgets.Dropdown(
            options=[300, 1200, 2400, 9600],
            value=9600,
            description="Baud Rate:",
            disabled=False,
        )

        self._connect_button = widgets.Button(
            description="Connect",
            disabled=False,
            button_style="",
            tooltip="Connect to the serial port",
        )

        self._connect_button.on_click(self._reconfigure)
        self._port: Optional[serial.Serial] = None

        super().__init__(
            [
                self._serial_port,
                self._baud_rate,
                self._connect_button,
            ]
        )

    @property
    def port(self: Self) -> serial.Serial:
        if self._port:
            return self._port
        else:
            raise AttributeError("Serial port is closed")

    def _connect(self: Self) -> serial.Serial:
        return serial.Serial(
            port=self._serial_port.value,
            baudrate=cast(int, self._baud_rate.value),
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            dsrdtr=True,
            rtscts=True,
            xonxoff=False,
        )

    def open_port(self: Self) -> None:
        if self._port:
            raise AttributeError("Serial port is already open")

        self._port = self._connect()
        self._connect_button.description = "Disconnect"

    def close_port(self: Self) -> None:
        if not self._port:
            raise AttributeError("Serial port is already closed")
        self._port.close()
        self._port = None
        self._connect_button.description = "Connect"

    def _reconfigure(self: Self, _button: widgets.Button) -> None:
        if self._port:
            self.close_port()
        else:
            self.open_port()
