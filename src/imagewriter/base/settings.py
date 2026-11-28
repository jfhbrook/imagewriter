from typing import Any, Self, cast

from imagewriter.base.character import Language
from imagewriter.base.motion import LinesPerInch
from imagewriter.base.print import PrintCommands
from imagewriter.base.quality import Quality
from imagewriter.base.switch import DIPSwitches, SoftwareSwitches
from imagewriter.base.units import Distance, Inch, Length, Pica, Point


class Settings:
    """
    ImageWriter II global settings.

    Most of these settings are controlled on the printer by a combination of physical
    DIP switches and in-memory software switches.
    """

    def __init__(
        self: Self,
        dip_switches: DIPSwitches,
        software_switches: SoftwareSwitches,
        left_margin: Distance | None = None,
        tab_stops: list[Length] | None = None,
        distance_between_lines: Distance | None = None,
        cr_insertion: bool = False,
        paper_out_sensor: bool = True,
        quality: Quality = Quality.DRAFT,
        emoji_codes: bool = True,
    ) -> None:
        self._dip_switches = dip_switches
        self.software_switches = software_switches

        self.left_margin = left_margin if left_margin is not None else Inch(0)
        self.page_length: Distance = Inch(dip_switches.form_length)
        self.pitch = dip_switches.pitch
        self.tab_stops = tab_stops if tab_stops is not None else []
        self.distance_between_lines = (
            distance_between_lines if distance_between_lines is not None else Pica(1)
        )
        self.cr_insertion = cr_insertion
        self.paper_out_sensor = paper_out_sensor
        self.quality = quality
        self.emoji_codes = emoji_codes

    @property
    def language(self: Self) -> Language:
        return self.software_switches.language

    @language.setter
    def language(self: Self, language: Language) -> None:
        self.software_switches.language = language

    @property
    def slashed_zero(self: Self) -> bool:
        return self.software_switches.slashed_zero

    @slashed_zero.setter
    def slashed_zero(self: Self, enabled: bool) -> None:
        self.software_switches.slashed_zero = enabled

    @property
    def lf_when_line_full(self: Self) -> bool:
        return self.software_switches.lf_when_line_full

    @lf_when_line_full.setter
    def lf_when_line_full(self: Self, enabled: bool) -> None:
        self.software_switches.lf_when_line_full = enabled

    @property
    def auto_lf_after_cr(self: Self) -> bool:
        return self.software_switches.auto_lf_after_cr

    @auto_lf_after_cr.setter
    def auto_lf_after_cr(self: Self, enabled: bool) -> None:
        self.software_switches.auto_lf_after_cr = enabled

    @property
    def perforation_skip(self: Self) -> bool:
        return not self.software_switches.perforation_skip_disabled

    @perforation_skip.setter
    def perforation_skip(self: Self, enabled: bool) -> None:
        self.software_switches.perforation_skip_disabled = not enabled

    @property
    def print_commands(self: Self) -> PrintCommands:
        return self.software_switches.print_commands

    @print_commands.setter
    def print_commands(self: Self, commands: PrintCommands) -> None:
        self.software_switches.print_commands = commands

    @property
    def software_select_response(self: Self) -> bool:
        return not self.software_switches.software_select_response_disabled

    @software_select_response.setter
    def software_select_response(self: Self, enabled: bool) -> None:
        self.software_switches.software_select_response_disabled = not enabled

    @property
    def include_eighth_data_bit(self: Self) -> bool:
        return not self.software_switches.ignore_eighth_data_bit

    @include_eighth_data_bit.setter
    def include_eighth_data_bit(self: Self, enabled: bool) -> None:
        self.software_switches.ignore_eighth_data_bit = not enabled

    @property
    def lines_per_inch(self: Self) -> LinesPerInch:
        value = int(72 / self.distance_between_lines.points)
        return cast(LinesPerInch, value)

    @lines_per_inch.setter
    def lines_per_inch(self: Self, value: LinesPerInch) -> None:
        if value == 6:
            self.distance_between_lines = Point(12)
        else:
            self.distance_between_lines = Point(9)

    @classmethod
    def replace(cls: type[Self], self: Self, **changes: Any) -> Self:
        new = cls(
            dip_switches=self._dip_switches,
            software_switches=SoftwareSwitches.replace(self.software_switches),
            left_margin=self.left_margin,
            tab_stops=self.tab_stops,
            distance_between_lines=self.distance_between_lines,
            cr_insertion=self.cr_insertion,
            paper_out_sensor=self.paper_out_sensor,
            quality=self.quality,
            emoji_codes=self.emoji_codes,
        )

        new.page_length = self.page_length
        new.pitch = self.pitch

        for name, value in changes.items():
            setattr(new, name, value)

        return new

    @classmethod
    def apply(cls: type[Self], self: Self, other: Self) -> None:
        # maintaining the identity of switches - hold my beer
        self.software_switches.switches &= set()
        self.software_switches.switches |= other.software_switches.switches

        self.left_margin = other.left_margin
        self.page_length = other.page_length
        self.pitch = other.pitch
        self.tab_stops = other.tab_stops
        self.distance_between_lines = other.distance_between_lines
        self.cr_insertion = other.cr_insertion
        self.paper_out_sensor = other.paper_out_sensor
        self.quality = other.quality
        self.emoji_codes = other.emoji_codes
