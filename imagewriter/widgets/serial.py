from typing import List, Protocol, Self

import ipywidgets as widgets
from serial.tools.list_ports import comports

from imagewriter.serial import BaudRate, SerialProtocol
from imagewriter.switch import DIPSwitches


class SerialPortWidget(widgets.Dropdown):
    def __init__(self: Self, port: str) -> None:
        ports: List[str] = [port.device for port in comports()]

        super().__init__(
            options=ports, value=port, description="Serial Port:", disabled=False
        )

    @property
    def port(self: Self) -> str:
        assert isinstance(self.value, str)
        return self.value

    @port.setter
    def port(self: Self, port: str) -> None:
        self.value = port


class SerialConnectButtonWidget(widgets.Button):
    NOT_CONNECTED = "Connect"
    CONNECTED = "Disconnect"

    def __init__(self: Self) -> None:
        super().__init__(
            description=self.NOT_CONNECTED,
            disabled=False,
            button_style="",
            tooltip="Connect to the serial port",
        )

    @property
    def connected(self: Self) -> bool:
        return self.description == self.CONNECTED

    def connect(self: Self) -> None:
        self.description = self.CONNECTED

    def disconnect(self: Self) -> None:
        self.description = self.NOT_CONNECTED


class SerialCallback(Protocol):
    def __call__(self: Self, widget: "SerialWidget") -> None: ...


class SerialWidget(widgets.VBox):
    def __init__(self: Self, port: str, dip_switches: DIPSwitches) -> None:
        self._dip_switches = dip_switches
        self._port_widget = SerialPortWidget(port)

        self._connect_button = SerialConnectButtonWidget()

        super().__init__(
            [
                self._port_widget,
                self._connect_button,
            ]
        )

    @property
    def port(self: Self) -> str:
        return self._port_widget.port

    @port.setter
    def port(self: Self, port: str) -> None:
        self._port_widget.port = port

    @property
    def baud_rate(self: Self) -> BaudRate:
        return self._dip_switches.baud_rate

    @property
    def protocol(self: Self) -> SerialProtocol:
        return self._dip_switches.protocol

    @property
    def connected(self: Self) -> bool:
        return self._connect_button.connected

    def connect(self: Self) -> None:
        self._connect_button.connect()

    def disconnect(self: Self) -> None:
        self._connect_button.disconnect()

    def on_toggle(self: Self, callback: SerialCallback) -> None:
        def cb(button: widgets.Button) -> None:
            callback(
                self,
            )

        self._connect_button.on_click(cb)
