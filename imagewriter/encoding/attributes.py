from imagewriter.encoding.base import Ctrl, Esc
from imagewriter.encoding.switch import CloseSoftwareSwitches, OpenSoftwareSwitches
from imagewriter.switch import SoftwareSwitch

START_DOUBLE_WIDTH = Ctrl("N")
STOP_DOUBLE_WIDTH = Ctrl("O")
START_UNDERLINE = Esc("X")
STOP_UNDERLINE = Esc("Y")
START_BOLDFACE = Esc("!")
STOP_BOLDFACE = Esc('"')
START_HALF_HEIGHT = Esc("w")
STOP_HALF_HEIGHT = Esc("W")
START_SUPERSCRIPT = Esc("x")
STOP_SUPERSCRIPT = Esc("z")
START_SUBSCRIPT = Esc("y")
STOP_SUBSCRIPT = STOP_SUPERSCRIPT

PRINT_SLASHED_ZERO = CloseSoftwareSwitches({SoftwareSwitch.SLASHED_ZERO})
PRINT_UNSLASHED_ZERO = OpenSoftwareSwitches({SoftwareSwitch.SLASHED_ZERO})
