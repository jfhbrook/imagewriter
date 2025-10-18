from typing import Any, Callable, Dict, Protocol, Self

from imagewriter.serial import Serial
from imagewriter.switch import DIPSwitchSettings, SoftwareSwitchSettings

SoftwareSwitchesFactory = Callable[[DIPSwitchSettings], SoftwareSwitchSettings]


def default_software_switches(
    dip_switches: DIPSwitchSettings,
) -> SoftwareSwitchSettings:
    return SoftwareSwitchSettings.defaults(dip_switches)


SerialKwargsFactory = Callable[[str, DIPSwitchSettings], Dict[str, Any]]


def default_serial_kwargs(port: str, dip_switches: DIPSwitchSettings) -> Dict[str, Any]:
    return dict(
        port=port, baudrate=dip_switches.baud_rate, protocol=dip_switches.protocol
    )


class SerialFactory(Protocol):
    def __call__(self: Self, **kwargs: Any) -> Serial: ...


def default_serial(**kwargs: Any) -> Serial:
    return Serial(**kwargs)


class Container:
    def __init__(
        self: Self,
        port: str,
        dip_switches: DIPSwitchSettings = DIPSwitchSettings.defaults(),
        software_switches: SoftwareSwitchesFactory = default_software_switches,
        serial_kwargs: SerialKwargsFactory = default_serial_kwargs,
        serial: SerialFactory = default_serial,
    ) -> None:
        self.dip_switches: DIPSwitchSettings = dip_switches
        self.software_switches: SoftwareSwitchSettings = software_switches(dip_switches)
        self.port: Serial = serial(**serial_kwargs(port, dip_switches))
