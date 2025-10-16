from typing import cast, List, Optional, Self

import ipywidgets as widgets
import serial
from serial.tools.list_ports import comports

import imagewriter.debug as debug


class Connection(widgets.VBox):
    def __init__(self: Self) -> None:
        ports: List[str] = [port.device for port in comports()]
        self._serial_port = widgets.Dropdown(
            options=ports, value=ports[0], description="Serial Port:", disabled=False
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

        self._connect_button.on_click(self.reconfigure)
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
            port: serial.Serial = self._connect()
            self._port = port
            return port

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

    def reconfigure(self: Self) -> None:
        if self.port:
            self.port.close()
        self._port = self._connect()


class SerialStateObserver(debug.SerialStateObserver):
    def __init__(self: Self, port: serial.Serial, widget: "PinActivity") -> None:
        super().__init__(port)
        self._widget = widget

    def on_change(self: Self) -> None:
        self._widget.dtr.value = self._fmt_signal(self.serial.dtr)
        self._widget.dtr.value = self._fmt_signal(self.serial.dtr)
        self._widget.dtr.value = self._fmt_signal(self.serial.dtr)
        self._widget.dtr.value = self._fmt_signal(self.serial.dtr)


class PinActivity(widgets.VBox):
    def __init__(self: Self, port: serial.Serial) -> None:
        self.dtr: widgets.Text = widgets.Text(value="")
        self.dsr: widgets.Text = widgets.Text(value="")
        self.rts: widgets.Text = widgets.Text(value="")
        self.cts: widgets.Text = widgets.Text(value="")

        super().__init__(
            [
                widgets.HBox(
                    [
                        widgets.Label("DTR:"),
                        self.dtr,
                    ]
                ),
                widgets.HBox(
                    [
                        widgets.Label("DSR:"),
                        self.dsr,
                    ]
                ),
                widgets.HBox(
                    [
                        widgets.Label("RTS:"),
                        self.rts,
                    ]
                ),
                widgets.HBox(
                    [
                        widgets.Label("CTS:"),
                        self.cts,
                    ]
                ),
            ]
        )

        self._port: serial.Serial = port
        self._observer: SerialStateObserver = SerialStateObserver(port, self)
        self.start()

    def start(self: Self) -> None:
        self._observer.start()

    def stop(self: Self) -> None:
        self._observer.stop()
