from typing import Optional, Self

from serial.tools.list_ports import comports

from imagewriter.connection import Connection
from imagewriter.serial import Serial
from imagewriter.settings import Settings
from imagewriter.switch import DIPSwitches


class Container:
    def __init__(
        self: Self,
        port: Optional[str] = None,
        dip_switches: Optional[DIPSwitches] = None,
    ) -> None:
        self._port: Optional[str] = port
        self.dip_switches: DIPSwitches = (
            dip_switches if dip_switches else self.create_dip_switches()
        )

        self._settings: Optional[Settings] = None
        self._serial: Optional[Serial] = None
        self._connection: Optional[Connection] = None

    def create_dip_switches(self: Self) -> DIPSwitches:
        """
        Create a DIPSwitches object.
        """

        return DIPSwitches.defaults()

    def create_port(self: Self) -> str:
        """
        Create a port.
        """

        return comports()[-1].device

    def reload_port(self: Self) -> None:
        """
        Reload the port, and any of its dependents.
        """

        if self._serial:
            self.reload_serial()

    def create_settings(self: Self) -> Settings:
        """
        Create a new Settings object.
        """

        return Settings.replace(
            Settings.defaults(self.dip_switches),
            lf_when_line_full=True,
            perforation_skip=True,
            include_eighth_data_bit=True,
        )

    def reload_settings(self: Self) -> None:
        """
        Reload the settings, and any of their dependents.
        """

        pass

    def create_serial(self: Self) -> Serial:
        """
        Create a new Serial object.
        """

        return Serial(
            port=self.port,
            baudrate=self.dip_switches.baud_rate,
            protocol=self.dip_switches.protocol,
        )

    def reload_serial(self: Self) -> None:
        """
        Reload the Serial object, and any of its dependents.
        """

        self.serial.close()
        self.serial.port = self.port
        self.serial.open()
        self.reload_connection()

    def create_connection(self: Self) -> Connection:
        """
        Create a new Connection object.
        """

        return Connection(self.serial)

    def reload_connection(self: Self) -> None:
        """
        Reload the Connection object, and any of its dependents.
        """

        # The Connection object already has a reference to the Serial
        # object, which has not been modified.
        pass

    @property
    def port(self: Self) -> str:
        if not self._port:
            self._port = self.create_port()
        return self._port

    @port.setter
    def port(self: Self, port: str) -> None:
        self._port = port
        self.reload_port()

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
