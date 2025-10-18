from typing import Protocol, Self

from imagewriter.serial import Serial
from imagewriter.switch import DIPSwitchSettings, SoftwareSwitchSettings


class SoftwareSwitchesFactory(Protocol):
    def __call__(
        self: Self, dip_switches: DIPSwitchSettings
    ) -> SoftwareSwitchSettings: ...


class SerialFactory(Protocol):
    def __call__(self: Self, port: str, dip_switches: DIPSwitchSettings) -> Serial: ...


def software_switches_factory(
    dip_switches: DIPSwitchSettings,
) -> SoftwareSwitchSettings:
    return SoftwareSwitchSettings.defaults(dip_switches)


def serial_factory(port: str, dip_switches: DIPSwitchSettings) -> Serial:
    return Serial(
        port=port, baudrate=dip_switches.baud_rate, protocol=dip_switches.protocol
    )


class Container:
    def __init__(
        self: Self,
        port: str,
        dip_switches: DIPSwitchSettings = DIPSwitchSettings.defaults(),
        software_switches: SoftwareSwitchesFactory = software_switches_factory,
        serial: SerialFactory = serial_factory,
    ) -> None:
        self.dip_switches: DIPSwitchSettings = dip_switches
        self.software_switches: SoftwareSwitchSettings = software_switches(dip_switches)
        self.port: Serial = serial(port, dip_switches)
