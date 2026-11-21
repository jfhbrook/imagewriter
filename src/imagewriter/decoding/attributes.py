from parsy import Parser  # type: ignore

from imagewriter.base.switch import SoftwareSwitch
from imagewriter.decoding.base import State, ctrl_command, esc_command
from imagewriter.decoding.switch import close_software_switch, open_software_switch
from imagewriter.encoding.attributes import (
    PRINT_SLASHED_ZERO,
    PRINT_UNSLASHED_ZERO,
    START_BOLDFACE,
    START_DOUBLE_WIDTH,
    START_HALF_HEIGHT,
    START_SUBSCRIPT,
    START_SUPERSCRIPT,
    START_UNDERLINE,
    STOP_BOLDFACE,
    STOP_DOUBLE_WIDTH,
    STOP_HALF_HEIGHT,
    STOP_SUBSCRIPT,
    STOP_SUPERSCRIPT,
    STOP_UNDERLINE,
)

start_double_width = ctrl_command(START_DOUBLE_WIDTH)
stop_double_width = ctrl_command(STOP_DOUBLE_WIDTH)

start_underline = esc_command(START_UNDERLINE)
stop_underline = esc_command(STOP_UNDERLINE)

start_boldface = esc_command(START_BOLDFACE)
stop_boldface = esc_command(STOP_BOLDFACE)

start_half_height = esc_command(START_HALF_HEIGHT)
stop_half_height = esc_command(STOP_HALF_HEIGHT)

start_superscript = esc_command(START_SUPERSCRIPT)
stop_superscript = esc_command(STOP_SUPERSCRIPT)
start_subscript = esc_command(START_SUBSCRIPT)
stop_subscript = esc_command(STOP_SUBSCRIPT)


def print_slashed_zero(state: State) -> Parser:
    return close_software_switch(state, SoftwareSwitch.SLASHED_ZERO, PRINT_SLASHED_ZERO)


def print_unslashed_zero(state: State) -> Parser:
    return open_software_switch(
        state, SoftwareSwitch.SLASHED_ZERO, PRINT_UNSLASHED_ZERO
    )
