from collections.abc import Callable

from parsy import Parser, alt  # type: ignore

from imagewriter.base.switch import SoftwareSwitch
from imagewriter.decoding.base import (
    State,
    bytes_,
    ctrl,
    ctrl_command,
    esc,
    esc_command,
    number,
)
from imagewriter.decoding.switch import close_software_switch, open_software_switch
from imagewriter.encoding.motion import (
    BACKSPACE,
    CLEAR_ALL_TABS,
    CR,
    LF,
    LINE_FEED_ENCODING,
    LINE_FEED_FORWARD,
    LINE_FEED_REVERSE,
    SET_TOP_OF_FORM,
    TAB,
    ClearManyTabs,
    LineFeed,
    PlaceExactPrintHeadPosition,
    SetAutoLFAfterCR,
    SetCRInsertion,
    SetDistanceBetweenLines,
    SetLFWhenLineFull,
    SetLinesPerInch,
    SetManyTabs,
    SetOneTab,
    SetPerforationSkip,
    SetUnidirectionalPrinting,
)

# form_feed

set_top_of_form = esc_command(SET_TOP_OF_FORM)


def set_perforation_skip(state: State) -> Parser:
    return alt(
        close_software_switch(
            state,
            SoftwareSwitch.PERFORATION_SKIP_DISABLED,
            SetPerforationSkip(enabled=False),
        ),
        open_software_switch(
            state,
            SoftwareSwitch.PERFORATION_SKIP_DISABLED,
            SetPerforationSkip(enabled=True),
        ),
    )


# insertion


def set_auto_lf_after_cr(state: State) -> Parser:
    return alt(
        close_software_switch(
            state, SoftwareSwitch.AUTO_LF_AFTER_CR, SetAutoLFAfterCR(True)
        ),
        open_software_switch(
            state, SoftwareSwitch.AUTO_LF_AFTER_CR, SetAutoLFAfterCR(False)
        ),
    )


set_cr_insertion = alt(
    esc("l1").map(lambda _: SetCRInsertion(True)),
    esc("l0").map(lambda _: SetCRInsertion(False)),
)


def set_lf_when_line_full(state: State) -> Parser:
    return alt(
        close_software_switch(
            state, SoftwareSwitch.LF_WHEN_LINE_FULL, SetLFWhenLineFull(True)
        ),
        open_software_switch(
            state, SoftwareSwitch.LF_WHEN_LINE_FULL, SetLFWhenLineFull(False)
        ),
    )


# line_feed

lf = bytes_(b"\n").map(lambda _: LF)


def _map_line_feed(n: int) -> Callable[[bytes], LineFeed]:
    return lambda _: LineFeed(n)


line_feed = ctrl("_") >> alt(
    *[bytes_(c).map(_map_line_feed(n)) for n, c in LINE_FEED_ENCODING.items()]
)

set_lines_per_inch = alt(
    esc_command(SetLinesPerInch(6)), esc_command(SetLinesPerInch(8))
)

set_distance_between_lines = esc("T") >> number(2).map(
    lambda n: SetDistanceBetweenLines(n)
)

line_feed_forward = esc_command(LINE_FEED_FORWARD)
line_feed_reverse = esc_command(LINE_FEED_REVERSE)

# tab

tab = bytes_(b"\t").map(lambda _: TAB)

_comma = bytes_(b",")
_stop = bytes_(b".")
_tab_stops = number(3).sep_by(_comma) << _stop

set_many_tabs = esc("(") >> _tab_stops.map(SetManyTabs)
set_one_tab = esc("U") >> number(3).map(SetOneTab)
clear_many_tabs = esc(")") >> _tab_stops.map(ClearManyTabs)
clear_all_tabs = esc_command(CLEAR_ALL_TABS)

# everything else

cr = bytes_(b"\r").map(lambda _: CR)
backspace = ctrl_command(BACKSPACE)

set_unidirectional_printing = alt(
    esc(">").map(lambda _: True), esc("<").map(lambda _: False)
).map(lambda is_: SetUnidirectionalPrinting(is_))


def place_exact_print_head_position(state: State) -> Parser:
    return esc("F") >> number(4).map(
        lambda n: PlaceExactPrintHeadPosition(n, state.pitch)
    )
