from concurrent.futures import Executor, ThreadPoolExecutor
from contextlib import contextmanager
import logging
from pprint import pformat
from typing import Generator

from dependency_injector import containers, providers
from serial.tools.list_ports import comports

from imagewriter.base.character import Language
from imagewriter.base.settings import Settings
from imagewriter.base.switch import DIPSwitches
from imagewriter.connection import Connection
from imagewriter.debug import SerialStateObserver
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


def provide_include_eighth_data_bit(settings: Settings) -> bool:
    return settings.include_eighth_data_bit


def provide_emoji_codes(settings: Settings) -> bool:
    return settings.emoji_codes


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
    """
    A dependency injection container for various ImageWriter II entities.

    Attributes:
        dip_switches: The default DIP switches for an ImageWriter II printer sold in
                      America
        settings: Sensible settings for an ImageWriter II printer sold in America
        executor: A shared `concurrent.futures.Executor` instance
        serial: A serial connection
        observer: A serial state observer
        connection: A managed ImageWriter II connection
        character_encoder: A character encoder for non-ASCII characters
        rich_text_builder: A builder for rich text
        document_renderer: A class for rendering Documents
        pandoc_renderer: A class for rendering text documents with `pandoc`
        test_page: A class for rendering test pages
    """

    port = providers.Callable(provide_port)

    dip_switches = providers.Object(DIP_SWITCHES)

    # Individual configuration from DIP switches
    baud_rate = providers.Callable(provide_baud_rate, dip_switches=dip_switches)
    protocol = providers.Callable(provide_protocol, dip_switches=dip_switches)

    settings = providers.Callable(provide_settings, dip_switches=dip_switches)

    # Individual configuration from settings
    language = providers.Callable(provide_language, settings=settings)
    include_eighth_data_bit = providers.Callable(
        provide_include_eighth_data_bit, settings=Settings
    )
    emoji_codes = providers.Callable(provide_emoji_codes, settings=settings)

    executor = providers.Resource(provide_executor)

    serial = providers.Factory(Serial, port=port, baudrate=baud_rate, protocol=protocol)
    observer = providers.Factory(SerialStateObserver, serial=serial, executor=executor)
    connection = providers.Resource(
        provide_connection, serial=serial, executor=executor
    )

    character_encoder = providers.Factory(
        CharacterEncoder,
        language=language,
        include_eighth_data_bit=include_eighth_data_bit,
        emoji_codes=emoji_codes,
    )
    rich_text_builder = providers.Factory(RichTextBuilder, settings=settings)
    document_renderer = providers.Factory(DocumentRenderer, settings=settings)
    pandoc_renderer = providers.Factory(PandocRenderer, settings=settings)

    test_page = providers.Factory(
        TestPage,
        rich_text_builder=rich_text_builder,
        pandoc_renderer=pandoc_renderer,
    )
