from concurrent.futures import Executor, ThreadPoolExecutor
from contextlib import contextmanager
import logging
from pprint import pformat
from typing import Generator

from dependency_injector import containers, providers
from serial.tools.list_ports import comports

from imagewriter.base.language import Language
from imagewriter.base.settings import Settings
from imagewriter.base.switch import DIPSwitches
from imagewriter.connection import Connection
from imagewriter.encoding.character import CharacterEncoder
from imagewriter.render import DocumentRenderer, PandocRenderer, RichTextBuilder
from imagewriter.serial import BaudRate, Serial, SerialProtocol
from imagewriter.test import TestPage

logger = logging.getLogger(__name__)

DIP_SWITCHES = DIPSwitches.defaults()


def provide_port() -> str:
    port = comports()[-1].device

    logger.debug(f"Providing port {port}")

    return port


def provide_baud_rate(dip_switches: DIPSwitches) -> BaudRate:
    logger.debug(f"Baud rate: {dip_switches.baud_rate}")

    return dip_switches.baud_rate


def provide_protocol(dip_switches: DIPSwitches) -> SerialProtocol:
    logger.debug(f"Protocol: {dip_switches.protocol.value}")
    return dip_switches.protocol


def provide_settings(dip_switches: DIPSwitches) -> Settings:
    settings = Settings.replace(
        Settings.defaults(dip_switches),
        lf_when_line_full=True,
        perforation_skip=True,
        include_eighth_data_bit=True,
    )

    logger.debug(f"""Settings:

    {pformat(settings)}

    """)

    return settings


def provide_language(settings: Settings) -> Language:
    return settings.language


@contextmanager
def provide_executor() -> Generator[Executor, None, None]:
    executor = ThreadPoolExecutor(max_workers=1)

    logger.debug("Executor created")

    yield executor

    logger.debug("Shutting down executor")

    executor.shutdown(wait=False, cancel_futures=True)


@contextmanager
def provide_connection(
    serial: Serial, executor: Executor
) -> Generator[Connection, None, None]:
    connection = Connection(serial=serial, executor=executor)

    yield connection

    connection.shutdown()


class Container(containers.DeclarativeContainer):
    port = providers.Callable(provide_port)

    dip_switches = providers.Object(DIP_SWITCHES)
    baud_rate = providers.Callable(provide_baud_rate, dip_switches=dip_switches)
    protocol = providers.Callable(provide_protocol, dip_switches=dip_switches)

    settings = providers.Callable(provide_settings, dip_switches=dip_switches)
    language = providers.Callable(provide_language, settings=settings)

    executor = providers.Resource(provide_executor)

    serial = providers.Factory(Serial, port=port, baudrate=baud_rate, protocol=protocol)
    connection = providers.Resource(
        provide_connection, serial=serial, executor=executor
    )

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

    test_page = providers.Factory(
        TestPage,
        rich_text_builder=rich_text_builder,
        pandoc_renderer=pandoc_renderer,
    )
