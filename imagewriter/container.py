from typing import Optional, Self

from imagewriter.connection import Connection
from imagewriter.serial import Serial
from imagewriter.settings import Settings
from imagewriter.switch import DIPSwitches


class Container:
    def __init__(
        self: Self,
        port: str,
        dip_switches: DIPSwitches = DIPSwitches.defaults(),
    ) -> None:
        self._port = port
        self.dip_switches: DIPSwitches = dip_switches

        self._settings: Optional[Settings] = None
        self._serial: Optional[Serial] = None
        self._connection: Optional[Connection] = None

    def create_settings(self: Self) -> Settings:
        return Settings.replace(
            Settings.defaults(self.dip_switches),
            lf_when_line_full=True,
            perforation_skip=True,
            include_eighth_data_bit=True,
        )

    def reload_settings(self: Self) -> None:
        pass

    def create_serial(self: Self) -> Serial:
        return Serial(
            port=self.port,
            baudrate=self.dip_switches.baud_rate,
            protocol=self.dip_switches.protocol,
        )

    def reload_serial(self: Self) -> None:
        self.serial.close()
        self.serial.port = self.port
        self.serial.open()

    def create_connection(self: Self) -> Connection:
        return Connection(self.serial)

    def reload_connection(self: Self) -> None:
        pass

    @property
    def port(self: Self) -> str:
        return self._port

    @port.setter
    def port(self: Self, port: str) -> None:
        self._port = port
        self.reload_serial()

    @property
    def settings(self: Self) -> Settings:
        if not self._settings:
            self._settings = self.create_settings()

        return self._settings

    @settings.setter
    def settings(self: Self, settings: Settings) -> None:
        self._settings = settings
        self.reload_settings()

    @property
    def serial(self: Self) -> Serial:
        if not self._serial:
            self._serial = self.create_serial()
        return self._serial

    @property
    def connection(self: Self) -> Connection:
        if not self._connection:
            self._connection = self.create_connection()
        return self._connection
