from typing import Self

import ipywidgets as widgets

from imagewriter.switch import DIPSwitches
from imagewriter.widgets.base import Label


def language(switches: DIPSwitches) -> str:
    return switches.language.value


def form_length(switches: DIPSwitches) -> str:
    return f"{switches.form_length} in"


def perforation_skip(switches: DIPSwitches) -> str:
    if isinstance(switches, DIPSwitches):
        return "Yes" if switches.perforation_skip else "No"

    return "No" if switches.perforation_skip_disabled else "Yes"


def pitch(switches: DIPSwitches) -> str:
    return switches.pitch.value


def auto_lf_after_cr(switches: DIPSwitches) -> str:
    return "Yes" if switches.auto_lf_after_cr else "No"


def baud_rate(switches: DIPSwitches) -> str:
    return str(switches.baud_rate)


def protocol(switches: DIPSwitches) -> str:
    return switches.protocol.value


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
