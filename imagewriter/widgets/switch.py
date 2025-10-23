import dataclasses
from typing import Any, cast, Optional, Self

import ipywidgets as widgets

from imagewriter.encoding.switch import apply_software_switches
from imagewriter.language import Language
from imagewriter.print import PrintCommands
from imagewriter.switch import DIPSwitches, SoftwareSwitches
from imagewriter.widgets.base import Label
from imagewriter.widgets.connection import ConnectionWidget


def language(switches: DIPSwitches | SoftwareSwitches) -> str:
    return switches.language.value


def form_length(switches: DIPSwitches) -> str:
    return f"{switches.form_length} in"


def software_select_response(switches: SoftwareSwitches) -> str:
    return "Disabled" if switches.software_select_response_disabled else "Enabled"


def lf_when_line_full(switches: SoftwareSwitches) -> str:
    return "Yes" if switches.lf_when_line_full else "No"


def print_commands(switches: SoftwareSwitches) -> str:
    return (
        "CR, LF and FF"
        if switches.print_commands == PrintCommands.CR_LF_AND_FF
        else "CR only"
    )


def auto_lf_after_cr(switches: DIPSwitches | SoftwareSwitches) -> str:
    return "Yes" if switches.auto_lf_after_cr else "No"


def slashed_zero(switches: SoftwareSwitches) -> str:
    return "Slashed" if switches.slashed_zero else "Unslashed"


def perforation_skip(switches: DIPSwitches | SoftwareSwitches) -> str:
    if isinstance(switches, DIPSwitches):
        return "Yes" if switches.perforation_skip else "No"

    return "No" if switches.perforation_skip_disabled else "Yes"


def pitch(switches: DIPSwitches) -> str:
    return switches.pitch.value


def baud_rate(switches: DIPSwitches) -> str:
    return str(switches.baud_rate)


def protocol(switches: DIPSwitches) -> str:
    return switches.protocol.value


def eighth_data_bit(switches: SoftwareSwitches) -> str:
    return "Ignored" if switches.ignore_eighth_data_bit else "Included"


class DIPSwitchWidget(widgets.VBox):
    def __init__(self: Self, dip_switches: DIPSwitches) -> None:
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
                        Label(value="Language:"),
                        self._language,
                    ]
                ),
                widgets.HBox(
                    [
                        Label(value="Form length:"),
                        self._form_length,
                    ]
                ),
                widgets.HBox(
                    [
                        Label(value="Perf skip:"),
                        self._perforation_skip,
                    ]
                ),
                widgets.HBox(
                    [
                        Label(value="Pitch:"),
                        self._pitch,
                    ]
                ),
                widgets.HBox(
                    [
                        Label(value="LF after CR:"),
                        self._auto_lf_after_cr,
                    ]
                ),
                widgets.HBox(
                    [
                        Label(value="Baud rate:"),
                        self._baud_rate,
                    ]
                ),
                widgets.HBox(
                    [
                        Label(value="Protocol:"),
                        self._protocol,
                    ]
                ),
            ]
        )


class SoftwareSwitchWidget(widgets.VBox):
    def __init__(
        self: Self,
        switches: SoftwareSwitches,
        connection: Optional[ConnectionWidget] = None,
    ) -> None:
        self.switches = switches
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
            value=language(switches),
            description="Language:",
            disabled=False,
        )
        self._software_select_response = widgets.Dropdown(
            options=[
                "Disabled",
                "Enabled",
            ],
            value=software_select_response(switches),
            description="SW Select:",
            disabled=False,
        )
        self._lf_when_line_full = widgets.Dropdown(
            options=[
                "No",
                "Yes",
            ],
            value=lf_when_line_full(switches),
            description="LF when full:",
            disabled=False,
        )
        self._print_commands = widgets.Dropdown(
            options=["Yes", "No"],
            value=print_commands(switches),
            description="LF/FF print:",
            disabled=False,
        )
        self._auto_lf_after_cr = widgets.Dropdown(
            options=["Yes", "No"],
            value=auto_lf_after_cr(switches),
            description="LF after CR:",
            disabled=False,
        )
        self._slashed_zero = widgets.Dropdown(
            options=["Slashed", "Unslashed"],
            value=slashed_zero(switches),
            description="Zero:",
        )
        self._perforation_skip = widgets.Dropdown(
            options=["Yes", "No"],
            value=perforation_skip(switches),
            description="Perf skip:",
        )
        self._eighth_data_bit = widgets.Dropdown(
            options=["Ignored", "Respected"],
            value=eighth_data_bit(switches),
            description="8th bit:",
        )
        self._apply_button = widgets.Button(
            description="Apply",
            disabled=False,
            button_style="",
            tooltip="Apply switches",
        )
        self._apply_status = Label(value="❓ Not yet applied")

        self._apply_button.on_click(lambda b: self.apply())

        super().__init__(
            [
                self._language,
                self._software_select_response,
                self._lf_when_line_full,
                self._print_commands,
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

    def update(
        self: Self, switches: Optional[SoftwareSwitches] = None, **changes: Any
    ) -> None:
        if switches:
            self._update(switches)
        else:
            self._update(dataclasses.replace(self.switches, **changes))

    def _update(self: Self, switches: SoftwareSwitches) -> None:
        self.switches = switches
        self._language.value = language(switches)
        self._software_select_response.value = software_select_response(switches)
        self._lf_when_line_full.value = lf_when_line_full(switches)
        self._print_commands.value = print_commands(switches)
        self._auto_lf_after_cr.value = auto_lf_after_cr(switches)
        self._slashed_zero.value = slashed_zero(switches)
        self._perforation_skip.value = perforation_skip(switches)
        self._eighth_data_bit.value = eighth_data_bit(switches)

    def apply(self: Self) -> None:
        self.switches = SoftwareSwitches(
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
            print_commands=self._print_commands.value == "CR, LF and FF",
            auto_lf_after_cr=self._auto_lf_after_cr.value == "Yes",
            slashed_zero=self._slashed_zero.value == "Slashed",
            perforation_skip_disabled=self._perforation_skip.value == "Disabled",
            ignore_eighth_data_bit=self._eighth_data_bit.value == "Ignored",
        )

        if self.connection:
            commands = apply_software_switches(self.switches)
            try:
                for cmd in commands:
                    self.connection.port.write(bytes(cmd))
                self._apply_status.value = "✅ Applied successfully"
            except Exception as err:
                self._apply_status.value = f"❌ Error: {err}"
                pass
        else:
            self._apply_status.value = "❌ Not connected"
