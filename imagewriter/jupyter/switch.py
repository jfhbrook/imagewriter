from typing import cast, Optional, Self

import ipywidgets as widgets

from imagewriter.encoding.switch import force_software_switch_settings
from imagewriter.jupyter.connection import Connection
from imagewriter.language import Language
from imagewriter.switch import SoftwareSwitchSettings


def language(settings: SoftwareSwitchSettings) -> str:
    return settings.language.value


def software_select_response(settings: SoftwareSwitchSettings) -> str:
    return "Disabled" if settings.software_select_response_disabled else "Enabled"


def lf_when_line_full(settings: SoftwareSwitchSettings) -> str:
    return "Yes" if settings.lf_when_line_full else "No"


def print_commands_include_lf_ff(settings: SoftwareSwitchSettings) -> str:
    return "Yes" if settings.print_commands_include_lf_ff else "No"


def auto_lf_after_cr(settings: SoftwareSwitchSettings) -> str:
    return "Yes" if settings.auto_lf_after_cr else "No"


def slashed_zero(settings: SoftwareSwitchSettings) -> str:
    return "Slashed" if settings.slashed_zero else "Unslashed"


def perforation_skip(settings: SoftwareSwitchSettings) -> str:
    return "No" if settings.perforation_skip_disabled else "Yes"


def eighth_data_bit(settings: SoftwareSwitchSettings) -> str:
    return "Ignored" if settings.ignore_eighth_data_bit else "Respected"


class Settings(widgets.VBox):
    def __init__(
        self: Self,
        settings: SoftwareSwitchSettings,
        connection: Optional[Connection] = None,
    ) -> None:
        self.settings = settings
        self.connection = connection
        self._language = widgets.Dropdown(
            options=[
                "American",
                "British",
                "German",
                "French",
                "Swedish",
                "Italian",
                "Spanish",
                "Danish",
            ],
            value=language(settings),
            description="Language:",
            disabled=False,
        )
        self._software_select_response = widgets.Dropdown(
            options=[
                "Disabled",
                "Enabled",
            ],
            value=software_select_response(settings),
            description="SW Select:",
            disabled=False,
        )
        self._lf_when_line_full = widgets.Dropdown(
            options=[
                "No",
                "Yes",
            ],
            value=lf_when_line_full(settings),
            description="LF when full:",
            disabled=False,
        )
        self._print_commands_include_lf_ff = widgets.Dropdown(
            options=["Yes", "No"],
            value=print_commands_include_lf_ff(settings),
            description="LF/FF print:",
            disabled=False,
        )
        self._auto_lf_after_cr = widgets.Dropdown(
            options=["Yes", "No"],
            value=auto_lf_after_cr(settings),
            description="LF after CR:",
            disabled=False,
        )
        self._slashed_zero = widgets.Dropdown(
            options=["Slashed", "Unslashed"],
            value=slashed_zero(settings),
            description="Zero:",
        )
        self._perforation_skip = widgets.Dropdown(
            options=["Yes", "No"],
            value=perforation_skip(settings),
            description="Perf skip:",
        )
        self._eighth_data_bit = widgets.Dropdown(
            options=["Ignored", "Respected"],
            value=eighth_data_bit(settings),
            description="8th bit:",
        )
        self._apply_button = widgets.Button(
            description="Apply",
            disabled=False,
            button_style="",
            tooltip="Apply settings",
        )

        self._apply_button.on_click(lambda b: self.apply())

        super().__init__(
            [
                self._language,
                self._software_select_response,
                self._lf_when_line_full,
                self._print_commands_include_lf_ff,
                self._auto_lf_after_cr,
                self._slashed_zero,
                self._perforation_skip,
                self._eighth_data_bit,
                self._apply_button,
            ]
        )

    def update(self: Self, settings: SoftwareSwitchSettings) -> None:
        self.settings = settings
        self._language.value = language(settings)
        self._software_select_response.value = software_select_response(settings)
        self._lf_when_line_full.value = lf_when_line_full(settings)
        self._print_commands_include_lf_ff.value = print_commands_include_lf_ff(
            settings
        )
        self._auto_lf_after_cr.value = auto_lf_after_cr(settings)
        self._slashed_zero.value = slashed_zero(settings)
        self._perforation_skip.value = perforation_skip(settings)
        self._eighth_data_bit.value = eighth_data_bit(settings)

        self.apply()

    def apply(self: Self) -> None:
        self.settings = SoftwareSwitchSettings(
            language={
                "American": Language.AMERICAN,
                "British": Language.BRITISH,
                "German": Language.GERMAN,
                "French": Language.FRENCH,
                "Swedish": Language.SWEDISH,
                "Italian": Language.ITALIAN,
                "Spanish": Language.SPANISH,
                "Danish": Language.DANISH,
            }[cast(str, self._language.value)],
            software_select_response_disabled=self._software_select_response
            == "Disabled",
            lf_when_line_full=self._lf_when_line_full.value == "Yes",
            print_commands_include_lf_ff=self._print_commands_include_lf_ff.value
            == "Yes",
            auto_lf_after_cr=self._auto_lf_after_cr.value == "Yes",
            slashed_zero=self._slashed_zero.value == "Slashed",
            perforation_skip_disabled=self._perforation_skip.value == "Disabled",
            ignore_eighth_data_bit=self._eighth_data_bit.value == "Ignored",
        )

        if self.connection:
            commands = force_software_switch_settings(self.settings)
            try:
                for cmd in commands:
                    self.connection.port.write(bytes(cmd))
            except AttributeError:
                pass
