import dataclasses
from typing import Any, Self

from imagewriter.base.character import Language
from imagewriter.base.pitch import Pitch
from imagewriter.base.print import PrintCommands
from imagewriter.base.quality import Quality
from imagewriter.base.switch import DIPSwitches, SoftwareSwitches
from imagewriter.base.units import Distance, Inch, Length, Pica, Point


@dataclasses.dataclass
class Settings:
    """
    ImageWriter II global settings.

    Most of these settings are controlled on the printer by a combination of physical
    DIP switches and in-memory software switches.
    """

    # boundaries
    left_margin: Distance
    page_length: Distance
    # fonts and pitch
    language: Language
    slashed_zero: bool
    pitch: Pitch
    # motion and insertion
    tab_stops: list[Length]
    distance_between_lines: Distance
    lf_when_line_full: bool
    auto_lf_after_cr: bool
    cr_insertion: bool
    perforation_skip: bool
    # paper
    paper_out_sensor: bool
    # print commands
    print_commands: PrintCommands
    # quality
    quality: Quality
    # select
    software_select_response: bool
    # protocol
    include_eighth_data_bit: bool
    # driver settings
    emoji_codes: bool

    @classmethod
    def defaults(cls: type[Self], dip_switches: DIPSwitches | None) -> Self:
        dip_sw = dip_switches if dip_switches is not None else DIPSwitches.defaults()
        software_sw = SoftwareSwitches.defaults(dip_sw)
        return cls(
            left_margin=Inch(0),
            page_length=Inch(dip_sw.form_length),
            language=software_sw.language,
            slashed_zero=software_sw.slashed_zero,
            pitch=dip_sw.pitch,
            tab_stops=[],
            distance_between_lines=Pica(1),
            lf_when_line_full=software_sw.lf_when_line_full,
            auto_lf_after_cr=software_sw.auto_lf_after_cr,
            cr_insertion=False,
            perforation_skip=not software_sw.perforation_skip_disabled,
            paper_out_sensor=True,
            print_commands=software_sw.print_commands,
            quality=Quality.DRAFT,
            software_select_response=not software_sw.software_select_response_disabled,
            include_eighth_data_bit=not software_sw.ignore_eighth_data_bit,
            emoji_codes=True,
        )

    @classmethod
    def replace(cls: type[Self], inst: Self, **changes: Any) -> Self:
        if "lines_per_inch" in changes:
            assert "distance_between_lines" not in changes, (
                "May only set lines_per_inch or distance_between_lines"
            )
            lines = changes["lines_per_inch"]
            del changes["lines_per_inch"]
            changes["distance_between_lines"] = Point(12 if lines == 6 else 9)

        return dataclasses.replace(inst, **changes)

    @property
    def lines_per_inch(self: Self) -> float:
        return 72 / self.distance_between_lines.points

    def switches(self: Self) -> SoftwareSwitches:
        return SoftwareSwitches(
            language=self.language,
            software_select_response_disabled=not self.software_select_response,
            lf_when_line_full=self.lf_when_line_full,
            print_commands=self.print_commands,
            auto_lf_after_cr=self.auto_lf_after_cr,
            slashed_zero=self.slashed_zero,
            perforation_skip_disabled=not self.perforation_skip,
            ignore_eighth_data_bit=not self.include_eighth_data_bit,
        )
