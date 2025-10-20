from typing import Protocol, Self

from imagewriter.connection import Connection

# from imagewriter.language import Language
# from imagewriter.pitch import Pitch
# from imagewriter.print import PrintCommands
# from imagewriter.quality import Quality
from imagewriter.serial import Serial
from imagewriter.settings import Settings
from imagewriter.switch import DIPSwitches, SoftwareSwitches

# from imagewriter.units import Inch, Pica


class SoftwareSwitchesFactory(Protocol):
    def __call__(self: Self, dip_switches: DIPSwitches) -> SoftwareSwitches: ...


class SerialFactory(Protocol):
    def __call__(self: Self, port: str, dip_switches: DIPSwitches) -> Serial: ...


class ConnectionFactory(Protocol):
    def __call__(self: Self, port: Serial) -> Connection: ...


class SettingsFactory(Protocol):
    def __call__(self: Self, dip_switches: DIPSwitches) -> Settings: ...


def serial_factory(port: str, dip_switches: DIPSwitches) -> Serial:
    return Serial(
        port=port, baudrate=dip_switches.baud_rate, protocol=dip_switches.protocol
    )


def settings_factory(dip_switches: DIPSwitches) -> Settings:
    return Settings.replace(
        Settings.defaults(dip_switches),
        lf_when_line_full=True,
        perforation_skip=True,
        include_eighth_data_bit=True,
    )


class Container:
    def __init__(
        self: Self,
        port: str,
        dip_switches: DIPSwitches = DIPSwitches.defaults(),
        serial: SerialFactory = serial_factory,
        connection: ConnectionFactory = Connection,
        settings: SettingsFactory = settings_factory,
    ) -> None:
        self._dip_switches: DIPSwitches = dip_switches
        self._port: Serial = serial(port, self._dip_switches)
        self._connection: Connection = connection(self._port)
        self._settings: Settings = settings(dip_switches)

    @property
    def dip_switches(self: Self) -> DIPSwitches:
        return self._dip_switches

    @property
    def port(self: Self) -> Serial:
        return self._port

    @property
    def connection(self: Self) -> Connection:
        return self._connection

    @property
    def settings(self: Self) -> Settings:
        return self._settings
