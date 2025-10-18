from typing import Optional, Self

from imagewriter.encoding.color import Color
from imagewriter.language import Language
from imagewriter.motion import LineFeedDirection, LinesPerInch, TabStops
from imagewriter.pitch import Pitch
from imagewriter.quality import Quality
from imagewriter.serial import BaudRate, SerialProtocol
from imagewriter.switch import DIPSwitches, SoftwareSwitches
from imagewriter.units import Distance, Inch, Length, length_to_distance, Point


class State:
    def __init__(
        self: Self,
        dip_switches: Optional[DIPSwitches] = None,
        software_switches: Optional[SoftwareSwitches] = None,
    ) -> None:
        self.dip_switches: DIPSwitches = (
            dip_switches if dip_switches else DIPSwitches.defaults()
        )
        self.software_switches: SoftwareSwitches = (
            software_switches
            if software_switches
            else SoftwareSwitches.defaults(self.dip_switches)
        )

        self._pitch: Pitch = self.dip_switches.pitch
        self.quality: Quality = Quality.DRAFT
        self._spacing: int = 0
        self.paper_out_sensor: bool = True
        self.unidirectional_printing: bool = False
        self.tab_stops: TabStops = TabStops(self.pitch)
        self.exact_print_head_position: Optional[int] = None
        self._distance_between_lines: Distance = Inch(1 / 6)
        self.lf_direction: LineFeedDirection = LineFeedDirection.FORWARD
        self.carriage_return_insertion: bool = False
        self.color: Color = Color.BLACK  # TODO: Separate color from encoding
        self._left_margin: Distance = Inch(0)
        self._page_length: Distance = Inch(self.dip_switches.form_length)

        self.double_width: bool = False
        self.underline: bool = False
        self.boldface: bool = False
        self.half_height: bool = False
        self.superscript: bool = False
        self.subscript: bool = False

    @property
    def baud_rate(self: Self) -> BaudRate:
        return self.dip_switches.baud_rate

    @property
    def protocol(self: Self) -> SerialProtocol:
        return self.dip_switches.protocol

    @property
    def language(self: Self) -> Language:
        return self.software_switches.language

    @property
    def software_select_response(self: Self) -> bool:
        return not self.software_switches.software_select_response_disabled

    @property
    def lf_when_line_full(self: Self) -> bool:
        return self.software_switches.lf_when_line_full

    @property
    def print_commands_include_lf_ff(self: Self) -> bool:
        return self.software_switches.print_commands_include_lf_ff

    @property
    def auto_lf_after_cr(self: Self) -> bool:
        return self.software_switches.auto_lf_after_cr

    @property
    def slashed_zero(self: Self) -> bool:
        return self.software_switches.slashed_zero

    @property
    def perforation_skip(self: Self) -> bool:
        return not self.software_switches.perforation_skip_disabled

    @property
    def ignore_eighth_data_bit(self: Self) -> bool:
        return self.software_switches.ignore_eighth_data_bit

    @property
    def pitch(self: Self) -> Pitch:
        return self._pitch

    @pitch.setter
    def pitch(self: Self, pitch: Pitch) -> None:
        self._pitch = pitch
        self.tab_stops.pitch = pitch

    @property
    def spacing(self: Self) -> Optional[int]:
        return self._spacing if self.pitch.is_proportional else None

    @spacing.setter
    def spacing(self: Self, spacing: int) -> None:
        self.spacing = spacing

    @property
    def left_margin(self: Self) -> Distance:
        return self._left_margin

    @left_margin.setter
    def left_margin(self: Self, distance: Length) -> None:
        self._left_margin = length_to_distance(
            distance, lambda cpi: Distance.from_characters(cpi, self.pitch)
        )

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
    def page_length(self: Self) -> Distance:
        return self._page_length

    @page_length.setter
    def page_length(self: Self, length: Length) -> None:
        self._page_length = length_to_distance(length, Distance.from_vertical)
