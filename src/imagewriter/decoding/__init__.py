from parsy import alt, any_char  # type: ignore

from imagewriter.base.settings import Settings
from imagewriter.decoding.attributes import (
    print_slashed_zero,
    print_unslashed_zero,
    start_boldface,
    start_double_width,
    start_half_height,
    start_subscript,
    start_superscript,
    start_underline,
    stop_boldface,
    stop_double_width,
    stop_half_height,
    stop_subscript,
    stop_superscript,
    stop_underline,
)
from imagewriter.decoding.base import State
from imagewriter.decoding.boundaries import set_left_margin, set_page_length
from imagewriter.decoding.cancel import cancel_current_line
from imagewriter.decoding.character import (
    disable_mode,
    enable_custom_character_mode,
    enable_mousetext_mapping_mode,
    set_max_custom_character_width,
)
from imagewriter.decoding.color import set_color
from imagewriter.decoding.graphics import print_graphics_data
from imagewriter.decoding.identification import request_self_identify
from imagewriter.decoding.language import (
    close_language_switches,
    open_language_switches,
)
from imagewriter.decoding.motion import (
    backspace,
    clear_all_tabs,
    clear_many_tabs,
    cr,
    lf,
    line_feed,
    line_feed_forward,
    line_feed_reverse,
    place_exact_print_head_position,
    set_auto_lf_after_cr,
    set_cr_insertion,
    set_distance_between_lines,
    set_lf_when_line_full,
    set_lines_per_inch,
    set_many_tabs,
    set_one_tab,
    set_perforation_skip,
    set_top_of_form,
    set_unidirectional_printing,
    tab,
)
from imagewriter.decoding.paper import set_paper_out_sensor
from imagewriter.decoding.pitch import insert_spaces, set_pitch, set_spacing
from imagewriter.decoding.print import set_print_commands
from imagewriter.decoding.quality import set_quality
from imagewriter.decoding.repeat import repeat
from imagewriter.decoding.reset import reset
from imagewriter.decoding.select import deselect, select, set_software_select_response
from imagewriter.decoding.serial import set_include_eighth_data_bit
from imagewriter.decoding.switch import close_software_switches, open_software_switches
from imagewriter.encoding.base import Command, Print


def decode(document: bytes, settings: Settings) -> list[Command]:
    state = State(settings)

    parser = alt(
        # specific switches
        #   language
        close_language_switches(state),
        open_language_switches(state),
        #   attributes
        print_slashed_zero(state),
        print_unslashed_zero(state),
        #   motion
        set_perforation_skip(state),
        set_auto_lf_after_cr(state),
        set_lf_when_line_full(state),
        #   select
        set_software_select_response(state),
        #   serial
        set_include_eighth_data_bit(state),
        #   general
        close_software_switches(state),
        open_software_switches(state),
        # attributes
        start_double_width,
        stop_double_width,
        start_underline,
        stop_underline,
        start_boldface,
        stop_boldface,
        start_half_height,
        stop_half_height,
        start_superscript,
        stop_superscript,
        start_subscript,
        stop_subscript,
        # boundaries
        set_left_margin(state),
        set_page_length,
        # cancel
        cancel_current_line,
        # characters
        disable_mode,
        enable_mousetext_mapping_mode,
        set_max_custom_character_width,
        enable_custom_character_mode,
        # color
        set_color,
        # graphics
        print_graphics_data,
        # identification
        request_self_identify,
        # motion
        #   form feed
        set_top_of_form,
        set_cr_insertion,
        #   line feed
        lf,
        line_feed,
        set_lines_per_inch,
        set_distance_between_lines,
        line_feed_forward,
        line_feed_reverse,
        #  tabs
        tab,
        set_many_tabs,
        set_one_tab,
        clear_many_tabs,
        clear_all_tabs,
        #   everything else
        cr,
        backspace,
        set_unidirectional_printing,
        place_exact_print_head_position(state),
        # paper
        set_paper_out_sensor,
        # pitch
        set_pitch(state),
        insert_spaces(state),
        set_spacing(state),
        # print
        set_print_commands(state),
        # quality
        set_quality,
        # repeat
        repeat,
        # reset
        reset,
        # select
        select,
        deselect,
        # otherwise
        any_char.map(Print),
    )

    # TODO: Return settings when state management is complete
    return parser.parse(document)
