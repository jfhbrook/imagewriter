import dataclasses
from typing import List, Optional, Self

from imagewriter.language import Language
from imagewriter.motion import LinesPerInch
from imagewriter.pitch import Pitch
from imagewriter.print import PrintCommands
from imagewriter.quality import Quality
from imagewriter.serial import BaudRate, SerialProtocol
from imagewriter.switch import DIPSwitches, SoftwareSwitches
from imagewriter.units import Distance, Inch, Length, length_to_distance, Pica, Point


class Settings:
    def __init__(
        self: Self,
        # dip switches
        dip_switches: Optional[DIPSwitches] = None,
        # software switches
        software_switches: Optional[SoftwareSwitches] = None,
        # boundaries
        left_margin: Distance = Inch(0),
        page_length: Optional[Distance] = None,
        # fonts and pitch
        language: Optional[Language] = None,
        slashed_zero: Optional[bool] = None,
        pitch: Optional[Pitch] = None,
        # motion and insertion
        tab_stops: Optional[List[Distance]] = None,
        distance_between_lines: Distance = Pica(1),
        lf_when_line_full: Optional[bool] = None,
        auto_lf_after_cr: Optional[bool] = None,
        carriage_return_insertion: bool = False,
        perforation_skip: Optional[bool] = None,
        # paper
        paper_out_sensor: bool = True,
        # print commands
        print_commands: Optional[PrintCommands] = None,
        # quality
        quality: Quality = Quality.DRAFT,
        # select
        software_select_response: Optional[bool] = None,
        # serial
        include_eighth_data_bit: Optional[bool] = None,
    ) -> None:
        # dip switches
        self.dip_switches: DIPSwitches = (
            dip_switches if dip_switches else DIPSwitches.defaults()
        )

        # software switches
        self.software_switches: SoftwareSwitches = dataclasses.replace(
            software_switches
            if software_switches
            else SoftwareSwitches.defaults(self.dip_switches)
        )

        # boundaries
        self._left_margin: Distance = left_margin
        self._page_length: Distance = (
            page_length
            if page_length is not None
            else Inch(self.dip_switches.form_length)
        )

        # fonts and pitch
        if language is not None:
            self.language = language

        if slashed_zero is not None:
            self.slashed_zero = slashed_zero

        self._pitch: Pitch = pitch if pitch is not None else self.dip_switches.pitch

        # motion and insertion
        self.tab_stops: List[Distance] = tab_stops if tab_stops is not None else list()
        self._distance_between_lines: Distance = distance_between_lines

        if lf_when_line_full is not None:
            self.lf_when_line_full = lf_when_line_full

        if auto_lf_after_cr is not None:
            self.auto_lf_after_cr = auto_lf_after_cr

        self.carriage_return_insertion: bool = carriage_return_insertion

        if perforation_skip is not None:
            self.perforation_skip = perforation_skip

        # paper
        self.paper_out_sensor: bool = paper_out_sensor

        # print commands
        if print_commands is not None:
            self.print_commands = print_commands

        # quality
        self.quality: Quality = quality

        # select
        if software_select_response is not None:
            self.software_select_response = software_select_response

        # serial
        if include_eighth_data_bit is not None:
            self.include_eighth_data_bit = include_eighth_data_bit

    # dip switches
    @property
    def baud_rate(self: Self) -> BaudRate:
        return self.dip_switches.baud_rate

    @property
    def protocol(self: Self) -> SerialProtocol:
        return self.dip_switches.protocol

    # fonts and pitch
    @property
    def language(self: Self) -> Language:
        return self.software_switches.language

    @language.setter
    def language(self: Self, language: Language) -> None:
        self.software_switches = dataclasses.replace(
            self.software_switches, language=language
        )

    @property
    def slashed_zero(self: Self) -> bool:
        return self.software_switches.slashed_zero

    @slashed_zero.setter
    def slashed_zero(self: Self, slashed_zero: bool) -> None:
        self.software_switches = dataclasses.replace(
            self.software_switches, slashed_zero=slashed_zero
        )

    @property
    def pitch(self: Self) -> Pitch:
        return self._pitch

    @pitch.setter
    def pitch(self: Self, pitch: Pitch) -> None:
        self._pitch = pitch

    # boundaries
    @property
    def left_margin(self: Self) -> Distance:
        return self._left_margin

    @left_margin.setter
    def left_margin(self: Self, distance: Length) -> None:
        self._left_margin = length_to_distance(
            distance, lambda cpi: Distance.from_characters(cpi, self.pitch)
        )

    @property
    def page_length(self: Self) -> Distance:
        return self._page_length

    @page_length.setter
    def page_length(self: Self, length: Length) -> None:
        self._page_length = length_to_distance(length, Distance.from_vertical)

    # motion and insertion
    @property
    def distance_between_lines(self: Self) -> Distance:
        return self._distance_between_lines

    @distance_between_lines.setter
    def distance_between_lines(self: Self, distance: Length) -> None:
        self._distance_between_lines = length_to_distance(
            distance, Distance.from_vertical
        )

    @property
    def lines_per_inch(self: Self) -> float:
        return 72 / self._distance_between_lines.points

    @lines_per_inch.setter
    def lines_per_inch(self: Self, lines: LinesPerInch) -> None:
        self._distance_between_lines = Point(12 if lines == 6 else 9)

    @property
    def lf_when_line_full(self: Self) -> bool:
        return self.software_switches.lf_when_line_full

    @lf_when_line_full.setter
    def lf_when_line_full(self: Self, lf_when_line_full: bool) -> None:
        self.software_switches = dataclasses.replace(
            self.software_switches, lf_when_line_full=lf_when_line_full
        )

    @property
    def auto_lf_after_cr(self: Self) -> bool:
        return self.software_switches.auto_lf_after_cr

    @auto_lf_after_cr.setter
    def auto_lf_after_cr(self: Self, auto_lf_after_cr: bool) -> None:
        self.software_switches = dataclasses.replace(
            self.software_switches, auto_lf_after_cr=auto_lf_after_cr
        )

    @property
    def perforation_skip(self: Self) -> bool:
        return not self.software_switches.perforation_skip_disabled

    @perforation_skip.setter
    def perforation_skip(self: Self, perforation_skip: bool) -> None:
        self.software_switches = dataclasses.replace(
            self.software_switches, perforation_skip=perforation_skip
        )

    # print commands
    @property
    def print_commands(self: Self) -> PrintCommands:
        return self.software_switches.print_commands

    @print_commands.setter
    def print_commands(self: Self, print_commands: PrintCommands) -> None:
        self.software_switches = dataclasses.replace(
            self.software_switches,
            print_commands=print_commands,
        )

    # select
    @property
    def software_select_response(self: Self) -> bool:
        return not self.software_switches.software_select_response_disabled

    @software_select_response.setter
    def software_select_response(self: Self, respond: bool) -> None:
        self.software_switches = dataclasses.replace(
            self.software_switches,
            software_select_response_disabled=not respond,
        )

    # serial
    @property
    def include_eighth_data_bit(self: Self) -> bool:
        return not self.software_switches.ignore_eighth_data_bit

    @include_eighth_data_bit.setter
    def include_eighth_data_bit(self: Self, include: bool) -> None:
        self.software_switches = dataclasses.replace(
            self.software_switches, ignore_eighth_data_bit=not include
        )
