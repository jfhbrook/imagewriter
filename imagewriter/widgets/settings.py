from typing import Optional, Self

import ipywidgets as widgets

from imagewriter.print import PrintCommands
from imagewriter.settings import Settings
from imagewriter.switch import DIPSwitches
from imagewriter.units import Distance, Inch, VERTICAL_RESOLUTION

# from imagewriter.widgets.base import Label
from imagewriter.widgets.language import LanguageWidget
from imagewriter.widgets.pitch import PitchWidget
from imagewriter.widgets.units import DistanceWidget

# # boundaries
# left_margin: Distance
# page_length: Distance
# # fonts and pitch
# language: Language
# slashed_zero: bool


class LeftMarginWidget(widgets.HBox):
    def __init__(self: Self, settings: Settings) -> None:
        self._settings = settings
        self._distance_widget = DistanceWidget(
            self._settings.left_margin, Inch(8), self._step_value
        )
        super().__init__([widgets.Label("Left Margin:"), self._distance_widget])

    @property
    def _step_value(self: Self) -> Distance:
        return Inch(1 / self._settings.pitch.characters_per_inch)

    @property
    def left_margin(self: Self) -> Distance:
        return self._distance_widget.distance


class PageLengthWidget(widgets.HBox):
    def __init__(self: Self, settings: Settings) -> None:
        self._settings = settings

        max_length = Inch(9999 / VERTICAL_RESOLUTION)
        step = Inch(1 / VERTICAL_RESOLUTION)

        self._distance_widget = DistanceWidget(
            self._settings.page_length, max_length, step
        )
        super().__init__([widgets.Label("Left Margin:"), self._distance_widget])

    @property
    def page_length(self: Self) -> Distance:
        return self._distance_widget.distance


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


class DistanceBetweenLinesWidget(widgets.HBox):
    def __init__(self: Self, settings: Settings) -> None:
        pass


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
            description="Perf skip:",
        )

    @property
    def perforation_skip(self: Self) -> bool:
        return self.value == "Yes"


class PaperOutSensorWidget(widgets.Dropdown):
    def __init__(self: Self, settings: Settings) -> None:
        pass


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
            description="LF/FF print:",
            disabled=False,
        )

    @property
    def print_commands(self: Self) -> PrintCommands:
        return (
            PrintCommands.CR_LF_AND_FF
            if self.value == "CR, LF and FF"
            else PrintCommands.CR_ONLY
        )


class QualityWidget(widgets.Dropdown):
    def __init__(self: Self, settings: Settings) -> None:
        pass


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
        self._pitch_widget = PitchWidget(self._settings)

        # TODO: tab stops

        self._distance_between_lines_widget = DistanceBetweenLinesWidget(self._settings)
        self._lf_when_line_full_widget = LFWhenLineFullWidget(self._settings)
        self._auto_lf_after_cr_widget = AutoLFAfterCRWidget(self._settings)
        self._cr_insertion_widget = CRInsertionWidget(self._settings)
        self._perforation_skip_widget = PerforationSkipWidget(self._settings)
        self._paper_out_sensor_widget = PaperOutSensorWidget(self._settings)
        self._print_commands_widget = PrintCommandsWidget(self._settings)
        self._quality_widget = QualityWidget(self._settings)
        self._software_select_response_widget = SoftwareSelectResponseWidget(
            self._settings
        )
        self._include_eighth_data_bit_widget = IncludeEighthDataBitWidget(
            self._settings
        )

        super().__init__(
            [
                self._left_margin_widget,
                self._page_length_widget,
                self._language_widget,
                self._slashed_zero_widget,
                self._pitch_widget,
                self._distance_between_lines_widget,
                self._lf_when_line_full_widget,
                self._auto_lf_after_cr_widget,
                self._cr_insertion_widget,
                self._perforation_skip_widget,
                self._paper_out_sensor_widget,
                self._print_commands_widget,
                self._quality_widget,
                self._software_select_response_widget,
                self._include_eighth_data_bit_widget,
            ]
        )
