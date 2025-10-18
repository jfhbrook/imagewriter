from typing import Protocol, Self

from imagewriter.connection import Connection
from imagewriter.serial import Serial
from imagewriter.switch import DIPSwitches, SoftwareSwitches


class SoftwareSwitchesFactory(Protocol):
    def __call__(self: Self, dip_switches: DIPSwitches) -> SoftwareSwitches: ...


class SerialFactory(Protocol):
    def __call__(self: Self, port: str, dip_switches: DIPSwitches) -> Serial: ...


class ConnectionFactory(Protocol):
    def __call__(self: Self, port: Serial) -> Connection: ...


def software_switches_factory(
    dip_switches: DIPSwitches,
) -> SoftwareSwitches:
    return SoftwareSwitches.defaults(dip_switches)


def serial_factory(port: str, dip_switches: DIPSwitches) -> Serial:
    return Serial(
        port=port, baudrate=dip_switches.baud_rate, protocol=dip_switches.protocol
    )


class Container:
    def __init__(
        self: Self,
        port: str,
        dip_switches: DIPSwitches = DIPSwitches.defaults(),
        software_switches: SoftwareSwitchesFactory = software_switches_factory,
        serial: SerialFactory = serial_factory,
        connection: ConnectionFactory = Connection,
    ) -> None:
        self._dip_switches: DIPSwitches = dip_switches
        self._software_switches: SoftwareSwitches = software_switches(dip_switches)
        self._port: Serial = serial(port, dip_switches)
        self._connection: Connection = connection(self._port)

    @property
    def dip_switches(self: Self) -> DIPSwitches:
        return self._dip_switches

    @property
    def software_switches(self: Self) -> SoftwareSwitches:
        return self._software_switches

    @property
    def port(self: Self) -> Serial:
        return self._port

    @property
    def connection(self: Self) -> Connection:
        return self._connection
