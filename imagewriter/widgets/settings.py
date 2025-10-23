from typing import Optional, Self

import ipywidgets as widgets

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


# TODO: Wire event to Pitch
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

    @property
    def lines_per_inch(self: Self) -> float:
        if self._stack.selected_index == 0:
            return (
                72 / self._distance_between_lines_widget.distance_between_lines.points
            )
        return self._lines_per_inch_widget.lines_per_inch


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


class AutoLFAfterCRWidget(widgets.Dropdown):
    def __init__(self: Self, settings: Settings) -> None:
        value = "Yes" if settings.lf_when_line_full else "No"
        super().__init__(
            options=["Yes", "No"],
            value=value,
            description="LF after CR:",
            disabled=False,
        )

    @property
    def auto_lf_after_cr(self: Self) -> bool:
        return self.value == "Yes"


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


class IncludeEighthDataBitWidget(widgets.Dropdown):
    def __init__(self: Self, settings: Settings) -> None:
        value = "Included" if settings.include_eighth_data_bit else "Ignored"

        super().__init__(
            options=["Ignored", "Respected"],
            value=value,
            description="8th bit:",
        )

    @property
    def include_eighth_data_bit(self: Self) -> bool:
        return self.value == "Included"


class SettingsWidget(widgets.VBox):
    def __init__(self: Self, dip_switches: Optional[DIPSwitches] = None) -> None:
        self._settings: Settings = Settings.defaults(
            dip_switches if dip_switches is not None else DIPSwitches.defaults()
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

        super().__init__(
            [
                Label("Page Settings:"),
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
                Label("Formatting:"),
                self._language_widget,
                self._pitch_widget,
                self._quality_widget,
                self._slashed_zero_widget,
                widgets.HBox(
                    [widgets.Label("Line Spacing:"), self._line_spacing_widget]
                ),
                Label("Advanced Settings:"),
                self._lf_when_line_full_widget,
                self._auto_lf_after_cr_widget,
                self._cr_insertion_widget,
                self._paper_out_sensor_widget,
                self._print_commands_widget,
                self._software_select_response_widget,
                self._include_eighth_data_bit_widget,
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
