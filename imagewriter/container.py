from concurrent.futures import Executor, ThreadPoolExecutor
from contextlib import contextmanager
from typing import cast, Generator

from dependency_injector import containers, providers
from serial.tools.list_ports import comports

from imagewriter.connection import Connection
from imagewriter.debug import SerialStateObserver
from imagewriter.encoding.character import CharacterEncoder
from imagewriter.language import Language
from imagewriter.render import DocumentRenderer, PandocRenderer, RichTextBuilder
from imagewriter.serial import BaudRate, Serial, SerialProtocol
from imagewriter.settings import Settings
from imagewriter.switch import DIPSwitches
from imagewriter.test import test_page

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


@contextmanager
def provide_executor() -> Generator[Executor, None, None]:
    executor = ThreadPoolExecutor()

    yield executor

    executor.shutdown(wait=False, cancel_futures=True)


@contextmanager
def provide_serial_state_observer(
    serial: Serial, executor: Executor
) -> Generator[SerialStateObserver, None, None]:
    observer = SerialStateObserver(serial=serial, executor=executor)

    yield observer

    observer.stop()


@contextmanager
def provide_connection(
    serial: Serial, executor: Executor
) -> Generator[Connection, None, None]:
    connection = Connection(serial=serial, executor=executor)

    yield connection

    connection.stop()


class Container(containers.DeclarativeContainer):
    port = providers.Callable(provide_port)

    dip_switches = providers.Object(DIP_SWITCHES)
    baud_rate = providers.Callable(provide_baud_rate, dip_switches=dip_switches)
    protocol = providers.Callable(provide_protocol, dip_switches=dip_switches)

    settings = providers.Callable(provide_settings, dip_switches=dip_switches)
    language = providers.Callable(provide_language, settings=settings)

    executor = cast(providers.Resource[Executor], providers.Resource(provide_executor))

    serial = providers.Factory(
        Serial, port=port, baud_rate=baud_rate, protocol=protocol
    )
    serial_state_observer = cast(
        providers.Resource[SerialStateObserver],
        providers.Resource(
            provide_serial_state_observer, serial=serial, executor=executor
        ),
    )
    connection = cast(
        providers.Resource[Connection],
        providers.Resource(provide_connection, serial=serial, executor=executor),
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
        test_page,
        character_encoder=character_encoder,
        document_renderer=document_renderer,
        pandoc_renderer=pandoc_renderer,
    )
