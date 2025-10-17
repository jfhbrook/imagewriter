from typing import cast, Optional, Self

import ipywidgets as widgets

from imagewriter.encoding.switch import force_software_switch_settings
from imagewriter.jupyter.connection import Connection
from imagewriter.language import Language
from imagewriter.switch import DIPSwitchSettings, SoftwareSwitchSettings


def language(switches: DIPSwitchSettings | SoftwareSwitchSettings) -> str:
    return switches.language.value


def form_length(switches: DIPSwitchSettings) -> str:
    return str(switches.form_length)


def software_select_response(switches: SoftwareSwitchSettings) -> str:
    return "Disabled" if switches.software_select_response_disabled else "Enabled"


def lf_when_line_full(switches: SoftwareSwitchSettings) -> str:
    return "Yes" if switches.lf_when_line_full else "No"


def print_commands_include_lf_ff(switches: SoftwareSwitchSettings) -> str:
    return "Yes" if switches.print_commands_include_lf_ff else "No"


def auto_lf_after_cr(switches: DIPSwitchSettings | SoftwareSwitchSettings) -> str:
    return "Yes" if switches.auto_lf_after_cr else "No"


def slashed_zero(switches: SoftwareSwitchSettings) -> str:
    return "Slashed" if switches.slashed_zero else "Unslashed"


def perforation_skip(switches: DIPSwitchSettings | SoftwareSwitchSettings) -> str:
    if isinstance(switches, DIPSwitchSettings):
        return "Yes" if switches.perforation_skip else "No"

    return "No" if switches.perforation_skip_disabled else "Yes"


def pitch(switches: DIPSwitchSettings) -> str:
    return switches.pitch.value


def baud_rate(switches: DIPSwitchSettings) -> str:
    return str(switches.baud_rate)


def protocol(switches: DIPSwitchSettings) -> str:
    return switches.protocol.value


def eighth_data_bit(switches: SoftwareSwitchSettings) -> str:
    return "Ignored" if switches.ignore_eighth_data_bit else "Respected"


class DIPSwitches(widgets.VBox):
    def __init__(self: Self, dip_switches: DIPSwitchSettings) -> None:
        self.dip_switches = dip_switches

        self._language = widgets.Label(value=language(dip_switches))
        self._form_length = widgets.Label(value=form_length(dip_switches))
        self._perforation_skip = widgets.Label(value=perforation_skip(dip_switches))
        self._pitch = widgets.Label(value=pitch(dip_switches))
        self._auto_lf_after_cr = widgets.Label(value=auto_lf_after_cr(dip_switches))
        self._baud_rate = widgets.Label(value=baud_rate(dip_switches))
        self._protocol = widgets.Label(value=protocol(dip_switches))

        super().__init__(
            [
                widgets.HBox(
                    [
                        widgets.Label(value="Language:", font_weight="bold"),
                        self._language,
                    ]
                ),
                widgets.HBox(
                    [
                        widgets.Label(value="Form length:", font_weight="bold"),
                        self._form_length,
                    ]
                ),
                widgets.HBox(
                    [
                        widgets.Label(value="Perf skip:", font_weight="bold"),
                        self._perforation_skip,
                    ]
                ),
                widgets.HBox(
                    [
                        widgets.Label(value="Pitch:", font_weight="bold"),
                        self._pitch,
                    ]
                ),
                widgets.HBox(
                    [
                        widgets.Label(value="LF after CR:", font_weight="bold"),
                        self._auto_lf_after_cr,
                    ]
                ),
                widgets.HBox(
                    [
                        widgets.Label(value="Baud rate:", font_weight="bold"),
                        self._baud_rate,
                    ]
                ),
                widgets.HBox(
                    [
                        widgets.Label(value="Protocol:", font_weight="bold"),
                        self._protocol,
                    ]
                ),
            ]
        )
        self._baud_rate = widgets.Label(value=str(dip_switches.baud_rate))
        self._protocol = widgets.Label(value=dip_switches.protocol.value)


class Settings(widgets.VBox):
    def __init__(
        self: Self,
        software_switches: SoftwareSwitchSettings,
        connection: Optional[Connection] = None,
    ) -> None:
        self.software_switches = software_switches
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
            value=language(software_switches),
            description="Language:",
            disabled=False,
        )
        self._software_select_response = widgets.Dropdown(
            options=[
                "Disabled",
                "Enabled",
            ],
            value=software_select_response(software_switches),
            description="SW Select:",
            disabled=False,
        )
        self._lf_when_line_full = widgets.Dropdown(
            options=[
                "No",
                "Yes",
            ],
            value=lf_when_line_full(software_switches),
            description="LF when full:",
            disabled=False,
        )
        self._print_commands_include_lf_ff = widgets.Dropdown(
            options=["Yes", "No"],
            value=print_commands_include_lf_ff(software_switches),
            description="LF/FF print:",
            disabled=False,
        )
        self._auto_lf_after_cr = widgets.Dropdown(
            options=["Yes", "No"],
            value=auto_lf_after_cr(software_switches),
            description="LF after CR:",
            disabled=False,
        )
        self._slashed_zero = widgets.Dropdown(
            options=["Slashed", "Unslashed"],
            value=slashed_zero(software_switches),
            description="Zero:",
        )
        self._perforation_skip = widgets.Dropdown(
            options=["Yes", "No"],
            value=perforation_skip(software_switches),
            description="Perf skip:",
        )
        self._eighth_data_bit = widgets.Dropdown(
            options=["Ignored", "Respected"],
            value=eighth_data_bit(software_switches),
            description="8th bit:",
        )
        self._apply_button = widgets.Button(
            description="Apply",
            disabled=False,
            button_style="",
            tooltip="Apply software_switches",
        )
        self._apply_status = widgets.Label(value="❓ Not yet applied")

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
                widgets.HBox(
                    [
                        self._apply_button,
                        self._apply_status,
                    ]
                ),
            ]
        )

    def update(self: Self, software_switches: SoftwareSwitchSettings) -> None:
        self.software_switches = software_switches
        self._language.value = language(software_switches)
        self._software_select_response.value = software_select_response(
            software_switches
        )
        self._lf_when_line_full.value = lf_when_line_full(software_switches)
        self._print_commands_include_lf_ff.value = print_commands_include_lf_ff(
            software_switches
        )
        self._auto_lf_after_cr.value = auto_lf_after_cr(software_switches)
        self._slashed_zero.value = slashed_zero(software_switches)
        self._perforation_skip.value = perforation_skip(software_switches)
        self._eighth_data_bit.value = eighth_data_bit(software_switches)

    def apply(self: Self) -> None:
        self.software_switches = SoftwareSwitchSettings(
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
            commands = force_software_switch_settings(self.software_switches)
            try:
                for cmd in commands:
                    self.connection.port.write(bytes(cmd))
                self._apply_status.value = "✅ Applied successfully"
            except Exception as err:
                self._apply_status.value = f"❌ Error: {err}"
                pass
        else:
            self._apply_status.value = "❌ Not connected"
