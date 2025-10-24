from dependency_injector import containers, providers
from serial.tools.list_ports import comports

from imagewriter.connection import Connection
from imagewriter.serial import BaudRate, Serial, SerialProtocol
from imagewriter.settings import Settings
from imagewriter.switch import DIPSwitches


def provide_port() -> str:
    return comports()[-1].device


def provide_baud_rate(dip_switches: DIPSwitches) -> BaudRate:
    return dip_switches.baud_rate


def provide_protocol(dip_switches: DIPSwitches) -> SerialProtocol:
    return dip_switches.protocol


DIP_SWITCHES = DIPSwitches.defaults()


def provide_settings(dip_switches: DIPSwitches) -> Settings:
    return Settings.replace(
        Settings.defaults(dip_switches),
        lf_when_line_full=True,
        perforation_skip=True,
        include_eighth_data_bit=True,
    )


def provide_serial(port: str, dip_switches: DIPSwitches) -> Serial:
    return Serial(
        port=port,
        baudrate=dip_switches.baud_rate,
        protocol=dip_switches.protocol,
    )


def provide_connection(serial: Serial) -> Connection:
    return Connection(serial)


class Container(containers.DeclarativeContainer):
    port = providers.Callable(provide_port)
    baud_rate = providers.Callable(provide_baud_rate)
    protocol = providers.Callable(provide_protocol)

    dip_switches = providers.Object(DIP_SWITCHES)
    settings = providers.Callable(provide_settings, dip_switches=dip_switches)

    serial = providers.Singleton(Serial)
    connection = providers.Callable(provide_connection, serial=serial)
