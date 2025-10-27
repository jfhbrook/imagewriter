from typing import Optional, Protocol, Self

import ipywidgets as widgets

from imagewriter.connection import Connection
from imagewriter.encoding.settings import apply_settings
from imagewriter.pitch import Pitch
from imagewriter.print import PrintCommands
from imagewriter.settings import Settings
from imagewriter.switch import DIPSwitches
from imagewriter.units import Distance, Inch, VERTICAL_RESOLUTION
from imagewriter.widgets.base import Label
from imagewriter.widgets.language import LanguageWidget
from imagewriter.widgets.pitch import PitchWidget
from imagewriter.widgets.quality import QualityWidget
from imagewriter.widgets.units import DistanceWidget


class LeftMarginWidget(DistanceWidget):
    def __init__(self: Self, settings: Settings) -> None:
        self._settings = settings
        super().__init__(settings.left_margin, Inch(8), self._step(settings.pitch))
        self.layout.width = "50%"

    def _step(self: Self, pitch: Pitch) -> Distance:
        return Inch(1 / pitch.characters_per_inch)

    def set_pitch(self: Self, pitch: Pitch) -> None:
        self.step = self._step(pitch)

    @property
    def left_margin(self: Self) -> Distance:
        return self.distance

    @left_margin.setter
    def left_margin(self: Self, left_margin: Distance) -> None:
        self.distance = left_margin


class PageLengthWidget(DistanceWidget):
    def __init__(self: Self, settings: Settings) -> None:
        super().__init__(
            settings.page_length,
            Inch(9999 / VERTICAL_RESOLUTION),
            Inch(1 / VERTICAL_RESOLUTION),
        )
        self.layout.width = "50%"

    @property
    def page_length(self: Self) -> Distance:
        return self.distance

    @page_length.setter
    def page_length(self: Self, page_length: Distance) -> None:
        self.distance = page_length


class SlashedZeroWidget(widgets.Dropdown):
    def __init__(self: Self, settings: Settings) -> None:
        value = "Slashed" if settings.slashed_zero else "Unslashed"

        super().__init__(
            options=["Slashed", "Unslashed"],
            value=value,
            description="Zero:",
        )

    @property
    def slashed_zero(self: Self) -> bool:
        return self.value == "Slashed"

    @slashed_zero.setter
    def slashed_zero(self: Self, slashed_zero: bool) -> None:
        self.value = "Slashed" if slashed_zero else "Unslashed"


class DistanceBetweenLinesWidget(DistanceWidget):
    def __init__(self: Self, settings: Settings) -> None:
        super().__init__(
            settings.distance_between_lines,
            Inch(99 / VERTICAL_RESOLUTION),
            Inch(1 / VERTICAL_RESOLUTION),
        )

    @property
    def distance_between_lines(self: Self) -> Distance:
        return self.distance

    @distance_between_lines.setter
    def distance_between_lines(self: Self, distance_between_lines: Distance) -> None:
        self.distance = distance_between_lines


class LinesPerInchWidget(widgets.Dropdown):
    def __init__(self: Self, settings: Settings) -> None:
        value = "8" if settings.lines_per_inch > 7 else "6"

        super().__init__(
            options=["6", "8"], value=value, description="", disabled=False
        )

    @property
    def lines_per_inch(self: Self) -> int:
        value = self.value if self.value else "6"
        return int(value)

    @lines_per_inch.setter
    def lines_per_inch(self: Self, lines_per_inch: int) -> None:
        self.value = lines_per_inch


class LineSpacingWidget(widgets.HBox):
    def __init__(self: Self, settings: Settings) -> None:
        self._distance_between_lines_widget = DistanceBetweenLinesWidget(settings)
        self._lines_per_inch_widget = LinesPerInchWidget(settings)

        self._selector_widget = widgets.Dropdown(
            options=["Dist bt Lines", "Lines per In"],
            value="Dist bt Lines",
            description="",
        )

        self._stack = widgets.Stack(
            [
                self._distance_between_lines_widget,
                self._lines_per_inch_widget,
            ],
            selected_index=0,
        )

        super().__init__([self._selector_widget, self._stack])

        self._selector_widget.observe(self._select, names="value")

    def _select(self: Self, change: str) -> None:
        if self._selector_widget.value == "Dist bt Lines":
            self._stack.selected_index = 0
        else:
            self._stack.selected_index = 1

    @property
    def distance_between_lines(self: Self) -> Distance:
        if self._stack.selected_index == 0:
            return self._distance_between_lines_widget.distance_between_lines
        return Inch(1 / self._lines_per_inch_widget.lines_per_inch)

    @distance_between_lines.setter
    def distance_between_lines(self: Self, distance_between_lines: Distance) -> None:
        self._distance_between_lines_widget.distance_between_lines = (
            distance_between_lines
        )
        self._lines_per_inch_widget.lines_per_inch = int(
            72 / distance_between_lines.points
        )

    @property
    def lines_per_inch(self: Self) -> float:
        if self._stack.selected_index == 0:
            return (
                72 / self._distance_between_lines_widget.distance_between_lines.points
            )
        return self._lines_per_inch_widget.lines_per_inch

    @lines_per_inch.setter
    def lines_per_inch(self: Self, lines_per_inch: int) -> None:
        self._lines_per_inch_widget.lines_per_inch = lines_per_inch
        self._distance_between_lines = Inch(1 / lines_per_inch)


class LFWhenLineFullWidget(widgets.Dropdown):
    def __init__(self: Self, settings: Settings) -> None:
        value = "Yes" if settings.lf_when_line_full else "No"
        super().__init__(
            options=[
                "No",
                "Yes",
            ],
            value=value,
            description="LF when full:",
            disabled=False,
        )

    @property
    def lf_when_line_full(self: Self) -> bool:
        return self.value == "Yes"

    @lf_when_line_full.setter
    def lf_when_line_full(self: Self, lf_when_line_full: bool) -> None:
        self.value = "Yes" if lf_when_line_full else "No"


class AutoLFAfterCRWidget(widgets.Dropdown):
    def __init__(self: Self, settings: Settings) -> None:
        value = "Yes" if settings.auto_lf_after_cr else "No"
        super().__init__(
            options=["Yes", "No"],
            value=value,
            description="LF after CR:",
            disabled=False,
        )

    @property
    def auto_lf_after_cr(self: Self) -> bool:
        return self.value == "Yes"

    @auto_lf_after_cr.setter
    def auto_lf_after_cr(self: Self, auto_lf_after_cr: bool) -> None:
        self.value = "Yes" if auto_lf_after_cr else "No"


class CRInsertionWidget(widgets.Dropdown):
    def __init__(self: Self, settings: Settings) -> None:
        value = "Yes" if settings.cr_insertion else "No"
        super().__init__(
            options=["Yes", "No"],
            value=value,
            description="CR Insert:",
            disabled=False,
        )

    @property
    def cr_insertion(self: Self) -> bool:
        return self.value == "Yes"

    @cr_insertion.setter
    def cr_insertion(self: Self, cr_insertion: bool) -> None:
        self.value = "Yes" if cr_insertion else "No"


class PerforationSkipWidget(widgets.Dropdown):
    def __init__(self: Self, settings: Settings) -> None:
        value = "Yes" if settings.perforation_skip else "No"
        super().__init__(
            options=["Yes", "No"],
            value=value,
            description="",
        )

    @property
    def perforation_skip(self: Self) -> bool:
        return self.value == "Yes"

    @perforation_skip.setter
    def perforation_skip(self: Self, perforation_skip: bool) -> None:
        self.value = "Yes" if perforation_skip else "No"


class PaperOutSensorWidget(widgets.Dropdown):
    def __init__(self: Self, settings: Settings) -> None:
        value = "Enabled" if settings.paper_out_sensor else "Disabled"

        super().__init__(
            options=[
                "Disabled",
                "Enabled",
            ],
            value=value,
            description="Paper Sensor:",
            disabled=False,
        )

    @property
    def paper_out_sensor(self: Self) -> bool:
        return self.value == "Enabled"

    @paper_out_sensor.setter
    def paper_out_sensor(self: Self, paper_out_sensor: bool) -> None:
        self.value = "Enabled" if paper_out_sensor else "Disabled"


class PrintCommandsWidget(widgets.Dropdown):
    def __init__(self: Self, settings: Settings) -> None:
        value = (
            "CR, LF and FF"
            if settings.print_commands == PrintCommands.CR_LF_AND_FF
            else "CR only"
        )

        super().__init__(
            options=["CR, LF and FF", "CR only"],
            value=value,
            description="Print Cmds:",
            disabled=False,
        )

    @property
    def print_commands(self: Self) -> PrintCommands:
        return (
            PrintCommands.CR_LF_AND_FF
            if self.value == "CR, LF and FF"
            else PrintCommands.CR_ONLY
        )

    @print_commands.setter
    def print_commands(self: Self, print_commands: PrintCommands) -> None:
        self.value = (
            "CR, LF and FF"
            if print_commands == PrintCommands.CR_LF_AND_FF
            else "CR only"
        )


class SoftwareSelectResponseWidget(widgets.Dropdown):
    def __init__(self: Self, settings: Settings) -> None:
        value = "Enabled" if settings.software_select_response else "Disabled"

        super().__init__(
            options=[
                "Disabled",
                "Enabled",
            ],
            value=value,
            description="SW Select:",
            disabled=False,
        )

    @property
    def software_select_response(self: Self) -> bool:
        return self.value == "Enabled"

    @software_select_response.setter
    def software_select_response(self: Self, software_select_response: bool) -> None:
        self.value = "Enabled" if software_select_response else "Disabled"


class IncludeEighthDataBitWidget(widgets.Dropdown):
    def __init__(self: Self, settings: Settings) -> None:
        value = "Included" if settings.include_eighth_data_bit else "Ignored"

        super().__init__(
            options=["Ignored", "Included"],
            value=value,
            description="8th bit:",
        )

    @property
    def include_eighth_data_bit(self: Self) -> bool:
        return self.value == "Included"

    @include_eighth_data_bit.setter
    def include_eighth_data_bit(self: Self, include_eighth_data_bit: bool) -> None:
        self.value = "Included" if include_eighth_data_bit else "Included"


class ApplyButtonWidget(widgets.Button):
    def __init__(self: Self) -> None:
        super().__init__(
            description="Apply",
            disabled=False,
            button_style="",
            tooltip="Apply settings",
        )


class ApplyStatusWidget(widgets.Label):
    NOT_APPLIED = "❓ Not yet applied"
    APPLIED = "✅ Applied successfully"
    ERROR = "❌ Error: {err}"

    def __init__(self: Self) -> None:
        super().__init__(value=self.NOT_APPLIED)

    def not_applied(self: Self) -> None:
        self.value = self.NOT_APPLIED

    def applied(self: Self) -> None:
        self.value = self.APPLIED

    def error(self: Self, err: Exception) -> None:
        self.value = self.ERROR.format(err=err)


class SettingsCallback(Protocol):
    def __call__(self: Self, widget: "SettingsWidget") -> None: ...


class SettingsWidget(widgets.VBox):
    def __init__(
        self: Self,
        dip_switches: Optional[DIPSwitches] = None,
        settings: Optional[Settings] = None,
    ) -> None:
        self._settings: Settings = (
            settings
            if settings is not None
            else Settings.defaults(
                dip_switches if dip_switches is not None else DIPSwitches.defaults()
            )
        )

        self._left_margin_widget = LeftMarginWidget(self._settings)

        self._page_length_widget = PageLengthWidget(self._settings)

        self._language_widget = LanguageWidget(self._settings.language)

        self._slashed_zero_widget = SlashedZeroWidget(self._settings)

        self._pitch_widget = PitchWidget(self._settings.pitch)

        # TODO: tab stops

        self._line_spacing_widget = LineSpacingWidget(self._settings)

        self._line_spacing_widget.layout.width = "75%"

        self._lf_when_line_full_widget = LFWhenLineFullWidget(self._settings)
        self._auto_lf_after_cr_widget = AutoLFAfterCRWidget(self._settings)
        self._cr_insertion_widget = CRInsertionWidget(self._settings)
        self._perforation_skip_widget = PerforationSkipWidget(self._settings)
        self._paper_out_sensor_widget = PaperOutSensorWidget(self._settings)
        self._print_commands_widget = PrintCommandsWidget(self._settings)
        self._quality_widget = QualityWidget(self._settings.quality)
        self._software_select_response_widget = SoftwareSelectResponseWidget(
            self._settings
        )
        self._include_eighth_data_bit_widget = IncludeEighthDataBitWidget(
            self._settings
        )

        self._apply_button = ApplyButtonWidget()
        self._apply_status = ApplyStatusWidget()

        super().__init__(
            [
                Label("Page Settings"),
                # TODO: Right justify labels
                widgets.HBox(
                    [
                        widgets.VBox(
                            [
                                widgets.Label("Left Margin:"),
                                widgets.Label("Page Length:"),
                                widgets.Label("Perf Skip:"),
                            ]
                        ),
                        widgets.VBox(
                            [
                                self._left_margin_widget,
                                self._page_length_widget,
                                self._perforation_skip_widget,
                            ]
                        ),
                    ]
                ),
                Label("Formatting"),
                self._language_widget,
                self._pitch_widget,
                self._quality_widget,
                self._slashed_zero_widget,
                widgets.HBox(
                    [widgets.Label("Line Spacing:"), self._line_spacing_widget]
                ),
                Label("Advanced Settings"),
                self._lf_when_line_full_widget,
                self._auto_lf_after_cr_widget,
                self._cr_insertion_widget,
                self._paper_out_sensor_widget,
                self._print_commands_widget,
                self._software_select_response_widget,
                self._include_eighth_data_bit_widget,
                widgets.HBox(
                    [
                        self._apply_button,
                        self._apply_status,
                    ]
                ),
            ]
        )

    def set_pitch(self: Self, value: str) -> None:
        self._left_margin_widget.set_pitch(self._pitch_widget.pitch)

    @property
    def settings(self: Self) -> Settings:
        self._settings = Settings.replace(
            self._settings,
            left_margin=self._left_margin_widget.left_margin,
            page_length=self._page_length_widget.page_length,
            language=self._language_widget.language,
            slashed_zero=self._slashed_zero_widget.slashed_zero,
            pitch=self._pitch_widget.pitch,
            distance_between_lines=self._line_spacing_widget.distance_between_lines,
            lf_when_line_full=self._lf_when_line_full_widget.lf_when_line_full,
            auto_lf_after_cr=self._auto_lf_after_cr_widget.auto_lf_after_cr,
            cr_insertion=self._cr_insertion_widget.cr_insertion,
            perforation_skip=self._perforation_skip_widget.perforation_skip,
            paper_out_sensor=self._paper_out_sensor_widget.paper_out_sensor,
            print_commands=self._print_commands_widget.print_commands,
            quality=self._quality_widget.quality,
            software_select_response=(
                self._software_select_response_widget.software_select_response
            ),
            include_eighth_data_bit=(
                self._include_eighth_data_bit_widget.include_eighth_data_bit
            ),
        )

        return self._settings

    @settings.setter
    def settings(self: Self, settings: Settings) -> None:
        self._settings = settings

        self._left_margin_widget.left_margin = settings.left_margin
        self._page_length_widget.page_length = settings.page_length
        self._language_widget.language = settings.language
        self._slashed_zero_widget.slashed_zero = settings.slashed_zero
        self._pitch_widget.pitch = settings.pitch
        self._line_spacing_widget.distance_between_lines = (
            settings.distance_between_lines
        )
        self._lf_when_line_full_widget.lf_when_line_full = settings.lf_when_line_full
        self._auto_lf_after_cr_widget.auto_lf_after_cr = settings.auto_lf_after_cr
        self._cr_insertion_widget.cr_insertion = settings.cr_insertion
        self._perforation_skip_widget.perforation_skip = settings.perforation_skip
        self._paper_out_sensor_widget.paper_out_sensor = settings.paper_out_sensor
        self._print_commands_widget.print_commands = settings.print_commands
        self._quality_widget.quality = settings.quality
        self._software_select_response_widget.software_select_response = (
            settings.software_select_response
        )
        self._include_eighth_data_bit_widget.include_eighth_data_bit = (
            settings.include_eighth_data_bit
        )

        self.applied()

    def apply(self: Self, connection: Connection) -> None:
        commands = apply_settings(self.settings)
        try:
            connection.write(commands)
            self.applied()
        except Exception as exc:
            self.error(exc)
            raise

        self.applied()

    def not_applied(self: Self) -> None:
        self._apply_status.not_applied()

    def applied(self: Self) -> None:
        self._apply_status.applied()

    def error(self: Self, err: Exception) -> None:
        self._apply_status.error(err)

    def on_apply(self: Self, callback: SettingsCallback) -> None:
        def cb(button: widgets.Button) -> None:
            callback(self)

        self._apply_button.on_click(cb)
