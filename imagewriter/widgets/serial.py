from typing import List, Optional, Protocol, Self

import ipywidgets as widgets
from serial.tools.list_ports import comports

from imagewriter.serial import BaudRate, SerialProtocol
from imagewriter.switch import DIPSwitches


class SerialPortWidget(widgets.Dropdown):
    def __init__(self: Self) -> None:
        ports: List[str] = [port.device for port in comports()]

        super().__init__(
            options=ports, value=ports[-1], description="Serial Port:", disabled=False
        )

    @property
    def port(self: Self) -> str:
        assert isinstance(self.value, str)
        return self.value


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

    def connect(self: Self) -> None:
        self.description = self.CONNECTED

    def disconnect(self: Self) -> None:
        self.description = self.NOT_CONNECTED


class SerialCallback(Protocol):
    def __call__(
        self: Self,
        widget: "SerialWidget",
        port: str,
        baud_rate: BaudRate,
        protocol: SerialProtocol,
    ) -> None: ...


class SerialWidget(widgets.VBox):
    def __init__(self: Self, dip_switches: Optional[DIPSwitches] = None) -> None:
        self._dip_switches = dip_switches if dip_switches else DIPSwitches.defaults()
        self._port_widget = SerialPortWidget()

        self.button = SerialConnectButtonWidget()

        super().__init__(
            [
                self._port_widget,
                self.button,
            ]
        )

    def on_connect(self: Self, callback: SerialCallback) -> None:
        def cb(button: widgets.Button) -> None:
            callback(
                self,
                self._port_widget.port,
                self._dip_switches.baud_rate,
                self._dip_switches.protocol,
            )

        self.button.on_click(cb)
