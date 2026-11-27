import logging
from collections.abc import Generator
from concurrent.futures import Executor, ThreadPoolExecutor
from contextlib import contextmanager

from dependency_injector import containers, providers
from serial.tools.list_ports import comports

from imagewriter.base.character import Language
from imagewriter.base.settings import Settings
from imagewriter.base.switch import DIPSwitches
from imagewriter.connection import Connection
from imagewriter.debug import SerialStateObserver
from imagewriter.encoding.character import CharacterEncoder
from imagewriter.render import DocumentRenderer, PandocRenderer, RichTextBuilder
from imagewriter.serial import Serial
from imagewriter.test import TestPage

logger = logging.getLogger(__name__)


def provide_port() -> str:
    return comports()[-1].device


def provide_settings(
    dip_switches: DIPSwitches,
    lf_when_line_full: bool,
    perforation_skip: bool,
    include_eighth_data_bit: bool,
) -> Settings:
    return Settings.replace(
        Settings.defaults(dip_switches),
        lf_when_line_full=lf_when_line_full,
        perforation_skip=perforation_skip,
        include_eighth_data_bit=include_eighth_data_bit,
    )


def provide_language(settings: Settings) -> Language:
    return settings.language


def provide_emoji_codes(settings: Settings) -> bool:
    return settings.emoji_codes


@contextmanager
def provide_executor() -> Generator[Executor]:
    executor = ThreadPoolExecutor()

    yield executor

    executor.shutdown(wait=False, cancel_futures=True)


@contextmanager
def provide_serial(port: str, dip_switches: DIPSwitches) -> Generator[Serial]:
    with Serial(
        port=port, baudrate=dip_switches.baud_rate, protocol=dip_switches.protocol
    ) as serial:
        yield serial


@contextmanager
def provide_connection(
    serial: Serial, executor: Executor, settings: Settings
) -> Generator[Connection]:
    connection = Connection(serial=serial, executor=executor)

    # TODO: await connection.write(apply_settings(settings))

    yield connection

    connection.shutdown()


def provide_character_encoder(settings: Settings) -> CharacterEncoder:
    return CharacterEncoder(
        language=settings.language,
        emoji_codes=settings.emoji_codes,
        include_eighth_data_bit=settings.include_eighth_data_bit,
    )


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

    dip_switches = providers.Object(DIPSwitches.defaults())

    settings = providers.Callable(
        provide_settings,
        dip_switches=dip_switches,
        lf_when_line_full=True,
        perforation_skip=True,
        include_eighth_data_bit=True,
    )

    # Individual configuration from settings
    language = providers.Callable(provide_language, settings=settings)
    emoji_codes = providers.Callable(provide_emoji_codes, settings=settings)

    # Persistent connection stuff
    executor = providers.Resource(provide_executor)

    serial = providers.Resource(provide_serial, port=port, dip_switches=dip_switches)
    observer = providers.Factory(SerialStateObserver, serial=serial, executor=executor)
    connection = providers.Resource(
        provide_connection, serial=serial, executor=executor, settings=settings
    )

    # Encoding and Rendering
    character_encoder = providers.Factory(provide_character_encoder, settings=settings)
    rich_text_builder = providers.Factory(RichTextBuilder, settings=settings)
    document_renderer = providers.Factory(DocumentRenderer, settings=settings)
    pandoc_renderer = providers.Factory(PandocRenderer, settings=settings)

    # Test page
    test_page = providers.Factory(
        TestPage,
        rich_text_builder=rich_text_builder,
        pandoc_renderer=pandoc_renderer,
    )
