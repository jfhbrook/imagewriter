from dependency_injector import containers, providers
from serial.tools.list_ports import comports

from imagewriter.connection import Connection
from imagewriter.encoding.character import CharacterEncoder
from imagewriter.language import Language
from imagewriter.render import DocumentRenderer, PandocRenderer, RichTextBuilder
from imagewriter.serial import BaudRate, Serial, SerialProtocol
from imagewriter.settings import Settings
from imagewriter.switch import DIPSwitches

DIP_SWITCHES = DIPSwitches.defaults()


def provide_port() -> str:
    return comports()[-1].device


def provide_baud_rate(dip_switches: DIPSwitches) -> BaudRate:
    return dip_switches.baud_rate


def provide_protocol(dip_switches: DIPSwitches) -> SerialProtocol:
    return dip_switches.protocol


def provide_settings(dip_switches: DIPSwitches) -> Settings:
    return Settings.replace(
        Settings.defaults(dip_switches),
        lf_when_line_full=True,
        perforation_skip=True,
        include_eighth_data_bit=True,
    )


def provide_language(settings: Settings) -> Language:
    return settings.language


class Container(containers.DeclarativeContainer):
    port = providers.Callable(provide_port)

    dip_switches = providers.Object(DIP_SWITCHES)
    baud_rate = providers.Callable(provide_baud_rate, dip_switches=dip_switches)
    protocol = providers.Callable(provide_protocol, dip_switches=dip_switches)

    settings = providers.Callable(provide_settings, dip_switches=dip_switches)
    language = providers.Callable(provide_language, settings=settings)

    serial = providers.Factory(
        Serial, port=port, baud_rate=baud_rate, protocol=protocol
    )
    connection = providers.Factory(Connection, serial=serial)

    map_mousetext = providers.Object(False)
    map_custom = providers.Object(False)
    character_encoder = providers.Factory(
        CharacterEncoder,
        language=language,
        map_mousetext=map_mousetext,
        map_custom=map_custom,
    )
    rich_text_builder = providers.Factory(RichTextBuilder, settings=settings)
    document_renderer = providers.Factory(DocumentRenderer, settings=settings)
    pandoc_renderer = providers.Factory(PandocRenderer, settings=settings)
